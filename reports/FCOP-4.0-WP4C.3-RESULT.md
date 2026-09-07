# WP4C.3 result — BLOCKED: historical public-method count

## Current blocking decision

WP4C.3b fixture alignment is complete. Resumed WP4C.3 is BLOCKED; no Gate is requested. The implementation and 19 canonical package files remain LOCAL_ONLY, uncommitted and preserved in this independent worktree. Only the passed isolated fixture commit and factual reports/Manifest are eligible for this blocked GitHub delivery. All reported implementation test passes refer to these preserved local bytes, NOT the report-only remote HEAD.

### Exact evidence and required ADMIN decision

The full FCoP regression exposed `tests/test_fcop/test_v4_creation.py:839`, `test_closeout_boundary_reflection_binding_and_subclass`:

```text
original_names = set(_METHOD_POLICIES) - {ten existing v4-only names}
assert len(original_names) == 38
E AssertionError: assert 39 == 38
```

An isolated rerun failed identically (1 failed, 1 warning, 1.48 s). AST/Git inspection proves the old fixed commit yields 38 and the current implementation yields 39; the ONLY delta is `rule_distribution`. The historical exclusion set at lines 834-837 predates this explicitly authorized public API and omits it. The test itself is unchanged, raw SHA-256 `1397e4aaf9b0158c3491c4821fc13eb6dd38a608f9c88af4c68e2f7c15417012`.

Original WP4C.3 sections 5.1/9 authorize one public method, and current boundary registration requires each public method to be explicitly classified. Removing a legacy policy, hiding the new method from enumeration, changing __len__, monkeypatching the old test or weakening the boundary would conceal the real addition and is not an acceptable repair. All original Project method ASTs are identical; public surface has exactly the authorized additive entry.

The required test file is outside the taskbook's write scope (only new test_v4_rule_distribution*.py and the public snapshot are allowed here). Original taskbook section 13 and WP4C.3b section 8 require stopping for a new regression/out-of-scope correction. No existing test, assertion, Test ID, skip/xfail, Core implementation or scope was changed to bypass it.

Proposed next ADMIN-only authorization: align the historical legacy-set exclusion with the authorized `rule_distribution` addition, retain `assert len(original_names) == 38` and all binding/subclass/autospec assertions, then rerun and resume. This is a proposal, not work performed or a new execution authorization.

### Validation checkpoint

- Exact WP4C.3 targets: 56/56 passed.
- Complete distribution: 99 passed / 77 deferred failures. This is 33 Meta + 56 targets + 1 control + 9 explained zero-write negative overlaps; all 86 future nodes remain outside acceptance scope. See the per-node conformance report.
- Core: 119/119 passed; MCP: 134/134 passed.
- FCoP: 1296 passed / 1 failed, 966.26 s; the sole failure is the historical method-count assertion. All 41 new unit nodes passed. Final Meta/control rerun: 34 passed, 13.26 s.
- Ruff and mypy: PASS (46 source files).
- Public snapshot checks passed with exactly the authorized new method.
- Build: wheel and sdist include all 19 v4 data files; no WP4C.6 acceptance or publication.
- Legacy source bytes 14/14 unchanged; fixture bytes unchanged after commit.

### Preserved local-only implementation inventory

The following 31 files are deliberately NOT staged or pushed with the blocked report delivery. Hashes were captured after the confirmed stop, so a future authorized resume can verify exact bytes without reconstructing or guessing. No cleanup, reset, stash or original-workspace mutation was used.

| Local preserved path | Bytes | SHA-256 |
| --- | ---: | --- |
| CHANGELOG.md | 130694 | aea366e3f64d903049e45d79bacec56fccf5057959f15abfe65d2671f8992c8d |
| pyproject.toml | 6075 | e51ff7f3fda0a1b9c27ab407275d452a0ea5dcfaeb5650c4137c485db8d446b5 |
| src/fcop/project.py | 265857 | f421d7fb2a444b90c63c18bea8c8c4751af90f3c8eeb9f2ed139e32f6acbf6ec |
| src/fcop/rules/_data/v4/authorization.en.md | 2128 | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| src/fcop/rules/_data/v4/authorization.zh.md | 2033 | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| src/fcop/rules/_data/v4/compatibility.en.md | 3521 | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| src/fcop/rules/_data/v4/compatibility.zh.md | 3024 | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| src/fcop/rules/_data/v4/convergence.en.md | 2283 | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| src/fcop/rules/_data/v4/convergence.zh.md | 2114 | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| src/fcop/rules/_data/v4/envelopes.en.md | 1743 | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| src/fcop/rules/_data/v4/envelopes.zh.md | 1672 | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| src/fcop/rules/_data/v4/idempotency.en.md | 1720 | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| src/fcop/rules/_data/v4/idempotency.zh.md | 1591 | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| src/fcop/rules/_data/v4/lifecycle.en.md | 3041 | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 2787 | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| src/fcop/rules/_data/v4/manifest.json | 11221 | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| src/fcop/rules/_data/v4/recovery.en.md | 3534 | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| src/fcop/rules/_data/v4/recovery.zh.md | 3099 | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| src/fcop/rules/_data/v4/relations.en.md | 1106 | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| src/fcop/rules/_data/v4/relations.zh.md | 1057 | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| src/fcop/rules/_data/v4/workspace.en.md | 1920 | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| src/fcop/rules/_data/v4/workspace.zh.md | 1723 | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |
| src/fcop/v4/boundary.py | 5988 | 1cb04f82d7bf5c4d14b73847e647131532019539ef801cae2344006f61dc9b4f |
| src/fcop/v4/creation.py | 45982 | 521288527b3335946a18ea136aa8ac2c53f4e0574bd3767633e58873039ce434 |
| src/fcop/v4/rule_distribution/__init__.py | 4096 | a7402c3c67b23d00201646be413e1fe12e6105c5caf2febca41742e408361f57 |
| src/fcop/v4/rule_distribution/_contract.py | 1716 | 519a40daf73012ee8f64009d744af59138390e67bbf6fd8dd7f07a14e1cec6e3 |
| src/fcop/v4/rule_distribution/_errors.py | 1022 | df1c0bece920f449bd4b60863188761fb18ee0a81280e0c1628f73e03e6815c8 |
| src/fcop/v4/rule_distribution/_loader.py | 6886 | eca7c4c9330dd6c351f07ebeee4112dcade03a76be93877df4fcd95a4b380ff4 |
| src/fcop/v4/rule_distribution/_selection.py | 6520 | 146027786c67e632ed18f2b7673211a27b58e818c3ced35fd7eee92b1f00a2f8 |
| tests/test_fcop/snapshots/public_surface.json | 54775 | 96d45a001c073083465ed3ae9a6db9725cdf3842256312a742808c6f15c456c5 |
| tests/test_fcop/test_v4_rule_distribution.py | 9179 | ef8a9716ff47682408f378971be7252b4f1015ca479576ff1e9a5e41647b012a |

The current taskbook, passed fixture, prior PR #21/#22 blockers and their ordered parent chain remain intact. The GitHub Manifest will describe a BLOCKED factual delivery, not a successful implementation. REQUESTED_GATE: NONE; WP4C_3_RULE_PACKAGE_ACCEPTED: false; WP4C_4_STARTED: false.

```yaml
WP4C_3B_FIXTURE_STATUS: COMPLETE
WP4C_3B_STATUS: BLOCKED
WP4C_3_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_3B_DIST_02_FIXTURE_ALIGNMENT_AND_WP4C_3_RESUME
BLOCKER: HISTORICAL_PUBLIC_METHOD_COUNT_NOT_SCOPED
DIST_02_FIXTURE: PASS
DEVELOPMENT_REFERENCES: 4/4_PINNED
FIXTURE_COMMIT: 115751b4c24a1924062a81a21e0d655e8cb5fedc
LOCAL_TARGET_NODES: 56/56
LOCAL_TEST_FCOP: 1296_PASSED_1_FAILED
LOCAL_NEW_UNIT_TESTS: 41/41
LOCAL_V4_CORE: 119/119
LOCAL_MCP: 134/134
LOCAL_DISTRIBUTION: 99_PASSED_77_DEFERRED_FAILURES
FUTURE_OWNER_NODES: 86_NOT_ACCEPTED_77_RED_9_EXPLAINED_NEGATIVE_OVERLAPS
OPEN_REGRESSION_FAILURES: 1
LOCAL_IMPLEMENTATION_FILES_PRESERVED: 31
IMPLEMENTATION_COMMITTED: false
IMPLEMENTATION_PUSHED: false
DELIVERY_KIND: FIXTURE_AND_BLOCKER_FACTS_ONLY
WORKTREE_STATUS: DIRTY_PRESERVED
WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
MCP_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: NONE_BLOCKED
```

Content and Manifest commit identities are recorded in the GitHub delivery Manifest and external readback receipt, avoiding a self-referential commit/hash claim in this Content file. No report-only CI result may be used as implementation acceptance.

## Earlier in-progress checkpoint (historical within this execution)

## Current task record (not a final receipt)

Current authority is WP4C.3b taskbook `3a11498c0d4aff736628e781f34516950cb34be8`, SHA-256 `5c4cb2506a6d987dea705a2c5d1b28108b01a3d2b68cbf7b0047dbb8d3d4dbcb`, input `ec81dc5ed80ff2a4492fd0d1611aad234949bfb5`. The previous missing-input blocker below is historical and has been resolved by the authorized isolated fixture commit `115751b4c24a1924062a81a21e0d655e8cb5fedc`.

[Fixture task/execution report](FCOP-4.0-WP4C.3B-DIST-02-FIXTURE-ALIGNMENT.md) records the actual local inputs, commit and pre-implementation validation. [Implementation plan](FCOP-4.0-WP4C.3-IMPLEMENTATION-PLAN.md) records the authorized production scope and pre-code choices.

Checkpoint: nine bilingual modules / 18 Markdown files / one Manifest authored and independently byte-checked; private loader/selector and the sole Project.rule_distribution entry implemented locally; exact target functions 56/56 passed. Final complete regression, full future-node classification, packaging inclusion, Content/Manifest delivery and remote raw-byte verification are still outstanding. No final GitHub delivery or Gate request is claimed. This report is a filesystem artifact in the independent FCoP worktree, not a CodeFlowMu EVAL task-record entry.

## Preserved WP4C.3a result below

Taskbook: `0559e0fdf5390aa830f98a38d83f96f1cd475ab1`, path `taskbooks/fcop-4.0/WP4C.3a/01-Historical-Audit-Scope-Alignment-and-WP4C.3-Resume-Taskbook-v1.0.zh.md`.
Raw bytes: 15954; SHA-256: `903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6`.
[ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567383721) and [hash erratum](https://github.com/joinwell52-AI/FCoP/pull/21#issuecomment-5567650164) were read back. The revoked `a61c4159...` is NOT an accepted identity.
Direct parent: `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; original WP4C.3 taskbook: `de213ec0f74f8976283a24986d4eb7de77c67142` (SHA-256 `a4b782db3a984be9872d6c99428c5fc669a1cd3135468b33ef8eba7a6c1b57d2`).
Audit correction commit: `e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab`, direct child of the corrected-identity taskbook.
Scope: `WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME`.

## New pre-implementation blocker: missing mandatory development inputs

`DIST-02[development-no-constitution]` in `tests/conformance/rule_distribution_v4/test_dist_01_06_manifest.py:40` calls `select` with `assembly_id=repository-development` and `constitution_ref=None`, then requires four references with path/revision/sha256 (lines 71-75).

Its actual inputs do NOT contain the four development references:
- `conftest.py:166-230`: Scenario creates only `fcop/fcop.json` in the workspace. The package contains the 18 business fixtures and their Manifest; the input directory contains a Host profile and the generic ADMIN-selection fixture.
- `conftest.py:243-263`: request has no `development_references`, development entry identity, development manual identity, or current development TASK/Gate reference bundle.
- `driver.py:22-36`: the driver only constructs Project(root) and forwards the request; it supplies no trusted reference registry or defaults.
- `git ls-tree -r --name-only 0559e0fdf5390aa830f98a38d83f96f1cd475ab1 docs/fcop-4.0/development` returns no paths. The fixture workspace also has no such directory.

Read-only inspection plus execution of the existing Scenario setup in an isolated temporary sandbox produced:

```json
{
  "development_references_present": false,
  "constitution_ref": null,
  "workspace_files": ["fcop/fcop.json"],
  "development_namespace_exists": false,
  "manifest_fields": ["artifacts", "manifest_schema", "package_version", "protocol_version"],
  "artifact_record_field_count": 11
}
```

This is a fixture-input finding, NOT a claim that a production implementation was run and failed. The production entry is still absent. Ordinary baseline red alone would not establish this finding; the explicit request and filesystem evidence above do.

Frozen RD-03 reserves repository-only development guidance separately; RD-19 requires four pinned references, with only the independent constitution optional. Original taskbook section 6.3 requires validating and returning those four fixed references; section 5.2 forbids caller-unrequested implicit selection. A rule package cannot invent the current development TASK/Gate, substitute business artifacts for a development manual, return placeholder paths/hashes, or bake this executor's own taskbook into every user's request.

By contrast, `test_dist_21_24_assembly_compat_mcp.py:43-79` (DIST-22) constructs four local reference files and passes `development_references`. This is an available example of complete local inputs, not authority to edit DIST-02.

The narrow likely correction is to supply the same categories of complete, pinned local inputs to the DIST-02 success fixture, preserving its ID, all assertions, and optional-constitution absence. ADMIN must decide and authorize that correction. It resides in a FOURTH frozen Conformance file, outside WP4C.3a's exception. No test edit or synthetic production fallback was made.

Stop basis: WP4C.3a section 8 (fourth Conformance file / 56 targets cannot be completed within scope); original WP4C.3 sections 8, 10 and 13. No Gate is requested.

## Completed and preserved

First-phase audit correction is independently committed and validated. FCoP 1256/1256, frozen v4 Core 119/119, MCP 134/134, Meta 33/33, DIST-30 1/1, Ruff and mypy pass. All 142 production behavior nodes remain expected red on the standard-entry baseline; no production capability or later-stage success is claimed. Full commands, the initial queue timeout and successful standard-entry reruns are preserved in [CONFORMANCE RESULT](FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md).

## Preserved history

PR #21 remains an OPEN Draft at `78ea6b89a1ef0df0e504a3cfa34cecddeb7dda24`; it was not rewritten, merged or repurposed. Its Content `0e89f94aa8df017817f76dadc8572c8bc5c0afdf` and Manifest remain ancestors. The prior 32/33 Meta and DIST-30 failure is an accepted historical blocker, now resolved by the separate audit commit. This report updates current facts; it does not erase that history.

## Current receipt

```yaml
WP4C_3A_STATUS: BLOCKED
WP4C_3_STATUS: BLOCKED
AUTHORIZED_SCOPE: WP4C_3A_AUDIT_SCOPE_ALIGNMENT_AND_WP4C_3_RESUME
STOP_REASON: DIST_02_DEVELOPMENT_REFERENCE_FIXTURE_INPUT_MISSING
TASKBOOK_COMMIT: 0559e0fdf5390aa830f98a38d83f96f1cd475ab1
TASKBOOK_SHA256: 903c5f0f249598ab3b5aaf7e947af8ed36fbc23928eff9b5db11e305acb21ba6
AUDIT_SCOPE_CORRECTION: PASS
AUDIT_CORRECTION_COMMIT: e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab
HISTORICAL_ALLOWLIST: 13/13_EXACT
META_STATIC: 33/33_PASS
DIST_30_CONTROL: 1/1_PASS
RULE_DISTRIBUTION_COLLECT_ONLY: 176
WP4C_3_TARGET_BASELINE: 56_EXPECTED_RED
FUTURE_OWNER_BASELINE: 86_EXPECTED_RED
FINAL_BASELINE_UNEXPECTED_FAILURES: 0
INTERMEDIATE_QUEUE_TIMEOUT: PRESERVED_NOT_REPRODUCED_ON_STANDARD_ENTRY
TEST_FCOP: 1256/1256_PASS
V4_CORE_CONFORMANCE: 119/119_PASS
MCP_REGRESSION: 134/134_PASS
RUFF: PASS
MYPY: PASS
DIST_TEST_IDS: 30_UNCHANGED
BEHAVIOR_ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
OTHER_RULE_DISTRIBUTION_CONFORMANCE_FILES_MODIFIED: 0
PRODUCTION_FILES_MODIFIED: 0
CANONICAL_ARTIFACTS_CREATED: 0
MANIFEST_DATA_FILES_CREATED: 0
NEW_PUBLIC_APIS: 0
FROZEN_SPEC_FILES_MODIFIED: 0
MCP_FILES_MODIFIED: 0
HOST_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
DELIVERY_KIND: AUDIT_CORRECTION_AND_BLOCKER_EVIDENCE_NOT_RULE_PACKAGE_IMPLEMENTATION
WP4C_3_RULE_PACKAGE_ACCEPTED: false
WP4C_4_STARTED: false
MAIN_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: NONE_BLOCKED
```

Worktree: D:/FCoP-wp4c3a-audit-scope-and-rule-package; branch: review/fcop-4.0-wp4c.3a-audit-scope-and-rule-package. Reports are followed by a report-only Content commit and a Manifest-only commit. The Manifest binds all eight non-Manifest delivery files; fixed final HEAD and all nine remote/raw/local hashes will be recorded in the new Draft PR receipt after actual readback. This is not a successful implementation delivery. PR base remains the WP4C.3a taskbook branch, never main.

Required ADMIN direction: narrowly authorize complete local four-reference inputs for DIST-02 without changing its test ID/assertions, global driver or production semantics, or identify another explicitly authorized source of those four current references. No correction is implemented without that direction. Stop; do not request the acceptance Gate.
