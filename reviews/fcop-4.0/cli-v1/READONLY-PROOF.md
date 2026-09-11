# CLI v1 filesystem no-write evidence

test_readonly_matrix runs seven observation commands × four workspace states
(empty, legacy v3, v4, invalid) × JSON/human rendering = 56 nodes.
Each compares the complete fixture tree/content snapshot before and after.
The root includes spaces and Chinese characters on native Windows.

Additional assertions cover invalid flags, escaping paths, partial initialization,
invalid/duplicate UTF-8 JSON declarations, exact REPORT replacement head, legacy
TASK validation and real subprocess JSON. Init writes only the requested Core
workspace: no TASK, AGENTS.md or .cursor configuration. Repeated init is rejected
with an identical snapshot. No validation repair is attempted.

scripts/cli_v1_installed_probe.py independently repeats byte/tree comparison
from installed distributions outside the repository using python -I -B.
It checks empty and initialized workspace reads, actual console entrypoint,
Core-only unavailable MCP output, and (when installed) stdio discovery.

No source changes under src/fcop/v4, spec, tests/conformance or retained public
surface snapshots. No CodeFlowMu, original dogfood, rule or Host changes.
