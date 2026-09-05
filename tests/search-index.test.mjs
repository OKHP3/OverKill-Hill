import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { test } from "node:test";

const run = promisify(execFile);

test("search extractor drops nested navigation and keeps a useful snippet", async () => {
  const script = [
    "import importlib.util",
    "from pathlib import Path",
    "spec = importlib.util.spec_from_file_location('builder', 'scripts/build-search-index.py')",
    "module = importlib.util.module_from_spec(spec)",
    "spec.loader.exec_module(module)",
    "html = '''<header class=\"site-header\"><nav class=\"primary-nav\"><div><a>Navigation omega</a></div></nav><a class=\"okh-skip-link\">Skip omega</a></header><main><h2>Real omega heading</h2><p>''' + ('x ' * 120) + '''omega at the end.</p></main>'''",
    "parser = module.TextExtractor()",
    "parser.feed(html)",
    "text = parser.collected_text()",
    "assert 'Navigation' not in text and 'Skip omega' not in text",
    "assert 'Real omega heading' in text",
    "assert len(module.excerpt(text, 80)) <= 81",
    "print('parser regression passed')",
  ].join(";");
  const { stdout } = await run("python3", ["-c", script]);
  assert.match(stdout, /parser regression passed/);
});

test("committed search index is current", async () => {
  const { stdout } = await run("python3", ["scripts/build-search-index.py", "--check"]);
  assert.match(stdout, /Search index is current/);
});
