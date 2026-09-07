import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

for (const failure of ['import', 'launch']) {
  test(`responsive browser ${failure} failure is BLOCKED without a static fallback`, () => {
    const dir = mkdtempSync(join(tmpdir(), 'responsive-mode-'));
    try {
      const preload = join(dir, 'missing.cjs');
      const report = join(dir, 'results.json');
      writeFileSync(preload, `const M = require('module'); const original = M._load;
M._load = function(name, ...args) {
  if (name === 'playwright') {
    ${failure === 'import' ? "throw new Error('simulated missing Playwright');" : "return { chromium: { launch: async () => { throw new Error('simulated missing Chromium'); } } };"}
  }
  return original.call(this, name, ...args);
};`);
      const run = spawnSync(process.execPath, ['--require', preload, 'scripts/responsive-qa.mjs', `--report=${report}`], { encoding: 'utf8' });
      assert.notEqual(run.status, 0);
      const result = JSON.parse(readFileSync(report, 'utf8'));
      assert.equal(result.status, 'BLOCKED');
      assert.equal(result.mode, 'playwright');
      assert.equal(result.pages_checked, 0);
      assert.equal(result.browser_acceptance, 'NOT RUN');
      assert.match(result.error, /simulated missing/);
      assert.match(result.commit, /^[a-f0-9]{40}$/);
      assert.equal(result.environment.node, process.version);
    } finally { rmSync(dir, { recursive: true, force: true }); }
  });
}

test('explicit static mode reports browser acceptance NOT RUN and preserves tracked files', () => {
  const before = spawnSync('git', ['diff', '--binary'], { encoding: 'utf8' }).stdout;
  const run = spawnSync(process.execPath, ['scripts/responsive-qa.mjs', '--static'], { encoding: 'utf8' });
  const result = JSON.parse(readFileSync('test-results/responsive-qa/results.json', 'utf8'));
  assert.equal(result.mode, 'static-lint');
  assert.equal(result.browser_acceptance, 'NOT RUN');
  assert(result.pages_checked > 0);
  assert.equal(spawnSync('git', ['diff', '--binary'], { encoding: 'utf8' }).stdout, before);
  assert.match(run.stdout, /NOT RUN/);
});
