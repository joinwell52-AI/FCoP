# ADMIN-authorized 4.0.1 continuation

The 4.0.0 blocker in REPORT.md is preserved as historical evidence. ADMIN's
2026-09-11 decision authorizes a Core merge primitive, partial inspection and both
4.0.1 packages on PR #37. No additional taskbook or reviewer rule was introduced.

## Implemented boundary

- Public Core `inspect_family` and `merge_branches`; new MCP `create_branch`,
  `inspect_family`, `merge_branches` delegate to public Core methods only.
- Convergence `write_review` shares the Core atomic merge path. Family lock is
  acquired exactly once, after the existing OS operation lock scoped to workspace
  merge identities. Different content for one Root/digest is rejected; equivalent
  requests share a single REVIEW. Request identity binds all formal fields,
  independently of reference ordering and optional null values.
- PREPARED Core receipt persists exact REVIEW bytes before no-overwrite publish;
  retry validates those bytes and commits the receipt. Existing fsync/publication,
  durable replacement, receipt-stage constants and fault-injection mechanisms are
  reused. Lifecycle movement semantics and their five-state recovery are unchanged.
- Both a historical singleton equivalent REVIEW and new durable results can be
  reused. Multiple historical REVIEWs or conflicting content are not silently
  selected or deleted. Original 4.0.0 facts are never overwritten.
- Incomplete family digest is null with structured reasons and merge_ready=false.
  Existing strict `family_digest` behavior stays unchanged. No surrogate digest.
- Both package versions become 4.0.1; MCP dependency >=4.0.1,<4.1.0. The released
  4.0.0 tag/artifacts and release workflows remain untouched.

## Tests and historical assertions

New acceptance tests cover real synchronized processes (including old/new writer
competition), process death at four durable boundaries, restarts, partial families,
stale digest, actual replacement REPORT, omitted/swapped heads, terminal gates,
damaged receipts, operation/content conflicts, historical singleton adoption and
real MCP stdio creation/inspection/merge. Targeted tests passed 28/28 before the
final regression, with the historical replay follow-up also checked independently.

An exact copy of the original 46-tool snapshot is retained as
`tests/test_fcop_mcp/snapshots/tool_surface_4_0_0.json` from baseline
`ec7f415f84bfb93534ffccedaad873accd744095`; the new test compares every retained
tool's full parameter snapshot, plus unchanged resources/templates. The current
snapshot is additive by exactly three tools. The Core snapshot is additive by
exactly two methods; the historical public method set remains exactly 38.

Only current-version/count assertions in historical non-frozen regression tests
were aligned to the explicitly authorized 4.0.1/49-tool additions. Their original
behavior, binding, signing and error assertions remain. Frozen Conformance and
Schemas are unchanged. README bilingual link/code-block equality was retained by
aligning document links, not weakening that test.

Initial full Core/MCP/v4 run recorded 10 failures and 1899 passes before snapshot,
version, count and README-link alignment. Those were not called successful runs.
The subsequent targeted compatibility run passed 74/74. A newly isolated dev
environment was used; the installed user-fcop service and original workspace were
not upgraded or changed during this development task.

## Delivery status

Implementation is in review. Full local regression, final artifact checks and
GitHub matrix results are recorded in the final delivery receipt when complete.
No full-regression or CI PASS is claimed by this intermediate report.
No merge, tag, publication, CodeFlowMu change or release Gate request has occurred.
