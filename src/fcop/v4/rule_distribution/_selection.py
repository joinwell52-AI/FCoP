"""Explicit assemblies; guidance is never lifecycle authority or Host output."""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._contract import MODULES, RELATIONS
from ._errors import reject
from ._loader import _Package, contained, parse, read_file, sha, text_bytes

_SELECTION = "RULE_SELECTION_INVALID"
_HOST = "RULE_HOST_UNAVAILABLE"
_EXCLUDED = "87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c"
_PROFILE_FIELDS = {
    "host_id", "profile_version", "supported_entry_kinds", "reference_mode",
    "projection_mode", "target_paths", "preserve_regions", "max_projection_bytes",
    "encoding", "newline", "languages",
}


def profile(request: Mapping[str, Any], action: str) -> dict[str, Any]:
    path = request.get("host_profile_path")
    if not isinstance(path, str) or not path or "\x00" in path or not Path(path).is_absolute():
        reject(_HOST, action, "Explicit local Host profile required")
    value = parse(read_file(Path(path), _HOST, action), _HOST, action)
    targets = {"codex": "AGENTS.md", "cursor": ".cursor/rules/fcop-v4.mdc", "claude-code": "CLAUDE.md"}
    host = value.get("host_id")
    if not isinstance(host, str) or host not in targets or set(value) != _PROFILE_FIELDS:
        reject(_HOST, action, "Unknown Host or profile fields")
    if (
        value["profile_version"] != "1.0-candidate.1"
        or value["projection_mode"] != "bounded_embed" or value["reference_mode"] != "none"
        or value["target_paths"] != [targets[host]]
        or value["supported_entry_kinds"] != (["cursor-mdc"] if host == "cursor" else ["markdown"])
        or value["preserve_regions"] != [["<!-- fcop:v4:begin -->", "<!-- fcop:v4:end -->"]]
        or type(value["max_projection_bytes"]) is not int or value["max_projection_bytes"] != 65536
        or value["encoding"] != "UTF-8-no-BOM" or value["newline"] != "LF"
        or value["languages"] not in (["en"], ["zh"])
    ):
        reject(_HOST, action, "Unproven Host profile contract")
    return value


def development(root: Path, request: Mapping[str, Any], action: str) -> dict[str, Any]:
    refs = request.get("development_references")
    if (
        not isinstance(refs, list) or len(refs) != 4
        or request.get("constitution_ref") is not None or request.get("source_dependencies")
    ):
        reject(_SELECTION, action, "Four explicit development references required")
    paths: set[str] = set()
    result: list[dict[str, Any]] = []
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != {"path", "revision", "sha256"}:
            reject(_SELECTION, action, "Incomplete pinned development reference")
        path, revision, digest = ref["path"], ref["revision"], ref["sha256"]
        if (
            not isinstance(path, str) or not path.startswith("docs/fcop-4.0/development/")
            or path in paths or not isinstance(revision, str)
            or re.fullmatch(r"[0-9a-f]{40}", revision) is None or revision == "0" * 40
            or not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            or digest in {_EXCLUDED, "0" * 64}
        ):
            reject(_SELECTION, action, "Invalid or excluded development identity")
        raw = read_file(contained(root, path, _SELECTION, action), _SELECTION, action)
        text_bytes(raw, _SELECTION, action)
        if sha(raw) != digest:
            reject(_SELECTION, action, "Development reference byte mismatch")
        paths.add(path)
        result.append(dict(ref))
    return {
        "assembly_id": "repository-development", "references": result,
        "constitution_ref": None, "business_modules": [], "selected_modules": [],
        "artifacts": [], "guidance": b"",
    }


def select(root: Path, package: _Package, request: Mapping[str, Any], action: str,
           *, validated_profile: dict[str, Any] | None = None) -> dict[str, Any]:
    if request.get("source_dependencies"):
        reject(_SELECTION, action, "Unadopted source dependency")
    assembly = request.get("assembly_id")
    if assembly == "repository-development":
        return {"protocol_version": "4.0", **development(root, request, action)}
    if assembly not in ("sequential", "parallel"):
        reject(_SELECTION, action, "Unknown assembly")
    expected = MODULES[:-1] if assembly == "sequential" else MODULES
    modules, languages = request.get("selected_modules"), request.get("selected_languages")
    if (
        not isinstance(modules, list) or not all(isinstance(m, str) for m in modules)
        or len(modules) != len(expected) or set(modules) != set(expected)
        or languages not in (["en"], ["zh"])
        or request.get("relation_fields", RELATIONS) != RELATIONS
    ):
        reject(_SELECTION, action, "Explicit closed modules, language and relations required")
    host = profile(request, action) if validated_profile is None else validated_profile
    if languages != host["languages"]:
        reject(_SELECTION, action, "Language is not adopted by the selected profile")
    artifacts = [a for a in package.artifacts if a["module_id"] in expected and a["language"] in languages]
    return {
        **package.summary(), "assembly_id": assembly, "selected_modules": list(expected),
        "selected_languages": list(languages), "relation_fields": list(RELATIONS),
        "artifacts": artifacts,
        "guidance": b"\n".join(package.raw[(m, lang)] for m in expected for lang in languages),
    }


def operation_scope(selected: dict[str, Any], request: Mapping[str, Any], action: str) -> dict[str, Any]:
    operation = request.get("operation")
    family_operations = {"create_branch", "family_digest", "convergence", "write_convergence", "root_archive"}
    ordinary_operations = {
        "create_task", "write_report", "write_review", "write_issue", "transition",
        "read_task", "list_reports", "read_report", "inspect_state", "recover_operation", "export_archive",
    }
    if not isinstance(operation, str) or operation not in family_operations | ordinary_operations:
        reject(_SELECTION, action, "Known explicit protocol operation required")
    family = operation in family_operations or bool(request.get("branch_of")) or bool(request.get("root_task_id")) or request.get("review_kind") == "convergence"
    if selected["assembly_id"] == "repository-development" or (family and selected["assembly_id"] != "parallel"):
        reject(_SELECTION, action, "Assembly lacks operation guidance")
    return {**selected, "guidance_complete": True, "lifecycle_authorized": False}
