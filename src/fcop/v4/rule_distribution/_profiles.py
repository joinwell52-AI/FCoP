"""Static Host byte contracts, never probing or authorization evaluators."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ._errors import reject
from ._files import external_file, hexadecimal
from ._loader import parse, sha
from ._selection import _PROFILE_FIELDS

HOSTS = {"codex": "AGENTS.md", "cursor": ".cursor/rules/fcop-v4.mdc", "claude-code": "CLAUDE.md"}
BEGIN = b"<!-- fcop:v4:begin -->\n"
END = b"<!-- fcop:v4:end -->\n"
CURSOR = b"---\ndescription: FCoP 4.0 selected guidance\nalwaysApply: true\n---\n\n"
HOST_ERROR = "RULE_HOST_UNAVAILABLE"


def inspect_profile(request: Mapping[str, Any], action: str,
                    *, adopted_reference: bool = False,
                    measurement_only: bool = False) -> tuple[dict[str, Any], bytes]:
    raw = external_file(request.get("host_profile_path"), HOST_ERROR, action)
    value = parse(raw, HOST_ERROR, action)
    host = value.get("host_id")
    if not isinstance(host, str) or host not in HOSTS or set(value) != _PROFILE_FIELDS:
        reject(HOST_ERROR, action, "Unknown static Host profile")
    reference = value["profile_version"] == "reference-fixture.1"
    # The reviewed bilingual input is evidence for byte measurement only.
    # It does not extend candidate profile admission in any effectful caller.
    bilingual = measurement_only and value["profile_version"] == "explicit-bilingual-fixture.1"
    version = "explicit-bilingual-fixture.1" if bilingual else (
        "reference-fixture.1" if reference else "1.0-candidate.1"
    )
    if (
        value["profile_version"] != version
        or value["projection_mode"] != ("reference" if reference else "bounded_embed")
        or value["reference_mode"] != ("relative-path" if reference else "none")
        or value["target_paths"] != [HOSTS[host]]
        or value["supported_entry_kinds"] != (["cursor-mdc"] if host == "cursor" else ["markdown"])
        or value["preserve_regions"] != [[BEGIN.decode().strip(), END.decode().strip()]]
        or type(value["max_projection_bytes"]) is not int
        or value["max_projection_bytes"] != (8192 if reference else 65536)
        or value["encoding"] != "UTF-8-no-BOM" or value["newline"] != "LF"
        or value["languages"] not in ((["en", "zh"],) if bilingual else (["en"], ["zh"]))
    ):
        reject(HOST_ERROR, action, "Unproven static Host contract")
    if reference and not adopted_reference:
        ref = request.get("reference_support_ref")
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or not hexadecimal(ref["sha256"]):
            reject(HOST_ERROR, action, "Reference mode requires explicit isolated evidence")
        evidence = external_file(ref["path"], HOST_ERROR, action)
        expected = {
            "host_id": host, "profile_sha256": sha(raw), "resolution": "PASS", "order": "PASS",
            "integrity": "PASS", "failure": "PASS", "evidence_kind": "isolated-static-fixture",
            "runtime_consumption_verified": None,
        }
        if sha(evidence) != ref["sha256"] or parse(evidence, HOST_ERROR, action) != expected:
            reject(HOST_ERROR, action, "Reference support evidence mismatch")
    return value, raw
