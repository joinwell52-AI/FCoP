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
    from fcop_mcp._version import __version__
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--root", help="Immutable workspace root selected by the host")
    parser.add_argument("--relay-url", help="Explicit foreground MCP WebSocket endpoint")
    args = parser.parse_args(argv)
    import os
    from pathlib import Path

    from fcop_mcp.registry import create_server
    mcp = create_server(args.root or os.environ.get("FCOP_PROJECT_DIR", Path.cwd()))

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
