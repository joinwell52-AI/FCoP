"""Independent unit checks for bundled data, strict reads and stage isolation."""

from __future__ import annotations

import hashlib
import inspect
import json
import shutil
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import FcopError, V4ProtocolError

DATA = Path(__file__).resolve().parents[2] / "src/fcop/rules/_data/v4"
MODULES = ["workspace", "envelopes", "relations", "authorization", "idempotency", "recovery", "lifecycle", "compatibility"]


@pytest.fixture
def distribution(tmp_path):
    root = tmp_path / "workspace"
    (root / "fcop").mkdir(parents=True)
    declaration = {
        "protocol": "fcop", "protocol_version": "4.0",
        "workspace_id": "urn:uuid:00000000-0000-4000-8000-000000000042",
        "encoding": {"name": "fcop-filesystem", "version": "4.0"}, "profiles": [],
    }
    (root / "fcop/fcop.json").write_bytes((json.dumps(declaration) + "\n").encode())
    package = tmp_path / "package"
    shutil.copytree(DATA, package)
    profile = tmp_path / "profile.json"
    profile.write_bytes((json.dumps({
        "host_id": "codex", "profile_version": "1.0-candidate.1",
        "supported_entry_kinds": ["markdown"], "reference_mode": "none",
        "projection_mode": "bounded_embed", "target_paths": ["AGENTS.md"],
        "preserve_regions": [["<!-- fcop:v4:begin -->", "<!-- fcop:v4:end -->"]],
        "max_projection_bytes": 65536, "encoding": "UTF-8-no-BOM",
        "newline": "LF", "languages": ["en"],
    }) + "\n").encode())
    request = {
        "manifest_path": str(package / "manifest.json"), "host_profile_path": str(profile),
        "workspace_id": declaration["workspace_id"], "protocol_version": "4.0",
        "assembly_id": "sequential", "selected_modules": MODULES.copy(),
        "selected_languages": ["en"],
    }
    return Project(root), request, package, root


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() if p.is_file() else None for p in root.rglob("*")}


def call(distribution, action="select", **changes):
    project, request, _, root = distribution
    before = snapshot(root.parent)
    try:
        return project.rule_distribution(action=action, request={**request, **changes})
    finally:
        assert snapshot(root.parent) == before


def test_bundled_and_external_identity(distribution):
    external = call(distribution, "validate")
    bundled = call(distribution, "validate", manifest_path=None)
    assert external == bundled
    assert len(external["artifacts"]) == 18
    assert len(external["clause_owners"]) == 73
    assert len(list(DATA.iterdir())) == 19


def test_public_signatures_and_legacy_rejection(distribution, tmp_path):
    project = distribution[0]
    bound = inspect.signature(project.rule_distribution)
    assert list(bound.parameters) == ["action", "request"]
    assert all(p.kind == inspect.Parameter.KEYWORD_ONLY for p in bound.parameters.values())
    assert list(inspect.signature(Project.rule_distribution).parameters) == ["self", "action", "request"]
    empty = tmp_path / "uninitialized"
    with pytest.raises(V4ProtocolError) as exc:
        Project(empty).rule_distribution(action="validate", request={})
    assert exc.value.code == "UNSUPPORTED_WORKSPACE_VERSION"
    assert not empty.exists()


def test_complete_package_checked_even_for_unselected_language(distribution):
    (distribution[2] / "convergence.zh.md").write_bytes(b"unselected byte drift\n")
    with pytest.raises(Exception) as exc:
        call(distribution)
    assert exc.value.code == "toolkit:RULE_ARTIFACT_MISMATCH"


@pytest.mark.parametrize("field,value", [
    ("size_bytes", False), ("load_order", True), ("sha256", "A" * 64),
    ("normative_clause_refs", []), ("depends_on", ["convergence"]),
    ("conflicts_with", ["workspace"]), ("audience", "repository-developer"),
])
def test_strict_artifact_metadata(distribution, field, value):
    manifest = distribution[2] / "manifest.json"
    document = json.loads(manifest.read_bytes())
    document["artifacts"][0][field] = value
    manifest.write_bytes((json.dumps(document) + "\n").encode())
    with pytest.raises(Exception) as exc:
        call(distribution, "validate")
    assert exc.value.code == "toolkit:RULE_MANIFEST_INVALID"


@pytest.mark.parametrize("raw", [b'{}', b'{}\n\n', b'{"x":NaN}\n', b'{"x":{"a":1,"a":2}}\n', b'[]\n', b'\xef\xbb\xbf{}\n'])
def test_strict_manifest_bytes(distribution, raw):
    (distribution[2] / "manifest.json").write_bytes(raw)
    with pytest.raises(Exception) as exc:
        call(distribution, "validate")
    assert exc.value.code == "toolkit:RULE_MANIFEST_INVALID"


@pytest.mark.parametrize("path", ["../workspace.en.md", "/workspace.en.md", "C:/secret.md", "nested\\workspace.en.md", "workspace.en.md/../workspace.en.md"])
def test_source_paths_fail_closed(distribution, path):
    manifest = distribution[2] / "manifest.json"
    document = json.loads(manifest.read_bytes())
    document["artifacts"][0]["source_path"] = path
    manifest.write_bytes((json.dumps(document) + "\n").encode())
    with pytest.raises(Exception) as exc:
        call(distribution, "validate")
    assert exc.value.code == "toolkit:RULE_ARTIFACT_MISMATCH"


def test_selection_deterministic_across_relocation(distribution, tmp_path):
    first = call(distribution)
    relocated = tmp_path / "relocated"
    shutil.copytree(distribution[2], relocated)
    second = call(distribution, manifest_path=str(relocated / "manifest.json"), selected_modules=list(reversed(MODULES)))
    assert first == second
    expected = b"\n".join((DATA / f"{m}.en.md").read_bytes() for m in MODULES)
    assert first["guidance"] == expected
    assert str(tmp_path) not in str(first)


@pytest.mark.parametrize("changes", [{"selected_modules": []}, {"selected_languages": []}, {"selected_modules": MODULES + ["workspace"]}, {"relation_fields": ["blocks"]}])
def test_no_implicit_selection(distribution, changes):
    with pytest.raises(Exception) as exc:
        call(distribution, **changes)
    assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"


def test_development_has_no_default_references(distribution):
    with pytest.raises(Exception) as exc:
        call(distribution, assembly_id="repository-development", constitution_ref=None)
    assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"


@pytest.mark.parametrize("scope_input", [{"operation": "invented-operation"}, {"operation": "transition", "root_task_id": "TASK-root"}, {"operation": "write_review", "review_kind": "convergence"}])
def test_unknown_and_partial_family_guidance_reject(distribution, scope_input):
    with pytest.raises(Exception) as exc:
        call(distribution, "validate_operation_scope", **scope_input)
    assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"


def test_development_reference_hashes_are_real(distribution):
    root = distribution[3]
    refs = []
    for name in ["entry", "manual", "contracts", "task-scope"]:
        path = f"docs/fcop-4.0/development/{name}.md"
        raw = f"Non-normative {name} unit input.\n".encode()
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_bytes(raw)
        refs.append({"path": path, "revision": "2" * 40, "sha256": hashlib.sha256(raw).hexdigest()})
    result = call(distribution, assembly_id="repository-development", development_references=refs)
    assert result["references"] == refs and result["business_modules"] == []
    (root / refs[0]["path"]).write_bytes(b"drift\n")
    with pytest.raises(Exception) as exc:
        call(distribution, assembly_id="repository-development", development_references=refs)
    assert exc.value.code == "toolkit:RULE_SELECTION_INVALID"


@pytest.mark.parametrize("action", ["measure_context", "build_artifacts", "shadow"])
def test_future_positive_capability_is_absent(distribution, action):
    with pytest.raises(V4ProtocolError) as exc:
        call(distribution, action)
    assert exc.value.code == "toolkit:OPERATION_NOT_IMPLEMENTED"


@pytest.mark.parametrize("action", ["plan", "inspect_profile", "status"])
def test_readonly_host_capability_has_no_effects(distribution, action):
    assert call(distribution, action)


def test_adoption_still_requires_explicit_authority(distribution):
    with pytest.raises(FcopError) as exc:
        call(distribution, "adopt")
    assert exc.value.code == "toolkit:RULE_ADOPTION_REQUIRED"


@pytest.mark.parametrize("action,kind,key", [("apply", "adoptions", "adoption_receipt_ref"), ("rollback", "deployments", "deployment_receipt_ref")])
def test_hash_matching_receipt_is_not_trusted(distribution, action, kind, key):
    raw = b'{}\n'
    digest = hashlib.sha256(raw).hexdigest()
    path = f"fcop/internal/rule-distribution/{kind}/{digest}.json"
    target = distribution[3] / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    with pytest.raises(FcopError) as exc:
        call(distribution, action, **{key: {"path": path, "sha256": digest}})
    assert exc.value.code == ("toolkit:RULE_ADOPTION_REQUIRED" if action == "apply" else "toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED")


def test_workspace_rechecked_before_package_read(distribution):
    manifest = distribution[3] / "fcop/fcop.json"
    declaration = json.loads(manifest.read_bytes())
    declaration["workspace_id"] = "urn:uuid:00000000-0000-4000-8000-000000000099"
    manifest.write_bytes((json.dumps(declaration) + "\n").encode())
    with pytest.raises(V4ProtocolError) as exc:
        call(distribution, "validate")
    assert exc.value.code == "WORKSPACE_ID_MISMATCH"
