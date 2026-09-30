# FCoP 4.0.5 MCP Boundary Refactor — verification record

Status: **MCP_BOUNDARY_REFACTOR_ACCEPTED** and
**FCoP_4_0_5_RELEASE_CANDIDATE_READY** for local artifacts only.
This is not authorization to publish, tag, or create a Release.

## Repository instruction gate

The preceding WP-1 Repository Instruction Cleanup passed. See
[`instruction-cleanup/REPOSITORY_INSTRUCTION_CLEANUP_REPORT.md`](instruction-cleanup/REPOSITORY_INSTRUCTION_CLEANUP_REPORT.md).
The default Core and MCP paths do not load `AGENTS.md`, `CLAUDE.md`, `.cursor`,
Team/Solo/ME seats, or Host sessions as protocol prerequisites. Historical
readers are reachable only through explicit compatibility imports.

During WP10 verification, the active getting-started pages were found to label
v3 Host rule projection as "canonical" and to describe `redeploy_rules()` as a
current MCP workflow. Work was paused at that finding. Both pages now label the
v3 source table as historical and identify root `AGENTS.md` as repository
developer guidance; the 4.0 setup/version guide distinguishes published 4.0.3
instructions from the local 4.0.5 `init_workspace` flow. The canonical code
path was unchanged by this documentation correction.

## Boundary implementation

- WP0: `baseline-tools.json` freezes the old 49 names, schemas, descriptions,
  implementation locations and policies.
- WP1: `canonical_tools.py` is the only default tool manifest. `registry.py`
  registers its 25 handlers and derives JSON schemas directly from signatures.
  Six read-only v4 rule resources are registered separately through Core.
- WP2–WP4: workspace inspection/validation and all TASK, Branch and envelope
  handlers delegate to Core. The default root is selected before startup.
  Pure initialization writes no Host instruction files.
- WP5–WP9: `write_task` is an opt-in forwarding shim; Profile, Toolkit, Host,
  Runtime and v3 tools are absent from default `tools/list`. Historical server
  and Project are under explicit `compatibility.v3` modules.
- WP10: reference, migration matrix, README/quickstart, changelog and both
  package versions describe the 25-tool 4.0.5 candidate.
- WP11: local wheel and sdist pairs are built. Exact filenames, SHA256 and
  member counts are in [`artifacts.json`](artifacts.json).

The supplied decision workbook is represented in [`migration-matrix.json`](migration-matrix.json):
49 distinct old names, one disposition each, 22 retained old canonical tools
plus three new workspace tools. The final taskbook overrides workbook advice
for `write_task` and `fcop_audit`.

WP0–WP11 gates: **PASS**. The 25-tool manifest, implementation registry,
generated reference, schema snapshot and installed `tools/list` agree. No
default tool switches the process root or exposes Profile, Host, Runtime,
CodeFlowMu, packaging, application scaffolding or v3 compatibility actions.

## Verification

- Full repository test suite: **2334 passed, 2 skipped**. Both skips are
  historical `docs/agents` schema checks without source files in the migrated
  repository. The focused 4.0.5 MCP boundary file: **11 passed**. The full
  MCP test suite: **172 passed**.
- Targeted Ruff checks of the new canonical boundary code and regression
  tests passed; `git diff --check` passed.
- Isolated wheel installation: [`cleanroom-proof.json`](cleanroom-proof.json).
  Installed `fcop` and `fcop-mcp` are both 4.0.5. Real stdio via installed
  `python -I -m fcop_mcp` matches all 25 names, descriptions and schemas,
  exposes six Core-backed read-only resources and no templates, initializes
  without Profile or Host files, and validates a TASK/REPORT flow.
  An installed in-process server with an explicit trusted Profile completed
  review, approval and archive.
- Isolated sdist installation: [`cleanroom-sdist-proof.json`](cleanroom-sdist-proof.json)
  repeats the same checks. The Core sdist has 192 members and excludes
  workspace-local environments. Neither environment installs CodeFlowMu or imports
  the development `src` directories. The installed CLI entrypoints report 4.0.5,
  and `fcop tools --json` reports 25 tools.

The final Windows `fcop-mcp.exe` console entrypoint passed a direct real-stdio
probe, including 25 tools, six rule resources, initialization and a TASK/REPORT
flow. `python -I -m fcop_mcp` passed independently from both wheel and sdist
installations. An earlier direct-wrapper attempt had timed out during
development; the final artifact did not reproduce that timeout.

Final wheel/sdist filenames, member counts, sizes and SHA256 hashes are in
[`artifacts.json`](artifacts.json). The 49→25 disposition matrix, canonical
snapshot and installed-version proofs are linked above or stored beside this
report. Legacy v3 Project, tool server and Host rule projection remain in
explicit compatibility modules; default Core and MCP do not require Team,
Solo, ME, seat assignment or Host session state.

No PyPI upload, tag, Release or CodeFlowMu modification was made.
