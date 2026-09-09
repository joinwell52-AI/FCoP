# MCP-only unpublished RC demonstration

Copy this directory outside the repository. The external `client.py` is
standard-library-only and never imports `fcop` or `fcop_mcp`. It speaks actual
stdio JSON-RPC, discovers the public 46/12/4 surface, and checks required input
fields before calling discovered tools.

In a fresh venv install the two verified local `4.0.0rc1` candidate artifacts.
Run `python -I -B client.py <fresh-directory>` outside the FCoP checkout.
No editable installation, PYTHONPATH or public candidate registry resolution
is permitted for acceptance.

`server.py` is separate trusted startup configuration using the public
`fcop_mcp.server.create_server` entry. It registers an educational fixed Profile
before accepting requests. It is not a production identity verifier; callers
cannot supply an authorization evaluator in business requests.

The client runs sequential and Branch/convergence workflows, records a
transport-level committed-response witness, withholds that result from the
simulated retrying application, kills the real server, and opens a new server
process. It checks disk bytes, states, events and family identity, then retries
the same operation and rejects a changed request without side effects.

The consumer keeps stderr and summaries outside the checkout. All application
network operations are denied; Windows event-loop socketpair plumbing is the
only narrowly identified stdlib exception. The example does not use Relay.

`--source` is explicitly SOURCE_ONLY parity, never clean-room evidence.
Nothing in this unpublished example authorizes main merge or release.
