"""WP4C.6 real public actions: archives, pure measurements and zero effects."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tarfile
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from fcop import Project
from fcop.errors import FcopError

from .test_v4_rule_distribution import distribution as distribution
from .test_v4_rule_distribution import snapshot


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def artifact_request(distribution, output="output", **changes):
    return {
        **distribution[1], "output_directory": str(distribution[3].parent / output),
        "formats": ["wheel", "sdist"], "offline": True, "build_isolation": False, **changes,
    }


def measure_request(distribution):
    historical = []
    for n in range(6):
        path = distribution[3].parent / f"historical-{n}.md"
        # Historical bytes need not be canonical UTF-8/LF rule-module bytes.
        raw = ("历史 / history\r\n" * (n + 1)).encode()
        path.write_bytes(raw)
        historical.append({"path": str(path), "sha256": digest(raw)})
    return {**distribution[1], "historical_surfaces": historical}


def reject_unchanged(distribution, action, request, category=None):
    before = snapshot(distribution[3].parent)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action=action, request=request)
    assert caught.value.code.startswith("toolkit:")
    if category:
        assert caught.value.code == "toolkit:" + category
    assert snapshot(distribution[3].parent) == before


def archive_members(path):
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            assert archive.namelist() == sorted(archive.namelist())
            assert len(set(archive.namelist())) == len(archive.namelist())
            assert all(m.date_time == (1980, 1, 1, 0, 0, 0) for m in archive.infolist())
            return {name: archive.read(name) for name in archive.namelist()}
    with tarfile.open(path) as archive:
        members = archive.getmembers()
        assert [m.name for m in members] == sorted(m.name for m in members)
        assert all(m.isfile() and m.mtime == 0 and m.uid == m.gid == 0 for m in members)
        return {m.name: archive.extractfile(m).read() for m in members}


def test_exports_exact_bytes_repeat_and_no_workspace_effects(distribution):
    expected = {p.name: p.read_bytes() for p in distribution[2].iterdir()}
    workspace = snapshot(distribution[3])
    results = []
    for directory in ("first", "second"):
        result = distribution[0].rule_distribution(
            action="build_artifacts", request=artifact_request(distribution, directory)
        )
        assert result["member_count"] == 19 and result["offline"] is True
        assert result["manifest_sha256"] == digest(expected["manifest.json"])
        assert set(result["artifacts"]) == {"wheel", "sdist"}
        hashes = {}
        for kind, value in result["artifacts"].items():
            path = Path(value)
            assert path.is_absolute() and path.is_file()
            members = archive_members(path)
            prefix = "fcop/rules/_data/v4/"
            actual = {n.split(prefix, 1)[1]: raw for n, raw in members.items() if prefix in n}
            assert actual == expected and len(actual) == 19
            assert not any(n.endswith(("AGENTS.md", "CLAUDE.md", "fcop-v4.mdc")) for n in members)
            assert not any("receipt" in n or "rule-distribution/" in n for n in members)
            assert not any(str(distribution[3].parent).encode() in raw for raw in members.values())
            assert not any(b"v1.0-rc.1" in raw for raw in members.values())
            hashes[kind] = digest(path.read_bytes())
        results.append(hashes)
    assert results[0] == results[1]
    assert snapshot(distribution[3]) == workspace


@pytest.mark.parametrize("change", [
    {"formats": []}, {"formats": ["wheel", "wheel"]}, {"formats": ["exe"]},
    {"formats": "wheel"}, {"formats": [None]}, {"offline": False}, {"offline": 1},
    {"build_isolation": True}, {"build_isolation": 0}, {"network": False},
    {"output_directory": "relative"}, {"output_directory": "//server/share/output"},
])
def test_export_invalid_request_is_zero_effect(distribution, change):
    reject_unchanged(distribution, "build_artifacts", artifact_request(distribution, **change))


@pytest.mark.parametrize("key", ["formats", "offline", "build_isolation", "output_directory"])
def test_export_missing_explicit_input(distribution, key):
    request = artifact_request(distribution)
    del request[key]
    reject_unchanged(distribution, "build_artifacts", request)


@pytest.mark.parametrize("target", ["workspace", "workspace/inside", "package", "package/inside", ".", "occupied"])
def test_export_output_ownership(distribution, target):
    if target == "occupied":
        occupied = distribution[3].parent / target
        occupied.mkdir()
        (occupied / "sentinel").write_bytes(b"user data\n")
    reject_unchanged(distribution, "build_artifacts", artifact_request(distribution, target), "RULE_OWNERSHIP_CONFLICT")


@pytest.mark.parametrize("file", ["manifest.json", "convergence.zh.md"])
def test_export_complete_input_drift_before_output(distribution, file):
    target = distribution[2] / file
    target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
    reject_unchanged(distribution, "build_artifacts", artifact_request(distribution))








@pytest.mark.parametrize("action", ["build_artifacts", "measure_context"])
def test_reparse_boundary_rejected(distribution, monkeypatch, action):
    request = artifact_request(distribution) if action == "build_artifacts" else measure_request(distribution)
    target = Path(request["output_directory"]) if action == "build_artifacts" else Path(request["historical_surfaces"][0]["path"])
    original = Path.lstat

    def reparse(path, *args, **kwargs):
        if path == target:
            return SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", reparse)
    reject_unchanged(distribution, action, request)




@pytest.mark.parametrize("action", ["build_artifacts", "measure_context"])
def test_legacy_actions_fail_closed(distribution, action):
    request = artifact_request(distribution) if action == "build_artifacts" else measure_request(distribution)
    root = distribution[3]
    (root / "fcop/fcop.json").write_bytes(b'{"protocol":"fcop","protocol_version":"3.0"}\r\n')
    legacy = (Project(root), *distribution[1:])
    reject_unchanged(legacy, action, request)




@pytest.mark.parametrize("action", ["build_artifacts", "measure_context"])
def test_actions_never_call_network_or_shell(distribution, monkeypatch, action):
    import socket
    import subprocess

    def forbidden(*args, **kwargs):
        raise AssertionError("No network or shell is authorized")

    request = artifact_request(distribution) if action == "build_artifacts" else measure_request(distribution)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(os, "system", forbidden)
    if action == "measure_context":
        reject_unchanged(distribution, action, request, "OPERATION_NOT_IMPLEMENTED")
    else:
        result = distribution[0].rule_distribution(action=action, request=request)
        assert result is not None


def test_mcp_accepted_snapshot_remains_46_12_4():
    # Preserve the accepted 4.0.0 surface; current additive 49-tool comparison
    # is enforced separately by test_all_46_existing_tool_signatures_unchanged.
    path = Path(__file__).resolve().parents[1] / "test_fcop_mcp/snapshots/tool_surface_4_0_0.json"
    surface = json.loads(path.read_bytes())
    assert len(surface["tools"]) == 46
    assert len(surface["resources"]["static"]) == 12
    assert len(surface["resources"]["templates"]) == 4
