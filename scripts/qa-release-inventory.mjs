// Runtime coverage follows the publication allowlist, independently of indexing.
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
export const ROOT = fileURLToPath(new URL('../', import.meta.url));
export function loadReleasePaths(root = ROOT) {
  const code = 'import runpy,json;from pathlib import Path;m=runpy.run_path("scripts/build-release.py");print(json.dumps([p.as_posix() for p in m["load_public_pages"](Path.cwd())]))';
  const files = JSON.parse(execFileSync(process.platform === 'win32' ? 'py' : 'python3', ['-c', code], {cwd: root, encoding: 'utf8'}));
  const paths = files.map(file => '/' + file.replace(/(^|\/)index\.html$/, '$1'));
  if (!paths.length || new Set(paths).size !== paths.length) throw new Error('Invalid release route inventory');
  return paths;
}
