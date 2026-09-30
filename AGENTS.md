# FCoP source repository

- This repository develops the FCoP Python library and its optional MCP adapter.
- Core is the sole authority for protocol facts, validation and state transitions.
- Canonical MCP is a thin Core adapter; its manifest owns the exposed tool surface.
- Keep Runtime, CodeFlowMu, Profile presets, Host configuration and Legacy compatibility outside Base Protocol.
- Preserve existing user changes. Use UTF-8; do not edit Chinese text with PowerShell.
- Source: `src/fcop/`; MCP: `mcp/src/fcop_mcp/`; tests: `tests/`.
- Run relevant tests with `python -m pytest`; run lint with `python -m ruff check`.
- Local package builds use `python -m build` at the repository root and in `mcp/`.
- Validate local wheels in a clean environment before claiming release-candidate readiness.
- Do not automatically publish packages, upload to PyPI, create tags or Releases, or merge changes.
