# 4.0.3 ownership boundary

Authority: fixed taskbook 8ec8658c15f2aa148bd42e3d6e6bb916921e4b0b, sections 2–8 and 13; ADMIN continuation and CLI supplement recorded in RESUME-PLAN.md.

## Exact normative delta

Spec-only commit: `1f91d53c51f040b1f4bd306d72d7e31ce35c7084`. Only the prescribed bilingual ownership paragraphs were added under F4.1.2. Both specs retain the same 73 clause IDs. The release-identity tests remove exactly this addition and the previously authorized identity header/self-references and compare the remaining normative text against its pinned historical hash.

| Source | SHA-256 |
| --- | --- |
| spec/fcop-4.0-spec.md | 8fba4ee790f380e71c50de0d841beb61d67ea9209cd4b77315d5523debe90140 |
| spec/fcop-4.0-spec.zh.md | 4cfe5696b85b8f26399719b8f74dc7593f3fb796e886a9040881961bf8ff910a |

Core read identity and both MCP spec payloads reference that actual commit and these exact bytes. No changes to Schema, the 18-file Core Conformance tree, creation, Encoding, lifecycle, authorization, convergence, idempotency or recovery semantics.

## Product disposition

The public rule_distribution entry/signature remains. Host-only actions reject before reading Host profiles, targets or receipts: redeploy, inspect_profile, status, adopt, plan, apply, verify_deployment, rollback, inspect_failure, rollback_partial, measure_context. Result is existing structured `toolkit:OPERATION_NOT_IMPLEMENTED`, not a new error code.

Removed private Host deployment, projection, profile, measurement and receipt modules. Retained strict package loader, read/validate/select, deterministic assemblies, operation-scope guidance checks, resources and artifact export. The recursive executable-input rejection helper moved unchanged to _request.py. inspect_layers reports package disk/index identity, empty Host entries and unknown Runtime consumption; no historical deployment receipts are trusted or deleted.

The repository's CLAUDE.md and two Cursor protocol mirrors were removed; AGENTS.md is now short repository-owned contributor guidance, not a protocol artifact, not packaged and not customer-deployed. All previous bytes remain recoverable in Git. This cleanup applies only to this isolated review worktree.

## Initialization qualification — not hidden

The existing atomic initializer uses `.fcop-init-*` staging and preserves failure evidence. That mechanism is unchanged, as required by taskbook section 13. Successful normal workspace state resides in `<project>/fcop/`; this report does **not** claim every failed initializer writes exclusively there. The prior BLOCKED reproduction is retained as historical evidence, and the continuation interpretation is explicit in RESUME-PLAN.md. No Host instruction bytes are generated or modified by initialization.

Original D:/FCoP and CodeFlowMu were not modified. Customer files are never automatically cleaned, migrated or redeployed.
