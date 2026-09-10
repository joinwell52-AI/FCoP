# FCoP architecture: work outside the model

[Back to FCoP](../README.md) · [简体中文](architecture.zh.md) · [4.0 setup](fcop-4.0-progress.md)

**FCoP externalizes formal agent work as durable, attributable and inspectable facts.** This explains the choice of files, the separation of delivery from acceptance, and the boundaries between a protocol, its tools and a Runtime.

This page explains the design of 4.0. The [4.0 specification](../spec/fcop-4.0-spec.md) defines fields, errors and transition conditions. Conceptual lists in historical research do not replace the current C1–C8 contracts.

## 1. A session may end; the work needs a durable home

A model can interpret a task, reason and request tools. Its context window does not replace persistent storage, operating-system permissions, process management or scheduling. When a model changes, a session stops or work moves to another person, the recipient still needs a record they can locate and inspect.

Suppose an agent changes an API and says it has finished. Its successor needs the assignment, the delivery corresponding to that attempt, test evidence, review decisions and unresolved problems. Saving the conversation alone does not supply stable identities and explicit relationships between those facts.

FCoP gives the task an identity, associates delivery with an attempt, records state transitions and points reviews at specific evidence. A successor can read the records without reconstructing the previous model's entire conversation.

![Work records persist across sessions](../assets/fcop-work-records.svg)

This makes records persistent and inspectable. Restarting a model, scheduling another step and granting tool access belong to the host Runtime. Persistent records support execution recovery; the protocol itself does not restart an agent.

## 2. Why files make a useful shared carrier

Files already exist in the environment shared by developers, agents, IDEs, scripts and version tools. Markdown bodies express the work; structured metadata preserves identity and relations; lifecycle paths express current state; transition records retain how that state changed.

A user can open the same task file without first deploying a database or messaging service. Teams can also retain, compare or search records with their own versioning and audit tools. Deployment and retention policies for those tools remain the team's responsibility.

The simplicity of files does not remove concurrency problems. The 4.0 reference implementation uses locks, commit receipts, atomic writes and recovery mechanisms. A single rename neither proves authorization nor substitutes for consistency checks across related records.

Files are the current reference carrier. Another storage backend would need encoding rules and conformance evidence. This release does not infer a SQLite, object-store or cross-machine synchronization adapter from that architectural possibility.

## 3. Four records make claims inspectable

| Record | Formal act it preserves | Boundary |
|---|---|---|
| TASK | Assigning work | Creation does not establish execution. |
| REPORT | Submitting a delivery claim and evidence for an attempt | A report does not establish truth or acceptance. |
| ISSUE | Recording a problem and its context | Discovery and resolution need their own facts. |
| REVIEW | Reviewing, accepting, authorizing or recording convergence | Writing “approved” does not grant issuer authority. |

Every entry into `active` in 4.0 generates a new `attempt_id`. Submission requires the current attempt's valid REPORT. Acceptance binds the REVIEW, REPORT and authorization. After rejection or reopening, an earlier attempt's report cannot satisfy the new submission gate.

Authorization must also be durable. The workspace explicitly adopts a usable Profile; the trusted host registers an evaluator for the issuer and its proof. The request's `actor` or `profile_ref` is a field, not a way to grant oneself authority. Without a usable authorization Profile, gated transitions reject the operation.

Protocol checks can establish whether a decision is correctly bound to permitted state and evidence. Reviewers still judge whether the delivery meets its objective. Structured evidence assists that judgment; it cannot replace it.

## 4. Keep the Core small and responsibilities explicit

A protocol should allow independent implementations. Requiring every user to copy one role organization, Python class, MCP tool list or product UI would make that difficult.

| Layer | Question it answers | Concrete role |
|---|---|---|
| Core | Which semantics must implementations preserve? | The eight C1–C8 contracts. |
| Specification | How are those semantics precisely defined and observed? | Fields, states, relations, errors, encodings and rules. |
| Conformance | How is compliance demonstrated? | Contract vectors, fixtures, behavioral tests and their results. |
| Toolkit | How do developers use, validate and query the protocol? | The `fcop` Python implementation and supporting tools. |
| Profile | Which roles and authority policies does an organization adopt? | Adopted policy and trusted issuer evaluation. |
| Runtime | Who keeps agents running and assigns execution? | Model calls, sessions, scheduling, permissions and UI. |

Conformance is a verification plane. A count of tools cannot establish compliance. Python and MCP are concrete consumption paths; independent implementations should use the specification's observable behavior as their compatibility target.

The current contracts are **C1 workspace identity, C2 four envelopes, C3 lifecycle, C4 relations, C5 evidence and convergence, C6 durable authorization, C7 create idempotency and C8 atomic recovery**. PM, DEV, QA and ADMIN role organizations belong to Profiles or applications.

<a id="parallel-work"></a>

## 5. Multiple ordered workflows produce parallel work

Ordered state transitions and parallel execution can coexist. Each task keeps its claim, execution, submission and review order. A Runtime can schedule several tasks at once, allowing each to advance independently.

For example, an API upgrade might need documentation changes and client adaptation. A Root expresses the shared objective, with two sibling Branches recording that work. A Branch is an ordinary TASK related through `branch_of`; it does not introduce another recursive task system. Nor is that relationship a Git branch.

![Parallel tasks with explicit evidence convergence](../assets/fcop-parallel-work.svg)

When the Branches finish, Root closure still needs to answer: do we have every Branch's current delivery? Has a Branch just reopened? Is an old report being mistaken for a new result?

In 4.0, Root archival checks that all Branches are in `done` or `archive`, their current REPORTs are valid, their completions passed the required gates, convergence covers exactly those reports, and `family_digest` matches the value checked at commit. Separate Root archive authorization must bind that current digest. A convergence record alone is not archive authority.

Creating a Branch, reopening or entering a new attempt, or replacing a current REPORT can invalidate old convergence. Related writes re-read and validate facts within one short family commit boundary. That boundary does not lock the duration of agent execution or unrelated independent TASKs.

Parallel closure therefore depends on current evidence and explicit decisions. How code is merged, conflicts are resolved and integration tests are run remains an application and Runtime concern.

## 6. FCoP, MCP and a Runtime work at different boundaries

| Capability | Responsible layer |
|---|---|
| Tool discovery and invocation by a model | MCP and client integration. |
| Formal work identity, state, relations and evidence | FCoP and its implementation. |
| Model execution, session continuation, scheduling and UI | The host Runtime. |
| Discovery, communication and routing between systems | Network integration; mappings to protocols such as A2A can be explored. |

The FCoP MCP adapter routes public operations to Core instead of defining another protocol interpretation. A Python consumer can use the same implementation directly without MCP.

Cross-system communication also needs its own protocols and authority boundaries. An architectural mapping to A2A does not mean 4.0 ships an A2A adapter. CodeFlowMu is a separate product Runtime; consult [CodeflowMu-Distribution releases](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases) for actual compatibility.

Rules need explicit delivery too. The nine bilingual modules in 4.0 are versioned and reach a host through adoption, deployment planning, receipts and rollback. A file existing, an index existing, adoption being recorded, a host entry being deployed and a Runtime actually consuming the rules are distinct facts. See the [rule distribution contract](fcop-4.0/rule-distribution-contract.md).

## Where to continue

- **Try the implementation:** [README demo](../README.md#try-it) and [4.0 setup](fcop-4.0-progress.md).
- **Implement or review:** [Full specification](../spec/fcop-4.0-spec.md) and [architecture decisions](../adr/README.md).
- **Explore the research:** [Field-report index](../essays/README.md), with each article read in its historical version context.
