"""Deterministic schema source. Run --check for drift; no network or dependencies."""

import argparse
import json
from pathlib import Path

BASE = "https://fcop.dev/schemas/v4/"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
S = {"type": "string", "minLength": 1}
UUID = {"type": "string", "pattern": r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"}
SHA = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
OP = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"}
PATH = {"type": "string", "pattern": r"^fcop/_lifecycle/(inbox|active|review|done|archive)/TASK-[A-Za-z0-9][A-Za-z0-9._-]*\.md$"}
TIME = {"type": "string", "format": "date-time"}
STAGE = {"enum": ["inbox", "active", "review", "done", "archive"]}


def nullable(value):
    return {"anyOf": [value, {"type": "null"}]}


def array(value, **kwargs):
    return {"type": "array", "items": value, **kwargs}


def ref(name):
    return {"$ref": BASE + name + ".schema.json"}


def identity(kind):
    return {"type": "string", "pattern": "^" + kind + r"-[A-Za-z0-9][A-Za-z0-9._-]*$"}


def obj(properties, required=None, *, opened=False):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": opened}


def documents():
    schemas = {}
    schemas["workspace"] = obj({
        "protocol": {"const": "fcop"}, "protocol_version": {"const": "4.0"},
        "workspace_id": UUID, "profiles": array(S, uniqueItems=True),
        "encoding": obj({"name": {"const": "fcop-filesystem"}, "version": {"const": "4.0"}}),
    }, opened=True)
    schemas["transition"] = obj({
        "at": TIME, "from": nullable(S), "to": S, "by": S, "tool": S,
        "attempt_id": UUID, "evidence_ref": array(S), "evidence_digest": array(SHA),
        "authorization_ref": identity("REVIEW"), "authorization_digest": SHA,
        "family_digest": SHA,
    }, ["at", "from", "to", "by", "tool"])
    schemas["authorization-binding"] = obj({"from": STAGE, "to": STAGE})
    common = {
        "protocol": {"const": "fcop"}, "version": {"type": "integer", "const": 4},
        "workspace_id": UUID, "sender": S, "recipient": S, "created_at": TIME,
    }
    for kind, extra in {
        "TASK": {"subject": S, "transitions": array(ref("transition"))},
        "REPORT": {"subject_ref": S, "attempt_id": UUID,
                   "report_kind": {"enum": ["final", "replacement"]}, "result": S},
        "ISSUE": {"subject_ref": S, "severity": S},
        "REVIEW": {"subject_ref": S, "review_kind": S, "decision": S},
    }.items():
        properties = {**common, "type": {"const": kind}, kind.lower() + "_id": identity(kind), **extra}
        required = list(properties)
        properties.update({"references": array(S)})
        if kind == "TASK":
            properties.update({"parent": nullable(identity("TASK")),
                               "branch_of": nullable(identity("TASK")),
                               "priority": {"enum": ["P0", "P1", "P2", "P3"]},
                               "operation_id": OP, "operation_kind": {"const": "create_task"},
                               "normalized_request_digest": SHA})
        if kind == "REVIEW":
            properties.update({"attempt_id": nullable(UUID), "family_digest": nullable(SHA),
                               "authorization_ref": nullable(identity("REVIEW")), "profile_ref": nullable(S),
                               "transition": nullable(ref("authorization-binding")),
                               "issued_at": TIME, "expires_at": nullable(TIME),
                               "authorization_scope": nullable({"const": "single_use"}),
                               "operation_kind": {"const": "lifecycle_transition"}})
        schemas[kind.lower()] = obj(properties, required, opened=True)
        if kind == "REVIEW":
            schemas["review"]["allOf"] = [{
                "if": {"properties": {"review_kind": {"const": "authorization"}},
                       "required": ["review_kind"]},
                "then": {"required": ["operation_kind", "transition", "authorization_scope",
                                      "issued_at", "references", "profile_ref"],
                         "properties": {"decision": {"const": "authorize"},
                                        "profile_ref": S, "transition": ref("authorization-binding"),
                                        "authorization_scope": {"const": "single_use"}}},
            }]
    schemas["create-operation"] = obj({
        "contract": {"const": "fcop-create-task-v1"}, "key": SHA,
        "workspace_id": UUID, "operation_kind": {"const": "create_task"},
        "operation_id": OP, "task_id": identity("TASK"), "path": PATH,
        "digest": SHA, "content_digest": SHA,
    })
    schemas["create-request-canonical"] = obj({
        "contract": {"const": "fcop-create-task-v1"}, "workspace_id": UUID,
        "operation_kind": {"const": "create_task"}, "operation_id": OP,
        "sender": S, "recipient": S, "subject": S, "body": S,
        "priority": {"enum": ["P0", "P1", "P2", "P3"]},
        "parent": nullable(identity("TASK")), "branch_of": nullable(identity("TASK")),
        "references": array(S, uniqueItems=True),
    })
    receipt = {
        "contract": {"const": "fcop-lifecycle-receipt-v1"}, "version": {"const": 1},
        "operation_id": OP, "workspace_id": UUID, "task_id": identity("TASK"),
        "operation_kind": {"const": "lifecycle_transition"},
        "from_stage": STAGE, "to_stage": STAGE, "tool": S, "actor": S,
        "report_ref": nullable(identity("REPORT")), "source_path": PATH, "target_path": PATH,
        "source_digest": SHA, "target_digest": SHA, "normalized_transition_digest": SHA,
        "evidence_ref": array(S), "evidence_digest": array(SHA), "attempt_id": UUID,
        "transition": ref("transition"), "stage": {"enum": ["PREPARED", "TARGET_DURABLE", "COMMITTED"]},
    }
    authorized = {
        "review_ref": nullable(identity("REVIEW")), "authorization_ref": identity("REVIEW"),
        "authorization_digest": SHA, "profile_ref": S, "request_profile_ref": nullable(S),
        "source_attempt_id": UUID, "target_attempt_id": UUID, "family_digest": nullable(SHA),
    }
    schemas["lifecycle-receipt"] = {"oneOf": [
        obj({**receipt, "from_stage": {"enum": ["inbox", "active"]}}),
        obj({**receipt, "from_stage": {"enum": ["review", "done"]}, **authorized}),
    ]}
    schemas["recovery-observation"] = obj({
        "operation_id": OP, "source": PATH, "target": PATH,
        "stage": {"enum": ["PREPARED", "TARGET_DURABLE", "COMMITTED"]}, "content_digest": SHA,
    })
    schemas["family-canonical"] = obj({
        "contract": {"const": "fcop-family-v1"}, "root_task_id": identity("TASK"),
        "branches": array(obj({"branch_task_id": identity("TASK"), "attempt_id": UUID,
                               "report_id": identity("REPORT"), "report_digest": SHA})),
    })
    return {name: {"$schema": DRAFT, "$id": BASE + name + ".schema.json",
                   "title": "FCoP 4.0 " + name, "version": "4.0.0", **schema}
            for name, schema in schemas.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    package = source.parents[2] / "src/fcop/_data/schemas/v4"
    drift = []
    for name, schema in documents().items():
        data = (json.dumps(schema, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
        for folder in (source, package):
            path = folder / (name + ".schema.json")
            if args.check:
                if not path.exists() or path.read_bytes() != data:
                    drift.append(str(path))
            else:
                folder.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    if drift:
        raise SystemExit("Schema drift: " + ", ".join(drift))
    print(f"{len(documents())} schema pairs: {'verified' if args.check else 'generated'}")


if __name__ == "__main__":
    main()
