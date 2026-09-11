# MCP catalog equality and compatibility

Authoritative declaration: mcp/src/fcop_mcp/disposition.py.
Public query: fcop_mcp.catalog.get_tool_catalog(name=None).
CLI uses optional discovery; Core has no new MCP runtime dependency.

test_catalog_cli_stdio_registry_equality compares:
1. set(disposition.TOOLS)
2. names returned by the public catalog
3. names returned by fcop tools --json
4. actual MCP stdio tools/list

Observed count: 49; the test derives expected membership from declarations,
not a duplicated 49-name list. Retained tool surface snapshot checks parameters
and types. Branch register_branch_tools remains the actual existing registrar.
The only declaration additions are create_branch, inspect_family, merge_branches.

test_catalog_does_not_import_runtime_and_returns_fresh_rows verifies in a
separate process that catalog access imports neither fastmcp nor server, and
returned mutable rows cannot mutate later results. Unknown names are invalid.
Core-only tools reports installed=false and exit 3 without import crashes.

No work tool, resource or template was added, removed or changed.
