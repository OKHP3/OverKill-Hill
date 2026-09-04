import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { after, before, test } from "node:test";
import { spawn } from "node:child_process";
import { dirname, join } from "node:path";

const testsDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = join(testsDirectory, "..");
const cspQaScript = join(repositoryRoot, "scripts", "csp-qa.mjs");
const fixtureDirectory = join(testsDirectory, "fixtures", "csp");
const fixtureFiles = new Map([
  ["/console-violation.html", "console-violation.html"],
  ["/page-error.html", "page-error.html"],
  ["/missing-resource.html", "missing-resource.html"],
  ["/unrendered-mermaid.html", "unrendered-mermaid.html"],
]);

let server;
let baseUrl;

async function serveFixture(request, response) {
  const path = new URL(request.url, "http://csp-fixture").pathname;

  if (path === "/boom.js") {
    response.writeHead(200, { "content-type": "text/javascript" });
    response.end('throw new Error("fixture page error");');
    return;
  }

  if (path === "/missing-local.png") {
    response.writeHead(404, { "content-type": "text/plain" });
    response.end("fixture resource intentionally missing");
    return;
  }

  const fixtureName = fixtureFiles.get(path);
  if (fixtureName) {
    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(await readFile(join(fixtureDirectory, fixtureName)));
    return;
  }

  response.writeHead(404, { "content-type": "text/plain" });
  response.end("fixture route not found");
}

before(async () => {
  server = createServer((request, response) => {
    serveFixture(request, response).catch((error) => {
      response.writeHead(500, { "content-type": "text/plain" });
      response.end(error.message);
    });
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  baseUrl = `http://127.0.0.1:${address.port}`;
});

after(async () => {
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
});

function runCspQa(path) {
  return new Promise((resolve, reject) => {
    const child = spawn(
      process.execPath,
      [cspQaScript, `--base-url=${baseUrl}`, `--paths=${path}`],
      { cwd: repositoryRoot },
    );
    let stdout = "";
    let stderr = "";
    const timeout = setTimeout(() => {
      child.kill("SIGKILL");
      reject(new Error(`CSP QA timed out for ${path}`));
    }, 60000);

    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", (error) => {
      clearTimeout(timeout);
      reject(error);
    });
    child.on("close", (status, signal) => {
      clearTimeout(timeout);
      resolve({
        output: `${stdout}\n${stderr}`,
        status,
        signal,
      });
    });
  });
}

test("fails on a browser CSP console violation", async () => {
  const result = await runCspQa("/console-violation.html");
  assert.notEqual(result.status, 0, result.output);
  const output = result.output;
  assert.match(output, /CSP: ERROR:/);
  assert.match(output, /console-violation\.html/);
});

test("fails on a page-level JavaScript error", async () => {
  const result = await runCspQa("/page-error.html");
  assert.notEqual(result.status, 0, result.output);
  const output = result.output;
  assert.match(output, /PAGEERROR: Error: fixture page error/);
  assert.match(output, /page-error\.html/);
});

test("fails on a failed local resource", async () => {
  const result = await runCspQa("/missing-resource.html");
  assert.notEqual(result.status, 0, result.output);
  const output = result.output;
  assert.match(output, /LOCAL HTTP ERROR: 404 .*missing-local\.png/);
});

test("fails when a Mermaid diagram does not render", async () => {
  const result = await runCspQa("/unrendered-mermaid.html");
  assert.notEqual(result.status, 0, result.output);
  const output = result.output;
  assert.match(output, /MERMAID: rendered 0\/1 diagrams/);
  assert.match(output, /unrendered-mermaid\.html/);
});