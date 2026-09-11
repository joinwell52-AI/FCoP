"""Thin argparse Setup/Observe/Diagnose projection. No work-tool dispatch."""
from __future__ import annotations

import argparse
import dataclasses
import importlib
import json
import os
import platform
import sys
from datetime import date, datetime
from enum import Enum
from importlib import metadata
from pathlib import Path
from typing import IO, Any

from fcop import Project, __version__
from fcop.errors import FcopError
from fcop.observation import bundled_inventory, inspect_object, validate_workspace, workspace_status

_COMMANDS = {
    "init": "Create a protocol workspace through Core (writes only on explicit invocation).",
    "status": "Observe workspace identity, version and layout without writes.",
    "inspect": "Inspect a TASK ID or envelope path through Core.",
    "validate": "Validate observable workspace/envelope facts; never repair.",
    "tools": "Read the optional MCP Tool Catalog; no server is started.",
    "doctor": "Diagnose installation and workspace; never repair or download.",
    "version": "Show installed package, protocol and Python versions.",
    "spec": "Locate installed schemas/rules and the frozen spec citation offline.",
}


def add_subparsers(sub: Any) -> None:
    for name, description in _COMMANDS.items():
        parser = sub.add_parser(name, help=description, description=description)
        parser.add_argument("--json", action="store_true", help="Emit one stable JSON result.")
        if name in {"init", "status", "inspect", "validate", "doctor"}:
            parser.add_argument("--root", type=Path, default=None, help="Project root (default cwd).")
        if name == "init":
            parser.add_argument("--protocol", default=None, help="Installed Core protocol (default).")
        if name == "inspect":
            target = parser.add_mutually_exclusive_group(required=True)
            target.add_argument("task_id", nargs="?")
            target.add_argument("--path", type=Path)
        if name == "validate":
            parser.add_argument("--path", type=Path)
        if name == "tools":
            parser.add_argument("tool_name", nargs="?")
        parser.set_defaults(func=dispatch)


def _json_default(value: Any) -> Any:
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return dataclasses.asdict(value)
    if isinstance(value, (Path, datetime, date)):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    raise TypeError(f"Unsupported output type: {type(value).__name__}")


def _mcp() -> dict[str, Any]:
    try:
        package = metadata.distribution("fcop-mcp")
    except metadata.PackageNotFoundError:
        return {"installed": False, "version": None}
    return {"installed": True, "version": package.version}


def _tools(name: str | None = None) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {"core_version": __version__, "mcp": _mcp(), "tools": [], "total": 0}
    if not result["mcp"]["installed"]:
        result["message"] = "fcop-mcp: not installed"
        return result, 3
    module = importlib.import_module("fcop_mcp.catalog")
    rows = module.get_tool_catalog(name)
    result.update(tools=rows, total=len(module.get_tool_catalog()))
    return result, 0


def _doctor(root: Path) -> tuple[dict[str, Any], int]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, action: Any, *, unavailable_warn: bool = False) -> None:
        try:
            evidence = action()
            checks.append(dict(check_id=check_id, status="PASS", message="Verified", evidence=evidence))
        except (ImportError, metadata.PackageNotFoundError) as exc:
            checks.append(dict(check_id=check_id, status="WARN" if unavailable_warn else "FAIL",
                               message=str(exc), evidence={"exception": type(exc).__name__}))
        except Exception as exc:
            checks.append(dict(check_id=check_id, status="FAIL", message=str(exc),
                               evidence={"exception": type(exc).__name__}))

    def runtime() -> dict[str, Any]:
        # The package currently declares a single >=major.minor minimum. Read it
        # from metadata; do not silently accept a future unsupported expression.
        requires = metadata.metadata("fcop")["Requires-Python"]
        import re

        match = re.fullmatch(r">=(\d+)\.(\d+)", requires or "")
        if not match:
            raise ValueError("Unsupported Requires-Python declaration for runtime check")
        if sys.version_info[:2] < tuple(map(int, match.groups())):
            raise ValueError("Python does not meet installed Requires-Python")
        return {"python": platform.python_version(), "requires_python": requires}

    check("python-runtime", runtime)
    check("core-package", lambda: {"version": metadata.version("fcop"), "import_version": __version__})

    def entrypoint() -> str:
        entries = [e for e in metadata.distribution("fcop").entry_points
                   if e.group == "console_scripts" and e.name == "fcop"]
        if len(entries) != 1 or not callable(entries[0].load()):
            raise ValueError("Missing/broken fcop entry point")
        return entries[0].value

    check("cli-entry-point", entrypoint)
    info = _mcp()
    checks.append(dict(check_id="mcp-installed", status="PASS" if info["installed"] else "WARN",
                       message="Installed" if info["installed"] else "fcop-mcp: not installed", evidence=info))
    if info["installed"]:
        check("mcp-import", lambda: importlib.import_module("fcop_mcp").__name__)
        check("package-compatibility", lambda: importlib.import_module(
            "fcop_mcp.routing").check_package_compatibility())
        check("mcp-catalog", lambda: _tools()[0])
    else:
        for name in ("mcp-import", "package-compatibility", "mcp-catalog"):
            checks.append(dict(check_id=name, status="WARN", message="Optional MCP unavailable", evidence=info))
    check("bundled-schema-rules-spec", bundled_inventory)
    check("workspace-config", lambda: workspace_status(root))
    if not (root / "fcop/fcop.json").exists() and not (root / "docs/agents/fcop.json").exists():
        checks.append(dict(check_id="workspace-detection", status="WARN", message="Not initialized",
                           evidence={"root": str(root)}))
    else:
        checks.append(dict(check_id="workspace-detection", status="PASS", message="Manifest exists",
                           evidence={"root": str(root)}))

    def readable() -> dict[str, Any]:
        if not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
            raise OSError("Project root is absent or unreadable")
        return {"root": str(root), "readable": True, "write_probe_performed": False}

    check("filesystem-readability", readable)
    return {"checks": checks}, 2 if any(c["status"] == "FAIL" for c in checks) else 0


def _run(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    root = (getattr(args, "root", None) or Path.cwd()).resolve()
    if args.cmd == "init":
        return Project(root).create_workspace(
            protocol_version=args.protocol or bundled_inventory()["protocol_version"]), 0
    if args.cmd == "status":
        return workspace_status(root), 0
    if args.cmd == "inspect":
        return inspect_object(root, task_id=args.task_id, path=args.path), 0
    if args.cmd == "validate":
        result = validate_workspace(root, path=args.path)
        return result, 0 if result["valid"] else 2
    if args.cmd == "tools":
        return _tools(args.tool_name)
    if args.cmd == "doctor":
        return _doctor(root)
    if args.cmd == "version":
        return {"core_version": __version__, "mcp": _mcp(), "python": platform.python_version(),
                "protocol_version": bundled_inventory()["protocol_version"]}, 0
    if args.cmd == "spec":
        return bundled_inventory(), 0
    raise ValueError("Unknown observation command")


def dispatch(args: argparse.Namespace, *, stdout: IO[str] | None = None) -> int:
    out = stdout or sys.stdout
    result: dict[str, Any] = {"schema_version": 1, "command": args.cmd, "status": "ok",
                              "data": None, "errors": [], "warnings": []}
    try:
        result["data"], code = _run(args)
        result["warnings"] = result["data"].get("warnings", [])
    except (ImportError, metadata.PackageNotFoundError, FileNotFoundError) as exc:
        code = 3
        result["errors"] = [{"code": type(exc).__name__, "message": str(exc)}]
    except (FcopError, ValueError, KeyError, OSError) as exc:
        code = 2
        if str(getattr(exc, "code", "")).startswith("UNSUPPORTED_"):
            code = 3
        result["errors"] = [{"code": str(getattr(exc, "code", type(exc).__name__)), "message": str(exc)}]
    except Exception as exc:
        code = 1
        result["errors"] = [{"code": type(exc).__name__, "message": str(exc)}]
    result["status"] = {0: "ok", 1: "error", 2: "invalid", 3: "unavailable"}[code]
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, default=_json_default,
                      allow_nan=False, indent=None if args.json else 2)
    out.write(("" if args.json else f"FCoP {args.cmd}: {result['status']}\n") + text + "\n")
    return code
