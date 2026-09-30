# FCoP 4.0.5 Canonical MCP Tools

The default MCP server exposes **25 Canonical MCP Tools + 6 read-only Core Resources**. The 25 tools below and the schema snapshot are generated from `fcop_mcp.canonical_tools.MANIFEST` and the registered Python signatures. FCoP Core owns every protocol fact and transition. Profiles, Toolkit commands, compatibility shims, Host configuration, Runtime services, packaging and application scaffolding are separate.

Start the server with an explicit `--root PATH` or `FCOP_PROJECT_DIR`. Call `init_workspace` to create a pure v4 workspace. It does not generate host instruction files, Team/Solo/ME roles, seats, or session state. An optional `profile` is an explicit reference; it does not grant authority without a trusted evaluator installed at server startup.

## workspace

### `init_workspace`

Create only a canonical FCoP 4.0 workspace at the server-bound root. An optional explicit profile is a reference, never executable authority.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "type": "object"
}
```

### `inspect_workspace`

Inspect protocol identity, envelopes, lifecycle, families and recovery facts without repair.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

### `validate_workspace`

Deterministically validate canonical workspace facts through Core validators; never repair or consult host/runtime state.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {},
  "type": "object"
}
```

## task

### `create_task`

Create a TASK using Core T1 and its workspace-scoped operation identity. Repeated requests retain Core idempotency semantics.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "workspace_id": {
      "type": "string"
    },
    "operation_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    },
    "subject": {
      "type": "string"
    },
    "body": {
      "type": "string"
    },
    "priority": {
      "default": "P2",
      "type": "string"
    },
    "references": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "parent": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "branch_of": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "thread_key": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "risk_level": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "workspace_id",
    "operation_id",
    "sender",
    "recipient",
    "subject",
    "body"
  ],
  "type": "object"
}
```

### `claim_task`

Request Core T2 inbox to active; actor records attribution and grants no authority.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "actor"
  ],
  "type": "object"
}
```

### `submit_task`

Request Core T3 active to review with the explicit current-attempt REPORT.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    },
    "report_ref": {
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "actor",
    "report_ref"
  ],
  "type": "object"
}
```

### `approve_task`

Request Core T4 review to done using independently validated review and authorization evidence.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    },
    "report_ref": {
      "type": "string"
    },
    "review_ref": {
      "type": "string"
    },
    "authorization_ref": {
      "type": "string"
    },
    "profile_ref": {
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "actor",
    "report_ref",
    "review_ref",
    "authorization_ref",
    "profile_ref"
  ],
  "type": "object"
}
```

### `reject_task`

Request Core T5 review to active; Core validates evidence and advances the attempt.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    },
    "report_ref": {
      "type": "string"
    },
    "review_ref": {
      "type": "string"
    },
    "authorization_ref": {
      "type": "string"
    },
    "profile_ref": {
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "actor",
    "report_ref",
    "review_ref",
    "authorization_ref",
    "profile_ref"
  ],
  "type": "object"
}
```

### `reopen_task`

Request Core T6 done to active with explicit reopen evidence and authorization.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    },
    "review_ref": {
      "type": "string"
    },
    "authorization_ref": {
      "type": "string"
    },
    "profile_ref": {
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "actor",
    "review_ref",
    "authorization_ref",
    "profile_ref"
  ],
  "type": "object"
}
```

### `archive_task`

Request Core T7 done to archive; Core enforces authorization and family convergence.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    },
    "actor": {
      "type": "string"
    },
    "authorization_ref": {
      "type": "string"
    },
    "profile_ref": {
      "type": "string"
    },
    "review_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "family_digest": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "task_id",
    "actor",
    "authorization_ref",
    "profile_ref"
  ],
  "type": "object"
}
```

### `inspect_task`

Read Core lifecycle, current attempt and transition evidence for a TASK.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    }
  },
  "required": [
    "task_id"
  ],
  "type": "object"
}
```

### `list_tasks`

List validated canonical TASK facts, optionally filtered by stage or relations.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "stage": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "sender": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "recipient": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "parent": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "branch_of": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "offset": {
      "default": 0,
      "type": "integer"
    },
    "limit": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "type": "object"
}
```

### `read_task`

Read a canonical TASK by its typed identity through Core.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string"
    }
  },
  "required": [
    "task_id"
  ],
  "type": "object"
}
```

## branch

### `create_branch`

Create a branch TASK through Core T1 with an explicit branch_of relation.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "root_task_id": {
      "type": "string"
    },
    "workspace_id": {
      "type": "string"
    },
    "operation_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    },
    "subject": {
      "type": "string"
    },
    "body": {
      "type": "string"
    },
    "priority": {
      "default": "P2",
      "type": "string"
    }
  },
  "required": [
    "root_task_id",
    "workspace_id",
    "operation_id",
    "sender",
    "recipient",
    "subject",
    "body"
  ],
  "type": "object"
}
```

### `inspect_family`

Read Core family membership, REPORT heads, digest and convergence readiness.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "root_task_id": {
      "type": "string"
    }
  },
  "required": [
    "root_task_id"
  ],
  "type": "object"
}
```

### `merge_branches`

Record the caller's convergence decision atomically in Core; never choose winners or archive the root.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "root_task_id": {
      "type": "string"
    },
    "workspace_id": {
      "type": "string"
    },
    "expected_family_digest": {
      "type": "string"
    },
    "branch_report_heads": {
      "additionalProperties": {
        "type": "string"
      },
      "type": "object"
    },
    "conclusion": {
      "type": "string"
    },
    "conflict_resolution": {
      "type": "string"
    },
    "operation_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    }
  },
  "required": [
    "root_task_id",
    "workspace_id",
    "expected_family_digest",
    "branch_report_heads",
    "conclusion",
    "conflict_resolution",
    "operation_id",
    "sender",
    "recipient"
  ],
  "type": "object"
}
```

## envelope-write

### `write_report`

Append a Core REPORT for the explicit TASK attempt; reporting does not accept or archive work.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "workspace_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    },
    "subject_ref": {
      "type": "string"
    },
    "attempt_id": {
      "type": "string"
    },
    "body": {
      "type": "string"
    },
    "result": {
      "type": "string"
    },
    "report_kind": {
      "default": "final",
      "type": "string"
    },
    "references": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "workspace_id",
    "sender",
    "recipient",
    "subject_ref",
    "attempt_id",
    "body",
    "result"
  ],
  "type": "object"
}
```

### `write_issue`

Append a Core ISSUE with explicit workspace and subject identity.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "workspace_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    },
    "subject_ref": {
      "type": "string"
    },
    "body": {
      "type": "string"
    },
    "severity": {
      "type": "string"
    },
    "references": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "workspace_id",
    "sender",
    "recipient",
    "subject_ref",
    "body",
    "severity"
  ],
  "type": "object"
}
```

### `write_review`

Append a typed Core REVIEW. Authority is evaluated only by trusted startup Profile evaluators.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "workspace_id": {
      "type": "string"
    },
    "sender": {
      "type": "string"
    },
    "recipient": {
      "type": "string"
    },
    "subject_ref": {
      "type": "string"
    },
    "review_kind": {
      "type": "string"
    },
    "decision": {
      "type": "string"
    },
    "body": {
      "type": "string"
    },
    "attempt_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "references": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "family_digest": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "authorization_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "profile_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "transition": {
      "anyOf": [
        {
          "additionalProperties": {
            "type": "string"
          },
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "issued_at": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "expires_at": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "authorization_scope": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "operation_kind": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "issuer_proof": {
      "default": null,
      "title": "Issuer Proof"
    }
  },
  "required": [
    "workspace_id",
    "sender",
    "recipient",
    "subject_ref",
    "review_kind",
    "decision",
    "body"
  ],
  "type": "object"
}
```

## envelope-read

### `list_reports`

List REPORTs through Core, including exact attempt and head selection semantics.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "subject_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "sender": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "attempt_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "head_only": {
      "default": false,
      "type": "boolean"
    },
    "offset": {
      "default": 0,
      "type": "integer"
    },
    "limit": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "type": "object"
}
```

### `read_report`

Read a canonical REPORT through Core identity resolution.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "filename_or_id": {
      "type": "string"
    }
  },
  "required": [
    "filename_or_id"
  ],
  "type": "object"
}
```

### `list_issues`

List validated canonical ISSUE facts, with deterministic filtering and pagination.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "sender": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "subject_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "severity": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "offset": {
      "default": 0,
      "type": "integer"
    },
    "limit": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "type": "object"
}
```

### `list_reviews`

List validated canonical REVIEW facts; listing grants no authorization.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "sender": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "subject_ref": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "review_kind": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "decision": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "offset": {
      "default": 0,
      "type": "integer"
    },
    "limit": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "type": "object"
}
```

### `read_review`

Read a validated REVIEW from its canonical bucket without changing its decision.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "review_id": {
      "type": "string"
    }
  },
  "required": [
    "review_id"
  ],
  "type": "object"
}
```

## review-decision

### `mark_human_approved`

Ask Core to append independent authorization evidence. Caller-supplied approver text alone is never authority; expires_at must be explicit.

Status: `canonical` · Since: `4.0.5` · Owner: `FCoP Core`

Input schema:

```json
{
  "additionalProperties": false,
  "properties": {
    "review_id": {
      "type": "string"
    },
    "decision": {
      "type": "string"
    },
    "approver": {
      "type": "string"
    },
    "profile_ref": {
      "type": "string"
    },
    "from_stage": {
      "type": "string"
    },
    "to_stage": {
      "type": "string"
    },
    "issued_at": {
      "type": "string"
    },
    "expires_at": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ]
    },
    "attempt_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "family_digest": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "issuer_proof": {
      "default": null,
      "title": "Issuer Proof"
    },
    "comment": {
      "default": "",
      "type": "string"
    }
  },
  "required": [
    "review_id",
    "decision",
    "approver",
    "profile_ref",
    "from_stage",
    "to_stage",
    "issued_at",
    "expires_at"
  ],
  "type": "object"
}
```

## Migration

Every one of the original 49 tools has exactly one disposition in [the migration guide](migration-4.0.5-mcp.md). `write_task` is an opt-in deprecated Python shim; `fcop_audit` is `fcop audit` in the Toolkit. Neither is registered by the default MCP server.
