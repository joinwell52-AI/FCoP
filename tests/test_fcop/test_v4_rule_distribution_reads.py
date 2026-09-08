"""WP4C.5b: real Project reads, byte identity and bounded authorization effects."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import FcopError
from fcop.rules import get_protocol_commentary, get_rules

from .test_v4_rule_distribution import distribution as distribution
from .test_v4_rule_distribution import snapshot
from .test_v4_rule_distribution_host import deploy, prepared


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False) + "\n").encode()


def read(distribution, uri, **extra):
    project, _, _, root = distribution
    before = snapshot(root.parent)
    try:
        return project.rule_distribution(
            action="read_resource", request={"resource_uri": uri, **extra}
        )
    finally:
        assert snapshot(root.parent) == before


@pytest.mark.parametrize("version", ["3.0", "4.0"])
@pytest.mark.parametrize(
    "uri", ["fcop://rules", "fcop://protocol", "fcop://team", "fcop://guidance/sequential/en"]
)
def test_versioned_content_and_transport(distribution, version, uri):
    _, _, package, root = distribution
    if version == "3.0":
        (root / "fcop/fcop.json").write_bytes(
            encoded({"protocol": "fcop", "protocol_version": version})
        )
        distribution = (Project(root), *distribution[1:])
    direct = read(distribution, uri, manifest_path=str(package / "manifest.json"))
    relay = read(
        distribution,
        uri,
        manifest_path=str(package / "manifest.json"),
        transport="relay-inprocess",
        network=False,
    )
    assert direct == relay
    assert direct["protocol_version"] == version and direct["resource_uri"] == uri
    if version == "3.0" and uri != "fcop://team":
        expected = get_protocol_commentary() if uri == "fcop://protocol" else get_rules()
        assert type(direct["content"]) is str
        assert direct["content"].encode() == expected.encode()
        assert direct["sha256"] == digest(expected.encode())
        assert direct["mime_type"] == "text/markdown"
    elif uri == "fcop://protocol":
        raw = (Path(__file__).resolve().parents[2] / "spec/fcop-4.0-spec.md").read_bytes()
        assert direct["content"] == {
            "path": "spec/fcop-4.0-spec.md",
            "revision": "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6",
            "sha256": digest(raw),
        }
        assert direct["sha256"] == digest(raw)
    elif version == "4.0" and uri == "fcop://rules":
        raw = (package / "manifest.json").read_bytes()
        assert direct["content"] == json.loads(raw)
        assert direct["sha256"] == digest(raw)
    elif version == "4.0" and uri == "fcop://team":
        assert direct["available"] is False and direct["reason"]


@pytest.mark.parametrize("assembly", ["sequential", "parallel"])
@pytest.mark.parametrize("language", ["en", "zh"])
def test_guidance_exact_order_and_no_development(distribution, assembly, language):
    package = distribution[2]
    result = read(
        distribution,
        f"fcop://guidance/{assembly}/{language}",
        manifest_path=str(package / "manifest.json"),
    )
    records = json.loads((package / "manifest.json").read_bytes())["artifacts"]
    chosen = sorted(
        [
            a
            for a in records
            if a["language"] == language
            and (assembly == "parallel" or a["module_id"] != "convergence")
        ],
        key=lambda a: a["load_order"],
    )
    expected = b"\n".join((package / a["source_path"]).read_bytes() for a in chosen)
    assert result["content"].encode() == expected
    assert result["sha256"] == digest(expected) and result["artifacts"] == chosen
    assert len(chosen) == (8 if assembly == "sequential" else 9)


@pytest.mark.parametrize(
    "uri",
    [
        "FCOP://rules",
        "fcop://RULES",
        "fcop://rules/",
        "fcop://rules?x=1&x=2",
        "fcop://%72ules",
        "fcop://guidance/../en",
        "fcop://guidance/sequential/fr",
        "fcop://guidance/repository-development/en",
    ],
)
def test_invalid_uri_rejects_zero_write(distribution, uri):
    with pytest.raises(FcopError) as caught:
        read(distribution, uri)
    assert caught.value.code == "toolkit:RULE_SELECTION_INVALID"


@pytest.mark.parametrize(
    "extra",
    [
        {"network": True},
        {"transport": "websocket"},
        {"deploy": False},
        {"adoption_receipt_ref": None},
        {"profile_evaluator": None},
        {"protocol_version": "3.0"},
        {"unknown": True},
    ],
)
def test_resource_requests_cannot_install_authority(distribution, extra):
    with pytest.raises(FcopError):
        read(distribution, "fcop://rules", **extra)


@pytest.mark.parametrize("kind", ["manifest", "module", "spec"])
def test_source_drift_rejects(distribution, monkeypatch, kind):
    from fcop.v4.rule_distribution import _read

    if kind == "spec":
        original = _read.external_file

        def drift(path, code, action):
            raw = original(path, code, action)
            return raw + b"drift\n" if str(path).endswith("fcop-4.0-spec.md") else raw

        monkeypatch.setattr(_read, "external_file", drift)
        uri = "fcop://protocol"
    else:
        path = distribution[2] / ("manifest.json" if kind == "manifest" else "convergence.zh.md")
        path.write_bytes(path.read_bytes() + b"drift\n")
        uri = "fcop://rules"
    with pytest.raises(FcopError):
        read(distribution, uri, manifest_path=str(distribution[2] / "manifest.json"))


def test_manifest_change_during_read_rejects(distribution, monkeypatch):
    from fcop.v4.rule_distribution import _read

    original = _read.external_file
    calls = []

    def changed(path, code, action):
        raw = original(path, code, action)
        if str(path).endswith("manifest.json"):
            calls.append(path)
            if len(calls) > 1:
                return raw + b" "
        return raw

    monkeypatch.setattr(_read, "external_file", changed)
    with pytest.raises(FcopError) as caught:
        read(distribution, "fcop://rules", manifest_path=str(distribution[2] / "manifest.json"))
    assert caught.value.code == "toolkit:RULE_ARTIFACT_MISMATCH"


def test_layers_disk_update_does_not_adopt_or_consume(distribution):
    project, request, package, root = distribution
    adopted = prepared(distribution)
    ref = deploy(distribution, adopted)
    arguments = {**request, "deployment_receipt_ref": ref}
    before = snapshot(root)
    first = project.rule_distribution(action="inspect_layers", request=arguments)
    manifest = json.loads((package / "manifest.json").read_bytes())
    manifest["package_version"] = "4.0.0-observation.2"
    (package / "manifest.json").write_bytes(encoded(manifest))
    second = Project(root).rule_distribution(action="inspect_layers", request=arguments)
    assert second["disk_manifest_sha256"] != first["disk_manifest_sha256"]
    assert second["index_manifest_sha256"] == second["disk_manifest_sha256"]
    assert second["index_invalidation_evidence"] == "uncached_current_read"
    assert second["adopted_manifest_sha256"] == first["adopted_manifest_sha256"]
    assert second["host_entry_sha256"] == first["host_entry_sha256"]
    assert second["runtime_consumption_verified"] is None and snapshot(root) == before
    (root / "AGENTS.md").write_bytes(b"user changed target\n")
    before = snapshot(root)
    drift = project.rule_distribution(action="inspect_layers", request=arguments)
    assert drift["host_entries"][0]["drifted"] is True and snapshot(root) == before
    (root / ref["path"]).write_bytes(b"{}\n")
    before = snapshot(root)
    with pytest.raises(FcopError):
        project.rule_distribution(action="inspect_layers", request=arguments)
    assert snapshot(root) == before


def shadow_case(distribution):
    downstream = distribution[3].parent / "consumer"
    downstream.mkdir()
    raw = b"fcop==3.2.5\nfcop-mcp==3.2.5\nnot-returned-secret-sentinel\n"
    (downstream / "requirements.txt").write_bytes(raw)
    auth = {
        "authorization_kind": "fcop-rule-distribution-shadow",
        "scope": "read-only",
        "downstream_kind": "fcop-consumer",
        "downstream_root": str(downstream),
        "allowed_relative_paths": ["requirements.txt"],
        "expected_sha256": {"requirements.txt": digest(raw)},
    }
    path = downstream.parent / "shadow-auth.json"
    path.write_bytes(encoded(auth))
    request = {
        "downstream_path": str(downstream),
        "deploy": False,
        "shadow_authorization_ref": {"path": str(path), "sha256": digest(path.read_bytes())},
    }
    return downstream, path, auth, request


def test_shadow_authorized_readonly_allowlist(distribution):
    downstream, _, _, request = shadow_case(distribution)
    (downstream / "excluded.txt").write_bytes(b"not authorized to read\n")
    before = snapshot(distribution[3].parent)
    result = distribution[0].rule_distribution(action="shadow", request=request)
    assert result["files"] == [
        {
            "path": "requirements.txt",
            "size_bytes": len((downstream / "requirements.txt").read_bytes()),
            "sha256": digest((downstream / "requirements.txt").read_bytes()),
            "detected_pins": ["fcop-mcp==3.2.5", "fcop==3.2.5"],
        }
    ]
    assert "secret-sentinel" not in json.dumps(result)
    assert snapshot(distribution[3].parent) == before


@pytest.mark.parametrize(
    "kind",
    [
        "missing",
        "digest",
        "scope",
        "target",
        "duplicate",
        "bom",
        "crlf",
        "unknown",
        "glob",
        "traversal",
        "too-many",
        "deploy",
    ],
)
def test_shadow_admission_zero_downstream_stat_open(distribution, monkeypatch, kind):
    downstream, path, auth, request = shadow_case(distribution)
    if kind == "scope":
        auth["scope"] = "write"
    if kind == "target":
        auth["downstream_root"] += "-different"
    if kind == "unknown":
        auth["authority"] = "ADMIN"
    if kind in {"glob", "traversal"}:
        auth["allowed_relative_paths"] = ["*.txt" if kind == "glob" else "../outside"]
    if kind == "too-many":
        auth["allowed_relative_paths"] = [f"p{i}" for i in range(17)]
    raw = encoded(auth)
    if kind == "duplicate":
        raw = raw.replace(b"{", b'{"scope":"write",', 1)
    if kind == "bom":
        raw = b"\xef\xbb\xbf" + raw
    if kind == "crlf":
        raw = raw.replace(b"\n", b"\r\n")
    path.write_bytes(raw)
    request["shadow_authorization_ref"]["sha256"] = digest(raw)
    if kind == "digest":
        request["shadow_authorization_ref"]["sha256"] = "0" * 64
    if kind == "missing":
        request["shadow_authorization_ref"] = None
    if kind == "deploy":
        request["deploy"] = True
    before = snapshot(distribution[3].parent)
    original_stat, original_open, original_scan = Path.stat, Path.open, os.scandir

    def is_downstream(value):
        return Path(str(value).removeprefix("\\\\?\\")).is_relative_to(downstream)

    def stat_guard(self, *args, **kwargs):
        assert not is_downstream(self), "unauthorized stat"
        return original_stat(self, *args, **kwargs)

    def open_guard(self, *args, **kwargs):
        assert not is_downstream(self), "unauthorized open"
        return original_open(self, *args, **kwargs)

    def scan_guard(value):
        assert not is_downstream(value), "unauthorized scan"
        return original_scan(value)

    with monkeypatch.context() as scoped:
        scoped.setattr(Path, "stat", stat_guard)
        scoped.setattr(Path, "open", open_guard)
        scoped.setattr(os, "scandir", scan_guard)
        with pytest.raises(FcopError) as caught:
            distribution[0].rule_distribution(action="shadow", request=request)
        assert caught.value.code == "toolkit:RULE_ADOPTION_REQUIRED"
    assert snapshot(distribution[3].parent) == before


def test_shadow_changed_bytes_and_symlink_rejected(distribution):
    downstream, path, auth, request = shadow_case(distribution)
    (downstream / "requirements.txt").write_bytes(b"fcop==4.0.0\n")
    with pytest.raises(FcopError):
        distribution[0].rule_distribution(action="shadow", request=request)
    link = downstream / "link.txt"
    link.symlink_to(downstream / "requirements.txt")
    auth["allowed_relative_paths"] = ["link.txt"]
    auth["expected_sha256"] = {"link.txt": digest(link.read_bytes())}
    path.write_bytes(encoded(auth))
    request["shadow_authorization_ref"]["sha256"] = digest(path.read_bytes())
    with pytest.raises(FcopError):
        distribution[0].rule_distribution(action="shadow", request=request)


@pytest.mark.parametrize("stage", ["before-downstream", "after-downstream"])
def test_shadow_authorization_changes_are_rejected(distribution, monkeypatch, stage):
    from fcop.v4.rule_distribution import _shadow

    downstream, path, _, request = shadow_case(distribution)
    original = _shadow.external_file
    reads = []

    def changing(value, code, action):
        reads.append(value)
        raw = original(value, code, action)
        count = reads.count(str(path))
        if value == str(path) and count == (2 if stage == "before-downstream" else 3):
            return raw + b"changed\n"
        return raw

    before = snapshot(distribution[3].parent)
    monkeypatch.setattr(_shadow, "external_file", changing)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="shadow", request=request)
    assert caught.value.code == "toolkit:RULE_ADOPTION_REQUIRED"
    if stage == "before-downstream":
        assert not any(Path(p).is_relative_to(downstream) for p in reads)
    assert snapshot(distribution[3].parent) == before


def test_shadow_directory_reparse_is_rejected(distribution):
    downstream, path, auth, request = shadow_case(distribution)
    junction = downstream / "indirect"
    if os.name == "nt":
        import _winapi

        _winapi.CreateJunction(str(downstream), str(junction))
    else:
        junction.symlink_to(downstream, target_is_directory=True)
    auth["allowed_relative_paths"] = ["indirect/requirements.txt"]
    auth["expected_sha256"] = {"indirect/requirements.txt": digest((downstream / "requirements.txt").read_bytes())}
    path.write_bytes(encoded(auth))
    request["shadow_authorization_ref"]["sha256"] = digest(path.read_bytes())
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="shadow", request=request)
    assert caught.value.code == "toolkit:RULE_ADOPTION_REQUIRED"
