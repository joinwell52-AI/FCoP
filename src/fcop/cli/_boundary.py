"""Explicit Profile, audit and package operations; never loaded by MCP."""
import json
import subprocess
import sys
from pathlib import Path


def add_subparsers(sub):
    audit = sub.add_parser("audit", help="Validate protocol facts without repair")
    audit.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    audit.add_argument("--json", action="store_true")
    audit.set_defaults(func=run)
    profile = sub.add_parser("profile", help="Explicit Profile discovery/validation")
    profile.add_argument("action", choices=["list", "validate"])
    profile.add_argument("profile", nargs="?")
    profile.set_defaults(func=run)
    for name in ("check-update", "upgrade"):
        parser = sub.add_parser(name, help="Explicit online package operation (outside MCP)")
        parser.set_defaults(func=run)


def run(args, *, stdout=None):
    try:
        if args.cmd == "audit":
            from fcop.toolkit.audit import audit
            result = audit(args.path)
            code = 0 if result["valid"] else 2
        elif args.cmd == "profile":
            from fcop.profiles import list_profiles, load_profile
            result = list_profiles() if args.action == "list" else load_profile(args.profile or "")
            code = 0
        else:
            command = [sys.executable, "-m", "pip"]
            command += ["index", "versions", "fcop"] if args.cmd == "check-update" else ["install", "--upgrade", "fcop", "fcop-mcp"]
            return subprocess.call(command)
        print(json.dumps(result, ensure_ascii=False, indent=2), file=stdout or sys.stdout)
        return code
    except (ValueError, OSError) as exc:
        print(str(exc), file=stdout or sys.stderr)
        return 2
