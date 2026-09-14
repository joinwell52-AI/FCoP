"""ADMIN 4.0.3 supplement: visible CLI chapters and executable self-checks."""

from __future__ import annotations

import importlib.util
import io
import os
import re
import socket
import subprocess
import sysconfig
from html.parser import HTMLParser
from pathlib import Path

import pytest

from fcop.cli._main import main

ROOT = Path(__file__).resolve().parents[2]
COMMANDS = ("init", "status", "inspect", "validate", "tools", "doctor", "version", "spec", "migrate")
SELF_CHECK = (
    "python -m pip install fcop", "fcop version", "fcop doctor",
    "fcop init --root ./my-project", "fcop status --root ./my-project",
    "fcop validate --root ./my-project", "python -m pip install fcop-mcp",
    "fcop tools", "fcop tools merge_branches --json",
)


class Visibility(HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = 0
        self.cli_visible = False

    def handle_starttag(self, tag, attrs):
        if tag == "details":
            self.details += 1
        if dict(attrs).get("id") == "cli":
            assert self.details == 0, "CLI chapter is hidden inside details"
            self.cli_visible = True

    def handle_endtag(self, tag):
        if tag == "details":
            self.details -= 1


@pytest.mark.parametrize("name", ["README.md", "README.zh.md", "fcop-README.pypi.md", "mcp/README.md"])
def test_markdown_has_visible_independent_cli_chapter(name):
    text = (ROOT / name).read_text(encoding="utf-8")
    heading = re.search(r"^## CLI(?: —|：).*?$", text, re.M)
    assert heading is not None
    prefix = text[:heading.start()]
    assert len(re.findall(r"<details\b", prefix)) == prefix.count("</details>")
    rest = text[heading.end():]
    section = re.split(r"\n## ", rest, maxsplit=1)[0]
    assert "CLI = Setup + Observe + Diagnose" in section and "MCP = Work" in section
    for command in COMMANDS:
        assert f"| `fcop {command}` |" in section
    for line in SELF_CHECK:
        assert line in section
    assert "<project>/fcop/" in section
    assert "不联网、不修改 Host" in section or "does not access the network or modify Host" in section


@pytest.mark.parametrize("name", ["scripts/pages/index.template.html", "docs/index.html"])
def test_homepage_cli_is_not_collapsed(name):
    text = (ROOT / name).read_text(encoding="utf-8")
    parser = Visibility()
    parser.feed(text)
    assert parser.cli_visible
    for command in COMMANDS:
        assert f"<code>fcop {command}</code>" in text
    for line in SELF_CHECK:
        assert line in text
    assert "CLI — Local Setup, Inspect &amp; Diagnose" in text
    assert "CLI：本地安装、检查与诊断" in text


def test_doctor_is_offline_and_customer_root_readonly(tmp_path, monkeypatch):
    (tmp_path / "AGENTS.md").write_bytes(b"Customer only\xff\r\n")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}

    def forbidden(*args, **kwargs):
        raise AssertionError("doctor must not open a network connection or launch a subprocess")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    output = io.StringIO()
    assert main(["doctor", "--root", str(tmp_path), "--json"], stdout=output) == 0, output.getvalue()
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before


def test_visible_self_check_commands_execute_in_fresh_customer_directory(tmp_path):
    root = tmp_path / "my-project"
    executable = Path(sysconfig.get_path("scripts")) / ("fcop.exe" if os.name == "nt" else "fcop")
    assert executable.is_file(), "Test the installed public console entry point"
    for args in (
        ["version"], ["doctor"], ["init", "--root", str(root)],
        ["status", "--root", str(root)], ["validate", "--root", str(root)],
        ["tools"], ["tools", "merge_branches", "--json"],
    ):
        result = subprocess.run([str(executable), *args], cwd=tmp_path,
                                capture_output=True, text=True, encoding="utf-8", timeout=45)
        expected = 3 if args[0] == "tools" and importlib.util.find_spec("fcop_mcp") is None else 0
        assert result.returncode == expected, (args, result.stdout, result.stderr)
    assert {p.name for p in tmp_path.iterdir()} == {"my-project"}
    assert {p.name for p in root.iterdir()} == {"fcop"}
