"""Assembly isolation, legacy routing and local-only resource mappings."""

import json

import pytest

from .conftest import EXCLUDED_RC, MODULES, SEQUENTIAL, field, json_bytes, sha, snapshot


@pytest.mark.parametrize("assembly", ["sequential", "parallel"])
def test_dist_21(case, assembly):
    """DIST-21; RD-17/18; Owner: WP4C.3. Arrange explicit assembly; Act select/admit; Assert exact increment."""
    modules = MODULES if assembly == "parallel" else SEQUENTIAL
    request = case.request(assembly_id=assembly, selected_modules=modules)
    selected = case.invoke("select", request, readonly=True)
    assert field(selected, "selected_modules") == modules
    assert field(selected, "relation_fields") == [
        "parent",
        "branch_of",
        "subject_ref",
        "references",
    ]
    assert ("convergence" in field(selected, "selected_modules")) is (assembly == "parallel")
    if assembly == "sequential":
        case.reject(
            "validate_operation_scope",
            "RULE_SELECTION_INVALID",
            {**request, "operation": "create_branch", "branch_of": "TASK-root"},
        )
    else:
        result = case.invoke(
            "validate_operation_scope",
            {**request, "operation": "create_branch", "branch_of": "TASK-root"},
            readonly=True,
        )
        assert field(result, "guidance_complete") is True
        assert field(result, "lifecycle_authorized") is False
        assert not (case.root / "fcop/_lifecycle").exists()
    assert json.loads((case.root / "fcop/fcop.json").read_bytes())["profiles"] == []


@pytest.mark.parametrize("variant", ["pinned-development", "business", "unpinned", "excluded"])
def test_dist_22(case, variant):
    """DIST-22; RD-19; Owner: WP4C.3. Arrange separate pinned bundle; Act read; Assert no tenth business module."""
    refs = []
    for name in ["entry", "manual", "contracts", "task-scope"]:
        data = f"Fixed {name} repository-development input.\n".encode()
        path = f"docs/fcop-4.0/development/{name}.md"
        case.put(case.root / path, data)
        refs.append({"path": path, "revision": "1" * 40, "sha256": sha(data)})
    if variant == "unpinned":
        del refs[1]["revision"]
    elif variant == "excluded":
        refs[1]["sha256"] = EXCLUDED_RC
    request = case.request(
        assembly_id="sequential" if variant == "business" else "repository-development",
        development_references=refs,
        constitution_ref=None,
    )
    if variant in {"unpinned", "excluded"}:
        case.reject("select", "RULE_SELECTION_INVALID", request)
    else:
        result = case.invoke("select", request, readonly=True)
        if variant == "business":
            assert field(result, "selected_modules") == SEQUENTIAL
            assert b"repository-development input" not in field(result, "guidance")
        else:
            assert field(result, "references") == refs
            assert field(result, "business_modules") == []
            assert field(result, "constitution_ref") is None


@pytest.mark.parametrize("variant", ["unversioned-v3", "explicit-v4-on-v3", "v4-no-adoption"])
def test_dist_23(case, variant):
    """DIST-23; RD-20; Owner: WP4C.5. Arrange legacy target; Act version routing; Assert no fallback/migration."""
    legacy = b"Legacy 3.x user-owned instruction sentinel.\r\n"
    case.put(case.root / "AGENTS.md", legacy)
    if variant != "v4-no-adoption":
        case.put(
            case.root / "fcop/fcop.json",
            json_bytes(
                {
                    "protocol": "fcop",
                    "protocol_version": "3.0",
                    "mode": "solo",
                    "roles": ["ME"],
                    "leader": "ME",
                }
            ),
        )
    before = (case.root / "fcop/fcop.json").read_bytes()
    if variant == "unversioned-v3":
        # No protocol_version in this request: the legacy routing contract.
        result = case.invoke("redeploy", {"force": False})
        assert field(result, "protocol_version").startswith("3")
        assert (case.root / "AGENTS.md").read_bytes() == legacy
        assert not (case.root / "fcop/internal/rule-distribution").exists()
        assert "4.0" not in str(field(result, "written_paths"))
    else:
        case.reject("apply", "RULE_ADOPTION_REQUIRED", case.request(adoption_receipt_ref=None))
        assert (case.root / "AGENTS.md").read_bytes() == legacy
    assert (case.root / "fcop/fcop.json").read_bytes() == before


@pytest.mark.parametrize(
    "resource", ["fcop://rules", "fcop://protocol", "fcop://guidance/sequential/en", "fcop://team"]
)
@pytest.mark.parametrize("version", ["3.0", "4.0"])
def test_dist_24(case, resource, version):
    """DIST-24; RD-21; Owner: WP4C.5. Arrange versioned resources; Act local adapter/Relay mapping; Assert read-only parity."""
    manifest = json.loads((case.root / "fcop/fcop.json").read_bytes())
    manifest["protocol_version"] = version
    case.put(case.root / "fcop/fcop.json", json_bytes(manifest))
    before = snapshot(case.sandbox)
    request = case.request(resource_uri=resource, protocol_version=version, transport="stdio-local")
    direct = case.invoke("read_resource", request, readonly=True)
    relay = case.invoke(
        "read_resource",
        {**request, "transport": "relay-inprocess", "network": False},
        readonly=True,
    )
    assert field(direct, "content") == field(relay, "content")
    assert field(direct, "protocol_version") == field(relay, "protocol_version") == version
    if version == "4.0" and resource == "fcop://rules":
        assert field(direct, "content") == case.manifest
        assert field(direct, "sha256") == sha((case.package / "manifest.json").read_bytes())
    elif resource == "fcop://protocol":
        assert {"path", "revision", "sha256"} <= field(direct, "content").keys()
        assert "entry_generated" not in field(direct, "content")
    elif resource == "fcop://team" and version == "4.0":
        assert field(direct, "available") is False
        assert field(direct, "reason")
    else:
        assert field(direct, "content")
    assert snapshot(case.sandbox) == before
