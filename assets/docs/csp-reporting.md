# CSP reporting

The site has one checked-in CSP policy for each page class: `standard`, `embed`,
and `utility`. `scripts/generate-csp.py` calculates hashes for the inline code
that remains, writes `config/csp-policies.json`, and applies the matching
enforced policy to every deployed HTML page. The edge `_headers` file contains
the union policy required for browsers that receive headers; the page meta tag
then tightens it by class.

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