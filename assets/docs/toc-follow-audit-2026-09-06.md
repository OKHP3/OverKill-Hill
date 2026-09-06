# Sidebar follow audit, 2026-09-06

Reviewed all 56 HTML pages in the release inventory, including routes omitted
from navigation and noindex routes. Four saved translation-review snapshots
under i18n are evidence, not deployed pages.

The 14 existing table-of-contents menus now share the Mac Studio centered,
delayed follow behavior. Ten menus had sticky ancestors that conflicted with
the translated child. The shared runtime disables those ancestors only when
follow is active, updates geometry after layout changes, handles both viewport
transitions, respects reduced motion, bounds tall menus with internal scrolling,
and stops before the footer. The 60 Hz easing retains the reference's 8% step;
animation stops when settled.

All 14 menus passed Chromium browser checks for easing/settling, valid targets,
active sections, short viewport keyboard reachability, both breakpoint
transitions, reduced motion, and footer clearance. An independent review also
checked manifesto at exactly 1024px and 1023px. The old runtime reproduced both
the sticky-parent conflict and mobile-to-desktop initialization failure through
browser interception; files on disk were not replaced for this comparison.
Separate Firefox/WebKit motion acceptance was not performed.

No new sidebars were added. Metadata cards, calls to action, and the First
Diagram inline overview remain in their existing roles. Every live HTML change
is limited to shared asset version queries. French, German, and Spain-Spanish
review records prove that their selected sources and targets have no other
changes; saved Mexican-Spanish reviewed snapshots remain unchanged.

## Complete route inventory

| HTML route | Sidebar disposition |
| --- | --- |
| /404.html | No matching aside navigation |
| /about/ | No matching aside navigation |
| /contact/ | No matching aside navigation |
| /de/about/ | No matching aside navigation |
| /de/contact/ | No matching aside navigation |
| /de/ | No matching aside navigation |
| /de/projects/ | No matching aside navigation |
| /en-gb/about/ | No matching aside navigation |
| /en-gb/contact/ | No matching aside navigation |
| /en-gb/ | No matching aside navigation |
| /en-gb/projects/ | No matching aside navigation |
| /es/about/ | No matching aside navigation |
| /es/contact/ | No matching aside navigation |
| /es/ | No matching aside navigation |
| /es/projects/ | No matching aside navigation |
| /es-mx/about/ | No matching aside navigation |
| /es-mx/contact/ | No matching aside navigation |
| /es-mx/ | No matching aside navigation |
| /es-mx/projects/ | No matching aside navigation |
| /found-ry/ | No matching aside navigation |
| /fr/about/ | No matching aside navigation |
| /fr/contact/ | No matching aside navigation |
| /fr/ | No matching aside navigation |
| /fr/projects/ | No matching aside navigation |
| / | No matching aside navigation |
| /legal/ | No matching aside navigation |
| /manifesto/ | Shared centered follow verified |
| /projects/abrahamic-reference-engine/ | Shared centered follow verified |
| /projects/bfs-framing-intelligent-futures/ | No matching aside navigation |
| /projects/bpmn-for-mermaid/ | Shared centered follow verified |
| /projects/first-diagram-is-a-liar/ | Shared centered follow verified |
| /projects/found-ry/ | Shared centered follow verified |
| /projects/glee-fully-chai-chasers/ | Shared centered follow verified |
| /projects/hometools/ | No matching aside navigation |
| /projects/ | No matching aside navigation |
| /projects/kierans-lifetrkr/ | Shared centered follow verified |
| /projects/mac-studio-local-ai-workbench/ | Shared centered follow verified |
| /projects/mermaid-theme-builder/ | Shared centered follow verified |
| /projects/pathscrib-r/ | No matching aside navigation |
| /projects/skillz/ | Shared centered follow verified |
| /projects/telling-forward/ | Shared centered follow verified |
| /projects/un-nocked-truth/ | No matching aside navigation |
| /prompt-forge/ | Shared centered follow verified |
| /search/ | No matching aside navigation |
| /under-construction.html | No matching aside navigation |
| /universe/ | No matching aside navigation |
| /vault/ | No matching aside navigation |
| /writings/biases-as-constants/ | No matching aside navigation |
| /writings/first-diagram-is-a-liar/ | Shared centered follow verified |
| /writings/first-diagram-is-a-liar/v03/v1-heat-a/ | No matching aside navigation |
| /writings/first-diagram-is-a-liar/v03/v1-heat-b/ | No matching aside navigation |
| /writings/first-diagram-is-a-liar/v03/v2-heat-a/ | No matching aside navigation |
| /writings/first-diagram-is-a-liar/v03/v2-heat-b/ | No matching aside navigation |
| /writings/ | No matching aside navigation |
| /writings/magnus-saga/ | No matching aside navigation |
| /writings/murderbird/ | Shared centered follow verified |
