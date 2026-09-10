"""Manifest identity, canonical byte integrity and authority rejection."""

import pytest

from .conftest import (
    EXCLUDED_RC,
    MODULES,
    OWNED,
    RELATIONS,
    SEQUENTIAL,
    field,
    json_bytes,
    sha,
    snapshot,
)


@pytest.mark.parametrize("variant", ["valid", "new-core-authority"])
def test_dist_01(case, variant):
    """DIST-01; RD-01/02; Owner: WP4C.3. Arrange claims; Act validate; Assert trace/no effects."""
    if variant != "valid":
        case.manifest["core_roles"] = ["NEW_ADMIN"]
        case.manifest["core_states"] = ["auto-approved"]
        case.flush()
        case.reject("validate", "RULE_MANIFEST_INVALID")
    else:
        before = snapshot(case.sandbox)
        result = case.invoke("validate", readonly=True)
        assert field(result, "protocol_version") == "4.0"
        assert field(result, "manifest_sha256") == sha(
            (case.package / "manifest.json").read_bytes()
        )
        assert set(field(result, "clause_owners")) == {r for refs in OWNED.values() for r in refs}
        assert snapshot(case.sandbox) == before


@pytest.mark.parametrize(
    "variant", ["ordinary", "development-no-constitution", "excluded-rc", "old-draft"]
)
def test_dist_02(case, variant):
    """DIST-02; RD-03/19; Owner: WP4C.3. Arrange audiences/sources; Act select; Assert isolation."""
    if variant in {"excluded-rc", "old-draft"}:
        request = case.request(
            assembly_id="repository-development",
            source_dependencies=[
                {
                    "path": "excluded-discussion.md",
                    "sha256": EXCLUDED_RC if variant == "excluded-rc" else "0" * 64,
                    "normative": False,
                    "license": "unresolved",
                }
            ],
        )
        case.reject("select", "RULE_SELECTION_INVALID", request)
    else:
        request = case.request(
            assembly_id="repository-development"
            if variant.startswith("development")
            else "sequential",
            constitution_ref=None,
        )
        if variant == "development-no-constitution":
            references = []
            for name, purpose in [
                ("entry", "FCoP repository development entry"),
                ("manual", "FCoP development guidance/manual"),
                ("contracts", "Fixed FCoP contract input"),
                ("task-scope", "Current TASK, authorized scope and Gate input"),
            ]:
                raw = f"Non-normative test input: {purpose}.\n".encode()
                path = f"docs/fcop-4.0/development/{name}.md"
                case.put(case.root / path, raw)
                references.append({"path": path, "revision": "1" * 40, "sha256": sha(raw)})
                assert (case.root / path).resolve().is_relative_to(case.root.resolve())
                assert sha((case.root / path).read_bytes()) == references[-1]["sha256"]
            request["development_references"] = references
        result = case.invoke("select", request, readonly=True)
        assert EXCLUDED_RC not in str(result)
        if variant == "ordinary":
            assert field(result, "selected_modules") == SEQUENTIAL
            assert "repository-developer" not in str(field(result, "guidance"))
        else:
            assert field(result, "constitution_ref") is None
            assert len(field(result, "references")) == 4
            assert all(
                {"path", "revision", "sha256"} <= ref.keys() for ref in field(result, "references")
            )
            assert field(result, "references") == request["development_references"]


@pytest.mark.parametrize(
    "variant", ["valid", "duplicate-owner", "missing-owner", "blocks", "relates_to", "supersedes"]
)
def test_dist_03(case, variant):
    """DIST-03; RD-04/05; Owner: WP4C.3. Arrange ownership/alias; Act validate/select; Assert exact sets."""
    if variant in {"duplicate-owner", "missing-owner"}:
        for a in case.manifest["artifacts"]:
            if a["module_id"] == "relations":
                a["normative_clause_refs"] = (
                    ["F4.2.1", *OWNED["relations"]]
                    if variant.startswith("duplicate")
                    else ["F4.5.1"]
                )
        case.flush()
        case.reject("validate", "RULE_MANIFEST_INVALID")
    elif variant != "valid":
        case.reject(
            "select", "RULE_SELECTION_INVALID", case.request(relation_fields=[*RELATIONS, variant])
        )
    else:
        result = case.invoke("select", case.request(relation_fields=RELATIONS), readonly=True)
        owners = field(result, "clause_owners")
        assert len(owners) == 73
        assert owners == {r: module for module, refs in OWNED.items() for r in refs}
        assert set(owners.values()) == set(MODULES)
        assert field(result, "relation_fields") == RELATIONS
        assert "relations" in field(result, "selected_modules")
        assert "convergence" not in field(result, "selected_modules")


@pytest.mark.parametrize(
    "variant",
    [
        "en",
        "zh",
        "bom",
        "embedded-bom",
        "crlf",
        "cr",
        "nul",
        "del",
        "invalid-utf8",
        "two-final-lf",
        "parity",
    ],
)
def test_dist_04(case, variant):
    """DIST-04; RD-06; Owner: WP4C.3. Arrange raw bytes/parity; Act validate; Assert no normalization."""
    target = case.package / "workspace.en.md"
    good = target.read_bytes()
    malformed = {
        "bom": b"\xef\xbb\xbf" + good,
        "embedded-bom": good[:-1] + b"\xef\xbb\xbf\n",
        "crlf": good.replace(b"\n", b"\r\n"),
        "cr": good.replace(b"\n", b"\r"),
        "nul": good[:-1] + b"\x00\n",
        "del": good[:-1] + b"\x7f\n",
        "invalid-utf8": good[:-1] + b"\xff\n",
        "two-final-lf": good + b"\n",
    }
    if variant in malformed:
        raw = malformed[variant]
        case.put(target, raw)
        # Re-pin the invalid raw bytes: failure must be encoding, not stale hash.
        case.manifest["artifacts"][0].update(sha256=sha(raw), size_bytes=len(raw))
        case.flush()
        case.reject("validate", "RULE_ARTIFACT_MISMATCH")
    elif variant == "parity":
        case.manifest["artifacts"][1]["normative_clause_refs"] = ["F4.2.1"]
        case.flush()
        case.reject("validate", "RULE_MANIFEST_INVALID")
    else:
        case.profile["languages"] = [variant]
        case.flush()
        result = case.invoke("select", case.request(selected_languages=[variant]), readonly=True)
        artifacts = field(result, "artifacts")
        assert len(artifacts) == 8
        assert {field(a, "language") for a in artifacts} == {variant}
        assert [field(a, "source_path") for a in artifacts] == [
            f"{m}.{variant}.md" for m in SEQUENTIAL
        ]
        for artifact in artifacts:
            raw = (case.package / field(artifact, "source_path")).read_bytes()
            assert field(artifact, "sha256") == sha(raw)
            assert field(artifact, "size_bytes") == len(raw)


@pytest.mark.parametrize(
    "variant",
    [
        "valid",
        "duplicate-key",
        "schema",
        "unknown",
        "missing-language",
        "duplicate-artifact",
        "adoption",
        "type",
        "latest",
    ],
)
def test_dist_05(case, variant):
    """DIST-05; RD-07; Owner: WP4C.3. Arrange JSON mutations; Act validate; Assert strict identity."""
    if variant == "duplicate-key":
        raw = json_bytes(case.manifest).replace(
            b'"protocol_version": "4.0"', b'"protocol_version": "5.0", "protocol_version": "4.0"'
        )
        case.put(case.package / "manifest.json", raw)
    else:
        if variant == "schema":
            case.manifest["manifest_schema"] = "unknown/v9"
        elif variant == "unknown":
            case.manifest["random_state"] = 9
        elif variant == "missing-language":
            case.manifest["artifacts"].pop()
        elif variant == "duplicate-artifact":
            case.manifest["artifacts"][-1] = case.manifest["artifacts"][0].copy()
        elif variant == "adoption":
            case.manifest["adopted_by"] = "ADMIN"
        elif variant == "type":
            case.manifest["artifacts"][0]["size_bytes"] = True
        elif variant == "latest":
            case.manifest["package_version"] = "latest"
        case.flush()
    if variant != "valid":
        case.reject("validate", "RULE_MANIFEST_INVALID")
    else:
        result = case.invoke("validate", readonly=True)
        assert field(result, "package_version") == "4.0.0-fixture.1"
        assert len(field(result, "artifacts")) == 18
        assert {
            (field(a, "module_id"), field(a, "language")) for a in field(result, "artifacts")
        } == {(m, language) for m in MODULES for language in ["en", "zh"]}


@pytest.mark.parametrize("variant", ["valid", "bytes", "size", "path", "symlink-escape", "missing"])
def test_dist_06(case, variant):
    """DIST-06; RD-07/08; Owner: WP4C.3. Arrange drift/escape; Act validate twice; Assert raw integrity."""
    artifact = case.package / "workspace.en.md"
    if variant == "bytes":
        case.put(artifact, artifact.read_bytes() + b"drift\n")
    elif variant == "size":
        case.manifest["artifacts"][0]["size_bytes"] += 1
        case.flush()
    elif variant == "path":
        case.manifest["artifacts"][0]["source_path"] = "../outside.md"
        case.flush()
    elif variant == "symlink-escape":
        outside = case.sandbox / "outside.md"
        case.put(outside, artifact.read_bytes())
        artifact.unlink()
        artifact.symlink_to(outside)
    elif variant == "missing":
        artifact.unlink()
    if variant != "valid":
        case.reject("validate", "RULE_ARTIFACT_MISMATCH")
    else:
        first = case.invoke("validate", readonly=True)
        assert field(first, "manifest_sha256") == sha((case.package / "manifest.json").read_bytes())
        case.put(artifact, artifact.read_bytes() + b"same-version-drift\n")
        case.reject("validate", "RULE_ARTIFACT_MISMATCH")
