---
protocol: fcop
version: "3.0"
sender: ME
recipient: ME
status: review
---

# MCP Branch Merge 4.0.1

Authority: ADMIN's current chat taskbook, titled FCoP MCP Branch Merge tool development.

Baseline: ec7f415f84bfb93534ffccedaad873accd744095 (origin/main).

Implement create_branch, inspect_family, and merge_branches in the MCP adapter,
preserving Core 4.0.0 and all existing 46 tools. Verify real stdio, durable
idempotency, concurrency, and regression coverage; deliver a Draft PR without
merging or publishing. Request FCOP_MCP_4_0_1_RELEASE_READY only upon completion.

First verify the installed Core's family digest and convergence append capabilities
in disposable workspaces. A genuine Core capability/atomicity gap must be reported
with executable evidence before inventing adapter semantics.

Solo review: scope accepted; no original-workspace, CodeFlowMu, Core, tag, or
release changes are allowed. Capability observations are not feature acceptance.

Execution disposition: stopped at the explicitly permitted Core capability
boundary. See REPORT.md and the executable probe. Development is incomplete;
no release gate is requested.

## ADMIN continuation, 2026-09-11

AUTHORIZE_FCOP_4_0_1_CORE_MERGE_PRIMITIVE supersedes the Core-immutable
restriction above. Both packages target 4.0.1; MCP requires Core >=4.0.1,<4.1.0.
Implement a public Core merge_branches primitive and partial family inspection,
with nullable unavailable digest, structured reasons and merge_ready=false.
Unify legacy convergence append and the new primitive under one Core family-lock
acquisition, durable idempotency, atomic publication and recoverable receipts.
Equivalent content has one REVIEW per Root/digest; competing content conflicts.
The MCP adapter only converts requests and invokes Core. Preserve all 46 existing
tools and add exactly three. No CodeFlowMu, merge, tag, or publication changes.
The prior blocker remains a historical observation of released 4.0.0, now resolved
by explicit implementation authority. Upon implementation and CI completion,
request FCOP_4_0_1_RELEASE_READY once.
