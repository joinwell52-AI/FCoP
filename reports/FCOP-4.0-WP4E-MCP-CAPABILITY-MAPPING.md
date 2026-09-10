---
protocol: fcop
version: '4.0'
sender: ME
recipient: ADMIN
stage: WP4E_PHASE_A
taskbook_commit: 793b5eef808cecc55437c8c2dc43e737b56b1300
baseline: 64a24295d6c1fa53a182a819d39b295c2ba8d2d0
status: FINAL_HEAD_VERIFICATION_PENDING
---

# WP4E MCP capability proof

## Evidence boundary

This is an executor report, not an ADMIN signature. The accepted WP4D parent is
`64a24295d6c1fa53a182a819d39b295c2ba8d2d0`, authenticated through
[OWNER Gate comment](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987).
The remote Manifest was read as 34249 bytes with SHA-256
`21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d`.
Taskbook: `793b5eef808cecc55437c8c2dc43e737b56b1300`, 13138 bytes, SHA-256
`05e39d231950917e56fef6cf63c9ee081316356058115a4942c47dffe3678bbc`.

Draft PR [#33](https://github.com/joinwell52-AI/FCoP/pull/33) targets main.
No main merge, tag, publication or CodeFlowMu operation is authorized or executed.
Final evidence/Manifest commits cannot substitute an earlier CI run for final HEAD CI.

## Public capability map

| Capability | Public entry | Evidence |
|---|---|---|
| v4 workspace | init_solo, init_project | explicit version route; tests/test_fcop_mcp/test_wp4b_delivery.py and installed client |
| TASK and Branch | create_task / write_task, branch_of | Root plus two Branches in stdio client |
| Persistent create | operation_id | simultaneous real service processes; one task, one Existing |
| T2/T3 | claim_task / submit_task | current REPORT head, actual file stage inspection |
| T4/T5 | approve_task / reject_task | acceptance/rejection evidence and single-use authorization; new attempt on T5 |
| T6 | reopen_task | separate reopen REVIEW and authorization; same request exact retry, zero snapshot delta |
| T7 | archive_task | ordinary task plus Root with Branches and digest-bound authorization |
| REPORT head | write_report, list_reports, read_report, inspect_task | tests/test_fcop_mcp/test_wp4b_resume.py and test_wp4b_delivery.py; no MCP-owned graph |
| Authorization append | write_review, mark_human_approved | trusted startup; tests/test_fcop_mcp/test_wp4b_authorization_append.py and existing delivery suite |
| Family digest | inspect_task(include_family_digest=true) | digest before convergence, equality after process restart |
| Convergence | write_review(review_kind=convergence) | references both Branch REPORT heads; then Root archive |
| Versioned resources | resources/list, resources/templates/list, resources/read | exact 46/12/4, installed resource probes and WP4C.5 compatibility tests |
| Rule deployment | existing redeploy_rules / deploy_role_templates | version routing; no new MCP runtime or inferred adoption |
| Failure / retry | structured code, Existing, zero effects | OPERATION_ID_CONFLICT and unchanged file/directory snapshots |

File references above are navigation; exact collected test names and final suite
counts are bound by CI evidence, not inferred from a tool name count.

## Independent MCP-only executable

`examples/v4/third-party/mcp-only/client.py` uses stdlib JSON-RPC over stdio.
It does not import fcop/fcop_mcp; a final sys.modules assertion enforces that.
Trusted evaluator configuration stays in server.py, not a tools/call request.

The final sample traverses all T2–T7 on an ordinary TASK, completes Root plus two
Branches, writes convergence referencing both REPORT heads, archives Root, and
checks 24 persisted transitions across the observed tasks.
Two distinct server PIDs submit real create writes after a dispatch barrier;
they share an operation_id and digest, return the same task, and exactly one
returns Existing. A repeated conflicting body returns structured OPERATION_ID_CONFLICT
with no file or directory changes. A third process reopens the filesystem and checks
both lifecycle and race retries against preserved results.
No method-existence probe is counted as behavioral coverage.

Source-only runs are labeled SOURCE_ONLY and never replace the 24 installed origins.
The demo evaluator is educational, not a production identity policy. No new general
MCP recovery tool is invented; Core recovery and exact retry are separately described.
