# Release plan — not release authorization

Current scope ends at Draft PR #48 review delivery. Requested Gate after verification: FCOP_4_0_3_FOUR_FILE_RETIREMENT_ACCEPTED.

No main merge, tag, PyPI upload, GitHub Release, production Pages deployment, Registry update, CodeFlowMu change or customer workspace migration has been performed.

After explicit ADMIN release authorization only:
1. Bind the approved final source and four candidate hashes; preserve commit history.
2. Merge/tag/publish only the exact authorized 4.0.3 pair and artifacts.
3. Verify public PyPI downloads and long descriptions against approved sources.
4. Deploy the generated homepage; update the Registry record and its factual banner only after confirming the actual public result.
5. Verify 49/12/4 and customer-root byte preservation from fresh public installations.
6. Return the public release receipt. Do not equate current local verification with publication.

Existing 4.0.2 and earlier releases/tags stay intact. The historical RC/Stable promotion workflows remain pinned to their own stages; no attempt was made to run an old 4.0.0 publication guard as a 4.0.3 release.
