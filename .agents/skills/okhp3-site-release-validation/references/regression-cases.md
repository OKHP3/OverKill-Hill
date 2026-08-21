# Site-release regression cases

1. **Stale fingerprint:** change a shared asset while leaving an old `?v=`;
   cache-bust check fails and names the expected hash.
2. **Missing generated index:** remove the committed search index; `--check`
   fails instead of generating or accepting an empty index.
3. **Noindex boundary:** a `noindex` HTML page appears in the sitemap, or an
   indexable page is omitted; reconciliation fails and reports the boundary.
4. **Missing embed:** an intended iframe is blocked by CSP or the third party is
   unavailable; report `BLOCKED`/`WARN`, do not remove the policy.
5. **Incomplete browser run:** one viewport or route is skipped; the report is
   incomplete and cannot be called a clean release.