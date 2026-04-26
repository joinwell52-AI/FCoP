"""Single source of truth for the fcop-mcp package version.

The same string is read by ``mcp/pyproject.toml`` via hatchling's
``[tool.hatch.version].path`` directive, so bumping a release is a
one-line edit here and never in two places at once.

Versioning policy is described in adr/ADR-0002 (package split) and
adr/ADR-0003 (pre-1.0 stability charter):

* `fcop` and `fcop-mcp` release independent patch / minor versions.
* 0.6.x never breaks MCP tool shape (ADR-0003 surface lock).
* 1.0 is a one-time re-alignment point for both packages.
"""

from __future__ import annotations

__version__ = "0.6.5"
