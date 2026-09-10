"""``python -m fcop_mcp`` entry point.

Also installed as the ``fcop-mcp`` console script via
``mcp/pyproject.toml``'s ``[project.scripts]`` table.

The only responsibility of this module is to start the FastMCP server
over stdio by default. Workspace configuration (``FCOP_PROJECT_DIR``)
and tool registration happen inside
:mod:`fcop_mcp.server`. Relay is selected only with the explicit
``--relay-url`` argument, never by workspace files or environment discovery.
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    """Boot the FastMCP stdio server.

    Returns the process exit code, so callers that want to wrap this
    (tests, supervisors, custom launchers) can do so without relying
    on ``sys.exit`` side effects.
    """
    parser = argparse.ArgumentParser(description="FCoP MCP stdio adapter; Relay is explicitly optional")
    parser.add_argument("--relay-url", help="Explicit foreground MCP WebSocket endpoint")
    args = parser.parse_args(argv)
    from fcop_mcp.server import mcp

    if args.relay_url is not None:
        import asyncio

        from fcop_mcp.relay import run_relay

        asyncio.run(run_relay(mcp, args.relay_url))
    else:
        # The SDK banner can perform a PyPI update check. Base stdio is offline.
        mcp.run(transport="stdio", show_banner=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
