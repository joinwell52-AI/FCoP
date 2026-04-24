"""Compat CLI for 0.5.x → 0.6.x migration.

Historically (``fcop`` 0.5.x) this console script started the FCoP MCP
server. Starting with 0.6.0 the server lives in a separate package,
``fcop-mcp`` (see ADR-0002). To avoid leaving 0.5.x users with a bare
``command not found`` after ``pip install --upgrade fcop``, the ``fcop``
wheel still ships a ``fcop`` entry point, but it only prints a migration
message and exits with a non-zero status.

This module is an **implementation detail**. It is not part of the
``fcop`` public API tracked by ADR-0001, and nothing in :mod:`fcop`
should import from here. The contract enforced by tests is only:

* the ``fcop`` console script exists,
* invoking it prints a message mentioning ``fcop-mcp``,
* the process exits with status 1.

Re-homing or renaming this module in a later minor is allowed.
"""

from __future__ import annotations

import sys

_MESSAGE = """\
fcop 0.6+ is a pure Python library. The MCP server moved to a separate
package called fcop-mcp.

To get the MCP server back, run one of:

    pip install fcop-mcp          # then: fcop-mcp
    uvx fcop-mcp                  # or zero-install via uv

Cursor / Claude Desktop MCP config (update your old entry):

    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }

Migration guide:
    https://github.com/joinwell52-AI/FCoP/blob/main/docs/MIGRATION-0.6.md

If you wanted the library (no MCP), you already have it — just `import fcop`.
"""


def main(argv: list[str] | None = None) -> int:
    """Print migration guidance and return exit code 1.

    Accepts ``argv`` purely so tests can exercise the function without
    monkey-patching ``sys.argv``. Real callers (the ``fcop`` console
    entry point) do not pass anything.
    """

    # argv is accepted so tests (and future options like --version /
    # --silent) can tweak behavior. Today it's unused on purpose.
    _ = argv

    # Always write to stderr so the message survives pipes / redirects
    # from users who were scripting against the old MCP server's stdout.
    print(_MESSAGE, file=sys.stderr, end="")
    return 1


if __name__ == "__main__":  # pragma: no cover - manual invocation
    sys.exit(main(sys.argv[1:]))
