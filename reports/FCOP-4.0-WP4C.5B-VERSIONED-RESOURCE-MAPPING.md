# WP4C.5B Versioned Resource Mapping

## Scope and result

WP4C.5b resolves representation without changing the frozen protocol or legacy
Markdown. The exact fixture correction is commit
76ebfc6fedf9b55b436e866b7c80f532423cfd3c. Only the version condition changes;
all inner assertions and eight DIST-24 nodes remain. Authority is the fixed
[WP4C.5b taskbook](https://github.com/joinwell52-AI/FCoP/blob/a6f3ce278977b7121700de76ea6d832fe518533f/taskbooks/fcop-4.0/WP4C.5b/01-V3-Protocol-Representation-Boundary-and-WP4C.5-Resume-Taskbook-v1.0.zh.md).

| URI | v3 Project / MCP | v4 Project / MCP | MCP MIME |
|---|---|---|---|
| fcop://rules | original get_rules string / exact same text | validated Manifest dict / full sorted JSON in Markdown code block | text/markdown |
| fcop://protocol | original get_protocol_commentary string / exact same text | fixed identity dict / title, then path, revision, sha256 fields | text/markdown |
| fcop://team | existing get_available_teams source / JSON | available=false and stable reason / JSON | application/json |
| fcop://guidance/{assembly}/{language} | sequential/en only, original rules string | sequential or parallel, en or zh; validated raw modules in load_order | text/markdown |

The unchanged `fcop://teams` catalog and three older Profile templates remain
separate. A v4 unavailable team result does not erase that existing catalog or
turn fixed roles into Core. Repository-development is not a default business
guidance URI. Unknown spelling, escaped URI, query fields, assembly/language,
network request, executable field or conflicting selection is rejected.

## Source and representation ownership

`src/fcop/v4/rule_distribution/_read.py` owns resource semantics and reuses
the accepted loader, selection, SHA and receipt readers. Project version
binding remains authoritative. It validates all eighteen artifact records and
raw bytes, then rechecks the Manifest and artifacts for observable read drift.
No cache, Registry, alternate specification body or remote source is introduced.

The v4 specification citation is `spec/fcop-4.0-spec.md` at
aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, 26218 bytes, SHA-256
0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9.
A source checkout also verifies those actual bytes. An installed wheel returns
the same immutable citation without reading a second MCP specification copy or
needing repository/network access.

`mcp/src/fcop_mcp/resources.py` calls Project once, then performs only a pure
representation. Its renderer does not select modules, load a Manifest, call a
legacy rules getter, classify versions, read a spec or compute a source digest.
The older independent `fcop://spec` projection is untouched. No new adapter
algorithm is concealed behind that pre-existing resource.

Rules Markdown is losslessly reversible to every Manifest field: four top-level
fields, eighteen artifact records, eleven fields in each record. This is not
an eleven-top-level-field Manifest. Protocol Markdown field order is fixed;
there is no time, absolute machine path, Host state or Runtime-consumption flag.

## Real transport and compatibility tests

`tests/test_fcop_mcp/test_wp4c5_resources.py` exercises real Project, FastMCP
direct calls, Client in-process calls and the existing `run_relay` JSON-RPC
handler. Only the external WebSocket connector is replaced by memory queues;
the actual Relay framing and server handlers run. No listener or network
connection is started for this parity test. Both versions and all four resource
kinds compare exact bytes and MIME, with workspace before/after snapshots.

New tests also spy on, but do not replace, the real Project call; require exactly
one read; reject invalid workspace declarations; and lock the old URI/MIME
surface. No mocked successful semantic result is used.

A discovered integration issue was corrected before delivery: FastMCP template
registration advertised Markdown, but a plain string template response acquired
text/plain on read. Returning the framework's explicit ResourceResult with a
Markdown ResourceContent fixes both direct and Relay MIME, without changing
the semantic reader or weakening the exact assertion. The 15-test independent
MCP resource suite passed after correction.

A second real transport finding was also closed: template matching discarded
query fields, and the SDK passed only uri to FastMCP while dropping extra RPC
parameters. A shared, distribution-resource-only parameter guard now runs at
both existing entry boundaries before this loss. It rejects query/fragment
and additional action fields; the existing SDK handler still owns dispatch.
It neither classifies workspace versions nor computes any resource semantics.
Five URI-injection and four actual RPC-extra-field tests retain their rejection
assertions. The independent suite is now 24 tests; final MCP full regression
passed 158/158, with Ruff and all 29 MCP source/test files passing mypy.

Final public surface is 46 tools, 12 static resources, 4 templates. Only the
current `tool_surface_v4.json` snapshot receives the two additions; historical
45/11/3 evidence and its snapshot remain unchanged. The existing installed-wheel
probe now expects 46/12/4 and additionally verifies five packaged Project/stdio
resource results and zero workspace writes. Final suite/artifact evidence is
recorded in the companion RESULT and delivery Manifest.
