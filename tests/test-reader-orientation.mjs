import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';

const base = process.env.BASE_URL || 'http://127.0.0.1:5000';
const browser = await chromium.launch({ headless: true });
const results = [];
const screenshotDir = process.env.A15_SCREENSHOT_DIR;
if (screenshotDir) await mkdir(screenshotDir, { recursive: true });
const check = (name, ok, detail = '') => results.push({ name, ok, detail });

async function runContext(label, options = {}) {
  const context = await browser.newContext({ viewport: options.viewport || { width: 1280, height: 800 }, colorScheme: options.colorScheme || 'light', reducedMotion: options.reducedMotion || 'no-preference', javaScriptEnabled: options.javaScriptEnabled ?? true });
  const page = await context.newPage();
  let blockedRequests = 0;
  if (options.blockApp) await page.route(/\/assets\/js\/app\.js(?:\?|$)/, route => {
    blockedRequests++;
    return route.abort();
  });
  await page.goto(`${base}/contact/`, { waitUntil: 'domcontentloaded' });
  const contact = await page.locator('body').innerText();
  check(`${label}: contact copy`, contact.includes('What are you trying to untangle?') && contact.includes('contact@overkillhill.com'));
  check(`${label}: contact heading visible`, await page.getByRole('heading', { name: 'What are you trying to untangle?' }).isVisible());
  check(`${label}: no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  const mailto = await page.locator('a[href^="mailto:"]').first().getAttribute('href');
  check(`${label}: mailto fallback`, mailto === 'mailto:contact@overkillhill.com');
  if (screenshotDir && options.screenshot) await page.screenshot({ path: join(screenshotDir, options.screenshot), fullPage: true });
  await page.goto(`${base}/writings/first-diagram-is-a-liar/`, { waitUntil: 'domcontentloaded' });
  const essay = await page.locator('body').innerText();
  check(`${label}: evidence route copy`, essay.includes('Want to inspect the evidence first?'));
  check(`${label}: evidence route visible`, await page.locator('p').filter({ hasText: 'Want to inspect the evidence first?' }).isVisible());
  const links = await page.locator('p').filter({ hasText: 'Want to inspect the evidence first?' }).locator('a').evaluateAll(as => as.map(a => a.getAttribute('href')));
  check(`${label}: five evidence links`, links.length === 5 && links.includes('#scoring-model') && links.includes('#v1-diagrams') && links.includes('#v2-diagrams') && links.includes('#council-scoring') && links.includes('#version-history'));
  const original = await page.locator('nav[aria-label="Jump to article sections"] a').evaluateAll(as => as.map(a => a.getAttribute('href')));
  check(`${label}: original jump menu`, original.includes('#roy') && original.includes('#council-scoring') && original.includes('#artifacts') && original.includes('#version-history'));
  const essayOverflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  check(`${label}: essay no horizontal overflow`, essayOverflow);
  const evidenceLinks = page.locator('p').filter({ hasText: 'Want to inspect the evidence first?' }).locator('a');
  for (let i = 0; i < links.length; i++) {
    await page.goto(`${base}/writings/first-diagram-is-a-liar/`, { waitUntil: 'domcontentloaded' });
    const before = await page.url();
    await evidenceLinks.nth(i).focus();
    const focusVisible = await evidenceLinks.nth(i).evaluate(el => el === document.activeElement);
    check(`${label}: keyboard focus ${links[i]}`, focusVisible);
    await page.keyboard.press('Enter');
    const hashReached = (await page.url()).endsWith(links[i]);
    const focusReached = await page.locator(links[i]).evaluate(el => el === document.activeElement || el.contains(document.activeElement));
    check(`${label}: keyboard activation ${links[i]}`, hashReached && (options.javaScriptEnabled === false || options.blockApp || focusReached));
    if (i === 0) {
      await page.goBack();
      check(`${label}: Back restores URL`, (await page.url()) === before);
      await page.goForward();
      check(`${label}: Forward restores fragment`, (await page.url()).endsWith(links[i]));
    }
  }
  await page.goto(`${base}/fr/contact/`, { waitUntil: 'domcontentloaded' });
  const frContact = await page.locator('body').innerText();
  check(`${label}: French Contact block`, frContact.includes('Qu’essayez-vous de démêler') && frContact.includes('contact@overkillhill.com'));
  check(`${label}: French mailto unchanged`, await page.locator('a[href^="mailto:"]').first().getAttribute('href') === 'mailto:contact@overkillhill.com');
  check(`${label}: French heading visible`, await page.getByRole('heading', { name: /Qu’essayez-vous de démêler/ }).isVisible());
  for (const [locale, heading] of [['en-gb', 'What are you trying to untangle?'], ['es-mx', '¿Qué estás tratando de desenredar?']]) {
    await page.goto(`${base}/${locale}/contact/`, { waitUntil: 'domcontentloaded' });
    check(`${label}: ${locale} heading visible`, await page.getByRole('heading', { name: heading, exact: true }).isVisible());
    check(`${label}: ${locale} remains noindex`, (await page.locator('meta[name="robots"]').getAttribute('content')).includes('noindex'));
    check(`${label}: ${locale} no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
  }
  if (options.blockApp) check(`${label}: script requests actually blocked`, blockedRequests >= 3);
  await context.close();
}

await runContext('desktop light', { screenshot: 'a15-contact-desktop.png' });
await runContext('phone dark reduced motion', { viewport: { width: 390, height: 844 }, colorScheme: 'dark', reducedMotion: 'reduce', screenshot: 'a15-contact-phone.png' });
await runContext('blocked app.js', { blockApp: true });
await runContext('no javascript', { javaScriptEnabled: false });

await browser.close();
const failed = results.filter(r => !r.ok);
for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'} ${r.name}${r.detail ? `: ${r.detail}` : ''}`);
if (failed.length) process.exit(1);
