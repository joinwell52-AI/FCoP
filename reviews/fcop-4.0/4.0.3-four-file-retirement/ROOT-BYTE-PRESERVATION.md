# Customer root byte preservation

Source checks: `test_403_root_ownership.py` 30/30 plus `test_403_mcp_root_ownership.py` 4/4; also executed against the installed wheel pair as part of a 36/36 behavior run.

Customer fixture includes arbitrary AGENTS.md (including invalid UTF-8 and CRLF), CLAUDE.md, .cursor/rules/customer.mdc, GEMINI.md, README.md and all 256 byte values in a binary file. Snapshots compare every existing byte and directory and reject unexpected additions outside fcop/.

Coverage:
- Empty and occupied roots; Project and real CLI initialization.
- Real T1/T2, REPORT, T3, assessment REVIEW, status/doctor/validate and reopened Project reads.
- Eleven retired Host actions × empty/occupied roots, exact structured rejection and no new internal/rule-distribution state.
- Four language/assembly combinations with rules and protocol reads.
- Both MCP initialization tools × empty/occupied roots, real resource reads and force/archive redeploy attempts.
- Offline doctor test traps socket.connect, create_connection and subprocess.Popen and preserves arbitrary customer bytes.
- Installed Branch test retains Root plus two Branches, explicit caller decision, merge, retry/conflict and restart behavior.

Successful normal operation leaves new workspace state only beneath fcop/. The unchanged atomic initialization staging/failure qualification is stated in OWNERSHIP-BOUNDARY.md; it is not silently excluded from the audit.
