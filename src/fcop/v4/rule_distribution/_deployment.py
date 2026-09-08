"""Short explicit distribution commits; no lifecycle, service or replay loop."""

from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, NoReturn
from uuid import uuid4

from fcop.errors import FcopError
from fcop.v4.encoding import (
    operation_lock,
    read_json,
    remove_authoritative,
    supported_local,
    sync_directory,
)

from ._errors import _DistributionError, reject
from ._files import (
    ADOPTION,
    ARTIFACT,
    INTERNAL,
    OWNERSHIP,
    RECOVERY,
    append_bytes,
    append_receipt,
    current_bytes,
    hexadecimal,
    json_bytes,
    path_at,
    receipt,
    timestamp,
)
from ._loader import read_file, sha
from ._profiles import CURSOR, HOSTS, inspect_profile
from ._projection import plan
from ._receipts import (
    adopt,
    adoption_chain,
    adoption_value,
    backup_bytes,
    deployment_chain,
    latest,
    managed,
    selected_inputs,
    verify_deployment,
)


def _safe_request(value: Any, action: str, depth: int = 0) -> None:
    if depth > 32:
        reject("RULE_SELECTION_INVALID", action, "Request nesting exceeds the bounded input shape")
    if callable(value):
        reject("RULE_HOST_UNAVAILABLE", action, "Caller executable logic is forbidden")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str) or any(term in key for term in ("evaluator", "resolver", "probe", "trusted_profiles", "caller_judge")):
                reject("RULE_HOST_UNAVAILABLE", action, "Caller judging or discovery fields are forbidden")
            _safe_request(item, action, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _safe_request(item, action, depth + 1)


def _move(stage: Path, target: Path, *, replace: bool) -> None:
    if stage.parent != target.parent:
        raise OSError("Distribution replacement must remain in its target directory")
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        move = ctypes.WinDLL("kernel32", use_last_error=True).MoveFileExW
        move.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD]
        move.restype = wintypes.BOOL
        if not move(str(stage), str(target), 0x8 | (0x1 if replace else 0)):
            raise ctypes.WinError(ctypes.get_last_error())
    elif replace:
        os.replace(stage, target)
    else:
        os.link(stage, target)
        sync_directory(target.parent)
        stage.unlink()
    sync_directory(target.parent)


def _stage(root: Path, relative: str, raw: bytes, action: str, *, durable: bool = True) -> Path:
    path = path_at(root, relative, RECOVERY, action)
    path.parent.mkdir(parents=True, exist_ok=True)
    path_at(root, relative, RECOVERY, action)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
        stream.flush()
        if durable:
            os.fsync(stream.fileno())
    if durable:
        sync_directory(path.parent)
        if path.read_bytes() != raw:
            reject(RECOVERY, action, "Staged bytes failed verification")
    return path


def _snapshot_package(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> None:
    package, _, profile_raw, _ = selected_inputs(root, workspace, request, action, require_adoption=True)
    source = Path(request["manifest_path"]) if request.get("manifest_path") else Path(__file__).resolve().parents[2] / "rules/_data/v4/manifest.json"
    raw = read_file(source, ARTIFACT, action)
    if sha(raw) != package.manifest_sha256:
        reject(ARTIFACT, action, "Manifest changed during preparation")
    prefix = f"{INTERNAL}/packages/{package.manifest_sha256}"
    for artifact in package.artifacts:
        append_bytes(root, f"{prefix}/{artifact['source_path']}", package.raw[artifact["module_id"], artifact["language"]], action)
    append_bytes(root, f"{prefix}/manifest.json", raw, action)
    append_bytes(root, f"{INTERNAL}/profiles/{sha(profile_raw)}.json", profile_raw, action)


def _target_evidence(target: dict[str, Any]) -> dict[str, Any]:
    return {k: target[k] for k in ("path", "before_sha256", "after_sha256", "managed_region_sha256", "backup_ref")}


def _result_value(request: Mapping[str, Any], planned: dict[str, Any], action: str) -> dict[str, Any]:
    return {
        **planned["planned_receipt"], "targets": [_target_evidence(t) for t in planned["targets"]],
        "recorded_at": timestamp(request.get("recorded_at"), RECOVERY, action),
    }


def _observe(root: Path, workspace: str, ref: Any, action: str) -> tuple[dict[str, Any], list[str]]:
    value = receipt(root, ref, "failures", RECOVERY, action)
    if set(value) != {"schema", "workspace_id", "targets", "success_refs", "nonce", "plan_sha256s"} or value["schema"] != "fcop-distribution-attempt/v1" or value["workspace_id"] != workspace:
        reject(RECOVERY, action, "Invalid failure identity")
    if not isinstance(value["targets"], list) or not 1 <= len(value["targets"]) <= 3:
        reject(RECOVERY, action, "Invalid bounded failure targets")
    nonce = value["nonce"]
    if not isinstance(nonce, str) or len(nonce) != 32 or any(c not in "0123456789abcdef" for c in nonce):
        reject(RECOVERY, action, "Invalid staging identity")
    writes = []
    seen = set()
    for target in value["targets"]:
        if not isinstance(target, dict) or set(target) != {"path", "before_sha256", "after_sha256", "managed_region_sha256", "backup_ref", "staging_path"}:
            reject(RECOVERY, action, "Invalid failure target fields")
        rel = target["path"]
        if not isinstance(rel, str) or rel not in HOSTS.values() or rel in seen:
            reject(RECOVERY, action, "Unproven failure target")
        seen.add(rel)
        if target["staging_path"] != Path(rel).with_name(f".fcop-distribution-{nonce}-{Path(rel).name}.tmp").as_posix():
            reject(RECOVERY, action, "Staging target is not bound to the attempt")
        if any(target[k] is not None and not hexadecimal(target[k]) for k in ("before_sha256", "after_sha256", "managed_region_sha256")):
            reject(RECOVERY, action, "Invalid failure digest")
        path_at(root, target["staging_path"], RECOVERY, action)
        raw = current_bytes(root, rel, action)
        actual = sha(raw) if raw is not None else None
        if actual not in (target["before_sha256"], target["after_sha256"]):
            reject(RECOVERY, action, "Partial target drift requires manual inspection")
        if actual == target["after_sha256"] and actual != target["before_sha256"]:
            writes.append(rel)
        # Before replacement an interruption may precede backup creation. An
        # observed changed target MUST already have its immutable old bytes.
        backup = target["backup_ref"]
        if backup is not None and (not isinstance(backup, dict) or set(backup) != {"path", "sha256"} or backup["sha256"] != target["before_sha256"] or backup["path"] != f"{INTERNAL}/backups/{target['before_sha256']}.bin"):
            reject(RECOVERY, action, "Invalid failure backup identity")
        if (backup is None) != (target["before_sha256"] is None):
            reject(RECOVERY, action, "Failure lacks original identity")
        if actual != target["before_sha256"] or backup is not None and path_at(root, backup["path"], RECOVERY, action).exists():
            backup_bytes(root, target, action)
    return value, writes


def _recovery_error(ref: dict[str, str], writes: list[str], action: str) -> NoReturn:
    error = _DistributionError(RECOVERY, action, "Distribution effects require explicit inspection")
    error.details.update(failure_ref=ref, proven_writes=writes, requires_explicit_recovery=True)
    raise error


def _pending(root: Path, workspace: str, targets: set[str], action: str) -> None:
    directory = path_at(root, f"{INTERNAL}/failures", RECOVERY, action)
    if not directory.exists():
        return
    for path in sorted(directory.glob("*.json")):
        ref = {"path": path.relative_to(root).as_posix(), "sha256": path.stem}
        value = receipt(root, ref, "failures", RECOVERY, action)
        recovery = path_at(root, f"{INTERNAL}/recovered/{path.stem}.json", RECOVERY, action)
        if recovery.is_file():
            recovered = read_json(recovery)
            if recovered != {"failure_ref": ref, "restored": True}:
                reject(RECOVERY, action, "Invalid recovery completion evidence")
            continue
        if value.get("success_refs") and all(path_at(root, r["path"], RECOVERY, action).is_file() for r in value["success_refs"]):
            for success in value["success_refs"]:
                deployment_chain(root, success, workspace, action)
            continue
        if targets.intersection(t.get("path") for t in value.get("targets", []) if isinstance(t, dict)):
            _, writes = _observe(root, workspace, ref, action)
            _recovery_error(ref, writes, action)


def _existing(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any] | None:
    if request.get("adoption_receipt_ref") is None or request.get("test_fault") is not None or "deployments" in request:
        return None
    package, host, profile_raw, _ = selected_inputs(root, workspace, request, action, require_adoption=True)
    old = latest(root, workspace, host["target_paths"][0], action)
    if old is None:
        return None
    ref, value = old
    if value["action"] != "deploy" or value["adoption_receipt_ref"] != request["adoption_receipt_ref"] or value["recorded_at"] != request.get("recorded_at"):
        return None
    if value["manifest_sha256"] != package.manifest_sha256 or value["host_profile_sha256"] != sha(profile_raw):
        return None
    # A new plan preserving changed user-owned bytes is an update, not an
    # exact replay of the last deployment. Validate it on the normal path.
    if any((sha(raw) if (raw := current_bytes(root, t["path"], action)) is not None else None) != t["after_sha256"] for t in value["targets"]):
        return None
    expected = request.get("expected_target_sha256")
    if expected is not None and expected != {t["path"]: t["before_sha256"] for t in value["targets"]}:
        reject(OWNERSHIP, action, "Retry target preconditions differ from the committed request")
    prior = request.get("previous_deployment_ref")
    supplied = request.get("plan")
    if supplied is not None:
        if not isinstance(supplied, dict) or supplied.get("manifest_sha256") != package.manifest_sha256 or supplied.get("host_profile_sha256") != sha(profile_raw):
            reject(OWNERSHIP, action, "Retry plan differs from current selection")
        prior = supplied.get("previous_deployment_ref")
        identities = []
        for path in path_at(root, f"{INTERNAL}/failures", RECOVERY, action).glob("*.json"):
            attempt = receipt(root, {"path": path.relative_to(root).as_posix(), "sha256": path.stem}, "failures", RECOVERY, action)
            if ref in attempt.get("success_refs", []):
                identities.extend(attempt.get("plan_sha256s", []))
        try:
            supplied_hash = _plan_hash(supplied)
        except (KeyError, TypeError, AttributeError, ValueError):
            reject(OWNERSHIP, action, "Malformed retry plan")
        if supplied_hash not in identities:
            reject(OWNERSHIP, action, "Retry requires the complete original plan")
    if prior is not None and prior != value["previous_deployment_ref"]:
        return None
    verify_deployment(root, workspace, {"deployment_receipt_ref": ref}, action)
    return {"deployment_receipt_ref": ref, "existing": True}


def apply(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    existing = _existing(root, workspace, request, action)
    if existing is not None:
        return existing
    batch = request.get("deployments")
    fault = request.get("test_fault")
    if fault is not None and (not isinstance(fault, dict) or set(fault) != {"window", "raise_after_observation"} or fault["window"] not in {"before_stage_durable", "between_replacements", "before_success_receipt"} or fault["raise_after_observation"] is not True):
        reject("RULE_SELECTION_INVALID", action, "Unknown deterministic failure seam")
    if batch is not None and (not isinstance(batch, list) or not 1 <= len(batch) <= 3 or fault is None or any(not isinstance(r, Mapping) for r in batch)):
        reject("RULE_SELECTION_INVALID", action, "Batch input is bounded failure verification only")
    requests = [dict(r) for r in batch] if batch is not None and all(isinstance(r, Mapping) for r in batch) else [dict(request)]
    plans = []
    adoptions: list[dict[str, Any] | None] = []
    for item in requests:
        if item.get("workspace_id", workspace) != workspace or item.get("protocol_version", "4.0") != "4.0":
            reject(ADOPTION, action, "Deployment workspace selection mismatch")
        if item.get("adoption_receipt_ref") is None:
            if batch is None and item.get("adopt_if_authorized") is not True:
                reject(ADOPTION, action, "Deployment requires explicit adoption")
            adoptions.append(adoption_value(root, workspace, item, action))
        else:
            selected_inputs(root, workspace, item, action, require_adoption=True)
            adoptions.append(None)
        candidate = plan(root, workspace, item, action)
        if item.get("plan") is not None and item["plan"] != candidate:
            reject(OWNERSHIP, action, "Supplied plan is stale or altered")
        timestamp(item.get("recorded_at"), RECOVERY, action)
        plans.append(candidate)
    paths = [t["path"] for p in plans for t in p["targets"]]
    if len(set(paths)) != len(paths):
        reject("RULE_SELECTION_INVALID", action, "Overlapping targets in bounded input")
    supported_local(Path(str(root)[4:]) if str(root).startswith("\\\\?\\") else root)
    directory = path_at(root, INTERNAL, RECOVERY, action)
    directory.mkdir(parents=True, exist_ok=True)
    # A bounded file-only commit can include slow native flushes. Wait for
    # the actual writer before classifying its intent; no lease or replay.
    with operation_lock(path_at(root, f"{INTERNAL}/commit.lock", RECOVERY, action), timeout=45):
        _pending(root, workspace, set(paths), action)
        # Under coordination the full plan and all raw inputs are read again.
        for item, prior in zip(requests, plans, strict=True):
            if plan(root, workspace, item, action) != prior:
                reject(OWNERSHIP, action, "Plan changed before commit")
        for item, value in zip(requests, adoptions, strict=True):
            if value is not None:
                if adoption_value(root, workspace, item, action) != value:
                    reject(ADOPTION, action, "Selection authority changed")
                item["adoption_receipt_ref"] = append_receipt(root, "adoptions", value, action)
        plans = [plan(root, workspace, item, action) for item in requests]
        values = [_result_value(item, p, action) for item, p in zip(requests, plans, strict=True)]
        success_refs = _commit_targets(root, workspace, plans, values, action, requests=requests, fault=fault)
    return {"deployment_receipt_ref": success_refs[0], "existing": False}

def _plan_hash(planned: Mapping[str, Any]) -> str:
    encoded = {**planned, "targets": [
        {**t, "after_bytes": t["after_bytes"].hex() if t.get("after_bytes") is not None else None}
        for t in planned["targets"]
    ]}
    return sha(json_bytes(encoded))


def _commit_targets(root: Path, workspace: str, plans: list[dict[str, Any]],
                    values: list[dict[str, Any]], action: str, *,
                    requests: list[dict[str, Any]] | None = None,
                    fault: dict[str, Any] | None = None,
                    adoption: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """One physical commit path, called with the existing short lock held.

    The intent is not a success or a replay queue. A caller must explicitly
    inspect/recover it after interruption. Target replacement is single-file.
    """
    success_refs = [{"path": f"{INTERNAL}/deployments/{sha(json_bytes(v))}.json", "sha256": sha(json_bytes(v))} for v in values]
    nonce = uuid4().hex
    flattened = [t for p in plans for t in p["targets"]]
    intents = [{**_target_evidence(t), "staging_path": Path(t["path"]).with_name(
        f".fcop-distribution-{nonce}-{Path(t['path']).name}.tmp").as_posix()} for t in flattened]
    ref = append_receipt(root, "failures", {
        "schema": "fcop-distribution-attempt/v1", "workspace_id": workspace,
        "targets": intents, "success_refs": success_refs, "nonce": nonce,
        "plan_sha256s": [_plan_hash(p) for p in plans],
    }, action)
    try:
        for request in requests or []:
            _snapshot_package(root, workspace, request, action)
        for i, (target, intent) in enumerate(zip(flattened, intents, strict=True)):
            desired = target["after_bytes"]
            stage = None
            if desired is not None:
                stage = _stage(root, intent["staging_path"], desired, action,
                               durable=not (fault and fault["window"] == "before_stage_durable"))
            if fault and fault["window"] == "before_stage_durable":
                raise OSError("Injected pre-durability observation")
            raw = current_bytes(root, target["path"], action)
            if (sha(raw) if raw is not None else None) != target["before_sha256"]:
                raise OSError("Target changed before backup")
            if raw is not None:
                append_bytes(root, target["backup_ref"]["path"], raw, action)
                backup_bytes(root, intent, action)
            if current_bytes(root, target["path"], action) != raw:
                raise OSError("Target changed immediately before replacement")
            path = path_at(root, target["path"], OWNERSHIP, action)
            if stage is None:
                if raw is not None:
                    remove_authoritative(path)
            else:
                _move(stage, path, replace=raw is not None)
            if current_bytes(root, target["path"], action) != desired:
                raise OSError("Replacement verification failed")
            if fault and fault["window"] == "between_replacements" and i == 0:
                raise OSError("Injected partial replacement observation")
        if fault and fault["window"] == "before_success_receipt":
            raise OSError("Injected pre-receipt observation")
        if adoption is not None:
            append_receipt(root, "adoptions", adoption, action)
        for value in values:
            append_receipt(root, "deployments", value, action)
    except (OSError, FcopError):
        try:
            _, writes = _observe(root, workspace, ref, action)
        except (OSError, FcopError):
            # Preserve the recorded reference even when external drift prevents
            # proving any completed write; never invent a partial success.
            writes = []
        _recovery_error(ref, writes, action)
    return success_refs



def inspect_failure(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    _, writes = _observe(root, workspace, request.get("failure_ref"), action)
    return {"failure_ref": request["failure_ref"], "proven_writes": writes, "requires_explicit_recovery": True}


def rollback_partial(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    ref = request.get("failure_ref")
    value, _ = _observe(root, workspace, ref, action)
    if not isinstance(ref, dict):
        reject(RECOVERY, action, "Explicit failure reference required")
    if any(path_at(root, r["path"], RECOVERY, action).exists() for r in value["success_refs"]):
        reject(RECOVERY, action, "Successful deployment requires explicit normal rollback")
    with operation_lock(path_at(root, f"{INTERNAL}/commit.lock", RECOVERY, action)):
        value, writes = _observe(root, workspace, ref, action)
        try:
            for t in value["targets"]:
                if t["path"] not in writes:
                    continue
                path = path_at(root, t["path"], RECOVERY, action)
                old = backup_bytes(root, t, action)
                if old is None:
                    remove_authoritative(path)
                else:
                    stage = _stage(root, path.with_name(f".fcop-restore-{uuid4().hex}.tmp").relative_to(root).as_posix(), old, action)
                    present = current_bytes(root, t["path"], action)
                    if (sha(present) if present is not None else None) != t["after_sha256"]:
                        _recovery_error(ref, writes, action)
                    _move(stage, path, replace=present is not None)
                if current_bytes(root, t["path"], action) != old:
                    _recovery_error(ref, writes, action)
            append_bytes(root, f"{INTERNAL}/recovered/{ref['sha256']}.json", json_bytes({"failure_ref": ref, "restored": True}), action)
        except (OSError, FcopError):
            _recovery_error(ref, writes, action)
    return {"restored": True, "failure_ref": ref}


def rollback(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    if "package_version" in request:
        reject(RECOVERY, action, "Arbitrary rollback label is forbidden")
    ref = request.get("deployment_receipt_ref")
    moment = timestamp(request.get("recorded_at"), RECOVERY, action)
    original = deployment_chain(root, ref, workspace, action)
    tail = latest(root, workspace, original["targets"][0]["path"], action)
    if tail is not None and tail[1]["action"] == "rollback" and tail[1]["previous_deployment_ref"] == ref and tail[1]["recorded_at"] == moment:
        verify_deployment(root, workspace, {"deployment_receipt_ref": tail[0]}, action)
        return {"deployment_receipt_ref": tail[0], "existing": True}
    try:
        verify_deployment(root, workspace, request, action)
        value = deployment_chain(root, ref, workspace, action)
        adopted = adoption_chain(root, value["adoption_receipt_ref"], workspace, action)
        for t in value["targets"]:
            previous = latest(root, workspace, t["path"], action)
            if previous is None or previous[0] != ref:
                reject(RECOVERY, action, "Rollback is not at the immediate history tail")
        prior = value["previous_deployment_ref"]
        previous_value = deployment_chain(root, prior, workspace, action) if prior else None
        restore = [backup_bytes(root, t, action) for t in value["targets"]]
        if previous_value is not None:
            previous_adoption = previous_value["adoption_receipt_ref"]
            adoption_chain(root, previous_adoption, workspace, action)
        else:
            previous_adoption = value["adoption_receipt_ref"]
        for t, raw in zip(value["targets"], restore, strict=True):
            if raw is None:
                current = current_bytes(root, t["path"], action)
                if current is None or current not in (managed(current, action), CURSOR + managed(current, action)):
                    reject(RECOVERY, action, "Removal requires unchanged managed-only target")
            elif previous_value is not None:
                expected = next(p for p in previous_value["targets"] if p["path"] == t["path"])
                if sha(managed(raw, action)) != expected["managed_region_sha256"]:
                    reject(RECOVERY, action, "Backup does not retain the immediate predecessor's owned region")
    except _DistributionError:
        reject(RECOVERY, action, "Rollback evidence is not complete and unchanged")
    moment = timestamp(request.get("recorded_at"), RECOVERY, action)
    predecessor_adoption = adoption_chain(root, previous_adoption, workspace, action)
    new_adoption = {**predecessor_adoption, "previous_receipt_ref": value["adoption_receipt_ref"],
                    "adopted_at": moment, "adopted_by": adopted["adopted_by"]}
    adoption_digest = sha(json_bytes(new_adoption))
    adoption_ref = {"path": f"{INTERNAL}/adoptions/{adoption_digest}.json", "sha256": adoption_digest}
    targets = []
    for target, old in zip(value["targets"], restore, strict=True):
        digest = target["after_sha256"]
        targets.append({
            "path": target["path"], "before_sha256": digest, "after_sha256": sha(old) if old is not None else None,
            "after_bytes": old, "managed_region_sha256": sha(managed(old, action)) if old is not None else None,
            "backup_ref": {"path": f"{INTERNAL}/backups/{digest}.bin", "sha256": digest} if digest else None,
        })
    result = {"receipt_schema": "fcop-rule-deployment/v1", "adoption_receipt_ref": adoption_ref,
              "manifest_sha256": predecessor_adoption["rule_manifest_sha256"],
              "host_profile_sha256": predecessor_adoption["selected_host_profile"]["sha256"],
              "action": "rollback", "previous_deployment_ref": ref,
              "targets": [_target_evidence(t) for t in targets], "recorded_at": moment}
    _pending(root, workspace, {t["path"] for t in targets}, action)
    with operation_lock(path_at(root, f"{INTERNAL}/commit.lock", RECOVERY, action)):
        _pending(root, workspace, {t["path"] for t in targets}, action)
        verify_deployment(root, workspace, request, action)
        for target in targets:
            tail = latest(root, workspace, target["path"], action)
            if tail is None or tail[0] != ref:
                reject(RECOVERY, action, "Rollback predecessor changed before commit")
        # Evidence and all backups are validated again before touching targets.
        if [backup_bytes(root, t, action) for t in value["targets"]] != restore:
            reject(RECOVERY, action, "Rollback backup changed before commit")
        refs = _commit_targets(root, workspace, [{"targets": targets}], [result], action, adoption=new_adoption)
    return {"deployment_receipt_ref": refs[0]}


def dispatch(root: Path, action: str, request: Mapping[str, Any]) -> dict[str, Any]:
    _safe_request(request, action)
    # Private Win32 I/O spelling only: logical/receipt paths remain relative.
    # This is neither Host probing nor a machine path in a projected file.
    if os.name == "nt" and not str(root).startswith("\\\\"):
        root = Path("\\\\?\\" + str(root))
    workspace = read_json(path_at(root, "fcop/fcop.json", ADOPTION, action))["workspace_id"]
    if action in {"inspect_profile", "status"}:
        ref = request.get("adoption_receipt_ref")
        deployment = request.get("deployment_receipt_ref")
        generated = False
        if deployment is not None:
            verify_deployment(root, workspace, request, action)
            ref = deployment_chain(root, deployment, workspace, action)["adoption_receipt_ref"]
            generated = True
        adopted = adoption_chain(root, ref, workspace, action) if ref else None
        host, _ = inspect_profile(request, action, adopted_reference=adopted is not None)
        if adopted is not None:
            selected_inputs(root, workspace, {**request, "adoption_receipt_ref": ref}, action, require_adoption=True)
        return {**host, "adapter_supported": True, "admin_adopted": adopted is not None,
                "entry_generated": generated, "runtime_consumption_verified": None}
    handlers = {"adopt": adopt, "plan": plan, "apply": apply, "verify_deployment": verify_deployment,
                "rollback": rollback, "inspect_failure": inspect_failure, "rollback_partial": rollback_partial}
    return handlers[action](root, workspace, request, action)
