# WP4A.1 Schema Binding

## Authority and execution plan

The fixed taskbook at `6ddf6a35235c6aedff6807e5e7aba3f7d515e2ff` was read from GitHub and its SHA-256 verified as `7fa10b9825a2b67c9c15032612d543045bef0b1d9ffc18e11dab96a16635e13b`. Its ancestors include the parent WP4 taskbook `a789cf070cfc626d23034753b18e8679780b7d50`, Core Gate `fea48393be8c83f4dbb6e085f54bb4ce391ee2ed`, effective Core `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`, and frozen contract `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6` (git merge-base --is-ancestor: 0 for each).

The old blocker report is historical, not an active veto: RESOLVED_BY_ADMIN_SCHEMA_BINDING. Its original SHA-256 is `3a9c42d321caf2d272bf4456a74517d8b2582ae81697718a4455c0177e4ff80e`. The old local commit `73a7dd930de70819193a30264ca31ac6f9dd8e4a` is not an ancestor (exit 1) and was not cherry-picked.

ME execution review: use only this independent worktree, leave both original worktrees intact. Implement deterministic offline schemas, reuse strict byte parsers and wire validation into existing v4 read/write boundaries. Preserve specialized Core error and behavioral gates; schema validation is structural, not authorization. No new Project method or arbitrary kwargs. Run SB-01 through SB-10, actual public applications, regression and clean artifact proof before Content + Manifest delivery. No later phase or self-signed Gate.

Exactly the five declared roots are open. Fully defined Core nested objects are closed. Unknown root values cannot replace required keys, carry authority, or enter canonical request inputs. Full-file evidence hashes still include their bytes. Lifecycle serialization preserves extension values, not original YAML layout. No prefix convention, extensions container, registry protocol, runtime dependency or service is introduced.

Verification results will be appended after execution; no pass is claimed by this plan.

## Executed binding checks

The original blocker copy has the identical SHA-256 shown above. It remains historical BLOCKED text, with its resolved disposition recorded here rather than rewriting history.

| Binding ID | Concrete assertion | Result |
|---|---|---|
| SB-01 | Actual workspace/TASK/REPORT/ISSUE/REVIEW accept opaque root value | PASS (5 roots) |
| SB-02 | Missing protocol plus Protocol lookalike rejected in all roots | PASS |
| SB-03 | Wrong workspace_id type plus alternate field rejected | PASS |
| SB-04 | Unknown encoding/event/binding/receipt/family Core members rejected | PASS |
| SB-05 | Duplicate JSON/YAML keys rejected before a validator can run | PASS |
| SB-06 | Unknown root assertions cannot supply REPORT/auth gates, override trusted three-state evaluator, or fill family coverage; T2 preserves opaque values | PASS |
| SB-07 | Same real create request with different thread_key/risk_level and reopened manifest extension context yields same digest/task and Existing | PASS |
| SB-08 | Adversarial REPORT extension-byte change remains structurally valid but invalidates T3 evidence binding; zero TASK movement | PASS |
| SB-09 | Local Profile rejects its own field but cannot waive missing Base protocol | PASS |
| SB-10 | Both old eight-schema sets match sixteen SHA-256 values captured from fixed Git content, without depending on clone depth | PASS (schema isolation); regression and initial CI correction in RESULT |

The dedicated schema/application module passed 47/47 nodes. The added exact canonical create-input schema was subsequently exercised with creation regression and structural negative matrix: 99/99. Final complete-suite evidence is in RESULT. No frozen Conformance ID or fixture was modified. There is no Profile registry, x-prefix rule, extensions container, public Project method, or new dependency.

Development failures were corrected locally, not hidden: initial schemas incorrectly prohibited nullable authorization context on ordinary REVIEWs, and the initial historical-event stage enum exceeded the existing read contract. Non-authorizing null context is now preserved; unknown event strings never certify valid edges or override NOW. New test harness errors (wrong inspect-state key and child interpreter import path) were also corrected. Existing test logic and frozen fixtures were not rewritten to force green.
