# CLI v1 contract (WP0)

CLI = Setup + Observe + Diagnose. MCP = Work.
Proposer/reviewer: ME solo, re-read against ADMIN fixed v4 taskbook before coding.

Nine commands: init, status, inspect, validate, tools, doctor, version, spec,
migrate. Historical migrate-workspace and bare fcop remain unchanged.
No extra first-level work command. argparse only; no new runtime dependency.

Common --json for the eight new commands; workspace commands accept --root
(default cwd). inspect takes TASK ID or mutually exclusive --path; validate
optionally --path. Path arguments relative to resolved --root, absolute paths
must remain inside the workspace. init accepts --protocol with default read
from installed workspace Schema, never another protocol constant.

Result envelope (CLI schema version 1):
{schema_version: 1, command: string, status: ok|invalid|unavailable|error,
 data: object|null, errors: [{code, message}], warnings: array}.
JSON is one deterministic sort-key UTF-8 document plus newline, no banners,
timestamps or terminal width dependence. Human output renders the same facts.
Parser errors go to stderr, exit 2; command results (including structured data
errors) go to stdout. Exception diagnostics never contaminate JSON stdout.

Exit 0 success/valid (warnings possible); 1 unexpected internal failure;
2 invalid data/input; 3 unsupported/unavailable environment/dependency.
Missing workspace: status succeeds initialized=false; inspect/validate exit 3;
doctor warns, does not initialize. Missing MCP: tools exit 3 with installed=false;
doctor warns but Core-only installation remains healthy. Legacy migration output
and its 0/1/2 exits remain unchanged. Bare fcop retains exit 1/stderr guidance.

Only init invokes Core bootstrap. No flags implying fix/repair/recover. All
observations compare workspace tree/content hashes before/after. Reads are
point-in-time observations, not a transaction across an actively changing tree;
family data/digest uses only Core inspection and retains null/errors/warnings.
Validation is limited to observable Core checks, not business completion,
authorization judgment, or an invented migration/recovery state machine.

Public read-only observation aggregation (module fcop.observation) wraps
existing Core parsers/validators and Project queries; no existing Project method
signature or work behavior changes. Inventory reports bundled versioned rules,
Schema and frozen v4 spec citation separately, including historical rule version.
MCP catalog exposes fresh sorted name/disposition rows from disposition.TOOLS,
with no FastMCP import/server construction and no copied signature metadata.
Tests compare CLI/catalog/declaration/real stdio sets and retained parameter
snapshot. Only the three already-released Branch declarations are added.

Release condition: C01-C20, full regression, read-only/Core-only/installed
proofs, build/Twine, exact-HEAD CI and complete evidence before merge. Then tag
the merged release commit v4.0.2, build/verify from that exact tag, publish both
packages, compare public README descriptions/bytes, post final receipt and stop.
