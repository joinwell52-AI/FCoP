# CLI v1 reference — FCoP 4.0.2

**CLI = Setup + Observe + Diagnose. MCP = Work.** Python 3.10–3.13.
`fcop` contains Core and CLI; `fcop-mcp` is optional. No new runtime dependencies.

```sh
pip install fcop
fcop version
fcop doctor
fcop init
fcop status
```

Optional Catalog discovery:

```sh
pip install fcop-mcp
fcop tools
fcop tools merge_branches --json
```

| Command | Input | Writes |
| --- | --- | --- |
| init | --root PATH, --protocol VERSION | Explicit Core workspace bootstrap only |
| status | --root PATH | No |
| inspect | TASK-ID or --path ENVELOPE, --root PATH | No |
| validate | --root PATH, optional --path ENVELOPE | No |
| tools | optional TOOL-NAME | No |
| doctor | --root PATH | No |
| version | none | No |
| spec | none | No |
| migrate | existing --to-v3, --project-root, --workspace, --apply | Dry-run unless --apply |

The eight non-migration commands support `--json`. Workspace roots default to
cwd; relative envelope paths are relative to that root. Absolute envelope paths
must remain within the workspace. Spaces and Unicode are supported. Quote paths
as appropriate for the shell. No task creation, approval, branching, convergence
or authorization command is provided; use MCP/Python work APIs.

`fcop --help` discovers commands. Bare `fcop` preserves the legacy migration
guidance on stderr and exit 1. `migrate-workspace` and both migrations retain
their existing flags, rendering and exit-code behavior.

## Results and errors

One JSON document on stdout, with stable fields:

```json
{"schema_version":1,"command":"status","status":"ok","data":{},"errors":[],"warnings":[]}
```

Fields are always present; data is command-specific or null on exception.
Status is `ok`, `error`, `invalid` or `unavailable`. Error rows contain `code`
and `message`. Datetimes, paths and enums use JSON-safe representations; no
timestamps or ANSI formatting are injected. Human rendering shows the same
facts as indented text/JSON. Parser errors go to stderr, exit 2; structured
command results go to stdout. Existing migration output is unchanged.

| Exit | Meaning |
| --- | --- |
| 0 | Success/valid; informational warnings may remain |
| 1 | Internal execution failure; bare invocation historical guidance |
| 2 | Invalid protocol/data/input; missing/unknown tool or unsafe path |
| 3 | Unsupported/unavailable workspace, package or environment |

Missing workspace: status reports initialized=false; inspect/validate return 3.
Doctor reports missing workspace or optional MCP as WARN, never initializes or
installs it. Malformed/partial/duplicate-key workspace manifests fail closed.
Existing init follows Core's already-exists error, never overwrites.

Doctor checks declared Python minimum, Core metadata/import, CLI entry point,
optional MCP metadata/import/compatibility/Catalog, bundled data integrity,
workspace parse/detection and filesystem readability. Each check carries
check_id, PASS/WARN/FAIL, message and evidence. No write-permission probe is used.

## Authority and limitations

`fcop.observation.workspace_status`, `inspect_object`, `validate_workspace` and
`bundled_inventory` are minimal public read-only queries over existing Core
parsers, Schema, Project inspection and rule loaders. No new state machine,
authorization decision or recovery action is introduced.

Inspect retains Core family null digest/readiness and errors; it does not invent
a digest or equate absence with completion. Validate checks observable envelopes,
canonical location/identity, directory/last-transition consistency and existing
reference rules. Unresolved weak references remain warnings, not fabricated
strong-reference failures. It does not judge work quality or consume authority.
Reads across an active writer are observations, not an atomic multi-file snapshot.

Spec reports the installed v4 Schema/rule paths and versions separately from
legacy rule versions. The v4 specification is a fixed path/revision/hash citation,
not a claim that its full text is present in a wheel. No network retrieval occurs.

The optional `fcop_mcp.catalog.get_tool_catalog(name=None)` returns fresh sorted
name/disposition rows from the MCP authoritative declaration. No copied tool
list/signatures and no server startup. Original MCP 49/12/4 remains unchanged.
