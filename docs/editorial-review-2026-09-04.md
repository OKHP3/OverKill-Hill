# Notion-backed editorial review

**Review date:** 2026-09-04  
**Review mode:** Notion staging with repository export  
**Owner sign-off:** Approved 2026-09-04

## Connector and access check

The connected Notion workspace supports the review workflow needed here:

- Page search returned the existing OverKill Hill website records and editorial review material.
- Page properties and page content were readable for the relevant records.
- The connector exposed content write access, and the review staging note was appended successfully to the existing About-page editorial review record.
- The comments endpoint was readable and returned no comments on the reviewed records. No comment was created because there was no existing discussion to update.
- No new workspace, database, or schema was created.

Account-specific Notion URLs, page IDs, and workspace structure are intentionally not reproduced in this public repository.

## Defined scope

This pass covered the highest-value editorial surfaces rather than the entire site:

| Route | Review focus |
|---|---|
| `/writings/` | Hub positioning, featured-card status, and consistency with the current article release |
| `/manifesto/` | Voice, structure, permanence of the origin section, and whether older Notion copy should be imported |
| `/about/` | Personal-brand voice, known typo, credentials claims, and scannable presentation |

The Notion material consulted was the canonical website record for each route, the existing About-page voice review, the `Improve Writing` guidance, and the older manifesto audit.

## Findings and dispositions

### `/writings/`

**Finding:** The featured card said `Featured · v1.0 Live`, while the same card described v0.5 as live and the current article record identifies v0.5 as the current release.

**Accepted correction:** Changed the featured-card kicker to `Featured · v0.5 Live` in `site-src/pages/writings/index.main.html`.

**Verification:** The generated `/writings/` HTML now carries the corrected kicker after running the existing site build.

### `/about/`

**Confirmed already addressed:** The prior Notion review identified agency-plural wording and the typo “part of he load.” The current source uses first-person singular wording for the personal-brand sections and says “carry part of the load.”

**Approved addition:** The owner approved a scannable credentials section covering 13+ years of enterprise systems experience, 28 professional certifications, enterprise-scale architecture work, a Salesforce rollout reaching approximately 5,000 users, and Information Technology and Cloud Computing studies at Western Governors University.

The wording was reconciled against the owner's public personal and business LinkedIn pages before publication. The employer is intentionally unnamed on the About page to avoid implying a connection between the owner's employment and OverKill Hill P³™. The page keeps first-person singular framing and describes the scale and nature of the experience without naming the employer.

### `/manifesto/`

**Disposition:** No copy change.

The current repository page is a newer living-manifesto structure with a protected origin section and an extended set of principles. The older Notion audit contains superseded October 2025 source material and was treated as review evidence, not as text to import. Importing it would risk regressing the current structure and voice.

## Cross-site implications

The personal-brand voice decision is relevant to shared editorial review for `glee-fully.tools` and `askjamie.bot`, but it must not be copied mechanically. Those sites may have different declared voices and audiences. Any shared copy pass should preserve each site’s own voice while avoiding accidental agency-plural language on pages that explicitly present Jamie or OverKill Hill as the subject.

No direct edits were made to either sibling site.

## Review record

The same findings, correction, credential suggestion, superseded-manifesto disposition, and cross-site note were staged in Notion. The owner approved the LinkedIn-aligned credential wording on 2026-09-04, with the additional instruction that the public page not name the employer. This repository export is the durable source for the approval and does not depend on a live Notion link.