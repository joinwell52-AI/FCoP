```
Internet-Engineering-Style Specification                FCoP Working Group
Request for Comments: FCoP-3.0                                       W. Zhu
Category: Coordination Protocol                              joinwell52-AI
ISSN: pending                                                   May 2026


                  Filesystem Coordination Protocol (FCoP)
                                Version 3.0

Status of This Memo

   This document specifies a coordination protocol for multi-agent
   systems that share a common filesystem. It is published as a
   community specification by the FCoP Working Group and is intended
   for implementation, interoperability testing, and reference by
   downstream agent runtimes and tooling.

   Distribution of this memo is unlimited.

Copyright Notice

   Copyright (c) 2026 joinwell52-AI. Released under the MIT License.

```

# Abstract

This memo defines version 3.0 of the Filesystem Coordination Protocol
(FCoP), a coordination protocol in which **file location defines the
current state of work** and **append-only events inside each file record
the audit history**. FCoP occupies the same architectural position for
multi-agent coordination that POSIX occupies for processes and that
OCI occupies for container images: it standardises the contract between
participants without owning their execution.

FCoP 3.0 reduces the protocol surface to three layers:

1. **State Layer (NOW truth)**: directory location.
2. **Event Layer (PAST trace)**: append-only `transitions:` array in the
   file's YAML frontmatter.
3. **Boundary Charter**: a meta-rule that prevents the protocol from
   absorbing runtime, scheduling, or enforcement responsibilities.

A "Custody" concept is explicitly retained as a **derived interpretation
only**, never as a stored protocol field.

---

# Status of This Memo

This document is the canonical English specification for FCoP 3.0.
Conforming implementations MUST satisfy every clause marked with the
key words "MUST", "MUST NOT", "REQUIRED", "SHALL", and "SHALL NOT" as
defined in [RFC2119].

The companion document `spec/fcop-3.0-spec.md` carries identical
normative content in a presentation-oriented layout. In case of
disagreement between the two, **this RFC-style document is authoritative**
for the wording of normative clauses; both documents are versioned
together.

---

# Table of Contents

```
1.  Introduction ............................................... 1
    1.1.  Requirements Language ................................ 1
    1.2.  Terminology .......................................... 2
2.  Canonical Statement ........................................ 2
3.  State Layer (NOW Truth) .................................... 3
    3.1.  Directory Topology ................................... 3
    3.2.  Substrate Assumption ................................. 3
    3.3.  Stage Definitions .................................... 4
    3.4.  Allowed Transitions .................................. 4
    3.5.  Core Rules (A, B, C) ................................. 4
4.  Event Layer (PAST Trace) ................................... 5
    4.1.  Frontmatter Schema ................................... 5
    4.2.  Event Schema ......................................... 5
    4.3.  Core Rules (E, F, G) ................................. 6
    4.4.  Atomicity (Write-Then-Rename) ........................ 6
5.  Boundary Charter ........................................... 7
    5.1.  Three Boundary Principles ............................ 7
    5.2.  Excluded Concerns .................................... 7
    5.3.  Filter Rule for Future Extensions .................... 8
    5.4.  Exemption Clause ..................................... 8
6.  Identity (Filename Grammar) ................................ 9
7.  Custody (Informative) ...................................... 9
8.  Conformance Requirements ................................... 10
9.  Security Considerations .................................... 11
10. Interoperability Considerations ............................ 11
11. Versioning ................................................. 12
12. References ................................................. 12
13. Authors' Addresses ......................................... 12
Appendix A.  Tool Layer (Informative) .......................... 13
Appendix B.  Migration from 2.x (Informative) .................. 13
Appendix C.  One-Sentence Specification ........................ 14
```

---

# 1. Introduction

Multi-agent collaboration over a shared filesystem requires a small,
stable set of conventions that all participants can rely on without
running a common runtime. Existing coordination layers either bind
participants to a specific orchestration framework (Temporal, LangGraph,
CrewAI) or define an event-sourced log that requires replay to
reconstruct current state (Git, Kafka, EventStore).

FCoP takes a different path: it treats the **filesystem itself** as the
coordination substrate. Directory location is the current state.
Append-only events inside each file record the history. No other
information is authoritative.

This approach is intentionally minimal. Any agent that can `read`,
`write`, and `rename` files can participate in FCoP without adopting
a specific SDK, runtime, or daemon.

## 1.1. Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [RFC2119].

## 1.2. Terminology

| Term | Definition |
|------|-----------|
| **Lifecycle root** | The `fcop/_lifecycle/` directory that contains the five stage subdirectories. |
| **Stage** | One of the five directories under the lifecycle root (`inbox`, `active`, `review`, `done`, `archive`). |
| **L1 tool** | A tool whose contract permits moving files between stages. |
| **Transition** | A single move of one file from one stage to another (or from creation to `inbox`). |
| **Event** | A YAML record in the `transitions:` array that witnesses one transition. |
| **NOW truth** | The current state of the system, defined exclusively by file location. |
| **PAST trace** | The history of state changes, defined exclusively by the append-only `transitions:` arrays. |
| **Custody** | A derived interpretation of file ownership; not a protocol field. |

---

# 2. Canonical Statement

> **FCoP is a filesystem-native protocol where file location defines
> current state, and all historical and ownership semantics are derived
> from append-only transition traces.**

In three lines (Layer 1 · cognitive bootstrap, per ADR-0040):

> **Files carry protocol. Paths address state. Events replay
> transitions.**
>
> 文件即协议；位置定义状态；事件记录历史。

Compressed formal definition (Layer 2 · semantic ontology):

> **Files externalize protocol semantics. Paths address state.
> Events are replayable evidence of state transitions.**
>
> 文件是协议的外化载体；位置是状态的地址映射；事件是状态转移的可重放证据。

(Historical / epigraph: *"file location is truth; everything else
is trace."* / *"文件位置即真相；其它一切都是踪迹。"* — the v1
canonical, retired as definitional surface per ADR-0040 but
retained in essays and reviews filed on or before 2026-05-21.)

FCoP is NOT an agent runtime, NOT a workflow engine, and NOT an
orchestration kernel. It defines the contract between participants;
it does not execute that contract.

---

# 3. State Layer (NOW Truth)

## 3.1. Directory Topology

Conforming implementations MUST maintain the following structure at
the project root:

```
fcop/
├── _lifecycle/
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
├── reports/
├── issues/
└── shared/
```

All five lifecycle subdirectories MUST reside on the same filesystem
mount point.

## 3.2. Substrate Assumption

> **FCoP 3.0 assumes a single-consistent filesystem boundary per
> lifecycle root.**

Implementations operating across distributed filesystems, network
mounts with relaxed consistency, or multi-host concurrent writers MUST
provide an external consistency layer. The protocol itself does not
specify or provide this layer.

Environments in which this assumption breaks by default include:

- distributed filesystems without strict POSIX semantics
- git worktree synchronisation across machines
- multi-host MCP servers writing concurrently to the same lifecycle
  root
- network mounts with non-zero attribute-cache TTL

In such environments, the consistency-providing layer is OUTSIDE the
FCoP protocol surface.

## 3.3. Stage Definitions

| Stage     | Definition          |
|-----------|---------------------|
| `inbox`   | created             |
| `active`  | claimed             |
| `review`  | pending confirmation|
| `done`    | completed           |
| `archive` | closed              |

These definitions are frozen. Implementations MUST NOT assign
additional semantics to these stage names.

## 3.4. Allowed Transitions

| From      | To        | Tool                              |
|-----------|-----------|-----------------------------------|
| —         | `inbox`   | `create_task`                     |
| `inbox`   | `active`  | `claim_task`                      |
| `active`  | `review`  | `submit_task`                     |
| `active`  | `done`    | `finish_task(skip_review=true)`   |
| `review`  | `done`    | `approve_task`                    |
| `review`  | `active`  | `reject_task`                     |
| `done`    | `archive` | `archive_task`                    |

Transitions not listed above are NOT permitted. Implementations MUST
reject any attempt to move a file along a path not in this table.

## 3.5. Core Rules (A, B, C)

> **Rule A · File path is the only NOW truth.**
> The directory containing a file defines its current state.
> Implementations MUST NOT rely on file contents (frontmatter, body,
> or any field) to determine current state.

> **Rule B · L1 tools perform filesystem state transitions.**
> Only tools designated as L1 (lifecycle tools) may move files between
> lifecycle subdirectories.

> **Rule C · Transitions are governed by explicit tool invocation
> only.** Both transition path and execution authority MUST be encoded
> in the tool call itself. No file field, role inference, or external
> policy may decide which transition occurs or who may execute it.

---

# 4. Event Layer (PAST Trace)

## 4.1. Frontmatter Schema

Every file in `_lifecycle/` MUST carry a `transitions:` array in its
YAML frontmatter. Example:

```yaml
---
protocol: fcop
version: 3
type: TASK
task_id: TASK-20260521-001-PM-to-DEV
transitions:
  - at: 2026-05-21T10:00:00+08:00
    from: null
    to: inbox
    by: PM-01
    tool: create_task
  - at: 2026-05-21T10:15:00+08:00
    from: inbox
    to: active
    by: DEV-01
    tool: claim_task
---
```

## 4.2. Event Schema

Each transition event MUST contain the following fields:

| Field   | Type                  | Description                          |
|---------|-----------------------|--------------------------------------|
| `at`    | ISO-8601 datetime     | When the transition occurred         |
| `from`  | string \| null        | Source stage (`null` for creation)   |
| `to`    | string                | Destination stage                    |
| `by`    | string                | Actor identifier                     |
| `tool`  | string                | L1 tool that performed the transition|

Optional fields:

| Field        | Type   | Description                                  |
|--------------|--------|----------------------------------------------|
| `note`       | string | Free-text annotation                         |
| `supersedes` | string | Reference to a corrected event (append-only) |

## 4.3. Core Rules (E, F, G)

> **Rule E · Every mv produces an event.**
> Each L1 transition MUST append exactly one event to the
> `transitions:` array.

> **Rule F · Events are append-only.**
> The `transitions:` array MUST NOT be modified or deleted.
> Corrections proceed by appending a new event that references the
> prior one via `supersedes`.

> **Rule G · Events are audit-only PAST trace.**
> The event stream is the only canonical source for history, audit,
> and trace. **Current state is determined by file location (Rule A),
> never by replaying events.** Implementations MUST NOT derive
> `current_state(file)` from `transitions:`. Replay is permitted
> only for audit and consistency verification.

## 4.4. Atomicity (Write-Then-Rename)

> **An event is not a side effect of a transition.**
> **An event is the transition itself, witnessed in writing.**

The event and the file move are not two operations to be sequenced;
they are two faces of the same coordination act. The pattern below
is the physical realisation of the witnessed transition as a single
observable commit.

Implementations MUST apply event writing and file movement as a single
atomic operation using the following pattern:

```
1. Read source file
2. Append event to transitions: array (in memory)
3. Write to temporary file in destination directory (.{id}.tmp)
4. fsync the temporary file
5. os.rename(tmp, destination)   ← POSIX atomic guarantee
6. Unlink source if source path differs from destination
```

Step 5 is the atomic commit point. Before step 5: state = source
location, no event written. After step 5: state = destination
location, event written. **No intermediate state is observable.**

---

# 5. Boundary Charter

## 5.1. Three Boundary Principles

> **Principle 1: Protocol describes, not executes.**
> FCoP defines that `active → review` is a valid transition. FCoP
> does NOT perform the `mv`, schedule who acts, or execute any task.

> **Principle 2: Protocol externalises, not owns.**
> FCoP defines file contracts and event schemas. FCoP does NOT own
> a log system, database, or any runtime state.

> **Principle 3: Protocol coordinates, not orchestrates.**
> FCoP defines what "reviewer may take over" means. FCoP does NOT
> decide who reviews when.

## 5.2. Excluded Concerns

The following are OUTSIDE FCoP scope and MUST NOT be added:

| Concern                                            | Owner             |
|----------------------------------------------------|-------------------|
| Task execution (LLM calls, tool invocation)        | Runtime layer     |
| Scheduling (queues, DAGs, retries)                 | Workflow engines  |
| Sandboxing, capability enforcement                 | OS / runtime      |
| Memory systems, vector databases                   | Memory layer      |
| Heartbeat, TTL, reclaim, auto-recovery             | Runtime policy    |
| Task assignment policy (who-does-what)             | Coordination intent|
| `risk_level` driving state transitions             | Coordination hint |
| `custody` / `ownership` as a stored field          | Interpretation only|

## 5.3. Filter Rule for Future Extensions

Any proposed extension to FCoP MUST pass the following five questions:

1. Does it describe semantics, or execute behavior? Reject the latter.
2. Does it define file contracts, or own runtime state? Reject the
   latter.
3. Does it coordinate multiple agents, or schedule a specific agent?
   Reject the latter.
4. Can it be re-implemented by another host without an FCoP runtime?
   Reject if no.
5. Does it overlap with Temporal / LangGraph / CrewAI in
   responsibility? Reject if yes.

## 5.4. Exemption Clause

Extensions may be re-discussed only when one of the following is
demonstrated with evidence:

- **E1 (Complexity-forced)**: 2+ independent projects report the same
  protocol gap within 6 months.
- **E2 (Cross-runtime breakdown)**: a real coordination scenario is
  shown to be impossible without the extension.
- **E3 (Internal contradiction)**: existing rules conflict
  irreconcilably.

The following remain NEVER exempt:

- FCoP owning LLM/tool execution
- FCoP owning runtime sandbox or capability enforcement
- FCoP owning a protocol-specific daemon or long-running process

---

# 6. Identity (Filename Grammar)

File identity is established by filename and is immutable for the
file's lifetime:

```
{TYPE}-{YYYYMMDD}-{NNN}-{SENDER}-to-{RECIPIENT}(-{slug}).md
```

| Component             | Definition                                |
|-----------------------|-------------------------------------------|
| `TYPE`                | `TASK` \| `REPORT` \| `ISSUE` \| `REVIEW` |
| `YYYYMMDD`            | UTC date of creation                      |
| `NNN`                 | Three-digit sequence within that date     |
| `SENDER`, `RECIPIENT` | Role codes (uppercase, alphanumeric, ≤16) |
| `slug`                | Optional human-readable trailing label    |

The filename MUST NOT change across the file's lifetime. Only file
location (per §3) changes.

---

# 7. Custody (Informative)

Custody is NOT part of the protocol state model. It is an emergent
interpretation of file ownership derived from §3 (location) and
§4 (events). Implementations MUST NOT introduce a `custodian` field
or any equivalent stored representation.

When implementations need to answer "who currently holds this file":

| File location          | Derived custodian                                  |
|------------------------|----------------------------------------------------|
| `_lifecycle/inbox/`    | none                                               |
| `_lifecycle/active/`   | the `by` of the most recent `to: active` event     |
| `_lifecycle/review/`   | none                                               |
| `_lifecycle/done/`     | the last `by` from `active` (audit only)           |
| `_lifecycle/archive/`  | same as `done`                                     |

This derivation is a read pattern, NOT a protocol rule.

---

# 8. Conformance Requirements

A conforming FCoP 3.0 implementation MUST:

| #   | Requirement                                                       | Source |
|-----|-------------------------------------------------------------------|--------|
| C1  | Maintain the lifecycle directory structure per §3.1               | §3.1   |
| C2  | Mount all lifecycle subdirectories on the same filesystem         | §3.1   |
| C3  | Reject any transition not listed in §3.4                          | §3.4   |
| C4  | Determine current state exclusively from file location (Rule A)   | §3.5   |
| C5  | Restrict topology mutation to L1 tools (Rule B)                   | §3.5   |
| C6  | Append exactly one event per transition (Rule E)                  | §4.3   |
| C7  | Treat `transitions:` as append-only (Rule F)                      | §4.3   |
| C8  | Never derive current state from events (Rule G)                   | §4.3   |
| C9  | Implement the write-then-rename atomic pattern (§4.4)             | §4.4   |
| C10 | Reject the excluded concerns listed in §5.2                       | §5.2   |

A conforming implementation MUST NOT:

| #   | Prohibition                                                       | Source |
|-----|-------------------------------------------------------------------|--------|
| P1  | Introduce a stored `custodian` field                              | §7     |
| P2  | Use file frontmatter fields to drive transition path or authority | Rule C |
| P3  | Run protocol-specific daemons or long-lived processes             | §5.4   |
| P4  | Execute LLM/tool calls as part of protocol operation              | §5.2   |
| P5  | Modify or delete past entries in `transitions:`                   | Rule F |

---

# 9. Security Considerations

FCoP delegates all enforcement to the underlying operating system and
runtime layer (Principle 1, §5.1).

- **Filesystem permissions**: Access control for the lifecycle root is
  the responsibility of the OS. FCoP does not specify file modes,
  ACLs, or user/group conventions.
- **Capability declaration vs enforcement**: Implementations MAY
  declare agent capabilities, but MUST NOT enforce them. Enforcement
  is the responsibility of the runtime that hosts each agent.
- **Append-only audit**: Rule F provides tamper-evident history at the
  protocol level. Tamper-resistance (against attackers with write
  access to the lifecycle root) requires external mechanisms such as
  signed commits or write-once storage; FCoP does not specify these.
- **Substrate trust**: §3.2 makes the single-consistent filesystem
  assumption explicit. Implementations deployed across untrusted
  consistency layers inherit the security properties of those layers.

---

# 10. Interoperability Considerations

FCoP is designed for cross-runtime interoperability. Any agent that
can perform `read`, `write`, and `rename` on the lifecycle root can
participate, regardless of language, framework, or runtime.

Implementations SHOULD:

- emit identical event schemas (§4.2) so that traces remain readable
  across implementations;
- preserve unknown optional fields when modifying a file;
- treat files lacking the `transitions:` field as legal historical
  artifacts (per Appendix B);
- never introduce host-specific extensions to the `_lifecycle/`
  directory structure.

---

# 11. Versioning

| Version | Date       | Change                                          |
|---------|------------|-------------------------------------------------|
| 3.0     | 2026-05-21 | Initial publication. State + Event + Boundary. |

Future versions follow these rules:

- **MAJOR (4.0)**: Changes §3 directory topology, stage definitions,
  allowed transitions, or any of Rules A/B/C.
- **MINOR (3.x)**: Adds optional fields, additional informative
  sections, or non-breaking event schema extensions.
- **PATCH (3.0.x)**: Editorial corrections only; no semantic change.

Appendix A (Tool Layer) and Appendix B (Migration) MAY change without
a version bump.

---

# 12. References

## Normative References

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate
  Requirement Levels", BCP 14, RFC 2119, March 1997.
- [POSIX-rename] IEEE Std 1003.1-2017, `rename()` atomicity guarantee.

## Informative References

- ADR-0035 · State Ontology (frozen)
- ADR-0036 · Event Layer
- ADR-0038 · Boundary Charter
- NOTE-custody-is-not-a-layer
- ADR-0033 · Trailing-slug filename adoption
- ADR-0004 · `os.rename()` atomicity guarantee
- `fcop-rules.mdc` Rule 2 · Files are the protocol, folders are the
  organization
- PROPOSAL `20260521-rfc-semantic-collapse-and-custody-rejection.md`

---

# 13. Authors' Addresses

```
Wei Zhu
joinwell52-AI

Repository: https://github.com/joinwell52-AI/FCoP
DOI:        10.5281/zenodo.19886036
License:    MIT
```

---

# Appendix A. Tool Layer (Informative)

The following tool classification is informational only and MAY evolve
without a protocol version bump.

| Layer | Purpose                                | Examples                                                                                              |
|-------|----------------------------------------|-------------------------------------------------------------------------------------------------------|
| L1    | Lifecycle topology                      | `create_task`, `claim_task`, `submit_task`, `finish_task`, `approve_task`, `reject_task`, `archive_task` |
| L2    | Coordination intent (no topology change)| `assign_agent`, `set_priority`, `notify_agent`                                                       |
| L3    | Execution artifacts                     | `run_task`, `generate_report`                                                                         |
| L4    | Observation (read-only)                 | `list_tasks`, `get_task`, `trace_task`                                                                |
| L5    | System / governance                     | `init_project`, `fcop_audit`                                                                          |

If any tool category begins to affect file location semantics, it MUST
be re-reviewed against §3.

---

# Appendix B. Migration from 2.x (Informative)

```
fcop/tasks/*.md       → fcop/_lifecycle/inbox/*.md
fcop/log/tasks/*.md   → fcop/_lifecycle/archive/*.md
fcop/log/reports/*.md → fcop/reports/*.md          (no longer archived)
fcop/log/issues/*.md  → fcop/issues/*.md           (add: resolved: true)
fcop/log/             → removed
```

Files migrated from 2.x MUST receive a synthetic transition event:

```yaml
transitions:
  - at: <file-mtime>
    from: null
    to: <current-stage>
    by: migration
    tool: fcop_migrate_v3
```

Files lacking `transitions:` are treated as legal historical
artifacts, but any new transition MUST begin appending events.

Reference migration script: `python -m fcop migrate --to-v3`

---

# Appendix C. One-Sentence Specification

> **FCoP is a coordination protocol in which file location defines the
> current state of work, append-only events inside the file record the
> audit history, and nothing else is authoritative.**

---

```
End of FCoP 3.0 RFC                                          [Page 14]
```
