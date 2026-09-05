import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { test } from "node:test";

const run = promisify(execFile);

test("missing locale directories fail without scanning the pilot scaffold", async () => {
  await assert.rejects(
    run("python3", ["scripts/build-search-index.py", "--locale=zz"]),
    (error) => {
      assert.equal(error.code, 1);
      assert.match(error.stderr, /Locale source directory is missing: zz/);
      assert.doesNotMatch(error.stderr, /i18n[\\/]pilot/);
      return true;
    },
  );
});
