# 4.0.3 four-file retirement — execution baseline

Status: IN_PROGRESS; no implementation, test-pass, merge or release claim.

## Authority and protected scene

- ADMIN task: PR #48; executor ME (solo); acceptor ADMIN. No sub-dispatch.
- Taskbook commit: `8ec8658c15f2aa148bd42e3d6e6bb916921e4b0b`.
- Fixed Git blob: 16,312 bytes; SHA-256 `1fccdeca2e7332cc5e5e397847409e9a4f86d32c81ada64dcce4d88bc7a1f70d` (computed from `git show`, not CRLF checkout bytes).
- Taskbook path: `taskbooks/fcop-4.0/4.0.3/01-Legacy-Four-File-Rule-Distribution-Retirement-and-4.0.3-Release-Taskbook-v1.0.zh.md`.
- Development base: `157acaeb0cbd11bbf0ce54fba18c2a7d0d980efb`, execution-time fetched `origin/main`.
- The taskbook commit is its direct child, changing one file only (GitHub PR API and `git log -1 --format=%H/%P` verified).
- Branch: `review/fcop-4.0.3-four-file-retirement`; existing OPEN Draft PR #48.
- Isolated worktree: `D:/FCoP-4.0.3-four-file-retirement`.
- Original `D:/FCoP` is dirty and preserved. No original branch checkout, cleanup, migration or rule redeployment. CodeFlowMu is outside the write scope.
- Implementation delivery only: merge, tags, PyPI, GitHub Release, Registry and production Pages publication require subsequent explicit ADMIN authorization.

The fixed taskbook is the task record. This baseline is the pre-implementation review of its scope; the executor will append result evidence and wait for ADMIN rather than self-accept or archive.

## Verified baseline inventory

| Surface | Observed source | Required disposition |
| --- | --- | --- |
| Core initialization | `src/fcop/v4/creation.py:_Creation.create` | Existing explicit v4 initialization creates no Host instructions. Preserve atomic initialization and Core encoding; verify customer bytes. |
| MCP initialization | `mcp/src/fcop_mcp/adapter.py:register_legacy_routes` | Explicit `protocol_version=4.0` routes to public `Project.create_workspace` before legacy `deploy_rules=True`; retain and test. |
| MCP redeploy | `mcp/src/fcop_mcp/disposition.py:TOOLS`; `adapter.py`; `projection.py`; `server.py:redeploy_rules` | Current disposition is PROFILE_DEPLOY; explicitly classify Legacy v1–v3 only without changing parameters/count. |
| v4 dispatcher | `src/fcop/v4/rule_distribution/__init__.py:_dispatch` | Public rule_distribution dispatches Host adoption/plan/apply/rollback operations; retire Host operations without losing reads/selection. |
| Host mappings | `_selection.py:profile`; `_profiles.py` | codex→AGENTS.md, cursor→.cursor/rules/fcop-v4.mdc, claude-code→CLAUDE.md; remove current product ownership. |
| Host writes | `_projection.py`, `_deployment.py`, `_receipts.py` | Host framing/replacement/backups/receipts and rollback exist; retire their current execution paths and associated tests. |
| Related queries | `_read.py:inspect_layers`, `_measurement.py:measure_context` | Read/measurement currently depend on deployment/profile helpers. Preserve non-Host package inspection and do not retain an indirect projection backdoor. |
| Package read/export | `_loader.py`, `_selection.py`, `_read.py`, `_artifacts.py` | Preserve strict 18-artifact/9-module validation, deterministic assemblies and explicit data export. |
| Current rule package | `src/fcop/rules/_data/v4/manifest.json` | 18 artifacts; 11 per-artifact fields; component version currently 4.0.0-candidate.1. No silent hash normalization. |
| Stable spec identity | `spec/fcop-4.0-spec.{md,zh.md}`, `_read.py:_SPEC`, MCP `_specs.json` | Add only authorized ownership invariant; update exact source citations/resource bytes and identity checks. Keep historical evidence pinned. |
| Root mirrors | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/fcop-{rules,protocol}.mdc` | Repository-owned cleanup only in this isolated branch; no customer-file deletion. |
| Current website | `docs/index.html` | Already 4.0.2, not 4.0.0. Still explicitly advertises Host projections at line 204. Update actual source and verify rendered preview, without publishing. |
| README | `README.md:206`, Chinese counterpart | Current adopted/deployed Host projection wording needs retirement. |
| Canonical PyPI descriptions | `fcop-README.pypi.md`, `mcp/README.md` | Inspect built metadata, not just repository text; public 4.0.3 verification remains pending release authorization. |
| Regression | `tests/conformance/rule_distribution_v4`, `tests/test_fcop/test_v4_rule_distribution*.py` | Separate retired Host requirements from retained manifest/assembly/resource/legacy/atomic guarantees. No generic skip/xfail workaround. |
| Historical contract | `docs/fcop-4.0/rule-distribution-contract.{md,zh.md}`, old WP4C reviews/taskbooks | Preserve traceable historical contracts/Gates; clearly identify superseded Host clauses rather than falsifying historical acceptance. |

## Pre-implementation checks still required

- Record fixed Git blob SHA-256 independently of checkout EOL conversion.
- Inventory all current entry points, root ownership effects and exact legacy fallback behavior.
- Resolve retained read/assembly behavior and obsolete projection checks with explicit evidence.
- Run directed tests, full regression, package verification and Draft PR CI.
- Do not call implementation READY until all taskbook section 16 criteria are supported.
