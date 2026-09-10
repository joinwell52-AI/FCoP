# FCoP 4.0 — compatibility

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace.

## F4.0.1

Read MUST/MUST NOT as requirements and SHOULD/MAY as recommendation or permission. Rule guidance cannot weaken a normative requirement.

## F4.0.2

Use the frozen English Core as primary authority; the Chinese clauses, objects, edges, errors and invariants must be equivalent. A language conflict blocks freeze/release.

## F4.0.3

Schema governs expressible structure, specification governs behavior, and tests verify rather than invent rules.

## F4.1.2

FCoP governs behavior but does not run Agent work, models, tools, hosts, sessions, schedulers, databases, UI, network or processes. Keep Core, its Specification, convenience Toolkit, policy Profile and execution Runtime distinct.

## F4.1.3

Keep Core limited to C1–C8: workspace identity, four envelopes, lifecycle, four relations, evidence/convergence, durable authorization, create idempotency and recoverable atomic semantics.

## F4.1.4

Do not promote fixed roles, EVAL, Ledger envelopes, Git branches/merge, CodeFlowMu surfaces, BCG, Relay or online upgrade into Core.

## F4.10.1

Use the frozen 31-code Base registry, not a rule-created error set: workspace 5, envelope/relation 5, evidence 7, authorization 5, idempotency 1, state/recovery 8. Consult F4.10.1 for exact spellings; module-specific guidance cites the applicable codes without adding a Base code.

## F4.10.2

Consume structured machine-recognizable errors with operation and subject references. Do not infer a stable error code solely from exception text.

## F4.10.3

Namespace Toolkit/Profile errors explicitly; never replace or reinterpret Base codes.

## F4.11.1

Continue reading a v3 workspace as v3 until explicit migration. Rule selection is not migration or declaration and grants no 4.0 write permission.

## F4.11.2

Treat finish_task and four history tools as LEGACY_V3_ONLY. A 4.0 Legacy query may read history, never move an authoritative TASK into it.

## F4.11.3

fcop is a reference Toolkit, fcop-mcp an optional adapter; tool/resource catalogs are not Core. Dispatch retained names by workspace version and fail closed if safe compatibility is unavailable. The frozen clause's historical counts are not a new distribution catalog.

## F4.11.4

A Branch is TASK creation with branch_of, not a mandatory new MCP tool. close_issue is not made official by downstream catalog drift.

## F4.11.5

Keep the Base MCP adapter thin and stdio-oriented. Optional Relay and upgrade/redeploy/GAL/workspace/session capabilities remain Toolkit/Profile/Runtime, not Core.

## F4.12.2

Conformance evidence must cover normal, rejection and applicable race/recovery cases for C1–C8, including the six WP0 scenarios and frozen fork, Profile, byte-digest, family-race, idempotency-layer and five-state recovery contracts. Guidance presence alone proves none of these.

## F4.12.3

Stop release when Schema, specification or tests conflict; none silently overrides another. All conformant implementations expose the same observable contract.

## F4.12.4

A candidate document or rule package does not authorize implementation, migration, push or release. Check the separately signed Gate and explicit current task scope; never advance a stage automatically.
