import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, mkdirSync, copyFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { loadReleasePaths, ROOT } from '../scripts/qa-release-inventory.mjs';

test('functional inventory includes shipped noindex and utility routes', () => {
  const paths = loadReleasePaths();
  for (const route of ['/search/', '/404.html', '/under-construction.html', '/es-mx/']) {
    assert(paths.includes(route), `missing shipped route ${route}`);
  }
  const sitemap = readFileSync(join(ROOT, 'sitemap.xml'), 'utf8');
  assert(!sitemap.includes('https://overkillhill.com/search/'));
  assert(!paths.some(path => path.startsWith('/assets/murderbird/')));
  assert.equal(new Set(paths).size, paths.length);
});

test('missing Chromium fails explicitly and reports do not alter tracked sources', () => {
  const temporary = mkdtempSync(join(tmpdir(), 'a10-browser-'));
  const before = execFileSync('git', ['diff', '--binary', 'HEAD'], {cwd: ROOT});
  try {
    const report = join(temporary, 'blocked.json');
    const result = spawnSync(process.execPath, ['scripts/responsive-qa.mjs', `--report=${report}`], {
      cwd: ROOT, encoding: 'utf8', env: {...process.env, PLAYWRIGHT_BROWSERS_PATH: join(temporary, 'missing')},
    });
    assert.equal(result.status, 2, result.stderr);
    assert.match(result.stderr, /BLOCKED: browser QA NOT RUN/);
    const evidence = JSON.parse(readFileSync(report));
    assert.equal(evidence.status, 'BLOCKED');
    assert.equal(evidence.browser_acceptance, false);
    assert.equal(evidence.mode, 'playwright');
    assert.match(evidence.commit, /^[0-9a-f]{40}$/);
    assert.deepEqual(evidence.results, []);
    assert.deepEqual(execFileSync('git', ['diff', '--binary', 'HEAD'], {cwd: ROOT}), before);
  } finally { rmSync(temporary, {recursive: true, force: true}); }
});

test('explicit static mode cannot claim browser acceptance', () => {
  const temporary = mkdtempSync(join(tmpdir(), 'a10-static-'));
  try {
    const report = join(temporary, 'static.json');
    const result = spawnSync(process.execPath, ['scripts/responsive-qa.mjs', '--static', `--report=${report}`], {cwd: ROOT, encoding: 'utf8'});
    assert([0, 1].includes(result.status), result.stderr);
    const evidence = JSON.parse(readFileSync(report));
    assert.equal(evidence.mode, 'static-lint');
    assert.equal(evidence.status, 'NOT RUN');
    assert.equal(evidence.browser_acceptance, false);
    assert.equal(evidence.pages_checked, loadReleasePaths().length);
  } finally { rmSync(temporary, {recursive: true, force: true}); }
});


test('new allowlisted noindex routes enter coverage without sitemap edits', () => {
  const root = mkdtempSync(join(tmpdir(), 'a10-inventory-'));
  try {
    for (const directory of ['scripts', 'site-src', 'es-mx/new-draft']) mkdirSync(join(root, directory), {recursive: true});
    copyFileSync(join(ROOT, 'scripts/build-release.py'), join(root, 'scripts/build-release.py'));
    writeFileSync(join(root, 'site-src/pages.json'), JSON.stringify({pages: [{path: 'index.html'}]}));
    writeFileSync(join(root, 'sitemap.xml'), '<urlset><url><loc>https://overkillhill.com/</loc></url></urlset>');
    writeFileSync(join(root, 'es-mx/new-draft/index.html'), '<meta name="robots" content="noindex">');
    assert.deepEqual(loadReleasePaths(root), ['/es-mx/new-draft/', '/']);
  } finally { rmSync(root, {recursive: true, force: true}); }
});


test('default static audit output leaves tracked sources unchanged', () => {
  const before = execFileSync('git', ['diff', '--binary', 'HEAD'], {cwd: ROOT});
  const result = spawnSync(process.platform === 'win32' ? 'py' : 'python3', ['scripts/audit-site.py', '--quiet'], {cwd: ROOT, encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /test-results\/static-audit\/report.md/);
  assert.deepEqual(execFileSync('git', ['diff', '--binary', 'HEAD'], {cwd: ROOT}), before);
});
