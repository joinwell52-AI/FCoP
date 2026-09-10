"""Selection, adoption, receipt provenance and independent Host evidence."""

import json

import pytest

from .conftest import HOSTS, SEQUENTIAL, WORKSPACE_ID, Scenario, field, json_bytes, sha, snapshot


@pytest.mark.parametrize("variant", ["permutation", "cycle", "missing-dependency", "conflict"])
def test_dist_07(case, variant):
    """DIST-07; RD-08; Owner: WP4C.3. Arrange graph/order; Act select; Assert deterministic closed selection."""
    if variant == "permutation":
        first = case.invoke("select", readonly=True)
        case.manifest["artifacts"].reverse()
        case.flush()
        second = case.invoke("select", readonly=True)
        assert field(first, "selected_modules") == field(second, "selected_modules") == SEQUENTIAL
        assert field(first, "artifacts") == field(second, "artifacts")
    elif variant == "missing-dependency":
        case.reject(
            "select", "RULE_SELECTION_INVALID", case.request(selected_modules=SEQUENTIAL[1:])
        )
    else:
        for artifact in case.manifest["artifacts"]:
            if artifact["module_id"] == "workspace":
                artifact["depends_on" if variant == "cycle" else "conflicts_with"] = ["envelopes"]
        case.flush()
        case.reject("select", "RULE_MANIFEST_INVALID")


@pytest.mark.parametrize(
    "variant",
    ["valid", "file-without-adoption", "wrong-workspace", "v3", "broken-previous", "actor-only"],
)
def test_dist_08(case, variant):
    """DIST-08; RD-09; Owner: WP4C.4. Arrange adoption evidence; Act adopt/status; Assert identity and zero migration."""
    if variant == "file-without-adoption":
        case.put(case.root / "AGENTS.md", b"Unowned pre-existing Host instructions.\n")
        status = case.invoke("status", readonly=True)
        assert field(status, "admin_adopted") is False
        assert field(status, "entry_generated") is not True
        case.reject("apply", "RULE_ADOPTION_REQUIRED", case.request(adoption_receipt_ref=None))
    elif variant == "valid":
        ref = case.adopt()
        receipt = case.read_receipt(ref, "adoptions")
        assert receipt["adopted_by"] == case.request()["admin_selection_ref"]
        assert receipt["previous_receipt_ref"] is None
        assert receipt["protocol_version"] == "4.0"
        assert json.loads((case.root / "fcop/fcop.json").read_bytes())["profiles"] == []
    else:
        request = case.request()
        if variant == "wrong-workspace":
            request["workspace_id"] = "urn:uuid:00000000-0000-4000-8000-000000000002"
        elif variant == "v3":
            case.put(
                case.root / "fcop/fcop.json",
                json_bytes(
                    {"protocol": "fcop", "protocol_version": "3.0", "workspace_id": WORKSPACE_ID}
                ),
            )
        elif variant == "broken-previous":
            request["previous_receipt_ref"] = {
                "path": "fcop/internal/rule-distribution/adoptions/missing.json",
                "sha256": "0" * 64,
            }
        else:
            request["admin_selection_ref"] = None
            request["actor"] = "ADMIN"
        case.reject("adopt", "RULE_ADOPTION_REQUIRED", request)


@pytest.mark.parametrize("variant", ["success", "before-drift", "receipt-tamper"])
def test_dist_09(case, variant):
    """DIST-09; RD-10; Owner: WP4C.4. Arrange real deploy; Act verify/update; Assert hashes and immutable facts."""
    ref, receipt = case.deploy()
    receipt_bytes = (case.root / ref["path"]).read_bytes()
    target = case.root / "AGENTS.md"
    assert receipt["targets"][0]["before_sha256"] is None
    assert receipt["targets"][0]["backup_ref"] is None
    assert receipt["targets"][0]["after_sha256"] == sha(target.read_bytes())
    assert receipt["manifest_sha256"] == sha((case.package / "manifest.json").read_bytes())
    if variant == "receipt-tamper":
        case.put(case.root / ref["path"], receipt_bytes + b" ")
        case.reject(
            "verify_deployment",
            "RULE_DEPLOYMENT_RECOVERY_REQUIRED",
            case.request(deployment_receipt_ref=ref),
        )
    elif variant == "before-drift":
        case.put(target, target.read_bytes() + b"user edit\n")
        case.reject(
            "verify_deployment", "RULE_OWNERSHIP_CONFLICT", case.request(deployment_receipt_ref=ref)
        )
        assert (case.root / ref["path"]).read_bytes() == receipt_bytes
    else:
        result = case.invoke(
            "verify_deployment", case.request(deployment_receipt_ref=ref), readonly=True
        )
        assert field(result, "verified") is True
        assert (case.root / ref["path"]).read_bytes() == receipt_bytes
        assert field(result, "runtime_consumption_verified") is None


@pytest.mark.parametrize(
    "variant",
    ["success", "missing-backup", "modified-backup", "modified-target", "arbitrary-version"],
)
def test_dist_10(case, variant):
    """DIST-10; RD-10; Owner: WP4C.4. Arrange two real deployments; Act rollback; Assert prior bytes/evidence."""
    first_ref, first = case.deploy()
    old_target = (case.root / "AGENTS.md").read_bytes()
    old_receipt = (case.root / first_ref["path"]).read_bytes()
    case.manifest["package_version"] = "4.0.0-fixture.2"
    case.flush()
    adoption = case.invoke(
        "adopt", case.request(previous_receipt_ref=first["adoption_receipt_ref"])
    )
    second_ref, second = case.deploy(field(adoption, "adoption_receipt_ref"))
    backup = second["targets"][0]["backup_ref"]
    assert backup is not None
    backup_path = case.root / backup["path"]
    assert backup_path.resolve().is_relative_to(case.root.resolve())
    assert backup_path.read_bytes() == old_target
    assert sha(old_target) == backup["sha256"]
    request = case.request(deployment_receipt_ref=second_ref)
    if variant == "missing-backup":
        backup_path.unlink()
    elif variant == "modified-backup":
        case.put(backup_path, b"invalid backup\n")
    elif variant == "modified-target":
        case.put(case.root / "AGENTS.md", b"user-owned changed target\n")
    elif variant == "arbitrary-version":
        request["package_version"] = "arbitrary-old-label"
    if variant != "success":
        case.reject("rollback", "RULE_DEPLOYMENT_RECOVERY_REQUIRED", request)
    else:
        result = case.invoke("rollback", request)
        ref = field(result, "deployment_receipt_ref")
        receipt = case.read_receipt(ref, "deployments")
        assert ref not in [first_ref, second_ref]
        assert receipt["action"] == "rollback"
        assert receipt["previous_deployment_ref"] == second_ref
        assert (case.root / "AGENTS.md").read_bytes() == old_target
    assert (case.root / first_ref["path"]).read_bytes() == old_receipt


@pytest.mark.parametrize(
    "variant",
    [*HOSTS, "unknown-host", "unknown-profile", "evaluator", "model-probe", "duplicate-key"],
)
def test_dist_11(case, variant):
    """DIST-11; RD-11/12; Owner: WP4C.4. Arrange static profiles; Act inspect_profile; Assert no caller trust/probes."""
    if variant in HOSTS:
        other = Scenario(case.sandbox / variant, case.node, variant)
        result = other.invoke("inspect_profile", readonly=True)
        assert field(result, "target_paths") == [HOSTS[variant]]
        assert field(result, "max_projection_bytes") == 65536
        assert field(result, "projection_mode") == "bounded_embed"
        assert field(result, "languages") == ["en"]
        assert field(result, "admin_adopted") is False
    else:
        if variant == "unknown-host":
            case.profile["host_id"] = "unknown"
        elif variant == "unknown-profile":
            case.profile["profile_version"] = "unproven-reference"
            case.profile["projection_mode"] = "reference"
        elif variant == "evaluator":
            case.profile["profile_evaluator"] = "always-AUTHORIZED"
        elif variant == "model-probe":
            case.profile["probe_model"] = True
        case.flush()
        if variant == "duplicate-key":
            raw = json_bytes(case.profile).replace(
                b'"host_id": "codex"', b'"host_id": "unknown", "host_id": "codex"'
            )
            case.put(case.sandbox / "inputs/profile.json", raw)
        case.reject("inspect_profile", "RULE_HOST_UNAVAILABLE")


@pytest.mark.parametrize(
    "evidence", ["support-only", "adoption-only", "generated", "consumption-only"]
)
def test_dist_12(case, evidence):
    """DIST-12; RD-11; Owner: WP4C.4. Arrange independent evidence; Act status; Assert four facts never imply each other."""
    request = case.request()
    if evidence == "adoption-only":
        request["adoption_receipt_ref"] = case.adopt()
    elif evidence == "generated":
        request["deployment_receipt_ref"] = case.deploy()[0]
    elif evidence == "consumption-only":
        case.put(
            case.sandbox / "inputs/consumption.json",
            json_bytes({"host": "codex", "result": "verified", "entry_sha256": "0" * 64}),
        )
        request["runtime_evidence_ref"] = {
            "path": str(case.sandbox / "inputs/consumption.json"),
            "sha256": sha((case.sandbox / "inputs/consumption.json").read_bytes()),
        }
    before = snapshot(case.sandbox)
    result = case.invoke("status", request, readonly=True)
    assert field(result, "adapter_supported") is True
    assert field(result, "admin_adopted") is (evidence in {"adoption-only", "generated"})
    assert field(result, "entry_generated") is (evidence == "generated")
    assert field(result, "runtime_consumption_verified") is None
    assert snapshot(case.sandbox) == before
