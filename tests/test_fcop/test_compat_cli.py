"""Tests for :mod:`fcop._compat_cli`.

The compat CLI is a migration shim for users upgrading from ``fcop``
0.5.x (when the package was an MCP server) to ``fcop`` 0.6.x (when it
is a pure library and the MCP server lives in the separate
``fcop-mcp`` package). The shim is pure CLI plumbing with no library
behavior, so the contract is small:

    1. Calling :func:`fcop._compat_cli.main` prints a migration message
       to **stderr** and returns exit code ``1``.
    2. The message names ``fcop-mcp`` so users can find the new package
       from a copy-pasted error.
    3. The message points at the migration guide URL in the repo.
    4. The ``fcop`` console script declared in ``pyproject.toml``
       resolves to :func:`fcop._compat_cli.main`.

This module is **not** part of the public API (ADR-0001), so we don't
add it to the ``test_public_surface.py`` snapshot.
"""

from __future__ import annotations

import importlib.metadata
import sys

import pytest


def test_main_returns_exit_code_one(capsys: pytest.CaptureFixture[str]) -> None:
    """``main()`` must return 1 so callers can detect the shim."""

    from fcop._compat_cli import main

    assert main() == 1
    captured = capsys.readouterr()
    # Message goes to stderr so pipes from old MCP-era scripts don't
    # mistake it for protocol output on stdout.
    assert captured.out == ""
    assert captured.err != ""


def test_main_message_mentions_fcop_mcp(capsys: pytest.CaptureFixture[str]) -> None:
    """Users grepping the error for 'fcop-mcp' must find it."""

    from fcop._compat_cli import main

    main()
    err = capsys.readouterr().err
    assert "fcop-mcp" in err
    # Both the pip install form and the uvx form should be mentioned so
    # users on either flow can self-serve.
    assert "pip install fcop-mcp" in err
    assert "uvx fcop-mcp" in err


def test_main_message_links_migration_guide(capsys: pytest.CaptureFixture[str]) -> None:
    """Link to the migration guide makes the shim actionable."""

    from fcop._compat_cli import main

    main()
    err = capsys.readouterr().err
    assert "MIGRATION-0.6.md" in err


def test_main_accepts_argv(capsys: pytest.CaptureFixture[str]) -> None:
    """``main(argv)`` signature is stable so future flags can be added."""

    from fcop._compat_cli import main

    # Shouldn't raise or change behavior in 0.6.1 — argv is accepted
    # purely to keep the door open for future ``--version`` / ``--silent``.
    assert main(["--anything"]) == 1
    assert main([]) == 1
    assert capsys.readouterr().err != ""


@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="requires entry_points(group=...) keyword (3.10+)",
)
def test_console_script_resolves_to_compat_cli() -> None:
    """The ``fcop`` console script in the installed wheel must point at
    :func:`fcop._compat_cli.main`.

    This runs only after ``pip install`` (editable or wheel) so that
    ``importlib.metadata`` can see the entry-point table.
    """

    entry_points = importlib.metadata.entry_points(group="console_scripts")
    matches = [ep for ep in entry_points if ep.name == "fcop"]
    if not matches:
        pytest.skip("fcop console script not installed (editable install required)")
    ep = matches[0]
    assert ep.value == "fcop._compat_cli:main", (
        f"expected fcop._compat_cli:main, got {ep.value}"
    )
