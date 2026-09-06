"""Public-reader handlers over the one existing lifecycle REPORT graph resolver.

Reads use the existing short family lock, one group at a time. There is no
workspace transaction, persistent index, repair or reader-specific head rule.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from fcop.errors import _V4Code
from fcop.v4.encoding import ID_RE, _parse_envelope_bytes, digest, fail, safe_path, strict_text
from fcop.v4.lifecycle import family_root_for, report_head
from fcop.v4.linearization import family_boundary

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation


class ReportQueries:
    def __init__(self, creation: _Creation) -> None:
        self.creation = creation

    def _scan(self) -> tuple[dict[Path, bytes], dict[Path, dict[str, Any]]]:
        content: dict[Path, bytes] = {}
        rows: dict[Path, dict[str, Any]] = {}
        directory = safe_path(self.creation.root, "fcop/reports")
        try:
            for candidate in sorted(directory.glob("REPORT-*.md")):
                path = safe_path(self.creation.root, candidate.relative_to(self.creation.root).as_posix())
                raw = path.read_bytes()
                fields = self.creation._validate(_parse_envelope_bytes(raw), path)
                self.creation._relations(fields)
                content[path] = raw
                rows[path] = fields
        except OSError as exc:
            raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT inventory changed while reading") from exc
        return content, rows

    def list_reports(
        self, *, subject_ref: str | None = None, attempt_id: str | None = None,
        sender: str | None = None, head_only: bool = False,
        limit: int | None = None, offset: int = 0,
    ) -> list[dict[str, Any]]:
        self.creation._check()
        if (
            (attempt_id is not None and subject_ref is None)
            or any(value is not None and (not isinstance(value, str) or not value)
                   for value in (subject_ref, attempt_id, sender))
            or type(head_only) is not bool
            or (limit is not None and (type(limit) is not int or limit < 0))
            or type(offset) is not int or offset < 0
        ):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid REPORT query arguments")
        inventory, rows = self._scan()
        groups = sorted({(r["subject_ref"], r["attempt_id"]) for r in rows.values()})
        result: list[dict[str, Any]] = []
        for subject, attempt in groups:
            family = family_root_for(self.creation, subject)
            with family_boundary(self.creation.root, self.creation.manifest["workspace_id"], family):
                self.creation._check()
                if family_root_for(self.creation, subject) != family:
                    raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT family changed during query")
                current, fields_by_path = self._scan()
                if current != inventory:
                    raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT inventory changed during query")
                # The exact same resolver is also called by T3/T4/T5 and REPORT writers.
                head_path, head = report_head(self.creation, subject, attempt)
                group = {p: f for p, f in fields_by_path.items()
                         if (f["subject_ref"], f["attempt_id"]) == (subject, attempt)}
                ids = {f["report_id"] for f in group.values()}
                for path, fields in group.items():
                    if (subject_ref is not None and subject != subject_ref
                        or attempt_id is not None and attempt != attempt_id
                        or sender is not None and fields["sender"] != sender
                        or head_only and path != head_path):
                        continue
                    # Projection only: graph validity and unique head came from report_head.
                    replaces = next((ref for ref in fields.get("references", []) if ref in ids), None)
                    result.append({
                        **fields, "replaces": replaces if fields["report_kind"] == "replacement" else None,
                        "is_head": path == head_path, "head_ref": head["report_id"],
                        "head_digest": digest(current[head_path]),
                        "path": path.relative_to(self.creation.root).as_posix(),
                        "content": strict_text(current[path]),
                    })
                after, _ = self._scan()
                if after != current:
                    raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT changed across head resolution")
        final, _ = self._scan()
        if final != inventory:
            raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT inventory changed before query completion")
        if (head_only and subject_ref is not None and attempt_id is not None
                and (subject_ref, attempt_id) not in groups):
            raise fail(_V4Code.REPORT_REQUIRED, "Requested attempt has no REPORT", subject=subject_ref)
        result.sort(key=lambda row: (row["subject_ref"], row["attempt_id"], row["report_id"]))
        return result[offset:] if limit is None else result[offset:offset + limit]

    def read_report(self, filename_or_id: str) -> dict[str, Any]:
        self.creation._check()
        if not isinstance(filename_or_id, str):
            raise fail(_V4Code.INVALID_ENVELOPE, "Exact REPORT identity required")
        identity = filename_or_id.removesuffix(".md")
        if not ID_RE.fullmatch(identity) or not identity.startswith("REPORT-"):
            raise fail(_V4Code.INVALID_ENVELOPE, "Exact REPORT identity required")
        # list validates every group before returning. It never substitutes its head
        # for a requested replaced REPORT; returned content remains the requested file.
        rows = self.list_reports()
        found = [row for row in rows if row["report_id"] == identity]
        if not found:
            raise fail(_V4Code.INVALID_ENVELOPE, "REPORT does not exist", subject=identity)
        return found[0]
