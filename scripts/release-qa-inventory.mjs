// Read the release builder's inventory without building or writing any files.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const root = fileURLToPath(new URL('../', import.meta.url));
export function loadReleaseInventory() {
  const code = 'import runpy,json;from pathlib import Path;m=runpy.run_path("scripts/build-release.py");print(json.dumps([p.as_posix() for p in m["load_public_pages"](Path.cwd())]))';
  const files = JSON.parse(execFileSync(process.env.PYTHON || (process.platform === 'win32' ? 'py' : 'python3'), ['-c', code], {
    cwd: root, encoding: 'utf8', env: { ...process.env, PYTHONUTF8: '1' },
  }));
  if (!files.length) throw new Error('Release inventory has no HTML files');
  return files.map(file => {
    const html = readFileSync(new URL(`../${file}`, import.meta.url), 'utf8');
    const path = '/' + (file === 'index.html' ? '' : file.replace(/\/index\.html$/, '/'));
    // Redirect notices, review pages, utilities, and locale drafts remain tested.
    const exception = null;
    return { file, path, exception, noindex: /content=["'][^"']*noindex/i.test(html) };
  });
}

export function loadFunctionalPaths() {
  const inventory = loadReleaseInventory();
  for (const entry of inventory.filter(entry => entry.exception)) {
    console.log(`QA exception: ${entry.path}: ${entry.exception}`);
  }
  const paths = inventory.filter(entry => !entry.exception).map(entry => entry.path);
  console.log(`Release QA inventory: ${inventory.length} shipped routes, ${paths.length} browser routes, ${inventory.length - paths.length} named exceptions.`);
  return paths;
}
