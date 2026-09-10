"""Pure deterministic framing and no-write deployment planning."""

from __future__ import annotations

import difflib
import posixpath
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._errors import reject
from ._files import ARTIFACT, INTERNAL, OWNERSHIP, RECOVERY, current_bytes, path_at
from ._loader import _Package, sha
from ._profiles import BEGIN, CURSOR, END
from ._receipts import deployment_chain, latest, managed, selected_inputs, verify_history


def framed(package: _Package, host: dict[str, Any], selected: dict[str, Any], target: str, action: str) -> bytes:
    header = (
        f"<!-- fcop:package={package.manifest['package_version']};manifest={package.manifest_sha256};"
        f"host={host['host_id']}@{host['profile_version']};assembly={selected['assembly_id']};"
        f"language={','.join(selected['selected_languages'])} -->\n"
    ).encode()
    chunks = [BEGIN, header]
    for artifact in selected["artifacts"]:
        module, language = artifact["module_id"], artifact["language"]
        raw = package.raw[module, language]
        # Current Manifest declares no separate relative-reference base. Never
        # silently relocate such a link into the Host's containing directory.
        text = raw.decode("utf-8")
        links = re.findall(r"\]\(([^)]+)\)|^\s*\[[^]]+\]:\s*(\S+)", text, flags=re.MULTILINE)
        for inline, definition in links:
            link = (inline or definition).strip().strip("<>")
            if not link.startswith(("https://", "http://")):
                reject(ARTIFACT, action, "Source reference has no proven target-relative base")
        if host["projection_mode"] == "reference":
            destination = f"{INTERNAL}/packages/{package.manifest_sha256}/{artifact['source_path']}"
            relative = posixpath.relpath(destination, posixpath.dirname(target) or ".")
            chunks.append(f"- [{module}:{language}]({relative}) sha256={artifact['sha256']}\n".encode())
        else:
            chunks.extend([f"<!-- fcop:module={module};language={language};sha256={artifact['sha256']} -->\n".encode(), raw, b"\n"])
    chunks.append(END)
    return b"".join(chunks)


def new_entry(host: dict[str, Any], block: bytes) -> bytes:
    """The complete new-file bytes shared by planning and read-only measurement."""
    return (CURSOR if host["host_id"] == "cursor" else b"") + block


def plan(root: Path, workspace: str, request: Mapping[str, Any], action: str = "plan") -> dict[str, Any]:
    package, host, profile_raw, selected = selected_inputs(root, workspace, request, action)
    targets: list[dict[str, Any]] = []
    backups: list[dict[str, str]] = []
    previous: dict[str, str] | None = None
    for relative in host["target_paths"]:
        path_at(root, relative, OWNERSHIP, action)
        before = current_bytes(root, relative, action)
        old = latest(root, workspace, relative, action)
        if old is not None:
            verify_history(root, workspace, old[0], action)
        explicit = request.get("previous_deployment_ref")
        if explicit is not None:
            deployment_chain(root, explicit, workspace, action)
            if old is None or old[0] != explicit:
                reject(RECOVERY, action, "Previous deployment is not the unique immediate predecessor")
        previous = old[0] if old else None
        block = framed(package, host, selected, relative, action)
        if before is None:
            if old is not None and any(t["after_sha256"] is not None for t in old[1]["targets"] if t["path"] == relative):
                reject(OWNERSHIP, action, "Previously owned target is missing")
            after = new_entry(host, block)
        else:
            if old is None:
                reject(OWNERSHIP, action, "Existing target has no proven ownership")
            old_target = next(t for t in old[1]["targets"] if t["path"] == relative)
            owned = managed(before, action)
            if sha(owned) != old_target["managed_region_sha256"]:
                reject(OWNERSHIP, action, "Managed bytes differ from previous receipt")
            if host["host_id"] == "cursor" and not before.startswith(CURSOR):
                reject(OWNERSHIP, action, "Unowned Cursor metadata")
            offset = before.index(BEGIN)
            after = before[:offset] + block + before[offset + len(owned):]
        if host["host_id"] == "cursor":
            for legacy in (".cursor/rules/fcop-rules.mdc", ".cursor/rules/fcop-protocol.mdc"):
                if path_at(root, legacy, OWNERSHIP, action).exists():
                    reject(OWNERSHIP, action, "Active legacy Cursor inputs cannot coexist")
        if len(after) > host["max_projection_bytes"]:
            reject("RULE_PROJECTION_LIMIT", action, "Full target exceeds the static profile cap")
        before_sha = sha(before) if before is not None else None
        expected = request.get("expected_target_sha256")
        if expected is not None and (not isinstance(expected, dict) or set(expected) != set(host["target_paths"]) or expected[relative] != before_sha):
            reject(OWNERSHIP, action, "Explicit target precondition is stale")
        backup = {"path": f"{INTERNAL}/backups/{sha(before)}.bin", "sha256": sha(before)} if before is not None else None
        if backup is not None:
            backups.append(backup)
        targets.append({
            "path": relative, "before_sha256": before_sha, "after_sha256": sha(after),
            "after_bytes": after, "size_bytes": len(after), "managed_region_sha256": sha(block),
            "backup_ref": backup,
            "diff": "".join(difflib.unified_diff((before or b"").decode().splitlines(keepends=True), after.decode().splitlines(keepends=True), fromfile=relative, tofile=relative)),
        })
    return {
        "selected_modules": selected["selected_modules"], "selected_languages": selected["selected_languages"],
        "manifest_sha256": package.manifest_sha256, "host_profile_sha256": sha(profile_raw),
        "targets": targets, "planned_backups": backups, "previous_deployment_ref": previous,
        "planned_receipt": {"receipt_schema": "fcop-rule-deployment/v1", "action": "deploy", "manifest_sha256": package.manifest_sha256,
                            "host_profile_sha256": sha(profile_raw), "adoption_receipt_ref": request.get("adoption_receipt_ref"),
                            "previous_deployment_ref": previous},
    }
