"""Argument adaptation and read-only file discovery over public Project methods."""

from __future__ import annotations

from typing import Any

from fcop.errors import V4ProtocolError, _V4Code

from fcop_mcp.disposition import EDGES
from fcop_mcp.routing import Route


def unavailable(name: str) -> V4ProtocolError:
    return V4ProtocolError(
        _V4Code.OPERATION_NOT_IMPLEMENTED, f"{name} has no accepted v4 projection",
        operation_ref=name,
    )


def _refs(value: Any) -> Any:
    if isinstance(value, str):
        return [item for item in value.replace(",", " ").split() if item]
    return value


def invoke_v4(route: Route, name: str, policy: str, args: dict[str, Any]) -> Any:
    # Project binds version-specific instance signatures at runtime; class-level
    # annotations intentionally retain the unchanged legacy public signatures.
    project: Any = route.project
    if policy == "LEGACY_V3_ONLY":
        raise V4ProtocolError(
            _V4Code.LEGACY_TRANSITION_NOT_ALLOWED, f"{name} is legacy-only",
            operation_ref=name, subject_ref=args.get("task_id"),
        )
    if policy in EDGES:
        source, target = EDGES[policy]
        evidence = {key: args[key] for key in (
            "report_ref", "review_ref", "authorization_ref", "profile_ref", "family_digest",
        ) if args.get(key) is not None}
        return project.transition(
            task_id=args["task_id"], from_stage=source, to_stage=target,
            tool=name, actor=args.get("actor", "agent"), **evidence,
        )
    if policy == "CREATE_TASK":
        request = {key: args[key] for key in (
            "workspace_id", "operation_id", "sender", "recipient", "subject", "body",
            "priority", "parent", "branch_of", "thread_key", "risk_level",
        ) if args.get(key) is not None}
        request["references"] = _refs(args.get("references") or [])
        for relation in ("parent", "branch_of"):
            if request.get(relation) == "":
                del request[relation]
        return project.create_task(**request)
    if policy == "APPEND_REPORT":
        return project.write_report(
            workspace_id=args.get("workspace_id"), sender=args["reporter"],
            recipient=args["recipient"], body=args["body"], subject_ref=args["task_id"],
            attempt_id=args.get("attempt_id"), report_kind=args.get("report_kind", "final"),
            result=args.get("result") or args["status"], references=args.get("references") or [],
        )
    if policy == "APPEND_ISSUE":
        return project.write_issue(
            workspace_id=args.get("workspace_id"), sender=args["reporter"],
            recipient=args.get("recipient"), body=args["body"],
            subject_ref=args.get("subject_ref"), severity=args["severity"],
            references=args.get("references") or [],
        )
    if policy == "APPEND_AUTHORIZATION":
        return project.mark_human_approved(**{key: args.get(key) for key in (
            "review_id", "approver", "decision", "profile_ref", "from_stage", "to_stage",
            "attempt_id", "family_digest", "issued_at", "expires_at", "issuer_proof", "comment",
        )})
    if policy == "APPEND_REVIEW":
        fields = {key: args[key] for key in (
            "workspace_id", "recipient", "subject_ref", "review_kind", "decision", "body",
            "attempt_id", "family_digest", "authorization_ref", "profile_ref", "transition",
            "issued_at", "authorization_scope", "operation_kind", "issuer_proof", "expires_at",
        ) if args.get(key) is not None}
        fields["sender"] = args.get("reviewer_role", args.get("approver"))
        fields["references"] = args.get("references") or []
        if args.get("expires_at") is None:
            fields["expires_at"] = None
        return project.write_review(**fields)
    if policy == "READ_TASK":
        return project.read_task(args["filename"])
    if policy == "INSPECT":
        task_id = args["filename"].removesuffix(".md")
        result = project.inspect_state(task_id=task_id)
        if args.get("include_family_digest"):
            result["family_digest"] = project.family_digest(root_task_id=task_id)
        return result
    if policy == "READ_REPORT":
        return project.read_report(filename_or_id=args["filename"])
    if policy == "LIST_REPORT":
        if args.get("status") == "archived":
            raise V4ProtocolError(_V4Code.LEGACY_TRANSITION_NOT_ALLOWED,
                                  "v4 REPORT queries never read legacy history", operation_ref=name)
        return {"items": project.list_reports(
            subject_ref=args.get("task_id") or None, sender=args.get("reporter") or None,
            attempt_id=args.get("attempt_id") or None, head_only=args.get("head_only", False),
            limit=args.get("limit") or None, offset=args.get("offset", 0),
        )}
    if policy == "READ_REVIEW":
        bucket = "reports" if policy == "READ_REPORT" else "reviews"
        filename = args["filename"]
        if not filename.endswith(".md"):
            filename += ".md"
        return project.inspect_state(envelope_path=f"fcop/{bucket}/{filename}")
    if policy.startswith("LIST_"):
        kind = policy.removeprefix("LIST_")
        if kind == "TASK":
            paths = sorted((route.workspace_path / "fcop/_lifecycle").glob("*/TASK-*.md"))
            values = [{**project.read_task(path.stem), "stage": path.parent.name} for path in paths]
        else:
            paths = sorted((route.workspace_path / "fcop" / (kind.lower() + "s")).glob(f"{kind}-*.md"))
            values = [project.inspect_state(
                envelope_path=path.relative_to(route.workspace_path).as_posix(),
            ) for path in paths]
        # Filters and pagination are projections; they do not choose valid heads or authorize.
        aliases = {"task_id": "subject_ref", "reporter": "sender", "reviewer_role": "sender"}
        for key in ("sender", "recipient", "reporter", "task_id", "severity", "decision", "reviewer_role",
                    "stage", "parent", "branch_of", "review_kind", "subject_ref",
                    "attempt_id", "authorization_ref", "profile_ref"):
            if args.get(key):
                values = [item for item in values if item.get(aliases.get(key, key)) == args[key]]
        if args.get("references"):
            values = [item for item in values if set(args["references"]).issubset(item.get("references", []))]
        status = args.get("status", "open")
        if status not in {"open", "archived", "all"}:
            raise V4ProtocolError(_V4Code.INVALID_ENVELOPE, "Invalid status filter", operation_ref=name)
        if kind == "TASK":
            if status != "all":
                values = [item for item in values if (item["stage"] == "archive") == (status == "archived")]
            if args.get("date"):
                values = [item for item in values if args["date"] in item["task_id"]]
        elif status == "archived":
            raise V4ProtocolError(_V4Code.LEGACY_TRANSITION_NOT_ALLOWED,
                                  "v4 fact queries never read legacy history", operation_ref=name)
        if kind == "REVIEW" and args.get("subject_type"):
            values = [item for item in values
                      if item["subject_ref"].split("-", 1)[0].lower() == args["subject_type"].lower()]
        offset = args.get("offset", 0)
        limit = args.get("limit") or len(values)
        if offset < 0 or limit < 0:
            raise V4ProtocolError(_V4Code.INVALID_ENVELOPE, "Invalid pagination", operation_ref=name)
        return {"items": values[offset:offset + limit], "total": len(values),
                "projection": "validated_envelopes_not_gate_or_head_selection"}
    if policy in {"STATUS", "CHECK", "AUDIT"}:
        paths = sorted((route.workspace_path / "fcop/_lifecycle").glob("*/TASK-*.md"))
        return {"protocol_version": "4.0", "tasks": [project.inspect_state(task_id=p.stem) for p in paths],
                "projection": "read_only_not_authorization"}
    # Existing product governance and rule deployment cannot be re-labelled as v4.
    raise unavailable(name)
