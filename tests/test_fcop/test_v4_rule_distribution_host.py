"""Independent Host-plane checks: real bytes, rejection effects and crash recovery."""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing
import os
import subprocess
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import FcopError
from fcop.v4.rule_distribution import _deployment
from fcop.v4.rule_distribution._files import path_at

from .test_v4_rule_distribution import distribution as distribution
from .test_v4_rule_distribution import snapshot


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def prepared(distribution):
    project, request, _, root = distribution
    authority = root.parent / "admin.md"
    authority.write_bytes(b"Explicit isolated unit selection: sequential codex en.\n")
    request = {**request, "recorded_at": "2026-09-08T10:00:00+08:00",
               "admin_selection_ref": {"path": str(authority), "sha256": digest(authority.read_bytes())}}
    receipt = project.rule_distribution(action="adopt", request=request)["adoption_receipt_ref"]
    return {**request, "adoption_receipt_ref": receipt}


def deploy(distribution, request):
    return distribution[0].rule_distribution(action="apply", request=request)["deployment_receipt_ref"]


def reject_unchanged(distribution, action, request, code):
    before = snapshot(distribution[3].parent)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action=action, request=request)
    assert caught.value.code == "toolkit:" + code
    assert snapshot(distribution[3].parent) == before


def test_adopt_only_receipt_and_exact_retry(distribution):
    request = prepared(distribution)
    before = snapshot(distribution[3].parent)
    result = distribution[0].rule_distribution(action="adopt", request=request)
    assert result["adoption_receipt_ref"] == request["adoption_receipt_ref"]
    assert snapshot(distribution[3].parent) == before
    internal = distribution[3] / "fcop/internal/rule-distribution"
    assert {p.name for p in internal.iterdir()} == {"adoptions"}
    assert len(list(internal.rglob("*.json"))) == 1
    assert json.loads((distribution[3] / "fcop/fcop.json").read_bytes())["profiles"] == []


def test_lost_apply_response_and_complete_plan_retry(distribution):
    request = prepared(distribution)
    plan = distribution[0].rule_distribution(action="plan", request=request)
    request["plan"] = plan
    ref = deploy(distribution, request)
    before = snapshot(distribution[3].parent)
    again = Project(distribution[3]).rule_distribution(action="apply", request=request)
    assert again["existing"] is True and again["deployment_receipt_ref"] == ref
    assert snapshot(distribution[3].parent) == before
    damaged = copy.deepcopy(request)
    damaged["plan"]["targets"][0]["diff"] += "unrelated\n"
    reject_unchanged(distribution, "apply", damaged, "RULE_OWNERSHIP_CONFLICT")


@pytest.mark.parametrize("value", [None, "2026-09-08", "2026-09-08T12:00:00", "not-time", 42])
def test_invalid_rollback_time_precedes_all_writes(distribution, value):
    request = prepared(distribution)
    ref = deploy(distribution, request)
    reject_unchanged(distribution, "rollback", {**request, "deployment_receipt_ref": ref, "recorded_at": value}, "RULE_DEPLOYMENT_RECOVERY_REQUIRED")


def test_rollback_lost_response_does_not_toggle_history(distribution):
    request = prepared(distribution)
    ref = deploy(distribution, request)
    rollback = {**request, "deployment_receipt_ref": ref, "recorded_at": "2026-09-08T10:01:00+08:00"}
    first = distribution[0].rule_distribution(action="rollback", request=rollback)
    before = snapshot(distribution[3].parent)
    second = Project(distribution[3]).rule_distribution(action="rollback", request=rollback)
    assert first["deployment_receipt_ref"] == second["deployment_receipt_ref"]
    assert second["existing"] is True
    assert snapshot(distribution[3].parent) == before
    assert not (distribution[3] / "AGENTS.md").exists()


def test_rollback_keeps_user_bytes_added_between_deployments(distribution):
    request = prepared(distribution)
    first = deploy(distribution, request)
    target = distribution[3] / "AGENTS.md"
    desired_old = b"User prefix\n" + target.read_bytes() + b"User suffix\n"
    target.write_bytes(desired_old)
    changed = {**request, "recorded_at": "2026-09-08T10:02:00+08:00", "previous_deployment_ref": first}
    second = deploy(distribution, changed)
    restored = distribution[0].rule_distribution(action="rollback", request={**changed, "deployment_receipt_ref": second})
    assert target.read_bytes() == desired_old
    assert restored["deployment_receipt_ref"] not in (first, second)


@pytest.mark.parametrize("kind", ["manifest", "source", "profile", "adoption", "admin", "target"])
def test_plan_revalidates_each_input_before_effect(distribution, kind):
    request = prepared(distribution)
    request["plan"] = distribution[0].rule_distribution(action="plan", request=request)
    root = distribution[3]
    paths = {"manifest": distribution[2] / "manifest.json", "source": distribution[2] / "convergence.zh.md",
             "profile": Path(request["host_profile_path"]), "adoption": root / request["adoption_receipt_ref"]["path"],
             "admin": Path(request["admin_selection_ref"]["path"]), "target": root / "AGENTS.md"}
    path = paths[kind]
    path.write_bytes(path.read_bytes() + b" " if path.exists() else b"User ownership\n")
    before = snapshot(root.parent)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="apply", request=request)
    assert caught.value.code.startswith("toolkit:RULE_")
    assert snapshot(root.parent) == before


@pytest.mark.parametrize("path", ["../outside", "/absolute", "C:/outside", "C:relative", "\\\\server\\share", "nul", "COM1.txt", "x/../y", "x\x00y", "x.", "x "])
def test_target_paths_reject_without_creating_directories(distribution, path):
    before = snapshot(distribution[3].parent)
    with pytest.raises(FcopError) as caught:
        path_at(distribution[3], path, "RULE_OWNERSHIP_CONFLICT", "plan")
    assert caught.value.code == "toolkit:RULE_OWNERSHIP_CONFLICT"
    assert snapshot(distribution[3].parent) == before


def test_native_junction_is_not_a_distribution_root(distribution):
    root = distribution[3]
    outside = root.parent / "outside"
    outside.mkdir()
    link = root / "alias"
    if os.name == "nt":
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True, check=False)
        assert result.returncode == 0, result.stderr
    else:
        link.symlink_to(outside, target_is_directory=True)
    before = snapshot(outside)
    with pytest.raises(FcopError) as caught:
        path_at(root, "alias/entry.md", "RULE_OWNERSHIP_CONFLICT", "plan")
    assert caught.value.code == "toolkit:RULE_OWNERSHIP_CONFLICT"
    assert snapshot(outside) == before


@pytest.mark.parametrize("raw", [b'\xef\xbb\xbf{}\n', b'{}\r\n', b'{"a":1,"a":2}\n', b'{"x":NaN}\n', b'{"x":Infinity}\n', b'{"x":"\\u0000"}\n'])
def test_profile_byte_contract_is_strict(distribution, raw):
    Path(distribution[1]["host_profile_path"]).write_bytes(raw)
    reject_unchanged(distribution, "inspect_profile", distribution[1], "RULE_HOST_UNAVAILABLE")


@pytest.mark.parametrize("field", ["profile_evaluator", "profile_resolver", "model_probe", "trusted_profiles", "nested"])
def test_business_request_cannot_supply_executable_authority(distribution, field):
    value = {"nested": {"judge": lambda: "AUTHORIZED"}} if field == "nested" else {field: lambda: "AUTHORIZED"}
    reject_unchanged(distribution, "plan", {**distribution[1], **value}, "RULE_HOST_UNAVAILABLE")


def test_cyclic_request_rejects_without_recursion_or_writes(distribution):
    cycle = {}
    cycle["child"] = cycle
    reject_unchanged(distribution, "plan", {**distribution[1], "cycle": cycle}, "RULE_SELECTION_INVALID")


def test_invalid_batch_item_is_not_ignored(distribution):
    request = prepared(distribution)
    reject_unchanged(distribution, "apply", {**request, "deployments": [None], "test_fault": {"window": "before_success_receipt", "raise_after_observation": True}}, "RULE_SELECTION_INVALID")


def test_manifest_unc_is_rejected_before_loader_io(distribution, monkeypatch):
    from fcop.v4.rule_distribution import _receipts

    def forbidden_loader(*args, **kwargs):
        raise AssertionError("UNC preflight must reject before the loader can access input")

    monkeypatch.setattr(_receipts, "load", forbidden_loader)
    reject_unchanged(distribution, "plan", {**distribution[1], "manifest_path": "\\\\server\\share\\manifest.json"}, "RULE_ARTIFACT_MISMATCH")


@pytest.mark.parametrize("variant", ["filename", "cross-workspace", "cyclic-tamper"])
def test_adoption_identity_and_chain_cannot_be_substituted(distribution, variant):
    request = prepared(distribution)
    root = distribution[3]
    ref = request["adoption_receipt_ref"]
    path = root / ref["path"]
    value = json.loads(path.read_bytes())
    if variant == "filename":
        changed = {**ref, "path": ref["path"].replace(ref["sha256"], "0" * 64)}
        (root / changed["path"]).write_bytes(path.read_bytes())
    elif variant == "cross-workspace":
        value["workspace_id"] = "urn:uuid:00000000-0000-4000-8000-000000000099"
        raw = (json.dumps(value) + "\n").encode()
        changed = {"path": f"fcop/internal/rule-distribution/adoptions/{digest(raw)}.json", "sha256": digest(raw)}
        (root / changed["path"]).write_bytes(raw)
    else:
        # A self-reference cannot preserve the original raw digest: reject at
        # that first broken identity rather than traversing an invented cycle.
        value["previous_receipt_ref"] = ref
        path.write_bytes((json.dumps(value) + "\n").encode())
        changed = ref
    reject_unchanged(distribution, "apply", {**request, "adoption_receipt_ref": changed}, "RULE_ADOPTION_REQUIRED")


@pytest.mark.parametrize("kind", ["receipt", "backup", "profile-snapshot"])
def test_owned_plan_rechecks_historical_evidence(distribution, kind):
    request = prepared(distribution)
    deploy(distribution, request)
    second = {**request, "recorded_at": "2026-09-08T10:02:00+08:00"}
    ref = deploy(distribution, second)
    third = {**request, "recorded_at": "2026-09-08T10:03:00+08:00"}
    third["plan"] = distribution[0].rule_distribution(action="plan", request=third)
    root = distribution[3]
    value = json.loads((root / ref["path"]).read_bytes())
    path = {"receipt": root / ref["path"], "backup": root / value["targets"][0]["backup_ref"]["path"],
            "profile-snapshot": root / f"fcop/internal/rule-distribution/profiles/{value['host_profile_sha256']}.json"}[kind]
    path.write_bytes(path.read_bytes() + b" ")
    before = snapshot(root.parent)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="apply", request=third)
    assert caught.value.code.startswith("toolkit:RULE_")
    assert snapshot(root.parent) == before


@pytest.mark.parametrize("window", ["before_stage_durable", "between_replacements", "before_success_receipt"])
def test_fault_with_owned_target_preserves_original_and_recovers(distribution, window):
    request = prepared(distribution)
    ref = deploy(distribution, request)
    root = distribution[3]
    original = (root / "AGENTS.md").read_bytes()
    history = (root / ref["path"]).read_bytes()
    # A real second selected package gives a distinguishable desired outcome.
    manifest = distribution[2] / "manifest.json"
    document = json.loads(manifest.read_bytes())
    document["package_version"] += ".fixture2"
    manifest.write_bytes((json.dumps(document) + "\n").encode())
    changed = {**request, "adoption_receipt_ref": None, "previous_receipt_ref": request["adoption_receipt_ref"]}
    changed["adoption_receipt_ref"] = distribution[0].rule_distribution(action="adopt", request=changed)["adoption_receipt_ref"]
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="apply", request={**changed, "test_fault": {"window": window, "raise_after_observation": True}})
    assert caught.value.code == "toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED"
    failure = caught.value.details["failure_ref"]
    before = snapshot(root.parent)
    inspection = Project(root).rule_distribution(action="inspect_failure", request={**changed, "failure_ref": failure})
    assert snapshot(root.parent) == before
    assert inspection["proven_writes"] == ([] if window == "before_stage_durable" else ["AGENTS.md"])
    outcome = Project(root).rule_distribution(action="rollback_partial", request={**changed, "failure_ref": failure})
    assert outcome["restored"] is True
    assert (root / "AGENTS.md").read_bytes() == original
    assert (root / ref["path"]).read_bytes() == history
    assert len(list((root / "fcop/internal/rule-distribution/deployments").glob("*.json"))) == 1


def _crash_after_replace(root, request):
    original = _deployment._move

    def interrupt(stage, target, *, replace):
        original(stage, target, replace=replace)
        os._exit(73)

    _deployment._move = interrupt
    Project(Path(root)).rule_distribution(action="apply", request=request)


def test_real_process_exit_after_replace_is_explicitly_recoverable(distribution):
    request = prepared(distribution)
    root = distribution[3]
    process = multiprocessing.get_context("spawn").Process(target=_crash_after_replace, args=(str(root), request))
    process.start()
    process.join(45)
    assert not process.is_alive()
    assert process.exitcode == 73
    assert (root / "AGENTS.md").is_file()
    attempts = list((root / "fcop/internal/rule-distribution/failures").glob("*.json"))
    assert len(attempts) == 1
    ref = {"path": attempts[0].relative_to(root).as_posix(), "sha256": attempts[0].stem}
    outcome = Project(root).rule_distribution(action="inspect_failure", request={**request, "failure_ref": ref})
    assert outcome["proven_writes"] == ["AGENTS.md"]
    restored = Project(root).rule_distribution(action="rollback_partial", request={**request, "failure_ref": ref})
    assert restored["restored"] is True and not (root / "AGENTS.md").exists()
    assert not list((root / "fcop/internal/rule-distribution/deployments").glob("*.json"))


def test_rollback_receipt_interruption_has_a_recoverable_intent(distribution, monkeypatch):
    request = prepared(distribution)
    ref = deploy(distribution, request)
    root = distribution[3]
    original = (root / "AGENTS.md").read_bytes()
    append = _deployment.append_receipt

    def interrupt(root, kind, value, action):
        if kind == "deployments" and action == "rollback":
            raise OSError("Unit simulated storage interruption, not a forged success")
        return append(root, kind, value, action)

    monkeypatch.setattr(_deployment, "append_receipt", interrupt)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action="rollback", request={**request, "deployment_receipt_ref": ref})
    assert caught.value.code == "toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED"
    assert not (root / "AGENTS.md").exists()
    failure = caught.value.details["failure_ref"]
    assert caught.value.details["proven_writes"] == ["AGENTS.md"]
    restored = Project(root).rule_distribution(action="rollback_partial", request={**request, "failure_ref": failure})
    assert restored["restored"] is True
    assert (root / "AGENTS.md").read_bytes() == original
    assert len(list((root / "fcop/internal/rule-distribution/deployments").glob("*.json"))) == 1
