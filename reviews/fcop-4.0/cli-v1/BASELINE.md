# CLI v1 baseline

Task: FCOP-4.0-CLI-ADAPTER-V1-20260911. ADMIN decision; ME solo execution.
Authority: [fixed v4 taskbook](https://github.com/joinwell52-AI/FCoP/blob/8bedfd3e132b7cca38e017ca518807332abb4bc2/taskbooks/fcop-4.0/CLI-V1/01-CLI-Adapter-v1-Development-Taskbook-v4.zh.md).
SHA-256: 923480c9a6c4ffa7211cb0032f5497ba4089bb97339fe203978359cd97254e3f.
Baseline/main: 8bedfd3e132b7cca38e017ca518807332abb4bc2; Core/MCP 4.0.1.
Initial 2332-node collection was collection only, not baseline test acceptance.

See reports/FCOP-4.0-CLI-V1-BASELINE.md for the pre-code record.
Worktree: D:/FCoP-4.0.2-cli-v1; branch: codex/fcop-4.0.2-cli-v1.
D:/FCoP was not switched, cleaned or redeployed. CodeFlowMu was not changed.

## Historical pre-existing full-suite blocker (resolved)

Test: tests/test_fcop/test_install_prompt.py::TestPromptIsStandardized::test_mcp_readme_inlines_canonical_en_prompt.
It compares the first MCP README text fence with the bundled legacy Cursor
installation prompt. At the fixed baseline that fence is already:
"create_branch → agents write REPORTs → inspect_family → merge_branches".

Original Git blobs:
- mcp/README.md SHA-256: 0f1626393bfba1bad01f0f04be15908060b1e8308185fd5c877c1a709d044ad6
- src/fcop/rules/_data/agent-install-prompt.en.md SHA-256: e71c0eaa084bd75cf9ce7947eae25c0c4d126affe2e52fb069fafae70abdc496

Reproduced with git show at the fixed commit and the exact two regex extraction
patterns from the test: BASELINE_ASSERTION_EQUAL=False. Current targeted run:
1 failed, 10 passed. No changes to that test or either canonical prompt.

Taskbook section 7 prohibits reintroducing large historical installation text
to the current PyPI landing pages; sections 9/12 require all tests to pass and
unrelated defects to be recorded without scope expansion. Release is BLOCKED.
ADMIN must settle the old inline-prompt test versus the current-page contract.

## ADMIN alignment and authorized resumption

The historical blocker above is preserved, not erased. ADMIN settled it at:
https://github.com/joinwell52-AI/FCoP/pull/40#issuecomment-5628747094
Actor/association verified through GitHub API: joinwell52-AI / OWNER.
Bound input: 7ec09f1c26c25d0c1273b2d2ab0c5bb79c35b969.
Correction commit: 80a6b08c48305a845b6fb2b025886db34375a7be.

Only the historical README inline-body assertion was replaced with exact
authoritative EN/ZH link and fcop://prompt/install Resource requirements.
The test additionally rejects re-embedding either full canonical prompt body.
Nine retained helper/test function ASTs are unchanged; both canonical Git blobs
are unchanged. EN SHA-256 remains the value above; ZH SHA-256 is
92178af0a81acb4fdfe67ecca11d5a520bf3ed80a46df1b1493a591b2ab18d0e.
Targeted install-prompt + CLI + catalog verification: 99 passed, 3 warnings.
No second ADMIN Gate is required after all original release gates pass.

The frozen EN/ZH specification still carries its WP1.1 candidate-status header.
This historical presentation issue was reported to ADMIN; the current task does
not authorize changing frozen specification bytes or their pinned identities.
It does not mean the published 4.0 package releases are candidates.

ADMIN subsequently required correcting that stale status before publication.
Read-only impact assessment found three bound verification surfaces:
- src/fcop/v4/rule_distribution/_read.py:33-35 and :65-74 bind and enforce
  the English source path, historical revision and exact whole-file SHA-256.
- tests/test_fcop/test_v4_rule_distribution_reads.py:68-74 asserts that identity.
- tests/conformance/rule_distribution_v4/test_dist_00_meta.py:276-295 enforces
  both current spec blobs against the frozen historical input byte-for-byte.
Changing only the title/status cannot satisfy those existing checks. Updating
their citation/baseline identities also touches production metadata and frozen
Conformance, beyond the prior narrowly authorized README-test correction.
No spec, production reference or frozen test was changed during this assessment.
Publication is held pending scope confirmation for the linked status/identity
alignment; no normative protocol behavior change is proposed.

## Current ADMIN amendment: identity alignment authorized

The preceding hold is historical and now resolved by the fixed amendment:
taskbooks/fcop-4.0/CLI-V1/02-CLI-Adapter-v1-Release-Identity-Amendment-v1.zh.md
at a72fef39d772104f5129b1b4ed1c6feeda62e31c, SHA-256
c21c094dd616bc4d216b1d3c7f57d9703ea11c18b84ad3afa4ea096c780465f5 (7623 bytes).
Resume instruction: https://github.com/joinwell52-AI/FCoP/pull/40#issuecomment-5628900858.
The amendment was merged into this review branch without rewriting its history.

Spec-only identity commit: 5c27e1bc90dce799aa7fa89e6cc717e01d47693e.
EN SHA-256: 9e6fd97ed4f3fa4bf9178babd54fd671fe4cc5f7bf7b8ee985d1726fb8c0e491.
ZH SHA-256: babe6acad7ddcd41ae06a3e9b21334b191576111905012f752a3052d5951dcf9.
Both now state Stable / Implemented / Released. The historical candidate input
remains in the preface and historical reports are untouched.

Core carries a fixed citation, not a duplicate full-text document. MCP packages
the exact EN/ZH payloads in _specs.json. Both references now bind the spec-only
commit and exact current hashes. v3 payloads remain unchanged. Only the current
spec identity comparison in distribution Conformance was mechanically rebound;
historical inputs, other contracts, behavior tests and their expectations remain.

Task self-review: this is release-identity/packaging metadata, not protocol policy.
No second ADMIN Gate is needed once final validation passes. Merge and publishing
remain conditional on actual final-HEAD results; those are recorded in PR #40.

### Exact restriction retained after full-suite cross-check

The cafffa53 intermediate run exposed RELEASE-GATE-01's exact phrase check:
the new word "itself" interrupted the required substring "does not authorize
Schema, tests, implementation, migration, push, or release". A focused rerun
reproduced 1 failed / 2 passed. The already-failing full run was interrupted;
it is not reported as a complete full-suite result. Its GitHub CI was 29/29,
which did not waive this locally observed Conformance failure.

The identity text now preserves the original restriction verbatim in EN/ZH.
No change was made to tests/conformance/v4/test_mcp_surface_contract.py or any
of the 18 frozen v4 Conformance files. This is within the fixed identity-text
amendment, not an exception to the release guard.

Current spec identity supersedes the intermediate 5c27e1b reference above:
revision 81d3229ee602341063879fe9100ab7db92417ffe;
EN SHA-256 fb10d1b14a678b77874012f88cf35a977d2f8517b1aa4a6fdc5a0e94546ef33d;
ZH SHA-256 0dac91db3e38e0cf06423a0d815beaaad9c9b4d6ec06e732f1012aec0e346f40.
The exact Core/MCP payload references and new identity proof were rebound.
