#!/usr/bin/env node
/**
 * Route-wide browser check for the enforcing Content Security Policy.
 *
 * Every route in sitemap.xml is loaded in a real browser. Cross-origin
 * requests are intentionally aborted so the result does not depend on CDN,
 * analytics, font, or embedded-app availability. Chromium still evaluates
 * the page's CSP before a request reaches the route handler, so an
 * unexpected CSP diagnostic remains a hard failure.
 *
 * The check fails on:
 *   - CSP violations reported by the browser console
 *   - page-level JavaScript errors
 *   - failed local requests or local HTTP error responses
 *   - Mermaid render warnings or diagrams left without an SVG
 *
 * Usage:
 *   npm run test:csp
 *   node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5000
 *   node scripts/csp-qa.mjs --base-url=http://127.0.0.1:5000 --paths=/fixture.html
 *   node scripts/csp-qa.mjs --external-health --base-url=https://overkillhill.com
 *   node scripts/csp-qa.mjs --external-health --report=third-party-report.json
 */

import { chromium } from "playwright";
import { readFileSync, writeFileSync } from "node:fs";

const DEFAULT_BASE_URL = "http://127.0.0.1:5000";
const baseArg = process.argv.find((arg) => arg.startsWith("--base-url="));
const baseUrl = (baseArg ? baseArg.slice("--base-url=".length) : DEFAULT_BASE_URL)
  .replace(/\/$/, "");
const baseOrigin = new URL(baseUrl).origin;
const pathsArg = process.argv.find((arg) => arg.startsWith("--paths="));
const reportArg = process.argv.find((arg) => arg.startsWith("--report="));
const externalHealthMode =
  process.argv.includes("--external-health") || process.argv.includes("--check-external");

if (reportArg && !externalHealthMode) {
  throw new Error("--report requires --external-health");
}

function loadPublicPaths() {
  if (pathsArg) {
    const paths = pathsArg.slice("--paths=".length)
      .split(",")
      .map((path) => path.trim())
      .filter(Boolean);
    if (!paths.length) throw new Error("--paths must contain at least one route");
    return [...new Set(paths.map((path) => {
      const url = new URL(path, baseUrl);
      if (url.origin !== baseOrigin || !path.startsWith("/") || url.search || url.hash) {
        throw new Error(`Invalid --paths route: ${path}`);
      }
      return url.pathname || "/";
    }))];
  }

  const sitemap = readFileSync(new URL("../sitemap.xml", import.meta.url), "utf8");
  const locations = [...sitemap.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/g)]
    .map((match) => match[1]);
  if (!locations.length) throw new Error("sitemap.xml has no public routes");
  return [...new Set(locations.map((location) => {
    const url = new URL(location);
    if (url.origin !== "https://overkillhill.com" || url.search || url.hash) {
      throw new Error(`Invalid sitemap URL: ${location}`);
    }
    return url.pathname || "/";
  }))];
}

const PUBLIC_PATHS = loadPublicPaths();
const CSP_DIAGNOSTIC = /content security policy|violates the following.*policy|refused to .* policy/i;
const MERMAID_RENDER_ERROR = /^\[mermaid-init\] render error/i;
const INTENTIONAL_EXTERNAL_FAILURE = "Failed to load resource: net::ERR_FAILED";

function isHttpUrl(value) {
  return value.protocol === "http:" || value.protocol === "https:";
}

function isLocalUrl(value) {
  try {
    return new URL(value).origin === baseOrigin;
  } catch {
    return false;
  }
}

function formatConsoleMessage(message) {
  const location = message.location?.url ? ` (${message.location.url})` : "";
  return `${message.type.toUpperCase()}: ${message.text}${location}`;
}

async function checkRoute(browser, path) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const blockedExternal = new Set();
  const consoleMessages = [];
  const pageErrors = [];
  const failedLocalRequests = [];
  const localHttpErrors = [];

  await page.route("**/*", async (route) => {
    const requestUrl = new URL(route.request().url());
    if (isHttpUrl(requestUrl) && requestUrl.origin !== baseOrigin) {
      blockedExternal.add(requestUrl.origin);
      await route.abort();
      return;
    }
    await route.continue();
  });

  page.on("console", (message) => {
    consoleMessages.push({
      type: message.type(),
      text: message.text(),
      location: message.location(),
    });
  });
  page.on("pageerror", (error) => {
    pageErrors.push(error.stack || error.message);
  });
  page.on("requestfailed", (request) => {
    if (isLocalUrl(request.url())) {
      failedLocalRequests.push(
        `${request.url()} (${request.failure()?.errorText || "unknown failure"})`,
      );
    }
  });
  page.on("response", (response) => {
    if (isLocalUrl(response.url()) && response.status() >= 400) {
      localHttpErrors.push(`${response.status()} ${response.url()}`);
    }
  });

  const errors = [];
  let response;
  try {
    response = await page.goto(`${baseUrl}${path}`, {
      waitUntil: "commit",
      timeout: 30000,
    });
    if (!response) {
      errors.push("navigation returned no response");
    } else if (response.status() >= 400) {
      errors.push(`navigation returned HTTP ${response.status()}`);
    }
    try {
      await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    } catch {
      errors.push("DOMContentLoaded was not observed within 5s");
    }
    await page.waitForTimeout(250);
  } catch (error) {
    errors.push(`navigation failed: ${error.message.split("\n")[0]}`);
  }

  let diagramCount = 0;
  if (!errors.length) {
    diagramCount = await page.locator(".mermaid").count();
    for (let index = 0; index < diagramCount; index += 1) {
      await page.locator(".mermaid").nth(index).scrollIntoViewIfNeeded();
      await page.waitForTimeout(200);
    }
    await page.waitForTimeout(500);
  }

  const diagramState = await page.evaluate(() => {
    const diagrams = [...document.querySelectorAll(".mermaid")];
    return {
      expected: diagrams.length,
      rendered: diagrams.filter((diagram) => diagram.querySelector("svg")).length,
      unrendered: diagrams
        .map((diagram, index) => ({ diagram, index }))
        .filter(({ diagram }) => !diagram.querySelector("svg"))
        .map(({ index }) => index + 1),
    };
  }).catch(() => ({ expected: diagramCount, rendered: 0, unrendered: [] }));

  const cspViolations = consoleMessages.filter(
    ({ text }) => CSP_DIAGNOSTIC.test(text),
  );
  const mermaidErrors = consoleMessages.filter(
    ({ type, text }) => (type === "warning" || type === "error") && MERMAID_RENDER_ERROR.test(text),
  );
  // A route-aborted cross-origin resource produces this generic browser
  // message. It is expected only because external availability is deliberately
  // removed from this gate; all specific diagnostics, including CSP messages,
  // stay unsuppressed.
  const unexpectedConsoleErrors = consoleMessages.filter(
    ({ type, text }) => type === "error" && text !== INTENTIONAL_EXTERNAL_FAILURE,
  );

  errors.push(
    ...cspViolations.map((message) => `CSP: ${formatConsoleMessage(message)}`),
    ...pageErrors.map((message) => `PAGEERROR: ${message}`),
    ...unexpectedConsoleErrors
      .filter(({ text }) => !cspViolations.some((message) => message.text === text))
      .map((message) => `CONSOLE: ${formatConsoleMessage(message)}`),
    ...failedLocalRequests.map((request) => `LOCAL REQUEST FAILED: ${request}`),
    ...localHttpErrors.map((responseError) => `LOCAL HTTP ERROR: ${responseError}`),
    ...mermaidErrors.map((message) => `MERMAID: ${formatConsoleMessage(message)}`),
  );
  if (diagramState.expected !== diagramState.rendered) {
    errors.push(
      `MERMAID: rendered ${diagramState.rendered}/${diagramState.expected} diagrams` +
      (diagramState.unrendered.length
        ? ` (missing ${diagramState.unrendered.map((index) => `#${index}`).join(", ")})`
        : ""),
    );
  }

  await page.close();
  return {
    path,
    pass: errors.length === 0,
    errors,
    diagrams: diagramState,
    blockedExternal: [...blockedExternal].sort(),
  };
}

function getExternalDependency(dependencies, request) {
  const requestUrl = new URL(request.url());
  if (!isHttpUrl(requestUrl) || requestUrl.origin === baseOrigin) return null;

  // Query strings often contain per-visit analytics identifiers. They are
  // irrelevant to endpoint availability, so keep the inventory stable and
  // avoid copying those values into CI logs or uploaded reports.
  requestUrl.search = "";
  requestUrl.hash = "";
  const key = requestUrl.href;
  if (!dependencies.has(key)) {
    dependencies.set(key, {
      url: key,
      origin: requestUrl.origin,
      routes: new Set(),
      resourceTypes: new Set(),
      requestCount: 0,
      responses: [],
      failures: [],
    });
  }
  const dependency = dependencies.get(key);
  return dependency;
}

function serialiseExternalDependency(dependency) {
  const hasHttpError = dependency.responses.some(({ status }) => status >= 400);
  const hasFailure = dependency.failures.length > 0;
  const hasResponse = dependency.responses.length > 0;
  let state = "available";
  if (hasHttpError || hasFailure) state = "unavailable";
  else if (!hasResponse) state = "no-response";

  return {
    url: dependency.url,
    origin: dependency.origin,
    routes: [...dependency.routes].filter(Boolean).sort(),
    resourceTypes: [...dependency.resourceTypes].sort(),
    requestCount: dependency.requestCount,
    responses: dependency.responses,
    failures: dependency.failures,
    state,
  };
}

async function checkExternalRoute(browser, path) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const dependencies = new Map();
  const cspDiagnostics = [];
  const localErrors = new Set();

  page.on("console", (message) => {
    if (CSP_DIAGNOSTIC.test(message.text())) {
      cspDiagnostics.push(formatConsoleMessage({
        type: message.type(),
        text: message.text(),
        location: message.location(),
      }));
    }
  });
  page.on("request", (request) => {
    const dependency = getExternalDependency(dependencies, request);
    if (dependency) {
      dependency.requestCount += 1;
      dependency.resourceTypes.add(request.resourceType());
      dependency.routes.add(path);
    }
  });
  page.on("requestfailed", (request) => {
    if (isLocalUrl(request.url())) {
      localErrors.add(
        `local request failed: ${request.url()} ` +
        `(${request.failure()?.errorText || "unknown failure"})`,
      );
    }
  });
  page.on("response", (response) => {
    const request = response.request();
    const dependency = getExternalDependency(dependencies, request);
    if (dependency) {
      dependency.responses.push({
        status: response.status(),
        statusText: response.statusText(),
      });
    } else if (isLocalUrl(response.url()) && response.status() >= 400) {
      localErrors.add(`local HTTP error: ${response.status()} ${response.url()}`);
    }
  });

  try {
    const response = await page.goto(`${baseUrl}${path}`, {
      waitUntil: "commit",
      timeout: 30000,
    });
    if (!response) {
      localErrors.add("navigation returned no response");
    } else if (response.status() >= 400) {
      localErrors.add(`navigation returned HTTP ${response.status()}`);
    }
    try {
      await page.waitForLoadState("domcontentloaded", { timeout: 5000 });
    } catch {
      localErrors.add("DOMContentLoaded was not observed within 5s");
    }
    // Give deferred analytics, fonts, embeds, and images a short, bounded
    // window to make their requests without making monitoring hang on them.
    await page.waitForTimeout(1000);
  } catch (error) {
    localErrors.add(`navigation failed: ${error.message.split("\n")[0]}`);
  }

  await page.close();
  return {
    path,
    dependencies: [...dependencies.values()].map(serialiseExternalDependency),
    cspDiagnostics,
    localErrors: [...localErrors],
  };
}

function mergeExternalDependencies(results) {
  const merged = new Map();
  for (const result of results) {
    for (const dependency of result.dependencies) {
      if (!merged.has(dependency.url)) {
        merged.set(dependency.url, {
          ...dependency,
          routes: [],
          resourceTypes: [],
          responses: [],
          failures: [],
        });
      }
      const existing = merged.get(dependency.url);
      existing.routes = [...new Set([...existing.routes, ...dependency.routes])].sort();
      existing.resourceTypes = [
        ...new Set([...existing.resourceTypes, ...dependency.resourceTypes]),
      ].sort();
      existing.requestCount += dependency.requestCount;
      existing.responses.push(...dependency.responses);
      existing.failures.push(...dependency.failures);
      existing.state = existing.failures.length ||
        existing.responses.some(({ status }) => status >= 400)
        ? "unavailable"
        : existing.responses.length
          ? "available"
          : "no-response";
    }
  }
  return [...merged.values()].sort((left, right) => left.url.localeCompare(right.url));
}

async function runExternalHealth() {
  console.log("OverKill Hill third-party runtime health");
  console.log("=".repeat(40));
  console.log(`Base URL: ${baseUrl}`);
  console.log(`Routes: ${PUBLIC_PATHS.length}`);
  if (pathsArg) console.log(`Focused paths: ${PUBLIC_PATHS.join(", ")}`);
  console.log(
    "Cross-origin requests are allowed for this non-blocking availability check.",
  );
  console.log(
    "External outages, CSP diagnostics, and local route failures are reported separately.\n",
  );

  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const path of PUBLIC_PATHS) {
      const result = await checkExternalRoute(browser, path);
      results.push(result);
      console.log(
        `${result.localErrors.length ? "FAIL" : "CHECK"} ${path} ` +
        `(${result.dependencies.length} external request(s))`,
      );
      result.localErrors.forEach((error) => console.log(`      LOCAL: ${error}`));
      result.cspDiagnostics.forEach((message) => console.log(`      CSP: ${message}`));
    }
  } finally {
    await browser.close();
  }

  const dependencies = mergeExternalDependencies(results);
  const externalOutages = dependencies.filter(
    ({ state }) => state === "unavailable" || state === "no-response",
  );
  const cspDiagnostics = results.flatMap(({ path, cspDiagnostics: messages }) =>
    messages.map((message) => ({ path, message })),
  );
  const localFailures = results.flatMap(({ path, localErrors }) =>
    localErrors.map((error) => ({ path, error })),
  );
  const report = {
    version: 1,
    mode: "external-health",
    baseUrl,
    routes: PUBLIC_PATHS,
    dependencies,
    externalOutages,
    cspDiagnostics,
    localFailures,
    summary: {
      routes: results.length,
      dependencies: dependencies.length,
      available: dependencies.filter(({ state }) => state === "available").length,
      externalOutages: externalOutages.length,
      cspDiagnostics: cspDiagnostics.length,
      localFailures: localFailures.length,
    },
    status: externalOutages.length
      ? "EXTERNAL_OUTAGE"
      : cspDiagnostics.length
        ? "CSP_BLOCKED"
        : localFailures.length
          ? "LOCAL_FAILURE"
          : "PASS",
  };

  console.log(
    `\nExternal health: ${report.summary.dependencies} dependency URL(s), ` +
    `${report.summary.available} available, ` +
    `${report.summary.externalOutages} external outage(s), ` +
    `${report.summary.cspDiagnostics} CSP diagnostic(s), ` +
    `${report.summary.localFailures} local route failure(s).`,
  );
  externalOutages.forEach((dependency) => {
    console.log(`  EXTERNAL OUTAGE: ${dependency.url} (${dependency.state})`);
  });
  if (cspDiagnostics.length) {
    console.log("  CSP diagnostics were observed during the availability check.");
  }
  if (localFailures.length) {
    console.log("  Local route failures were observed during the availability check.");
  }

  if (reportArg) {
    const reportPath = reportArg.slice("--report=".length);
    if (!reportPath) throw new Error("--report must contain a file path");
    writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
    console.log(`Report: ${reportPath}`);
  }

  if (externalOutages.length || cspDiagnostics.length || localFailures.length) {
    process.exitCode = 1;
  }
}

async function main() {
  if (externalHealthMode) {
    await runExternalHealth();
    return;
  }
  console.log("OverKill Hill CSP browser QA");
  console.log("=".repeat(32));
  console.log(`Base URL: ${baseUrl}`);
  console.log(`Routes: ${PUBLIC_PATHS.length}`);
  if (pathsArg) console.log(`Focused paths: ${PUBLIC_PATHS.join(", ")}`);
  console.log("Cross-origin requests are blocked; blocked origins are reported as warnings.");
  console.log("CSP diagnostics remain unsuppressed.\n");

  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const path of PUBLIC_PATHS) {
      const result = await checkRoute(browser, path);
      results.push(result);
      if (result.pass) {
        console.log(`PASS  ${path} (${result.diagrams.rendered} Mermaid diagram(s))`);
      } else {
        console.log(`FAIL  ${path}`);
        result.errors.forEach((error) => console.log(`      → ${error}`));
      }
      if (result.blockedExternal.length) {
        console.log(`      WARN blocked cross-origin requests: ${result.blockedExternal.join(", ")}`);
      }
    }
  } finally {
    await browser.close();
  }

  const failures = results.filter((result) => !result.pass);
  const renderedDiagrams = results.reduce(
    (total, result) => total + result.diagrams.rendered,
    0,
  );
  console.log(
    `\nCSP QA: ${results.length} routes, ${renderedDiagrams} Mermaid diagram(s), ` +
    `${failures.length} route failure(s).`,
  );
  if (failures.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(`CSP QA could not run: ${error.stack || error.message}`);
  process.exitCode = 1;
});