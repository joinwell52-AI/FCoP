# WP4B version routing and trust boundary

Reporter: ME. Authority: WP4B through WP4B.3a; fixed input
`74f0150eee88bcef754fbd5182d2eba9836a04ec`. This report does not sign a Gate.

## One dispatch boundary

`mcp/src/fcop_mcp/routing.py::WorkspaceRouter` classifies the declared
manifest with strict UTF-8 and duplicate-key rejection, preserves legacy CRLF,
and passes exact v4 to the Project v4 boundary. It does not infer version from
directories, request arguments or a failing operation. Rebinding reclassifies.
`disposition.py::TOOLS` is the one immutable dispatch table. Global catalog/
package utilities and the three Profile catalog templates are not workspace
identity authorities; explicit bootstrap is a separate creation operation.

`adapter.py` preserves legacy positional/default semantics and adds only
optional v4 fields. A v4 writer requires its formal workspace/operation/evidence
inputs at runtime. A failed v4 call never enters a legacy writer. Project
instances receive a copied, immutable server-startup trusted Profile registry.
No tool can register an evaluator. Reading a role resource cannot grant rights.

## Authorization facts: WP4B.3

The existing `Project.mark_human_approved` now appends an authorization REVIEW.
It derives workspace, subject, recipient and the old REVIEW reference itself;
fixes authorization kind, lifecycle operation kind and single-use scope; checks
the actual TASK source stage/attempt and edge-specific family binding under the
existing family boundary; requires timezone-aware issued_at and an explicit
nullable expires_at; calls the trusted evaluator; rechecks expiry and immutable
inputs before publication. The old REVIEW is never rewritten. No TASK is moved.

`src/fcop/v4/authorization.py::validate_profile_issuer` is the single evaluator
invocation implementation shared by append and consumption. Only exact
AUTHORIZED succeeds. DENIED, UNKNOWN, exceptions, malformed proof, missing/
unadopted Profile and caller-provided judge material fail closed. Consumption
does not trust a prior successful append: it repeats issuer/time/digest/binding
and single-use checks. Existing inert extension fields do not overrule the
registered evaluator (SB-06 regression). Generic write_review semantics remain
unchanged: recording a generic fact is not proof that it can authorize a Gate.

Evidence: `tests/test_fcop/test_v4_authorization_append.py` (46 cases);
`tests/test_fcop_mcp/test_wp4b_authorization_append.py` (5 real Client cases).
The first directed pre-implementation run was 35 failed. An intermediate
expiry-after-evaluator test failed and was fixed by looking up the shared
clock at publication time. Full corrected directed authorization + REPORT/
lifecycle regression: 114 passed. All failure tests snapshot complete workspace
bytes; successful append preserves old bytes and adds one REVIEW only.

## C2-R02 local alignment

Only `tests/conformance/v4/test_c2_envelopes.py::test_c2_r02` changes within
frozen Conformance. AST comparison against input proves all 6 original
assertions unchanged, 14 additional assertions, and every other module-level
node/function unchanged. The local driver receives the adopted Profile at
trusted initialization; business parameters carry only formal proof/bindings.
It arranges a legal current review-stage attempt, checks exactly one evaluator
call and its arguments, canonical saved authorization fields, and unchanged TASK
bytes/path. It does not perform a later transition to make C2 pass.
Global driver/conftest unchanged; original ID/clause unchanged; no skip/xfail.

## REPORT query and shared authority

WP4B.2/.2a activate the two existing public names list_reports/read_report.
`src/fcop/v4/reports.py` calls the same `lifecycle.report_head` resolver as
T3 and other consumers. Zero head returns REPORT_REQUIRED; multiple heads
return REPORT_HEAD_AMBIGUOUS. Filtering/pagination cannot hide invalid graphs.
Inventory is rescanned around the existing short per-family locks; any observed
change fails closed. This is not a workspace-wide transaction or new index.
Exact replaced-report reads preserve their own content and expose current head
metadata. Twenty directed reader tests plus 48 lifecycle cases passed (68 total).

## Thinness and limits

MCP contains no lifecycle/authorization/receipt/family-digest algorithms.
It uses Project.transition for T2–T7 and Project operations for all formal writes.
No private fcop.v4 authorization or REPORT resolver is imported by MCP.
MCP uses the existing V4ProtocolError and its enum to project stable Core codes
into standard MCP CallToolResult(isError=true, structuredContent=...); no second
Base error registry is introduced.

TASK/ISSUE/REVIEW queries enumerate files and call public Project readers;
filters are read-only projections. TASK state inspection is Project.inspect_state,
not a promise of a new whole-workspace evidence audit. Actual lifecycle Gates
remain the authority for evidence/authorization eligibility. Optional governance,
Profile deployment and undistributed v4 guidance return explicit unavailable
results; they are not falsely labelled as implemented Core features.
No recovery tool or generic transition tool is added; the accepted Core retains
its recovery authority, and exact retries exercise it through public operations.
