# Publishing regression cases

1. **Wrong commit:** validation passed on SHA A but deployment is attempted from
   SHA B; the commit helper blocks before any write.
2. **Missing workflow scope:** an OAuth/PAT credential lacks repository contents
   or workflow permission; stop and request provider-side repair, never print or
   paste the credential.
3. **Untrusted pull request:** a fork-controlled workflow path requests Pages
   write/OIDC access; reject it and use trusted read-only validation.
4. **Stale cache:** deployed HTML points at an old shared-asset fingerprint;
   report edge failure and do not claim the deployment is complete.
5. **Incomplete edge verification:** deployment succeeds but sitemap, headers,
   index, or representative routes were not checked; status is `PARTIAL`.