# CSP reporting

The site has one checked-in CSP policy for each page class: `standard`, `embed`,
`utility`, `diagram`, and `embed-diagram`. `scripts/generate-csp.py` calculates
hashes for the inline code that remains, writes `config/csp-policies.json`, and
applies the matching enforcing policy to every deployed HTML page. The edge
`_headers` file contains the union policy required for browsers that receive
headers; the page meta tag then tightens it by class.

## Local review

The included preview server accepts `POST /__csp-report` and appends valid
JSON reports to `/tmp/overkill-hill-csp-reports.jsonl`. Set `CSP_REPORT_FILE`
to choose another local path. Review the file with:

```sh
journalctl --no-pager  # only if the server is managed by systemd
cat /tmp/overkill-hill-csp-reports.jsonl
```

GitHub Pages is static and cannot execute this endpoint. In production, route
`/__csp-report` at the CDN or hosting edge to an approved collector, keeping
the same path and retaining only the fields needed for debugging. Do not
commit reports because URLs and browser details may contain user-provided
data. A live-edge check is intentionally separate from this static
configuration change.

## Route-wide browser check

The committed browser gate loads every route in `sitemap.xml` with the
enforcing policy active:

```sh
npm run test:csp
```

CI runs it against the local preview server. The check deliberately aborts
all cross-origin HTTP(S) requests, including Google Analytics, web fonts,
jsDelivr, GitHub Pages embeds, and avatar images. This keeps the result
deterministic and prevents an outage or rate limit at a third-party service
from looking like a site regression. The browser's generic
`Failed to load resource: net::ERR_FAILED` message for those intentional
aborts is reported as expected network noise.

The check does **not** suppress CSP diagnostics. CSP violations are emitted
before request interception and fail the route. Local request failures, local
HTTP errors, page-level JavaScript errors, Mermaid render warnings, and
Mermaid diagrams that do not produce an SVG also fail the route. Third-party
network availability and live-edge response-header enforcement remain
separate checks.

## Third-party runtime health

The CSP gate is intentionally not an availability check: it aborts every
cross-origin request so a CDN, analytics provider, font host, embed, or avatar
outage cannot make local validation flaky. To observe those user-visible
dependencies separately, run the browser harness in external-health mode
against a deployed site:

```sh
npm run test:csp:external -- \
  --base-url=https://overkillhill.com \
  --report=third-party-runtime-report.json
```

This mode loads every deployed route listed in `sitemap.xml` without
intercepting cross-origin requests. It inventories the external endpoints
requested (with query strings removed so per-visit analytics identifiers do not
enter CI artifacts), the routes and resource types that requested them, and
their HTTP or network outcomes. An endpoint with an HTTP error or failed
request is reported as an `EXTERNAL_OUTAGE`. CSP console diagnostics are reported in their own
`cspDiagnostics` section, and failures loading the local deployed route are
reported in `localFailures`; neither is silently folded into dependency
availability.

The command exits nonzero when it observes an external outage, CSP diagnostic,
or local route failure so it is useful in an operator-run check. The scheduled
and manually dispatched GitHub Actions monitor runs it with the failure
explicitly treated as non-blocking, uploads the JSON inventory, and prints the
classification. Pull-request and push validation run only the deterministic
local CSP gate above, never this network-dependent check.