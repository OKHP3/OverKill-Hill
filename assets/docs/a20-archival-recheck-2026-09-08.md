# A20 archival recheck and human acceptance protocol

Status: **technical closeout complete; NOT fully accepted for archival as an entirely completed A20 task.** Human/device acceptance remains open. No delegation occurred during this recheck.

Option B [PR81](https://github.com/OKHP3/OverKill-Hill/pull/81) and all ten A20 acceptance files are verified unchanged on main; its Pages run34255540899 passed. All eight original A20 branch tips, including the two Option B tips, are preserved remotely. Later site changes belong to their own scoped acceptances.

The remaining public .well-known 404 defect was personally diagnosed and repaired in [PR87](https://github.com/OKHP3/OverKill-Hill/pull/87). The pinned Pages upload action defaults to excluding hidden directories, dropping endpoints after package validation. The fix enables hidden-file inclusion only in the allowlisted, byte-verified site-release directory. A regression failed before the fix; all 12 package tests passed afterward. The branch was normally reconciled with the media release; its net change remained two files and nine lines. Required hosted validation and locale checks passed before normal squash merge at f805158a364b96ac9b3f44a5ee92f0d4fa95d67a.

[Pages run34260828061](https://github.com/OKHP3/OverKill-Hill/actions/runs/34260828061) completed successfully. At 18:11:47 UTC the live manifest identified that exact merged revision, and both public endpoints returned HTTP200 with exact raw Git-byte and manifest-digest matches. [Live evidence](../audit/a20-hidden-pages-live-2026-09-08.json) closes this defect; previous 404 records remain historical evidence. Replit configuration and site content were not changed by this fix.

The additional bounded A15 review is also complete: ACCEPT WITH LIMITS for 60cf2d1ed8d81d99d05754b5f94dbb2712b6ed3f against f805158a. A Git-object-only check confirms that only the intended French Contact hash pair changes, the other three French pairs remain exact main, both actual Contact hashes match review receipts, and removing marked additions restores all five original published pages. Regional noindex/native-false boundaries remain. The es-MX inserted block exactly matches its owning reviewed input; whole-template/output differences are expected generator transformations, not a claim of identical complete documents. [Independent delta evidence](../audit/a20-a15-final-delta-2026-09-08.json). The reported 121 browser assertions remain A15 evidence, not a suite independently rerun here. A21 owns PR86 integration and publication.

No coding, GitHub preservation, or deployment action remains for this A20-owned fix. Full acceptance still requires the actual human executions below. The current session cannot supply native macOS/iOS hardware, a physical phone session, or human judgments. Automation and text/DOM inspection cannot honestly replace those outcomes. No human acceptance or scope waiver has been inferred.

## Remaining actual-execution protocol

Record tester, date, exact live manifest commit, device, OS, browser and assistive-technology versions. For each task retain outcome, spoken behavior/focus observations and relevant audio/screen evidence. Record failures and repeat outcomes after corrections.

1. With native Safari/VoiceOver on macOS or iOS, and NVDA with Firefox on Windows, read the homepage purpose and navigate its headings. Include reduced-motion and unavailable-enhancement behavior where practicable.
2. Use the skip link and confirm reading/focus continues in main content.
3. Open compact navigation and reach Contact. Confirm menu state and heading announcement, and read the optional inquiry guidance.
4. Search for mermaid, navigate results, verify loading/selection/error announcements, open a result, and verify Escape returns focus. Search MurderBird on the dedicated search page.
5. Use Read the story, confirm entry at The Maker and continued story navigation. Exercise Status and source and More from the forge summaries with spoken open/closed state.
6. On a physical phone, test touch targets, portrait/landscape, scrolling, overflow, screen-reader exploration and long-form orientation. Run actual 200%/400% browser zoom and text enlargement, short-height layout, light/dark focus and visual font/contrast judgment.

Qualified human/native French acceptance remains separate if full language acceptance is required. Regional drafts must remain noindex/unaccepted. No automated result supplies the missing native-language judgment.

The raw existing A20 .local probes/logs/results are retained outside the worktree at C:/Users/jamie/.codex/review-archives/a20-2026-09-08/raw-review-evidence.zip; 162 files, SHA256 9d9a9cbe3ca27ba0f2c29f38d82664ddb08bbbcadf9b0bd3932aeff3ed107301. Ephemeral TLS credentials and reproducible package copies are excluded. Original raw directories were not deleted. This does not claim recovery of any previously removed ignored output.
