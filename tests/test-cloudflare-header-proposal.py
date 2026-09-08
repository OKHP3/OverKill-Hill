"""Offline A19 contract tests. These do not emulate Cloudflare's edge."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "config/hosting/cloudflare-staging/_headers"


def parse_single_rule(text):
    """Accept only this proposal's one-rule subset, preventing overlap drift."""
    rules = []
    headers = {}
    for line in text.splitlines():
        if len(line) > 2000:
            raise ValueError("Cloudflare line limit exceeded")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            rules.append(line)
            continue
        name, value = line.strip().split(":", 1)
        name = name.lower()
        if name in headers:
            raise ValueError("Repeated header would combine values")
        headers[name] = value.strip()
    if rules != ["/*"]:
        raise ValueError("Proposal requires one universal rule")
    return headers


class HeaderProposalTests(unittest.TestCase):
    def setUp(self):
        self.text = ADAPTER.read_text()
        self.headers = parse_single_rule(self.text)

    def test_host_limits_and_no_overlap(self):
        self.assertLessEqual(max(map(len, self.text.splitlines())), 2000)
        self.assertEqual(len(self.headers), 8)
        with self.assertRaises(ValueError):
            parse_single_rule(self.text + "\n/assets/img/*\n  Cache-Control: immutable\n")
        with self.assertRaises(ValueError):
            parse_single_rule(self.text + "\n/assets/img/*\n")
        with self.assertRaises(ValueError):
            parse_single_rule(self.text + "\n  X-Long: " + "a" * 2000)

    def test_stable_images_and_queries_always_revalidate(self):
        # The parser rejects extra rules, so image/favicon paths cannot inherit
        # a second immutable directive. Cache-busting queries are no exception.
        self.assertEqual(self.headers["cache-control"],
                         "public, max-age=0, must-revalidate")
        self.assertNotIn("immutable", self.text)

    def test_csp_adds_ancestor_control_without_resource_restrictions(self):
        self.assertEqual(self.headers["content-security-policy"], "frame-ancestors 'self'")
        self.assertEqual(self.headers["x-frame-options"], "SAMEORIGIN")
        # This policy cannot block outgoing MTB/Skillz frames or Mermaid styles.
        # Browser and provider staging acceptance remains a separate test.
        self.assertNotIn("frame-src", self.headers["content-security-policy"])
        self.assertNotIn("default-src", self.headers["content-security-policy"])

    def test_staging_is_noindex_and_hsts_is_bounded(self):
        self.assertEqual(self.headers["x-robots-tag"], "noindex")
        self.assertEqual(self.headers["strict-transport-security"], "max-age=300")
        self.assertNotIn("preload", self.text)
        self.assertNotIn("includeSubDomains", self.text)

    def test_no_unapproved_isolation_or_report_receiver(self):
        for header in ("cross-origin-opener-policy", "cross-origin-embedder-policy",
                       "cross-origin-resource-policy", "reporting-endpoints"):
            self.assertNotIn(header, self.headers)
        self.assertNotIn("report-uri", self.text)
        self.assertEqual(self.headers["permissions-policy"],
                         "camera=(), microphone=(), geolocation=()")


if __name__ == "__main__":
    unittest.main()
