import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { chromium } from 'playwright';

test('interactive Mermaid SVG links remain in the keyboard order with group semantics', async () => {
  const source = readFileSync(new URL('../assets/js/mermaid-init.js', import.meta.url), 'utf8');
  const enhance = source.slice(source.indexOf('function enhanceMermaidLinks('), source.indexOf('\nfunction renderOne('));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    await page.setContent('<button id="start">Before</button><div id="diagram" role="img"><svg role="img"><a href="#target" target="_blank"><text>Project</text></a><a><text>Decoration</text></a></svg></div><button id="target">After</button>');
    await page.evaluate('(() => {' + enhance + '\nenhanceMermaidLinks(document.getElementById("diagram"));})()');
    await page.locator('#start').focus();
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.getAttribute('href')), '#target');
    assert.equal(await page.locator('#diagram').getAttribute('role'), 'group');
    assert.equal(await page.locator('svg').getAttribute('role'), 'group');
    assert.equal(await page.locator('svg a[href]').getAttribute('rel'), 'noopener noreferrer');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'target');
  } finally { await browser.close(); }
});
