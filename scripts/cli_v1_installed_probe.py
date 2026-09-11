"""Installed CLI/MCP smoke, run as python -I -B; never imports repository code.

Creates disposable fixture workspaces only. Suitable before/after PyPI release.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from importlib import metadata
from pathlib import Path


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            if p.is_file() else "directory" for p in sorted(root.rglob("*"))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mcp", action="store_true")
    args = parser.parse_args()
    import fcop

    assert fcop.__version__ == metadata.version("fcop") == "4.0.2"
    assert "site-packages" in str(Path(fcop.__file__).resolve())
    assert bool(importlib.util.find_spec("fcop_mcp")) == args.mcp
    executable = Path(sys.executable).parent / ("fcop.exe" if os.name == "nt" else "fcop")
    results = []
    spec_hashes = {
        "en": "fb10d1b14a678b77874012f88cf35a977d2f8517b1aa4a6fdc5a0e94546ef33d",
        "zh": "0dac91db3e38e0cf06423a0d815beaaad9c9b4d6ec06e732f1012aec0e346f40",
    }
    spec_revision = "81d3229ee602341063879fe9100ab7db92417ffe"
    with tempfile.TemporaryDirectory(prefix="fcop-cli-v1-proof-") as directory:
        root = Path(directory)
        help_result = subprocess.run([str(executable), "--help"], cwd=root,
                                     capture_output=True, encoding="utf-8", timeout=60)
        assert help_result.returncode == 0
        assert all(name in help_result.stdout for name in (
            "init", "status", "inspect", "validate", "tools", "doctor", "version", "spec", "migrate"))
        assert snapshot(root) == {}

        def call(command, *arguments, expected=0):
            before = snapshot(root)
            completed = subprocess.run([str(executable), command, *map(str, arguments), "--json"],
                                       cwd=root, capture_output=True, encoding="utf-8", timeout=60)
            assert completed.returncode == expected, (command, completed.stdout, completed.stderr)
            value = json.loads(completed.stdout)
            assert value["schema_version"] == 1 and value["command"] == command
            assert "\x1b" not in completed.stdout and not completed.stderr
            if command != "init":
                assert snapshot(root) == before, command
            results.append({"command": command, "exit": expected})
            return value["data"]

        call("status")
        call("validate", expected=3)
        call("doctor")
        call("version")
        identity = call("spec")["specification"]
        assert identity == {"path": "spec/fcop-4.0-spec.md", "revision": spec_revision,
                            "sha256": spec_hashes["en"], "bundled_text": False}
        call("init")
        project = fcop.Project(root)
        workspace_id = call("status")["workspace_id"]
        task = project.create_task(workspace_id=workspace_id, operation_id="installed-proof",
                                   sender="ME", recipient="ME", subject="Installed CLI", body="Evidence")
        assert call("inspect", task["task_id"])["task_id"] == task["task_id"]
        assert call("validate")["valid"]
        call("doctor")
        catalog = call("tools", expected=0 if args.mcp else 3)
        if args.mcp:
            from importlib.resources import files

            from fcop_mcp.catalog import get_tool_catalog
            from fcop_mcp.disposition import TOOLS
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            assert metadata.version("fcop-mcp") == "4.0.2"
            assert {r["name"] for r in catalog["tools"]} == set(TOOLS)
            assert {r["name"] for r in get_tool_catalog()} == set(TOOLS)
            environment = dict(os.environ, FCOP_PROJECT_DIR=str(root))
            environment.pop("PYTHONPATH", None)
            registry = json.loads(files("fcop_mcp").joinpath("_specs.json").read_bytes())
            for lang, expected in spec_hashes.items():
                entry = registry["v4/" + lang]
                assert entry["source_commit"] == spec_revision
                assert hashlib.sha256(entry["content"].encode()).hexdigest() == entry["sha256"] == expected
                assert "Stable · Implemented · Released" in entry["content"].splitlines()[2]

            async def verify():
                params = StdioServerParameters(command=sys.executable, args=["-I", "-B", "-m", "fcop_mcp"],
                                                env=environment, cwd=str(root))
                async with stdio_client(params) as streams, ClientSession(*streams) as session:
                    await session.initialize()
                    names = {t.name for t in (await session.list_tools()).tools}
                    assert names == set(TOOLS)
                    assert len((await session.list_resources()).resources) == 12
                    assert len((await session.list_resource_templates()).resourceTemplates) == 4
                    for lang, uri in (("en", "fcop://spec/en"), ("zh", "fcop://spec")):
                        entry = registry["v4/" + lang]
                        response = await session.read_resource(uri)
                        text = response.contents[0].text
                        expected = (
                            "> Read-only specification projection; workspace protocol: v4\n"
                            f"> Source: {entry['source_path']} @ {spec_revision}\n"
                            f"> Source payload SHA-256: {spec_hashes[lang]}\n\n{entry['content']}"
                        )
                        assert text == expected
                    return len(names)

            before = snapshot(root)
            count = asyncio.run(verify())
            assert snapshot(root) == before
        else:
            assert catalog["mcp"]["installed"] is False
            count = None
    print(json.dumps({"result": "PASS", "core": fcop.__version__, "mcp": args.mcp,
                      "tools": count, "checks": results, "import_path": fcop.__file__}))


if __name__ == "__main__":
    main()
