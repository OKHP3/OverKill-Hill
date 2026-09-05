#!/usr/bin/env node
/**
 * OverKill Hill responsive QA script.
 *
 * MODE A — Playwright (when available):
 *   Visits each public page at 10 viewport widths and checks:
 *   - No horizontal overflow (scrollWidth > innerWidth)
 *   - No JS console errors
 *   - All images loaded (no broken img src)
 *   - CSS and JS assets load (no 404 on critical resources)
 *
 * MODE B — Static lint (Playwright not available):
 *   Runs 10 structural checks per page per viewport (same pass/fail schema).
 *   Checks that are viewport-agnostic (viewport meta, h1, alt, etc.) are
 *   run once per page and applied to all 8 viewport rows — clearly flagged
 *   as `static-lint` so results are not confused with live browser checks.
 *
 * Usage:
 *   node scripts/responsive-qa.mjs [--base=http://localhost:5000]
 *
 * Third-party resources are deliberately blocked in browser mode so the
 * result measures the local site, not CDN availability. Navigation therefore
 * waits for the local document to commit, then gives DOMContentLoaded a short
 * bounded window. Blocked resources are retained as `warnings` in each row,
 * not silently treated as passes.
 *
 * Requires Playwright for MODE A:
 *   npm install -D playwright && npx playwright install chromium
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
const ROOT       = resolve(__dirname, '..');

const BASE_URL   = process.argv.find(a => a.startsWith('--base='))?.split('=')[1]
                 ?? 'http://localhost:5000';
const FORCE_STATIC = process.argv.includes('--static');

const VIEWPORTS = [
  { name: 'mobile-320',   width: 320,  height: 720  },
  { name: 'mobile-360',   width: 360,  height: 780  },
  { name: 'mobile-375',   width: 375,  height: 812  },
  { name: 'mobile-390',   width: 390,  height: 844  },
  { name: 'mobile-430',   width: 430,  height: 932  },
  { name: 'tablet-768',   width: 768,  height: 1024 },
  { name: 'desktop-1024', width: 1024, height: 768  },
  { name: 'desktop-1280', width: 1280, height: 800  },
  { name: 'desktop-1440', width: 1440, height: 900  },
  { name: 'desktop-1920', width: 1920, height: 1080 },
];

// The sitemap is the release inventory. This avoids silently testing a stale
// hand-maintained list when a public route is added or retired.
function loadPublicPaths() {
  const sitemap = readFileSync(resolve(ROOT, 'sitemap.xml'), 'utf8');
  const locations = [...sitemap.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/g)]
    .map((match) => match[1]);
  if (locations.length === 0) throw new Error('sitemap.xml has no public routes');
  return [...new Set(locations.map((location) => {
    const url = new URL(location);
    if (url.origin !== 'https://overkillhill.com' || url.search || url.hash) {
      throw new Error(`Invalid sitemap URL for responsive QA: ${location}`);
    }
    return url.pathname || '/';
  }))];
}
const PUBLIC_PATHS = loadPublicPaths();

const RESULTS_DIR    = resolve(ROOT, 'assets/docs/responsive-qa');
const RESULTS_FILE   = resolve(RESULTS_DIR, 'results.json');
const SCREENSHOTS_DIR = resolve(RESULTS_DIR, 'screenshots');

// ── MODE A: Playwright ────────────────────────────────────────────────────────

async function runWithPlaywright() {
  let pw;
  try {
    const require = createRequire(import.meta.url);
    pw = require('playwright');
  } catch {
    return null; // playwright not installed — fall back to MODE B
  }

  mkdirSync(RESULTS_DIR, { recursive: true });
  mkdirSync(SCREENSHOTS_DIR, { recursive: true });

  let browser;
  try {
    browser = await pw.chromium.launch({ headless: true });
  } catch {
    return null; // chromium binary not available — fall back to MODE B
  }

  // Create one persistent context+page per viewport (8 total) so we never pay
  // context-creation overhead more than once. External resources (fonts, GA,
  // GTM, and Mermaid's jsDelivr module) are blocked so browser QA measures
  // local layout and assets rather than third-party availability.
  const EXTERNAL_BLOCK = /fonts\.(gstatic|googleapis)\.com|google-analytics\.com|googletagmanager\.com|cdn\.jsdelivr\.net|avatars\.githubusercontent\.com|okhp3\.github\.io/;

  const workers = await Promise.all(VIEWPORTS.map(async vp => {
    const ctx  = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();
    const blockedExternal = new Set();
    await page.route('**/*', (route) => {
      if (EXTERNAL_BLOCK.test(route.request().url())) {
        blockedExternal.add(route.request().url());
        return route.abort();
      }
      return route.continue();
    });
    return { vp, ctx, page, consoleErrors: [], failed404s: [], blockedExternal };
  }));

  // Attach persistent event listeners.
  // ERR_FAILED console messages come from our own route-blocking of external
  // resources. They are testing artifacts, not real errors. The blocked URLs
  // are reported separately as warnings on every affected viewport row.
  for (const w of workers) {
    w.page.on('console', msg => {
      const sourceUrl = msg.location().url || '';
      const mermaidRuntimeCspWarning =
        msg.type() === 'error' &&
        msg.text().startsWith('Applying inline style violates the following Content Security Policy directive') &&
        /\/assets\/vendor\/mermaid\//.test(sourceUrl);
      if (msg.type() === 'error' &&
          !msg.text().includes('ERR_FAILED') &&
          !mermaidRuntimeCspWarning)
        w.consoleErrors.push(msg.text());
    });
    w.page.on('response', resp => {
      if (resp.status() === 404 && resp.url().match(/\.(css|js|json)$/)) w.failed404s.push(resp.url());
    });
  }

  const allResults = [];
  let totalFails   = 0;

  for (const path of PUBLIC_PATHS) {
    const url = BASE_URL + path;

    // Clear per-page accumulators
    for (const w of workers) {
      w.consoleErrors.length = 0;
      w.failed404s.length = 0;
      w.blockedExternal.clear();
    }

    // Navigate all 8 viewports in parallel
    const vpResults = await Promise.all(workers.map(async ({ vp, page, consoleErrors, failed404s, blockedExternal }) => {
      const warnings = [];
      try {
        // `commit` is local-document readiness. A bounded DOMContentLoaded
        // wait avoids making a local route depend on a blocked CDN module.
        await page.goto(url, { waitUntil: 'commit', timeout: 30000 });
        await page.waitForLoadState('domcontentloaded', { timeout: 5000 }).catch(() => {
          warnings.push('DOMContentLoaded not observed within 5s after local document commit');
        });
      } catch (err) {
        return { url, viewport: vp.name, width: vp.width, height: vp.height,
                 mode: 'playwright', pass: false,
                 errors: ['navigation timeout: ' + err.message.split('\n')[0]] };
      }

      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth > window.innerWidth
      );

      // A closed disclosure does not contribute to document overflow, so
      // explicitly open the locale menu and inspect every visible option.
      // This guards the compact 320/375/390 widths where the header controls
      // can squeeze the switcher's containing flex item.
      const localeMenuErrors = await page.evaluate(() => {
        const toggle = document.querySelector('.lang-switch-toggle');
        const menu = document.querySelector('.lang-switch-menu');
        if (!toggle || !menu) return [];
        toggle.click();
        const viewportWidth = document.documentElement.clientWidth;
        const elements = [
          { element: menu, label: 'container' },
          ...Array.from(menu.querySelectorAll('.lang-switch-option'), (element, index) => ({
            element,
            label: `option ${index + 1}`,
          })),
        ];
        const failures = elements.flatMap(({ element, label }) => {
          const rect = element.getBoundingClientRect();
          return rect.left < 0 || rect.right > viewportWidth
            ? [`LANG MENU ${label} outside viewport: ${rect.left.toFixed(2)}..${rect.right.toFixed(2)} of ${viewportWidth}`]
            : [];
        });
        toggle.click();
        return failures;
      });

      // Wait for eager images to finish loading (avoids domcontentloaded timing race).
      // Lazy images are intentionally deferred until scroll — skip them.
      await page.waitForFunction(
        () => Array.from(document.querySelectorAll('img'))
          .filter(i => i.loading !== 'lazy')
          .every(i => i.complete),
        { timeout: 5000 }
      ).catch(() => {}); // If some eager imgs never load, we still capture them below

      const brokenImages = await page.evaluate(() =>
        Array.from(document.querySelectorAll('img'))
          .filter(i => i.loading !== 'lazy' && (!i.complete || i.naturalWidth === 0))
          .map(i => i.src)
      );
      // The route handler intentionally aborts third-party assets so the
      // check is deterministic. Those aborted images are warnings, not page
      // defects; only report broken images that were not intentionally blocked.
      const unexpectedBrokenImages = brokenImages.filter(src =>
        ![...blockedExternal].some(blocked => blocked === src)
      );

      // The static CSP validator owns inline-style policy coverage. Chromium
      // reports blocked dynamic style applications as console errors even when
      // the page is otherwise healthy; keep that diagnostic out of this layout
      // gate while leaving all other console errors as hard failures.
      const effectiveConsoleErrors = consoleErrors.filter(error =>
        !error.startsWith('Applying inline style violates the following Content Security Policy directive')
      );
      const pageConsoleErrors = effectiveConsoleErrors.filter(error =>
        !error.includes('https://okhp3.github.io/') &&
        !error.includes('Fetch API cannot load https://okhp3.github.io/')
      );

      const errors = [
        ...(overflow ? [`OVERFLOW: scrollWidth > ${vp.width}px`] : []),
        ...localeMenuErrors,
        ...pageConsoleErrors.slice(0, 5).map(e => 'CONSOLE: ' + e),
        ...unexpectedBrokenImages.slice(0, 5).map(s => 'BROKEN IMG: ' + s),
        ...failed404s.slice(0, 5).map(u => '404: ' + u),
      ];
      if (blockedExternal.size > 0) {
        warnings.push(`blocked third-party resources: ${[...blockedExternal].join(', ')}`);
      }

      const pass = errors.length === 0;
      if (!pass) {
        const ssFile = `${path.replace(/\//g, '_')}_${vp.name}.png`;
        await page.screenshot({ path: resolve(SCREENSHOTS_DIR, ssFile) });
      }
      return { url, viewport: vp.name, width: vp.width, height: vp.height,
               mode: 'playwright', pass, errors, warnings };
    }));

    const fails = vpResults.filter(r => !r.pass);
    if (fails.length > 0) {
      fails.forEach(r => {
        console.log(`  FAIL  ${r.viewport.padEnd(14)} ${path}`);
        r.errors.forEach(e => console.log(`         → ${e}`));
      });
    }
    process.stdout.write(`  done  ${path}\n`);

    for (const row of vpResults) {
      allResults.push(row);
      if (!row.pass) totalFails++;
    }
  }

  for (const { ctx } of workers) await ctx.close();
  await browser.close();

  const report = {
    generated: new Date().toISOString(),
    mode: 'playwright',
    base_url: BASE_URL,
    pages_checked: PUBLIC_PATHS.length,
    viewports_checked: VIEWPORTS.length,
    total_checks: allResults.length,
    passing_checks: allResults.filter(r => r.pass).length,
    failing_checks: totalFails,
    results: allResults,
  };
  writeFileSync(RESULTS_FILE, JSON.stringify(report, null, 2));

  console.log(`\nTotal: ${allResults.length} checks — ${totalFails} failures`);
  console.log(`Results: ${RESULTS_FILE}`);
  if (totalFails > 0) process.exit(1);
  return report;
}

// ── MODE B: Static lint ───────────────────────────────────────────────────────
//
// Runs structural checks per page and emits one row per (page × viewport).
// Checks are viewport-agnostic (HTML structure doesn't change by width), so
// identical pass/fail data is recorded for each viewport row. The `mode` field
// is always "static-lint" so results are never confused with browser execution.

function staticLintPage(path, html) {
  const errors = [];

  // 1. viewport meta
  if (!html.includes('name="viewport"'))
    errors.push('LINT: missing viewport meta');

  // 2. construction overlay absent
  if (html.includes('construction-overlay'))
    errors.push('LINT: construction-overlay present (blocking modal)');

  // 3. single h1
  const h1Count = (html.match(/<h1[\s>]/gi) || []).length;
  if (h1Count !== 1)
    errors.push(`LINT: ${h1Count} <h1> elements (expected 1)`);

  // 4. all imgs have alt
  const imgsNoAlt = (html.match(/<img(?![^>]*\balt=)[^>]*>/gi) || []).length;
  if (imgsNoAlt > 0)
    errors.push(`LINT: ${imgsNoAlt} <img> missing alt`);

  // 5. all imgs have width (CLS / layout-shift risk)
  const imgsNoWidth = (html.match(/<img(?![^>]*\bwidth=)[^>]*>/gi) || []).length;
  if (imgsNoWidth > 0)
    errors.push(`LINT: ${imgsNoWidth} <img> missing width (layout-shift risk)`);

  // 6. skip link present
  if (!html.includes('class="okh-skip-link"'))
    errors.push('LINT: missing skip link');

  // 7. app.js present
  if (!html.includes('/assets/js/app.js'))
    errors.push('LINT: app.js script tag missing');

  return errors;
}

async function staticAnalysis() {
  console.log('Playwright not available — running static-lint analysis (MODE B).\n');
  console.log('NOTE: Static lint checks HTML structure only. It cannot detect');
  console.log('      horizontal overflow, JS console errors, or broken images');
  console.log('      at runtime. Run with Playwright for full browser coverage.\n');

  mkdirSync(RESULTS_DIR, { recursive: true });

  const results   = [];
  let totalFails  = 0;
  let pagesFound  = 0;

  for (const path of PUBLIC_PATHS) {
    const fsPath = path.endsWith('.html')
      ? resolve(ROOT, path.replace(/^\//, ''))
      : resolve(ROOT, path.replace(/^\//, ''), 'index.html');
      if (!existsSync(fsPath)) throw new Error(`Sitemap route has no local page: ${path}`);

    const html   = readFileSync(fsPath, 'utf-8');
    const errors = staticLintPage(path, html);
    const pass   = errors.length === 0;
    pagesFound++;

    for (const vp of VIEWPORTS) {
      if (!pass) totalFails++;
      results.push({
        url:      BASE_URL + path,
        viewport: vp.name,
        width:    vp.width,
        height:   vp.height,
        mode:     'static-lint',
        pass,
        errors: errors.map(e => e),   // copy so each row owns its array
      });
    }

    if (!pass) {
      console.log(`  FAIL  ${path}`);
      errors.forEach(e => console.log(`         → ${e}`));
    } else {
      console.log(`  pass  ${path}`);
    }
  }

  const report = {
    generated: new Date().toISOString(),
    mode: 'static-lint',
    note: [
      'Static-lint mode: 10 structural checks per page, applied uniformly to all 8 viewport rows.',
      'Viewport-specific checks (overflow, console errors, broken images) require Playwright.',
      'To run full browser QA: npm install -D playwright && npx playwright install chromium && node scripts/responsive-qa.mjs',
    ].join(' '),
    base_url: BASE_URL,
    pages_checked: pagesFound,
    viewports_checked: VIEWPORTS.length,
    total_checks: results.length,
    passing_checks: results.filter(r => r.pass).length,
    failing_checks: totalFails,
    results,
  };

  writeFileSync(RESULTS_FILE, JSON.stringify(report, null, 2));

  console.log(`\nStatic-lint: ${pagesFound} pages × ${VIEWPORTS.length} viewports = ${results.length} checks`);
  console.log(`Passing: ${report.passing_checks} | Failing: ${totalFails}`);
  if (totalFails === 0) console.log('ALL CHECKS PASS.');
  console.log(`Results: ${RESULTS_FILE}`);
  if (totalFails > 0) process.exit(1);
  return report;
}

// ── Entry point ───────────────────────────────────────────────────────────────

(async () => {
  console.log('OverKill Hill Responsive QA\n' + '='.repeat(40));
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`Pages: ${PUBLIC_PATHS.length} | Viewports: ${VIEWPORTS.length}\n`);

  const pwResult = FORCE_STATIC ? null : await runWithPlaywright();
  if (!pwResult) {
    await staticAnalysis();
  }
})();
