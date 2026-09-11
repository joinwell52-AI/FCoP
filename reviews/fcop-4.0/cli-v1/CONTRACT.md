# CLI v1 contract and implementation boundary

The pre-code contract is reports/FCOP-4.0-CLI-V1-CONTRACT.md.
CLI = Setup + Observe + Diagnose; MCP = Work.

Nine commands: init, status, inspect, validate, tools, doctor, version, spec,
migrate. Historical migrate-workspace and bare fcop remain compatible.
New observations use a stable schema_version=1 JSON result; exits 0/1/2/3
distinguish success, internal failure, invalid input/data, unavailable.
Human rendering uses the same data. Parser errors remain stderr/2.

Only explicit init or existing migration apply writes workspace state.
There are no work-tool aliases, evaluators, repair flags or background tasks.
fcop.observation is a public minimal read-only Core aggregation. It reuses
existing readers, parsers, relation validation and report-head resolution.
It does not alter Project signatures, lifecycle, merge, recovery or authority.

MCP get_tool_catalog() returns fresh sorted name/disposition rows from the
registration declarations. The three existing Branch declarations join that
table; the legacy wrapper skips them, preserving their existing registration.
No server start, copied signature schema or CLI-maintained tool list is involved.

Limits: multi-file observations are not atomic across concurrent writers.
Validation is limited to existing observable Core checks, not task quality.
Catalog does not invent unavailable description/signature fields. spec reports
the frozen specification identity/citation separately from actual bundled files.
Absence of a REPORT is an explicit warning/null head; unready family state remains
the existing Core null digest and structured readiness evidence.
