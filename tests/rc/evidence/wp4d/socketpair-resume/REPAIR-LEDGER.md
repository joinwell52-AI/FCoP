# WP4D incremental verification repair ledger

Current correction: the later timed rechecks did not invalidate the earlier
valid 14/14 and before/after byte-equality proof at unchanged content d1a86f3.
Requiring a live downstream quiet window was an executor judgment error;
that escalation is withdrawn. The user clarified that only FCoP is being
upgraded, while CodeFlowMu remains below 4.0. No further live downstream
inspection, coordination or action is performed. All unsuccessful rechecks
and historical wording below remain as evidence, not as current requirements.
Final FCoP delivery and final-HEAD CI must still be completed independently.

Authority: ba8830c1871f6516fec1e2779d21c09b9a5e96ea,
SHA-256 badc8a597a01407dec012d1085a5cac5815f8608e8afec742688846beb11c625,
7652 bytes. This ledger is not a Gate or final COMPLETE report.

1. Socketpair code identity: 7002fb5c1893d153acdcd07b29391cc6ddb9f533
   changes only the sample server and adds the isolated subprocess test.
   The first local test counted two aliased function names as two identities;
   that pre-hook assertion failed. The test now deduplicates by identity.
   Both original failure and corrected pass JUnit are preserved here.
   Actual stdlib IPC passes; direct bind/connect/getaddrinfo/sendto and two
   filename/name-spoofed functions are rejected with exact messages.
2. Mypy failure: all 12 MCP jobs on 7002fb5 rejected the newly added test's
   missing return annotation before running pytest. Raw diagnostic excerpts
   are preserved in mypy-failures.json. This was an executor omission, not
   a network guard, Core, MCP or taskbook defect. Commit 3a162c4 adds only
   -> None; local mypy and the executable guard test passed afterward.
3. Commit caa8084 adds native Windows to the existing Ubuntu full source
   regression job, preserves both jobs without fail-fast, separates their
   JUnit artifact names, and uses environment-based path lookup to avoid
   Windows backslash escapes in inline Python. No old matrix is removed.
4. Commit 8fa9c3ccd0365afbc0a94b1c2cda5aa7ccf797ec binds the candidate content
   commit separately from the executing CI HEAD. Only a contiguous suffix
   of single-parent WP4D report/evidence/Manifest-only commits is ignored;
   any source, sample, test or other change becomes a new content identity.
   Six real-Git regression cases verify this boundary. Build exports the
   resolved content, consumer checks both identities, and all consumers in
   the run receive the same freshly built first set. No JSON identity is
   rewritten. Exact build tool preflight and observed metadata version are
   also recorded. Targeted identity + guard tests: 7 passed, zero skips.
5. Commit d1a86f32d87f000fe0aec444563decdc892dc142 corrects a consumer
   checkout precondition: the new strict ancestry check cannot classify a
   depth-one clone. Run 34376903241 failed all 12 consumers before install;
   shallow-checkout-failure.log preserves an exact traceback excerpt.
   Only consumer fetch-depth: 0 is added; ancestry assertions and candidate
   identity checks are not weakened. All three RC job definitions now fetch
   complete ancestry. All matrices are rerun at this new candidate identity.
6. A supplemental timed CodeFlowMu shadow recheck observed a changed
   downstream inventory during its read window (16:44:30–16:46:17 UTC).
   The strict before/after equality assertion rejected it; this failure is
   preserved in shadow-recheck-failure.json. No production file, process,
   service or zero-drift assertion was changed. A separate unchanged-input
   read-only recheck is required; the earlier successful 14/14 evidence is
   retained and never overwritten by a fabricated pass.
   Two later diagnoses identified untracked downstream verification files:
   runs/03-target.txt was added, then runs/05-shell-regression.txt changed
   bytes under CFM-INDEPENDENT-UPDATER-20260910. Tracked bytes and HEAD
   were unchanged in both observed windows. The final strict recheck failed
   at 16:54:02 UTC. No CodeFlowMu process was paused or changed. A quiet
   window requires ADMIN coordination; no completed Manifest or Gate is
   claimed. All candidate CI checks at d1a86f3 passed independently.

The final source threshold is strengthened from 1924 to 1931: the original
suite plus one guard test and six content-identity cases. Business assertions,
frozen Conformance and production files are unchanged. Source, wheel and
sdist verification still need the final fixed content/CI results; old passing
counts cannot satisfy the final Gate. Historical failed runs remain visible.
