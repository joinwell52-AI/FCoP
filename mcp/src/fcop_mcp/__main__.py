"""``python -m fcop_mcp`` entry point.

Also installed as the ``fcop-mcp`` console script via
``mcp/pyproject.toml``'s ``[project.scripts]`` table.

The only responsibility of this module is to start the FastMCP server
over stdio. Configuration discovery (``FCOP_PROJECT_DIR`` / relay
credentials) and tool registration happen inside
:mod:`fcop_mcp.server` so this file stays trivially testable.
"""

from __future__ import annotations

import sys


def main() -> int:
    """Boot the FastMCP stdio server.

    Returns the process exit code, so callers that want to wrap this
    (tests, supervisors, custom launchers) can do so without relying
    on ``sys.exit`` side effects.
    """
    from fcop_mcp.server import mcp

    mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
