---
protocol: fcop
version: "3.0"
sender: ME
recipient: ME
status: blocked
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
