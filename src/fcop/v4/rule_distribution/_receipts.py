"""Immutable distribution evidence validation; no mutable adoption registry."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._errors import _DistributionError, reject
from ._files import (
    ADOPTION,
    ARTIFACT,
    INTERNAL,
    OWNERSHIP,
    RECOVERY,
    append_receipt,
    current_bytes,
    external_file,
    hexadecimal,
    path_at,
    receipt,
    timestamp,
)
from ._loader import _Package, load, parse, read_file, sha, text_bytes
from ._profiles import BEGIN, CURSOR, END, HOSTS, inspect_profile
from ._selection import select

ADOPTION_FIELDS = {
    "receipt_schema", "workspace_id", "protocol_version", "rule_package_version",
    "rule_manifest_sha256", "assembly_id", "selected_modules", "selected_languages",
    "selected_host_profile", "target_paths", "adopted_by", "adopted_at", "previous_receipt_ref",
}
DEPLOYMENT_FIELDS = {
    "receipt_schema", "adoption_receipt_ref", "manifest_sha256", "host_profile_sha256",
    "action", "previous_deployment_ref", "targets", "recorded_at",
}


def selection_evidence(ref: Any, action: str) -> None:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or not hexadecimal(ref["sha256"]):
        reject(ADOPTION, action, "Explicit ADMIN selection evidence required")
    raw = external_file(ref["path"], ADOPTION, action)
    text_bytes(raw, ADOPTION, action)
    if not raw.strip() or sha(raw) != ref["sha256"]:
        reject(ADOPTION, action, "Selection evidence identity mismatch")


def adoption_chain(root: Path, ref: Any, workspace: str, action: str) -> dict[str, Any]:
    first: dict[str, Any] | None = None
    seen: set[str] = set()
    while ref is not None:
        value = receipt(root, ref, "adoptions", ADOPTION, action)
        if ref["sha256"] in seen:
            reject(ADOPTION, action, "Cyclic adoption chain")
        seen.add(ref["sha256"])
        if (
            set(value) != ADOPTION_FIELDS or value["receipt_schema"] != "fcop-rule-adoption/v1"
            or value["workspace_id"] != workspace or value["protocol_version"] != "4.0"
            or not hexadecimal(value["rule_manifest_sha256"])
            or not isinstance(value["selected_host_profile"], dict)
            or set(value["selected_host_profile"]) != {"host_id", "profile_version", "sha256"}
            or not hexadecimal(value["selected_host_profile"].get("sha256"))
            or not isinstance(value["selected_host_profile"].get("host_id"), str)
            or value["selected_host_profile"].get("host_id") not in HOSTS
            or value["selected_host_profile"].get("profile_version") not in ("1.0-candidate.1", "reference-fixture.1")
            or not isinstance(value["rule_package_version"], str) or not value["rule_package_version"]
        ):
            reject(ADOPTION, action, "Invalid adoption field contract or workspace")
        from ._contract import MODULES

        expected = MODULES[:-1] if value["assembly_id"] == "sequential" else MODULES
        if (
            value["assembly_id"] not in ("sequential", "parallel")
            or value["selected_modules"] != expected
            or value["selected_languages"] not in (["en"], ["zh"])
            or value["target_paths"] != [HOSTS[value["selected_host_profile"]["host_id"]]]
        ):
            reject(ADOPTION, action, "Invalid adopted selection")
        timestamp(value["adopted_at"], ADOPTION, action)
        selection_evidence(value["adopted_by"], action)
        if first is None:
            first = value
        ref = value["previous_receipt_ref"]
    if first is None:
        reject(ADOPTION, action, "Missing adoption receipt")
    return first


def selected_inputs(root: Path, workspace: str, request: Mapping[str, Any], action: str,
                    *, require_adoption: bool = False) -> tuple[_Package, dict[str, Any], bytes, dict[str, Any]]:
    ref = request.get("adoption_receipt_ref")
    adopted = adoption_chain(root, ref, workspace, action) if ref is not None else None
    if require_adoption and adopted is None:
        reject(ADOPTION, action, "Explicit adoption receipt required")
    source = Path(request["manifest_path"]) if request.get("manifest_path") else Path(__file__).resolve().parents[2] / "rules/_data/v4/manifest.json"
    manifest_raw = external_file(str(source), ARTIFACT, action)
    preflight = parse(manifest_raw, "RULE_MANIFEST_INVALID", action)
    candidates = preflight.get("artifacts")
    if isinstance(candidates, list):
        for candidate in candidates:
            if isinstance(candidate, dict) and "source_path" in candidate:
                path_at(source.parent, candidate["source_path"], ARTIFACT, action)
    package = load(str(source), action)
    if sha(manifest_raw) != package.manifest_sha256:
        reject(ARTIFACT, action, "Manifest input changed or is indirect")
    for artifact in package.artifacts:
        raw_source = external_file(str(source.parent / artifact["source_path"]), ARTIFACT, action)
        if raw_source != package.raw[artifact["module_id"], artifact["language"]]:
            reject(ARTIFACT, action, "Artifact input changed or is indirect")
    host, raw = inspect_profile(request, action, adopted_reference=adopted is not None)
    selected = select(root, package, request, action, validated_profile=host)
    if selected["assembly_id"] == "repository-development":
        reject("RULE_SELECTION_INVALID", action, "Development references are not a business Host entry")
    if adopted is not None:
        expected = {
            "rule_package_version": package.manifest["package_version"],
            "rule_manifest_sha256": package.manifest_sha256,
            "assembly_id": selected["assembly_id"], "selected_modules": selected["selected_modules"],
            "selected_languages": selected["selected_languages"],
            "selected_host_profile": {"host_id": host["host_id"], "profile_version": host["profile_version"], "sha256": sha(raw)},
            "target_paths": host["target_paths"],
        }
        if any(adopted[k] != v for k, v in expected.items()):
            reject(ADOPTION, action, "Request differs from adopted bytes or selection")
    return package, host, raw, selected


def adoption_value(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    selection_evidence(request.get("admin_selection_ref"), action)
    previous = request.get("previous_receipt_ref")
    if previous is not None:
        adoption_chain(root, previous, workspace, action)
    try:
        package, host, raw, selected = selected_inputs(root, workspace, request, action)
    except _DistributionError as exc:
        if exc.code == "toolkit:RULE_HOST_UNAVAILABLE":
            reject(ADOPTION, action, "Profile is incompatible with adoption")
        raise
    return {
        "receipt_schema": "fcop-rule-adoption/v1", "workspace_id": workspace,
        "protocol_version": "4.0", "rule_package_version": package.manifest["package_version"],
        "rule_manifest_sha256": package.manifest_sha256, "assembly_id": selected["assembly_id"],
        "selected_modules": selected["selected_modules"], "selected_languages": selected["selected_languages"],
        "selected_host_profile": {"host_id": host["host_id"], "profile_version": host["profile_version"], "sha256": sha(raw)},
        "target_paths": host["target_paths"], "adopted_by": request["admin_selection_ref"],
        "adopted_at": timestamp(request.get("recorded_at"), ADOPTION, action), "previous_receipt_ref": previous,
    }


def adopt(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    value = adoption_value(root, workspace, request, action)
    return {"adoption_receipt_ref": append_receipt(root, "adoptions", value, action)}


def managed(raw: bytes, action: str) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        reject(OWNERSHIP, action, "Invalid preserved UTF-8")
    if "\ufeff" in text or "\r" in text or any(ord(c) < 32 and c not in "\t\n" or ord(c) == 127 for c in text):
        reject(OWNERSHIP, action, "Invalid preserved Encoding")
    if raw.count(BEGIN) != 1 or raw.count(END) != 1:
        reject(OWNERSHIP, action, "Missing or repeated managed block")
    start, end = raw.index(BEGIN), raw.index(END)
    if start > end or start > 0 and raw[start - 1:start] != b"\n":
        reject(OWNERSHIP, action, "Invalid managed marker position")
    return raw[start:end + len(END)]


def deployment_chain(root: Path, ref: Any, workspace: str, action: str) -> dict[str, Any]:
    seen: set[str] = set()
    first: dict[str, Any] | None = None
    while ref is not None:
        value = receipt(root, ref, "deployments", RECOVERY, action)
        if ref["sha256"] in seen or set(value) != DEPLOYMENT_FIELDS:
            reject(RECOVERY, action, "Invalid or cyclic deployment chain")
        seen.add(ref["sha256"])
        if value["receipt_schema"] != "fcop-rule-deployment/v1" or value["action"] not in ("deploy", "rollback"):
            reject(RECOVERY, action, "Unknown deployment contract")
        adopted = adoption_chain(root, value["adoption_receipt_ref"], workspace, action)
        if value["manifest_sha256"] != adopted["rule_manifest_sha256"] or value["host_profile_sha256"] != adopted["selected_host_profile"]["sha256"]:
            reject(RECOVERY, action, "Deployment is not bound to its adoption")
        timestamp(value["recorded_at"], RECOVERY, action)
        targets = value["targets"]
        if not isinstance(targets, list) or [t.get("path") for t in targets if isinstance(t, dict)] != adopted["target_paths"]:
            reject(RECOVERY, action, "Deployment target identity mismatch")
        for target in targets:
            if not isinstance(target, dict) or set(target) != {"path", "before_sha256", "after_sha256", "managed_region_sha256", "backup_ref"}:
                reject(RECOVERY, action, "Invalid target evidence fields")
            path_at(root, target["path"], RECOVERY, action)
            for key in ("before_sha256", "after_sha256", "managed_region_sha256"):
                if target[key] is not None and not hexadecimal(target[key]):
                    reject(RECOVERY, action, "Invalid target digest")
            if (target["backup_ref"] is None) != (target["before_sha256"] is None):
                reject(RECOVERY, action, "Missing recorded backup")
            if (target["after_sha256"] is None) != (target["managed_region_sha256"] is None) or value["action"] == "deploy" and target["after_sha256"] is None:
                reject(RECOVERY, action, "Invalid deployment outcome identity")
        if first is None:
            first = value
        ref = value["previous_deployment_ref"]
    if first is None:
        reject(RECOVERY, action, "Missing deployment receipt")
    return first


def latest(root: Path, workspace: str, target: str, action: str) -> tuple[dict[str, str], dict[str, Any]] | None:
    directory = path_at(root, f"{INTERNAL}/deployments", RECOVERY, action)
    records: dict[str, tuple[dict[str, str], dict[str, Any]]] = {}
    if directory.exists():
        for path in sorted(directory.glob("*.json")):
            ref = {"path": path.relative_to(root).as_posix(), "sha256": path.stem}
            value = deployment_chain(root, ref, workspace, action)
            if any(t["path"] == target for t in value["targets"]):
                records[path.stem] = ref, value
    parents = {v[1]["previous_deployment_ref"]["sha256"] for v in records.values() if v[1]["previous_deployment_ref"]}
    tails = [v for k, v in records.items() if k not in parents]
    if len(tails) > 1:
        reject(RECOVERY, action, "Ambiguous deployment history")
    return tails[0] if tails else None


def backup_bytes(root: Path, target: dict[str, Any], action: str) -> bytes | None:
    ref = target["backup_ref"]
    if ref is None:
        return None
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or ref["sha256"] != target["before_sha256"] or ref["path"] != f"{INTERNAL}/backups/{ref['sha256']}.bin":
        reject(RECOVERY, action, "Invalid backup identity")
    raw = read_file(path_at(root, ref["path"], RECOVERY, action), RECOVERY, action)
    if sha(raw) != ref["sha256"]:
        reject(RECOVERY, action, "Backup bytes changed")
    return raw


def recorded_inputs(root: Path, workspace: str, value: dict[str, Any], action: str) -> tuple[_Package, dict[str, Any], dict[str, Any]]:
    package_path = path_at(root, f"{INTERNAL}/packages/{value['manifest_sha256']}/manifest.json", ARTIFACT, action)
    package = load(str(package_path), action)
    if package.manifest_sha256 != value["manifest_sha256"]:
        reject(ARTIFACT, action, "Package snapshot changed")
    profile_path = path_at(root, f"{INTERNAL}/profiles/{value['host_profile_sha256']}.json", ARTIFACT, action)
    host, raw = inspect_profile({"host_profile_path": str(profile_path)}, action, adopted_reference=True)
    if sha(raw) != value["host_profile_sha256"]:
        reject(ARTIFACT, action, "Profile snapshot changed")
    adopted = adoption_chain(root, value["adoption_receipt_ref"], workspace, action)
    selection = select(root, package, {
        "assembly_id": adopted["assembly_id"], "selected_modules": adopted["selected_modules"],
        "selected_languages": adopted["selected_languages"], "host_profile_path": str(profile_path),
    }, action, validated_profile=host)
    if package.manifest["package_version"] != adopted["rule_package_version"] or host["target_paths"] != adopted["target_paths"]:
        reject(RECOVERY, action, "Snapshot selection differs from adoption")
    return package, host, selection


def verify_history(root: Path, workspace: str, ref: Any, action: str) -> None:
    # Validate old bytes too, not merely the currently selected snapshot.
    deployment_chain(root, ref, workspace, action)
    while ref is not None:
        value = receipt(root, ref, "deployments", RECOVERY, action)
        recorded_inputs(root, workspace, value, action)
        for target in value["targets"]:
            backup_bytes(root, target, action)
        ref = value["previous_deployment_ref"]


def verify_deployment(root: Path, workspace: str, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    from ._projection import framed

    ref = request.get("deployment_receipt_ref")
    value = deployment_chain(root, ref, workspace, action)
    verify_history(root, workspace, ref, action)
    package, host, selection = recorded_inputs(root, workspace, value, action)
    for target in value["targets"]:
        raw_target = current_bytes(root, target["path"], action)
        actual = sha(raw_target) if raw_target is not None else None
        if actual != target["after_sha256"]:
            reject(OWNERSHIP, action, "Full deployment target changed")
        if raw_target is not None:
            if sha(managed(raw_target, action)) != target["managed_region_sha256"]:
                reject(OWNERSHIP, action, "Managed region changed")
            if managed(raw_target, action) != framed(package, host, selection, target["path"], action):
                reject(ARTIFACT, action, "Projection order, source bytes or reference resolution differs")
            if host["host_id"] == "cursor" and not raw_target.startswith(CURSOR):
                reject(OWNERSHIP, action, "Cursor metadata changed")
        backup_bytes(root, target, action)
    return {"verified": True, "runtime_consumption_verified": None, "deployment_receipt_ref": ref}
