---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
subject: WP4F actual MCP environment identity and gated upgrade plan
---

# Actual local MCP: Phase B plan, not an upgrade receipt

## Read-only discovery

The discovered host configuration is
`C:/Users/Administrator/.cursor/mcp.json`, server key `fcop` (the host may
expose this as `user-fcop`). Its command is
`C:/Users/Administrator/.cursor/fcop_mcp_venv/Scripts/python.exe`, arguments
`["-m", "fcop_mcp"]`, no server-specific environment keys. A read-only
`importlib.metadata.version` query in that interpreter reports
`fcop==3.2.2` and `fcop-mcp==3.2.2`.

This identifies a configured environment; it does not prove that the current
Codex session has a live connection to that server. No package in that
environment has been upgraded and no running host/service has been restarted.
The candidate tests use a separate test environment and temporary workspaces.

## Gate-dependent execution

After ADMIN signs `FCOP_4_STABLE_RELEASE_READY` and the public Stable packages
pass published-byte verification:

1. Re-read the exact host configuration and interpreter metadata; record the
   configuration SHA-256, package versions and matching service process before
   any mutation. Preserve the MCP name, command, arguments and transport.
2. Keep a reinstall path for the observed old pair. Install the exact public
   `fcop==4.0.0` and `fcop-mcp==4.0.0` into that interpreter, using no global or
   CodeFlowMu environment. Verify module paths and package metadata agree.
3. Restart only the identified FCoP service through its owning host. Never
   terminate unrelated Python processes. If host control is unavailable, ask
   for the precise host restart action rather than claiming it occurred.
4. Reconnect and read tools/resources/templates: 46/12/4 and `reopen_task`.
   Compare configuration bytes before and after; they must be unchanged.
5. Using the same upgraded interpreter in a new disposable workspace, execute
   the real stdio consumer from `tests/stable/third-party/mcp-only/client.py`:
   Root plus two Branches, explicit convergence, two independent concurrent
   service processes, exact operation retry, conflicting digest rejection and
   restart recovery. Preserve result and stderr logs.
6. Distinguish the host-connected discovery result from the isolated scenario
   result in the final receipt. No test may initialize, migrate or modify the
   user's existing project workspace.

## Authorization fixture boundary

The scenario server registers its educational Profile evaluator at trusted
server initialization, exactly as the accepted RC sample does. The caller
does not supply evaluator code in an operation request. This is an isolated
test fixture, not a production approval policy and not a modification of the
host's MCP configuration. Do not claim that live-host authorization semantics
were exercised merely because the isolated fixture passed.

If an upgrade fails, retain evidence and use the saved package pair to restore
the affected FCoP environment only. Do not delete an already published version,
rewrite the RC tag, mutate protocol behavior or modify CodeFlowMu. Phase B ends
with a factual final receipt; no additional development stage is authorized.
