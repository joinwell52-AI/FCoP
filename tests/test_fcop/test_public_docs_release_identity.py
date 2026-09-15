"""Public release surfaces must not drift behind the installed package identity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _version(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    assert match is not None
    return match.group(1)


def test_public_homepage_matches_current_core_and_mcp_release() -> None:
    core = _version("src/fcop/_version.py")
    mcp = _version("mcp/src/fcop_mcp/_version.py")
    assert core == mcp

    page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    for value in (
        f"FCoP {core}",
        f"releases/tag/v{core}",
        f"pypi.org/project/fcop/{core}/",
        f"pypi.org/project/fcop-mcp/{mcp}/",
        f'fcop=={core}',
        f'fcop-mcp=={mcp}',
        "Registry entry: 4.0.3 (checked Sep 14, 2026)",
        "注册表条目：4.0.3（核对日期：2026-09-14）",
        "Published and verified",
        "已发布并核验",
        "Zenodo v4.0.3 · DOI",
        "<strong>49</strong> tools",
        "<strong>12</strong> resources",
        "<strong>4</strong> templates",
        "10.5281/zenodo.22746175",
    ):
        assert value in page

    for command in (
        "fcop init",
        "fcop status",
        "fcop inspect",
        "fcop validate",
        "fcop tools",
        "fcop doctor",
        "fcop version",
        "fcop spec",
        "fcop migrate",
    ):
        assert command in page

    for tool in ("create_branch", "inspect_family", "merge_branches"):
        assert tool in page

    current_package = re.findall(r"Current package: ([^ <]+)", page)
    assert current_package == [core]



def test_public_entrypoints_lead_with_multi_agent_purpose() -> None:
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh.md").read_text(encoding="utf-8")
    page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    template = (ROOT / "scripts/pages/index.template.html").read_text(encoding="utf-8")

    for value in (
        "Multi-agent collaboration",
        "Files as protocol",
        "No complex infrastructure",
        "Agent governance",
        "Agents do not need to chat directly.",
        "Even when an agent is gone, the work remains.",
    ):
        assert value in readme_en

    for value in (
        "多 Agent 协作",
        "文件即协议",
        "无需复杂基础设施",
        "Agent 治理",
        "Agent 之间不需要直接聊天。",
        "即使 Agent 离开了，工作依然在那里。",
    ):
        assert value in readme_zh

    for surface in (page, template):
        for value in (
            "MULTI-AGENT COLLABORATION · FILES AS PROTOCOL",
            "Multi-agent collaboration.",
            "Files as protocol.",
            "Agent governance",
            "No database or broker required",
            "多 Agent 协作。",
            "文件即协议。",
            "Agent 治理",
            "无需数据库或消息队列",
            "Agents do not need to chat directly. The files are the protocol.",
            "Agent 无需直接聊天，文件就是协议。",
        ):
            assert value in surface

def test_official_mcp_registry_manifest_matches_current_mcp_release() -> None:
    mcp = _version("mcp/src/fcop_mcp/_version.py")
    manifest = json.loads((ROOT / "mcp/server.json").read_text(encoding="utf-8"))

    assert manifest["name"] == "io.github.joinwell52-AI/fcop"
    assert manifest["version"] == mcp
    assert manifest["packages"] == [
        {
            "registryType": "pypi",
            "identifier": "fcop-mcp",
            "version": mcp,
            "transport": {"type": "stdio"},
            "environmentVariables": [
                {
                    "name": "FCOP_PROJECT_DIR",
                    "description": (
                        "Absolute path to your project root "
                        "(optional, auto-detected if omitted)."
                    ),
                    "isRequired": False,
                    "format": "string",
                    "isSecret": False,
                }
            ],
        }
       ]
    assert manifest["description"] == (
        "Durable tasks, reports, reviews and branch convergence "
        "for multi-agent teams over local files."
    )
    assert len(manifest["description"]) <= 100
