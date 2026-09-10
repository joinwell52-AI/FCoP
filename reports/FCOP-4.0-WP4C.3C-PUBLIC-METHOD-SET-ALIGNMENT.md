# WP4C.3c historical public-method alignment and WP4C.3 resume

## Current status

The authorized historical-test alignment is complete in commit 96ad2ae812c60a6362d9c360dbb815621a0cbe1a. Full local regression and implementation validation passed: FCoP 1297/1297, Core 119/119, MCP 134/134, independent new units 41/41, target nodes 56/56, Meta 33/33 and DIST-30 1/1. Collection remains 176; complete distribution is 99 passed / 77 future deferred failures, with nine explicitly explained zero-write negative overlaps. No unexpected failure remains. Content/Manifest delivery and raw remote verification must still complete before the final Gate request.

## Authority and protected import

- Taskbook ec2e43cd87ce264da1b77365558a182736ccb24f; taskbooks/fcop-4.0/WP4C.3c/01-Legacy-Public-Method-Set-Alignment-and-WP4C.3-Closeout-Taskbook-v1.0.zh.md.
- GitHub raw response equals Git Blob: 13805 bytes, SHA-256 c81c883c6ccf4f132ed12f511684eed93fc455fc37125b85ed4c15d8fbaeee80; strict UTF-8/LF.
- [ADMIN authorization](https://github.com/joinwell52-AI/FCoP/pull/23#issuecomment-5572037831).
- Input HEAD c19808f4bc07948729bb841ec569627cb672fde7, preceding Content 29ceaed54d63bbdff5057621b7dc0329535b1f98 and Fixture 115751b4c24a1924062a81a21e0d655e8cb5fedc remain ancestors.
- Taskbook is the direct input child, adding only its own file.
- Worktree D:/FCoP-wp4c3b-development-fixture-and-rule-package; renamed branch review/fcop-4.0-wp4c.3c-public-method-closeout.
- Raw PR #23 RESULT Git Blob table supplied the inventory. Expanded tracked/untracked modifications were exactly those 31 paths, all sizes and hashes matched.
- Authorized git merge --ff-only imported only the taskbook. Candidate identities matched again afterward and before the isolated test commit. No stash/reset/clean, candidate rewrite, original-workspace checkout or new dependency occurred.

## Exact historical identity, not a relaxed count

The old exclusion list had ten v4-only methods; authorized rule_distribution was incorrectly included in historical_names, producing 39 versus the retained assertion of 38.

The corrected v4-only set is exactly:

```text
create_workspace create_task derive_workspace inspect_state transition
finish_task family_digest recover_operation inject_fault export_archive
rule_distribution
```

The independently pinned historical set is exactly:

```text
apply_recovery archive_review archive_task archive_to_history
assert_boundary audit audit_drift boundary_violations
deploy_protocol_rules deploy_role_templates drop_suggestion
init init_custom init_solo inspect_task is_initialized
list_history list_issues list_reports list_reviews list_tasks
mark_human_approved poll_once read_history_task read_issue
read_report read_review read_task recover_session report_failure
role_occupancy status subscribe_events validate_team
write_issue write_report write_review write_task
```

Read-only AST extraction from c19808f4bc07948729bb841ec569627cb672fde7:src/fcop/v4/boundary.py independently confirms these exact 38 names. The test checks equality against that pinned set, length 38, v4-only length 11, rule_distribution presence and exclusion, disjointness, exhaustive union, no removed historical policy and exactly one additive policy. Original policy values are unchanged.

All 110 pre-existing Project method ASTs, including signatures/decorators/bodies, match the input. Recursive public snapshot comparison has exactly one delta: /project/methods/rule_distribution. No second API, hidden policy, changed iteration/length/inspect behavior or production workaround exists.

## Original test integrity

Only test_closeout_boundary_reflection_binding_and_subclass changed; all other top-level test function ASTs/names/decorators match. Original 12 Assert nodes are retained verbatim; total is now 20. No skip/xfail or renamed Test ID. The existing statement sequence remains intact with new set checks inserted.

Retained checks: validate_team staticmethod and class/instance results; inspect.unwrap name/doc/signature; bound instance identity; is_initialized; real legacy write_task/read_task; autospec unknown arguments; patch.object binding calls; inherited/overridden class behavior; unclassified-public-method rejection.

- Old raw test SHA-256: 1397e4aaf9b0158c3491c4821fc13eb6dd38a608f9c88af4c68e2f7c15417012.
- New raw test SHA-256: 960f24c1e9063101e7202cd4e73ec891d77bac19646f2c0054a844a265b04722.
- Alignment commit changes only tests/test_fcop/test_v4_creation.py.
- No candidate production byte was changed to complete this correction.

## Candidate continuity: before/after fast-forward and before test commit

Each SHA is BOTH the before and after value; all 31 rows also passed immediately before test commit. No candidate delta requires explanation. Source: [PR #23 RESULT](https://github.com/joinwell52-AI/FCoP/blob/c19808f4bc07948729bb841ec569627cb672fde7/reports/FCOP-4.0-WP4C.3-RESULT.md).

| Candidate path | Bytes | Before and after SHA-256 | Result |
| --- | ---: | --- | --- |
| CHANGELOG.md | 130694 | aea366e3f64d903049e45d79bacec56fccf5057959f15abfe65d2671f8992c8d | unchanged |
| pyproject.toml | 6075 | e51ff7f3fda0a1b9c27ab407275d452a0ea5dcfaeb5650c4137c485db8d446b5 | unchanged |
| src/fcop/project.py | 265857 | f421d7fb2a444b90c63c18bea8c8c4751af90f3c8eeb9f2ed139e32f6acbf6ec | unchanged |
| src/fcop/rules/_data/v4/authorization.en.md | 2128 | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b | unchanged |
| src/fcop/rules/_data/v4/authorization.zh.md | 2033 | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 | unchanged |
| src/fcop/rules/_data/v4/compatibility.en.md | 3521 | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 | unchanged |
| src/fcop/rules/_data/v4/compatibility.zh.md | 3024 | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e | unchanged |
| src/fcop/rules/_data/v4/convergence.en.md | 2283 | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e | unchanged |
| src/fcop/rules/_data/v4/convergence.zh.md | 2114 | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a | unchanged |
| src/fcop/rules/_data/v4/envelopes.en.md | 1743 | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 | unchanged |
| src/fcop/rules/_data/v4/envelopes.zh.md | 1672 | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef | unchanged |
| src/fcop/rules/_data/v4/idempotency.en.md | 1720 | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a | unchanged |
| src/fcop/rules/_data/v4/idempotency.zh.md | 1591 | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 | unchanged |
| src/fcop/rules/_data/v4/lifecycle.en.md | 3041 | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b | unchanged |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 2787 | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef | unchanged |
| src/fcop/rules/_data/v4/manifest.json | 11221 | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 | unchanged |
| src/fcop/rules/_data/v4/recovery.en.md | 3534 | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 | unchanged |
| src/fcop/rules/_data/v4/recovery.zh.md | 3099 | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 | unchanged |
| src/fcop/rules/_data/v4/relations.en.md | 1106 | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 | unchanged |
| src/fcop/rules/_data/v4/relations.zh.md | 1057 | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 | unchanged |
| src/fcop/rules/_data/v4/workspace.en.md | 1920 | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 | unchanged |
| src/fcop/rules/_data/v4/workspace.zh.md | 1723 | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b | unchanged |
| src/fcop/v4/boundary.py | 5988 | 1cb04f82d7bf5c4d14b73847e647131532019539ef801cae2344006f61dc9b4f | unchanged |
| src/fcop/v4/creation.py | 45982 | 521288527b3335946a18ea136aa8ac2c53f4e0574bd3767633e58873039ce434 | unchanged |
| src/fcop/v4/rule_distribution/__init__.py | 4096 | a7402c3c67b23d00201646be413e1fe12e6105c5caf2febca41742e408361f57 | unchanged |
| src/fcop/v4/rule_distribution/_contract.py | 1716 | 519a40daf73012ee8f64009d744af59138390e67bbf6fd8dd7f07a14e1cec6e3 | unchanged |
| src/fcop/v4/rule_distribution/_errors.py | 1022 | df1c0bece920f449bd4b60863188761fb18ee0a81280e0c1628f73e03e6815c8 | unchanged |
| src/fcop/v4/rule_distribution/_loader.py | 6886 | eca7c4c9330dd6c351f07ebeee4112dcade03a76be93877df4fcd95a4b380ff4 | unchanged |
| src/fcop/v4/rule_distribution/_selection.py | 6520 | 146027786c67e632ed18f2b7673211a27b58e818c3ced35fd7eee92b1f00a2f8 | unchanged |
| tests/test_fcop/snapshots/public_surface.json | 54775 | 96d45a001c073083465ed3ae9a6db9725cdf3842256312a742808c6f15c456c5 | unchanged |
| tests/test_fcop/test_v4_rule_distribution.py | 9179 | ef8a9716ff47682408f378971be7252b4f1015ca479576ff1e9a5e41647b012a | unchanged |

The same identities must match the eventual Content blobs; files were not discarded and recreated without provenance.

## Pre-commit validation

Windows / Python 3.12.9, source-root PYTHONPATH, PYTHONDONTWRITEBYTECODE=1; pytest -p no:cacheprovider. Existing deprecation warnings retained.

| Check | Actual result |
| --- | --- |
| Exact historical test function | 1 passed, 3 warnings, 7.10s |
| test_v4_creation.py + test_public_surface.py | 102 passed, 3 warnings, 76.28s |
| Candidate identities | 31/31 unchanged |
| Historical / v4-only sets | 38/38 and 11/11 |
| Original assertions removed | 0; 12 retained, 8 added |
| Other public additions | 0 |
| Ruff src/fcop, tests/test_fcop, distribution suite | PASS |
| mypy --cache-dir nul | PASS, 46 source files |

Complete regression commands, timings, 86 future-node dispositions and raw JUnit identities are recorded in FCOP-4.0-WP4C.3-CONFORMANCE-RESULT.md. Local wheel/sdist inclusion and member-byte identity pass for all nineteen v4 data files in each archive; no WP4C.6 or release acceptance is claimed. Canonical modules 9/9, artifacts 18/18, Manifest 1/1, fields 11/11, unique primary clauses 73/73 and legacy bytes 14/14 also pass. All candidate bytes remain unchanged. Final Content and Manifest hashes and remote readback are recorded externally in the Draft PR receipt to avoid self-referential commit/hash claims.

## Preserved blocker history and Gate boundary

- [PR #21](https://github.com/joinwell52-AI/FCoP/pull/21): historical audit scope incorrectly applied to later-stage files; separately authorized audit correction followed.
- [PR #22](https://github.com/joinwell52-AI/FCoP/pull/22): DIST-02 lacked four mandatory fixed local references; WP4C.3b fixed only its local fixture.
- [PR #23](https://github.com/joinwell52-AI/FCoP/pull/23): public-method classification blocker and candidate identities preserved; WP4C.3c now authorizes precise alignment.
- These are real intermediate failures, not erased or retroactively called successful. Existing PRs are not reused, rewritten or merged.
- All validations and remote readback must pass before requesting WP4C_3_RULE_PACKAGE_ACCEPTED. The Gate remains unsigned. WP4C.4, main merge and release remain unauthorized.
