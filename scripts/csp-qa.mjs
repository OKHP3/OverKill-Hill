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
 */

import { chromium } from "playwright";
import { readFileSync } from "node:fs";

const DEFAULT_BASE_URL = "http://127.0.0.1:5000";
const baseArg = process.argv.find((arg) => arg.startsWith("--base-url="));
const baseUrl = (baseArg ? baseArg.slice("--base-url=".length) : DEFAULT_BASE_URL)
  .replace(/\/$/, "");
const baseOrigin = new URL(baseUrl).origin;

function loadPublicPaths() {
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

async function main() {
  console.log("OverKill Hill CSP browser QA");
  console.log("=".repeat(32));
  console.log(`Base URL: ${baseUrl}`);
  console.log(`Routes: ${PUBLIC_PATHS.length}`);
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