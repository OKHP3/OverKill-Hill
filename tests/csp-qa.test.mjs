import assert from "node:assert/strict";
import { createServer } from "node:http";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { after, before, test } from "node:test";
import { spawn } from "node:child_process";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";

const testsDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = join(testsDirectory, "..");
const cspQaScript = join(repositoryRoot, "scripts", "csp-qa.mjs");
const fixtureDirectory = join(testsDirectory, "fixtures", "csp");
const fixtureFiles = new Map([
  ["/console-violation.html", "console-violation.html"],
  ["/page-error.html", "page-error.html"],
  ["/missing-resource.html", "missing-resource.html"],
  ["/unrendered-mermaid.html", "unrendered-mermaid.html"],
  ["/external-network-failure.html", "external-network-failure.html"],
  ["/external-csp-blocked.html", "external-csp-blocked.html"],
  ["/external-csp-and-outage.html", "external-csp-and-outage.html"],
  ["/external-csp-shared.html", "external-csp-shared.html"],
  ["/external-outage-shared.html", "external-outage-shared.html"],
]);

let server;
let externalServer;
let baseUrl;
let externalBaseUrl;
let focusedReportDirectory;
let focusedReportNumber = 0;
const focusedResults = [];

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

  if (path === "/external-health.html") {
    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(`<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>External health fixture</title></head>
  <body>
    <main><h1>External health fixture</h1>
      <img src="${externalBaseUrl}/healthy.png" alt="healthy dependency">
      <img src="${externalBaseUrl}/outage.png" alt="unavailable dependency">
    </main>
  </body>
</html>`);
    return;
  }

  const fixtureName = fixtureFiles.get(path);
  if (fixtureName) {
    const fixture = await readFile(join(fixtureDirectory, fixtureName), "utf8");
    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(fixture.replaceAll("__EXTERNAL_BASE_URL__", externalBaseUrl));
    return;
  }

  response.writeHead(404, { "content-type": "text/plain" });
  response.end("fixture route not found");
}

before(async () => {
  focusedReportDirectory = await mkdtemp(join(tmpdir(), "csp-focused-results-"));
  externalServer = createServer((request, response) => {
    const path = new URL(request.url, "http://external-fixture").pathname;
    if (path === "/healthy.png") {
      response.writeHead(200, { "content-type": "image/png" });
      response.end(Buffer.from(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
        "base64",
      ));
      return;
    }
    if (path === "/outage.png") {
      response.writeHead(503, { "content-type": "text/plain" });
      response.end("fixture dependency intentionally unavailable");
      return;
    }
    if (path === "/aborted.png") {
      request.socket.destroy();
      return;
    }
    if (path === "/blocked.png") {
      response.writeHead(200, { "content-type": "image/png" });
      response.end(Buffer.from(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
        "base64",
      ));
      return;
    }
    if (path === "/shared.png") {
      response.writeHead(503, { "content-type": "text/plain" });
      response.end("shared fixture dependency intentionally unavailable");
      return;
    }
    response.writeHead(404, { "content-type": "text/plain" });
    response.end("external fixture route not found");
  });
  await new Promise((resolve) => externalServer.listen(0, "127.0.0.1", resolve));
  const externalAddress = externalServer.address();
  externalBaseUrl = `http://127.0.0.1:${externalAddress.port}`;

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
  await new Promise((resolve, reject) =>
    externalServer.close((error) => error ? reject(error) : resolve()));
  const reportPath = process.env.CSP_FIXTURE_REPORT;
  if (reportPath) {
    try {
      await writeFile(reportPath, `${JSON.stringify({
        version: 1,
        mode: "csp-fixtures",
        fixtures: focusedResults,
      }, null, 2)}\n`);
    } catch (error) {
      console.error(`Could not write CSP fixture report: ${error.message}`);
    }
  }
  await rm(focusedReportDirectory, { recursive: true, force: true });
});

function runCspQa(path, flags = []) {
  return new Promise((resolve, reject) => {
    const focused = !flags.includes("--external-health") && !flags.includes("--check-external");
    const reportPath = focused
      ? join(focusedReportDirectory, `${focusedReportNumber++}.json`)
      : null;
    const child = spawn(
      process.execPath,
      [
        cspQaScript,
        `--base-url=${baseUrl}`,
        `--paths=${path}`,
        ...(reportPath ? [`--report=${reportPath}`] : []),
        ...flags,
      ],
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
      const result = {
        output: `${stdout}\n${stderr}`,
        status,
        signal,
      };
      if (reportPath) {
        readFile(reportPath, "utf8")
          .then((content) => {
            const report = JSON.parse(content);
            focusedResults.push({
              path,
              pass: report.results?.[0]?.pass ?? status === 0,
              errors: report.results?.[0]?.errors ?? [],
            });
            resolve({ ...result, report });
          })
          .catch(reject);
        return;
      }
      resolve(result);
    });
  });
}

function runFixtureSummary(reportPath, summaryPath) {
  return new Promise((resolve, reject) => {
    const child = spawn(
      process.execPath,
      [
        cspQaScript,
        `--fixture-summary=${reportPath}`,
        `--summary=${summaryPath}`,
      ],
      { cwd: repositoryRoot },
    );
    let stdout = "";
    let stderr = "";
    const timeout = setTimeout(() => {
      child.kill("SIGKILL");
      reject(new Error("CSP fixture summary timed out"));
    }, 10000);

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

test("keeps every browser diagnostic category visible in the focused summary", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-summary-"));
  const reportPath = join(reportDirectory, "fixture-report.json");
  const summaryPath = join(reportDirectory, "summary.md");
  const diagnostics = [
    ["csp", "CSP", "CSP: blocked | policy\nwith a second line"],
    ["page-error", "PAGEERROR", "PAGEERROR: Error: page exploded"],
    ["console", "CONSOLE", "CONSOLE: ERROR: console exploded"],
    [
      "local-request",
      "LOCAL REQUEST FAILED",
      "LOCAL REQUEST FAILED: /app.js (net::ERR_FAILED)",
    ],
    [
      "local-http",
      "LOCAL HTTP ERROR",
      "LOCAL HTTP ERROR: 404 /missing.png",
    ],
    ["mermaid", "MERMAID", "MERMAID: ERROR: render failed"],
  ];
  const fixtures = diagnostics.map(([name, category, message]) => ({
    path: `/${name}.html`,
    errors: [message],
    category,
  }));
  fixtures.push({
    path: "/unknown.html",
    errors: ["NETWORK: new browser diagnostic | preserve this"],
  });

  try {
    await writeFile(reportPath, `${JSON.stringify({
      version: 1,
      mode: "csp-fixtures",
      fixtures,
    })}\n`);

    const result = await runFixtureSummary(reportPath, summaryPath);
    assert.equal(result.status, 0, result.output);
    const summary = await readFile(summaryPath, "utf8");

    for (const [name, category] of diagnostics) {
      assert.match(
        summary,
        new RegExp(`\\| /${name}\\.html \\| ${category} \\|`),
        `missing focused summary category ${category}`,
      );
      assert.doesNotMatch(
        summary,
        new RegExp(`\\| /${name}\\.html \\| none observed \\|`),
        `recognized category ${category} was rendered as none observed`,
      );
    }
    assert.match(
      summary,
      /\| \/csp\.html \| CSP \| CSP: blocked \\| policy with a second line \|/,
    );
    assert.match(
      summary,
      /\| \/unknown\.html \| none observed \| NETWORK: new browser diagnostic \\| preserve this \|/,
    );
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});

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

test("reports external outages separately from the local CSP gate", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-external-health-"));
  const reportPath = join(reportDirectory, "report.json");
  try {
    const result = await runCspQa("/external-health.html", [
      "--external-health",
      `--report=${reportPath}`,
    ]);
    assert.notEqual(result.status, 0, result.output);
    assert.match(result.output, /EXTERNAL OUTAGE:/);
    assert.doesNotMatch(result.output, /CSP diagnostics were observed/);

    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.mode, "external-health");
    assert.equal(report.status, "EXTERNAL_OUTAGE");
    assert.equal(report.summary.cspDiagnostics, 0);
    assert.equal(report.summary.localFailures, 0);
    assert.equal(report.summary.externalOutages, 1);

    const healthy = report.dependencies.find(({ url }) => url.endsWith("/healthy.png"));
    const outage = report.dependencies.find(({ url }) => url.endsWith("/outage.png"));
    assert.equal(healthy.state, "available");
    assert.equal(outage.state, "unavailable");
    assert.ok(healthy.requestCount >= 1);
    assert.ok(outage.requestCount >= 1);
    assert.deepEqual(outage.routes, ["/external-health.html"]);
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});

test("preserves the browser failure reason for an aborted external request", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-network-failure-"));
  const reportPath = join(reportDirectory, "report.json");
  try {
    const result = await runCspQa("/external-network-failure.html", [
      "--external-health",
      `--report=${reportPath}`,
    ]);
    assert.notEqual(result.status, 0, result.output);
    assert.match(result.output, /EXTERNAL OUTAGE:/);
    assert.match(result.output, /net::ERR_/);

    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.status, "EXTERNAL_OUTAGE");
    assert.equal(report.summary.externalOutages, 1);

    const aborted = report.dependencies.find(({ url }) => url.endsWith("/aborted.png"));
    assert.ok(aborted, JSON.stringify(report, null, 2));
    assert.equal(aborted.state, "unavailable");
    assert.equal(aborted.responses.length, 0);
    assert.equal(aborted.failures.length, 1);
    assert.match(aborted.failures[0].errorText, /^net::ERR_/);
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});

test("reports CSP-blocked dependencies separately from external outages", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-blocked-health-"));
  const reportPath = join(reportDirectory, "report.json");
  try {
    const result = await runCspQa("/external-csp-blocked.html", [
      "--external-health",
      `--report=${reportPath}`,
    ]);
    assert.notEqual(result.status, 0, result.output);
    assert.match(result.output, /CSP diagnostics were observed/);
    assert.doesNotMatch(result.output, /EXTERNAL OUTAGE:/);

    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.mode, "external-health");
    assert.equal(report.status, "CSP_BLOCKED");
    assert.equal(report.summary.cspDiagnostics, 1);
    assert.equal(report.summary.externalOutages, 0);
    assert.equal(report.summary.localFailures, 0);

    const blocked = report.dependencies.find(({ url }) => url.endsWith("/blocked.png"));
    assert.ok(blocked, JSON.stringify(report, null, 2));
    assert.equal(blocked.state, "blocked-by-csp");
    assert.equal(blocked.cspBlocked, true);
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});

test("keeps an external outage visible alongside a CSP-blocked dependency", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-mixed-health-"));
  const reportPath = join(reportDirectory, "report.json");
  try {
    const result = await runCspQa("/external-csp-and-outage.html", [
      "--external-health",
      `--report=${reportPath}`,
    ]);
    assert.notEqual(result.status, 0, result.output);
    assert.match(result.output, /EXTERNAL OUTAGE:/);
    assert.match(result.output, /CSP diagnostics were observed/);

    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.mode, "external-health");
    assert.equal(report.status, "EXTERNAL_OUTAGE");
    assert.equal(report.summary.dependencies, 2);
    assert.equal(report.summary.externalOutages, 1);
    assert.equal(report.summary.cspDiagnostics, 1);
    assert.equal(report.summary.localFailures, 0);
    assert.equal(report.externalOutages.length, 1);
    assert.equal(report.cspDiagnostics.length, 1);

    const blocked = report.dependencies.find(({ url }) => url.endsWith("/blocked.png"));
    const outage = report.dependencies.find(({ url }) => url.endsWith("/outage.png"));
    assert.ok(blocked, JSON.stringify(report, null, 2));
    assert.ok(outage, JSON.stringify(report, null, 2));
    assert.equal(blocked.state, "blocked-by-csp");
    assert.equal(blocked.cspBlocked, true);
    assert.equal(outage.state, "unavailable");
    assert.equal(outage.cspBlocked, false);
    assert.ok(outage.responses.some(({ status }) => status === 503));
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});

test("keeps a shared-route outage visible when another route blocks the same URL with CSP", async () => {
  const reportDirectory = await mkdtemp(join(tmpdir(), "csp-shared-health-"));
  const reportPath = join(reportDirectory, "report.json");
  const paths = "/external-csp-shared.html,/external-outage-shared.html";
  try {
    const result = await runCspQa(paths, [
      "--external-health",
      `--report=${reportPath}`,
    ]);
    assert.notEqual(result.status, 0, result.output);
    assert.match(result.output, /EXTERNAL OUTAGE:/);
    assert.match(result.output, /CSP diagnostics were observed/);

    const report = JSON.parse(await readFile(reportPath, "utf8"));
    assert.equal(report.status, "EXTERNAL_OUTAGE");
    assert.deepEqual(report.routes, [
      "/external-csp-shared.html",
      "/external-outage-shared.html",
    ]);
    assert.equal(report.summary.dependencies, 1);
    assert.equal(report.summary.externalOutages, 1);
    assert.equal(report.summary.cspDiagnostics, 1);

    const shared = report.dependencies.find(({ url }) => url.endsWith("/shared.png"));
    assert.ok(shared, JSON.stringify(report, null, 2));
    assert.deepEqual(shared.routes, [
      "/external-csp-shared.html",
      "/external-outage-shared.html",
    ]);
    assert.equal(shared.cspBlocked, true);
    assert.equal(shared.state, "unavailable");
    assert.ok(shared.responses.some(({ status }) => status === 503));

    const outage = report.externalOutages.find(({ url }) => url.endsWith("/shared.png"));
    assert.ok(outage, JSON.stringify(report, null, 2));
    assert.deepEqual(outage.routes, shared.routes);
    assert.ok(outage.responses.some(({ status }) => status === 503));
    assert.equal(outage.state, "unavailable");
  } finally {
    await rm(reportDirectory, { recursive: true, force: true });
  }
});