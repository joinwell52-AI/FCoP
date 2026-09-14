# 4.0.3 execution checkpoint — initialization boundary needs ADMIN clarification

Status: BLOCKED_ON_SCOPE_CLARIFICATION. Not READY_FOR_ADMIN_REVIEW; no release Gate requested.

## The exact conflict

Taskbook section 3 says the only permitted normal v4 initialization write scope is `<project>/fcop/`. Section 13 forbids changing the existing workspace Encoding and recoverable atomic semantics.

The unchanged implementation at `src/fcop/v4/creation.py:211–241` deliberately stages the complete workspace in `<project>/.fcop-init-*`, then publishes that directory atomically as `fcop/`. A failure before publication or a losing concurrent initializer preserves the staging directory as recovery evidence. It is therefore not just an in-memory path or a Host-rule file.

The existing tests at `tests/test_fcop/test_v4_creation.py:649–783` require preservation of this evidence, including exactly one losing `.fcop-init-*` directory after a real two-process race. Moving the staging mechanism into a prematurely visible `fcop/`, deleting losing evidence, or changing these assertions would change the protected initialization boundary. None of those changes was made.

This is **not** evidence that normal v4 initialization writes AGENTS/CLAUDE/Cursor files. It does not. It is a mismatch between an absolute filesystem write-scope requirement and the preserved atomic initialization implementation.

## Reproduction on unchanged Core

Run the adjacent `initialization-boundary-repro.py` with the task environment's Python. It uses a disposable customer directory, injects an I/O failure immediately before directory publication, then retries initialization.

Observed on 2026-09-14:

```text
status: REPRODUCED_NOT_ACCEPTED
staging: .fcop-init-jmmu6rnz
target: fcop
first_error: RECOVERY_REQUIRED
retry_error: RECOVERY_REQUIRED
retry_zero_write: true
host_instruction_files_created: false
```

The staging directory held fcop.json, `_lifecycle/{inbox,active,review,done,archive}`, reports, issues, reviews, operations and cold. The canonical `fcop/` remained absent. Evidence was preserved at `C:/Users/Administrator/AppData/Local/Temp/fcop-403-init-boundary-ppq2tok8`.

`git diff 8ec8658c15f2aa148bd42e3d6e6bb916921e4b0b -- src/fcop/v4/creation.py src/fcop/v4/encoding.py` was empty. The reproduction uses those unchanged files, not a replacement initialization implementation.

Existing initialization boundary tests were run separately:

```text
pytest tests/test_fcop/test_v4_creation.py
  -k 'closeout_initialization_faults or closeout_existing_canonical_and_staging_preserved or closeout_spawn_initialization_no_overwrite' -q
8 passed, 90 deselected, 3 existing deprecation warnings; 1.32s
```

## Safe partial work preserved locally

Four production candidate files and two new test files remain **uncommitted**, in the independent worktree only. They are not an implementation acceptance delivery. Candidate changes disable the public v4 Host deployment actions, decouple pure rule selection from Host profiles, and label MCP redeploy as Legacy-only. No initialization, lifecycle, authorization, recovery, encoding, specification, customer Host file or version was changed.

| Local candidate file | Raw checkout SHA-256 |
| --- | --- |
| mcp/src/fcop_mcp/disposition.py | 89e597de2886face27b6f1eeda8759d403e94da386b1b55cdddfd64adcbd2ea0 |
| mcp/src/fcop_mcp/projection.py | 01a6ad14a8ddd1a5726a0e3184b633be438260a3c8ed71ed6af62f913109de25 |
| src/fcop/v4/rule_distribution/__init__.py | 9f418c60b86dd9883388a03deef3c7a2be7e952a649b626b11d1208ff987e9e1 |
| src/fcop/v4/rule_distribution/_selection.py | c7445e34d1ed68830d18fc11326d2dd52ecbfb82a608226315c28840c8086b7f |
| tests/test_fcop/test_403_root_ownership.py | fe1adba921659d6ac96b35ffc1df218e447948d9f2b88b3d777ede87ecbaeabc |
| tests/test_fcop_mcp/test_403_mcp_root_ownership.py | c768f404642a392c5b9ee65daa0502edeff3dfe3db390d82e8ac6c5c37191aa8 |

Directed combined run: **130 passed**, 3 existing warnings, 27.81s. It covers the two new ownership test files (32 nodes) plus the existing creation tests (98 nodes). Actual stdio tests include both initialization tools, existing/absent customer files, rules/protocol/four guidance reads, redeploy zero writes, and catalog **49/12/4**.

JUnit: `C:/Users/Administrator/.codex/tmp/fcop-403-directed-and-initialization.xml`; SHA-256 `1ec28bc9def284e5648bed7dcaa1b96282cacb42f3eed48c4dcf8bd9c0996ebc`.

Initial directed run was 24 failed / 8 passed because the new tests omitted the existing `toolkit:` prefix in `toolkit:OPERATION_NOT_IMPLEMENTED`. The test expectation was corrected to the existing precise structured code; production error codes were not changed. The subsequent 130-node run passed. The first stand-alone reproduction used an unresolved Windows short temp path; resolving the test root fixed the harness assertion. These intermediate failures are not erased or misrepresented as production defects.

Ruff on the four candidate production files and two new tests: PASS. Full regression, obsolete Host-test retirement, bilingual ownership clauses, version changes, packaging, website and final CI remain NOT_RUN / INCOMPLETE. The 130-node run is not full-release acceptance.

## Requested clarification

Recommended narrow clarification: section 3's persistent business workspace is `fcop/`; the existing same-volume `.fcop-init-*` atomic initialization staging and failure-evidence mechanism is explicitly retained as an Encoding exception. It does not permit any Host instruction creation, modification or deletion. Successful initialization leaves no staging directory; failed or losing concurrent initialization preserves evidence according to the existing tests.

Alternatively, if section 3 must prohibit **all** temporary or failed initialization writes outside `fcop/`, the task needs explicit authorization and a replacement atomic initialization contract. The executor must not silently invent that contract or remove the existing recovery assertions.

No additional independent reviewer or release-formality requirement is being introduced. The missing decision concerns only this concrete existing filesystem behavior.

## Standard checkpoint receipt

```text
STATUS: BLOCKED_ON_SCOPE_CLARIFICATION
BASE_COMMIT: 157acaeb0cbd11bbf0ce54fba18c2a7d0d980efb
BRANCH: review/fcop-4.0.3-four-file-retirement
FINAL_COMMIT: SEE_CHECKPOINT_MANIFEST_AND_PR_RECEIPT
DRAFT_PR: 48
FCOP_VERSION: 4.0.2 (4.0.3 NOT BUILT)
FCOP_MCP_VERSION: 4.0.2 (4.0.3 NOT BUILT)
MCP_SURFACE: 49/12/4 (LOCAL DIRECTED STDIO PROOF)
ROOT_OWNERSHIP_TEST: 32 DIRECTED NODES PASS; INITIALIZATION STAGING EXCEPTION UNRESOLVED
FULL_TESTS: NOT_RUN; DIRECTED_COMBINED 130 PASS; INITIALIZATION_REPRODUCTION 8 PASS
PACKAGE_HASHES: NOT_BUILT
PYPI_DESCRIPTION_STATUS: NOT_UPDATED_OR_PUBLISHED
HOMEPAGE_STATUS: BASELINE_SOURCE_IS_4.0.2; NOT_UPDATED_OR_PUBLISHED
PUBLIC_RELEASE_STATUS: NOT_AUTHORIZED; NOT_PERFORMED
MCP_REGISTRY_STATUS: NOT_MODIFIED
UNRESOLVED: SECTION_3_INITIALIZATION_STAGING_VS_SECTION_13_ATOMIC_ENCODING_PRESERVATION
REQUESTED_ADMIN_GATE: NONE; REQUESTING_NARROW_SCOPE_CLARIFICATION
```
