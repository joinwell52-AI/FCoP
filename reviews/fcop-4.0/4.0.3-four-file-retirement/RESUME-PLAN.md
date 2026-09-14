# 4.0.3 continuation plan

On 2026-09-14 ADMIN instructed: “你继续完成任务！” after the initialization boundary checkpoint. Continue PR #48 in the preserved independent worktree. This is not release or merge authorization.

The implementation preserves the existing `.fcop-init-*` atomic initialization staging and failure evidence unchanged, as required by taskbook section 13. The permanent business workspace is `fcop/`; no Host instruction file is created, modified, required, or deleted. This interpretation and the existing staging behavior must remain explicit in the final ownership evidence; do not claim that failed initialization has no staging writes outside `fcop/`.

The prior BLOCKED checkpoint remains historical evidence. All six candidate checkout hashes were rechecked against that checkpoint and matched before continuation.

Work remaining: retire all public Host projection paths and their dedicated tests; retain package reading, validation, selection, assemblies and resource routing; add the exact bilingual ownership invariant; synchronize source identities, release metadata and current documentation; run full regressions and artifact checks; deliver evidence on Draft PR #48. No CodeFlowMu work, automatic customer migration, main merge, tag, public publication, or Registry mutation.

ADMIN supplemental request: expose a non-collapsed, independent CLI section in README.md, README.zh.md, the actual GitHub Pages homepage source, fcop-README.pypi.md and mcp/README.md. Each introduces all nine CLI commands with purposes and a visible Install & Verify example. Preserve CLI = Setup + Observe + Diagnose / MCP = Work; explicitly state offline local use, doctor no network/Host writes, no CLI work-operation surface, and customer Host ownership. This is part of the same task and Gate, not a new stage.

Review before execution: this plan does not change initialization, Encoding, lifecycle, authorization, idempotency, recovery, or Branch semantics. Historical tests and artifacts must not be presented as current Host installation requirements. Tests removed or replaced must be individually classified as projection-only; unrelated assertions stay enforced.
