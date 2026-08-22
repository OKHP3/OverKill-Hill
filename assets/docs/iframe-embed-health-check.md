# External iframe embed health check

The project pages embed live applications hosted on `okhp3.github.io`. The
embed is an intentional trust boundary: the child application is external,
mutable content and is not part of this repository's deploy. Each iframe
therefore has a restrictive sandbox and permissions policy. Clipboard and
fullscreen are denied. The Chai Chasers game is the only embed granted
`autoplay`, because its preview includes game audio.

## Expected child-origin behavior

The child origin must remain an HTTPS URL on `okhp3.github.io`, matching the
project link shown in the page disclosure. The child must load as an
independent application inside the sandbox; it must not need access to the
parent document, parent cookies, clipboard, or fullscreen. `allow-same-origin`
is retained for the child application's own browser storage and normal
same-origin fetch behavior; it does not make the GitHub Pages child same-origin
with `overkillhill.com`. Exporting tools may use `allow-downloads`; no embed
should add clipboard or fullscreen permissions without a documented feature
requirement.

This setup does not validate cross-origin `postMessage` traffic. A future
hardening pass should add origin-checked messaging if the parent and child
applications begin exchanging messages.

## Manual verification procedure

Run this check after changing an embed URL, sandbox, permissions policy, or
the hosted child application:

1. Start the **Start application** workflow and open each affected page in the
   preview: Mermaid Theme Builder, BPMN for Mermaid, Abrahamic Reference
   Engine, Skillz Forge, Found‑Rᵧ, and Glee-fully Chai Chasers.
2. Confirm the visible **External app** disclosure identifies `okhp3.github.io`
   and its link opens the expected child URL in a new tab.
3. Confirm the iframe resolves over HTTPS, the loading overlay clears, and
   the page's reload and full-screen/new-tab fallback controls still work.
4. Exercise the core child interaction: load a Mermaid theme, render a BPMN
   example, search the reference engine, filter Skillz, move through Found‑Rᵧ,
   and start one Chai Chasers round.
5. For the exporting tools, verify an intended file export still downloads.
   For Chai Chasers, verify the game remains usable and audio behavior is
   unchanged; autoplay may still be subject to the browser's user-gesture
   policy.
6. In browser developer tools, inspect each iframe element and confirm it has
   `sandbox`, a restrictive `allow` value, and the expected referrer policy.
   Confirm there is no `clipboard-read`, `clipboard-write`, or unrestricted
   `fullscreen` grant.
7. Check the browser console for sandbox, blocked-permission, failed-resource,
   or frame-loading errors. A child-origin change, a new required capability,
   or a failed export is a release blocker and requires revisiting the policy
   rather than widening permissions blindly.