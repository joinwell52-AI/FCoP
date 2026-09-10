<p align="center"><a href="docs/architecture.en.md"><img src="assets/fcop-logo-256.png" alt="FCoP architecture" width="88" /></a></p>

# FCoP — File-based Coordination Protocol

[English](README.md) · [简体中文](README.zh.md)

**Keep agent work beyond the conversation.**

Tasks, deliveries, issues and review decisions become durable files that people, tools and the next agent can inspect. A session can end without taking the work record with it.

<p>
  <a href="https://pypi.org/project/fcop/4.0.0/"><img src="https://img.shields.io/badge/Python-4.0.0-245ac4" alt="fcop on PyPI: 4.0.0" /></a>
  <a href="https://pypi.org/project/fcop-mcp/4.0.0/"><img src="https://img.shields.io/badge/MCP-4.0.0-7055a2" alt="fcop-mcp on PyPI: 4.0.0" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-237456" alt="MIT license" /></a>
</p>

**[Try Python](#try-it) · [Connect MCP](#mcp) · [Architecture series (中文)](docs/fcop-architecture-series/README.md) · [Architecture](#architecture) · [Papers & citation](#research)**

<a href="docs/architecture.en.md"><img src="assets/fcop-work-records.svg" alt="Agent work is persisted as TASK, REPORT, ISSUE and REVIEW files, then read by people, tools and another session." width="960" /></a>

**Stable version: 4.0.0** — [released September 10, 2026](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0). This repository contains the open protocol, the `fcop` Python implementation and the optional `fcop-mcp` adapter. Python 3.10+; no model API key is needed for the local example.

## Why put work outside the model?

“I have finished” is a statement in a conversation. A teammate still needs to know **which assignment was attempted, what was delivered, who reviewed it and what remains unresolved**. Keeping those facts only in a chat makes a handoff depend on reconstructing that chat.

FCoP gives formal work a shared representation: Markdown files with structured metadata, stable identities, explicit relationships and recorded state transitions. An agent can write them, a human can open them, and a script can validate them. The filesystem reference implementation needs no database or message broker.

| Record | What it preserves | Why it matters |
|---|---|---|
| **TASK** | Assignment, participants and lifecycle | The next worker can locate the work and its current state. |
| **REPORT** | Delivery claim and evidence for an attempt | “Submitted” remains distinguishable from “accepted.” |
| **ISSUE** | A problem and its context | A blocker survives the session that discovered it. |
| **REVIEW** | Review, acceptance or authorization facts | Decisions can be checked against the work and evidence they concern. |

Persistence makes a claim inspectable; it does not make the claim true. FCoP checks protocol relationships and gates. Reviewers evaluate the substance of the delivered work, and the host Runtime supplies execution, scheduling and permissions.

<a id="try-it"></a>

## Try it: create once, read from another client

In an activated **Python 3.10+ virtual environment**, install the published library:

```sh
python -m pip install "fcop==4.0.0"
```

Save this as `demo.py` and run `python demo.py`. It writes a real TASK, opens the workspace through a fresh `Project` instance, then retries the original request.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from fcop import Project

with TemporaryDirectory(prefix="fcop-demo-") as directory:
    root = Path(directory) / "workspace"
    project = Project(root)
    workspace = project.create_workspace(protocol_version="4.0")
    request = dict(
        workspace_id=workspace["workspace_id"],
        operation_id="demo-create-1",
        sender="ME", recipient="ME",
        subject="Inspect this handoff",
        body="Read the task and check the evidence before accepting delivery.",
    )
    first = project.create_task(**request)

    next_client = Project(root)
    state = next_client.inspect_state(task_id=first["task_id"])
    retry = next_client.create_task(**request)

    assert Path(state["path"]).is_file()
    assert retry["existing"] and retry["task_id"] == first["task_id"]
    print("State read from disk:", state["stage"])
    print("Same task after retry:", retry["task_id"] == first["task_id"])
```

```text
State read from disk: inbox
Same task after retry: True
```

The example cleans up its temporary directory when it exits. Use your own project directory to retain the files. Retrying `create_task` with the same `operation_id` and normalized payload reuses its durable result; changing the payload is a conflict. This guarantee is specifically for task creation.

**Continue with the [4.0 setup and version guide](docs/fcop-4.0-progress.md)** for a lasting workspace, lifecycle operations and the authorization needed to complete a task.

<a id="mcp"></a>

## Give your agent the same operations through MCP

The optional adapter exposes FCoP to an MCP-capable client over stdio. Install it in the same activated environment:

```sh
python -m pip install "fcop==4.0.0" "fcop-mcp==4.0.0"
```

Add this entry to the client's MCP configuration. Replace both absolute paths; on Windows the command ends in `.venv/Scripts/fcop-mcp.exe`.

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/.venv/bin/fcop-mcp",
      "env": {"FCOP_PROJECT_DIR": "/absolute/path/to/new-workspace"}
    }
  }
}
```

Once connected, initialize a **new** workspace with `init_solo(role_code="ME", protocol_version="4.0")`. Use its workspace identity when calling `create_task`, then inspect the TASK with `inspect_task(filename=task_id)`. Installing an MCP server alone does not initialize a workspace or start an agent team.

**46 tools / 12 resources / 4 resource templates.** The adapter routes to the same Python Core. Default initialization has no trusted authorization Profile: creation, claim and submission are available, but acceptance, rejection, reopening and archival need an explicitly adopted Profile and an issuer evaluator registered by the trusted host. A role name typed into a request cannot supply that authority.

[MCP tool reference](docs/mcp-tools.md) · [Stable external Python example](tests/stable/third-party/python-only/app.py) · [Stable external MCP example](tests/stable/third-party/mcp-only/client.py). The full examples include an educational Profile; a real deployment must supply its own trust policy.

## From a delivery claim to an accepted result

Each TASK follows an ordered lifecycle. In 4.0, entering `active` starts a new attempt, and submission links that attempt's REPORT. Acceptance then binds the review and authorization to the current evidence.

<a href="spec/fcop-4.0-spec.md"><img src="assets/fcop-lifecycle.svg" alt="FCoP 4.0 lifecycle: inbox, active, review, done and archive; authorized rejection and reopening return to a new active attempt." width="960" /></a>

`active → done` is absent from 4.0. Reopening through `reopen_task` creates a new attempt for ordinary tasks as well as Branches. An old REPORT cannot satisfy a new attempt's submission gate. See the [complete lifecycle and C1–C8 contracts](spec/fcop-4.0-spec.md) · [中文规范](spec/fcop-4.0-spec.zh.md).

## Parallel work, with an explicit way to finish

Multiple ordered workflows can advance concurrently. A Branch is an ordinary TASK linked to one Root by `branch_of`; sibling Branches keep their own attempts, reports and reviews. Your Runtime decides who runs them and when.

<a href="docs/architecture.en.md#parallel-work"><img src="assets/fcop-parallel-work.svg" alt="Two sibling Branch tasks proceed independently through work, report and review; Root closure checks current evidence, convergence and archive authorization." width="960" /></a>

Before a Root with Branches can be archived, FCoP checks completed Branches, their current REPORTs, a matching `family_digest`, a convergence REVIEW and separate Root archive authorization. A reopened Branch or changed REPORT invalidates stale convergence. Related writes share a short commit boundary; agents do not hold that lock while doing their work. This closes an evidence set; code integration remains the application's responsibility.

<a id="architecture"></a>

## A small protocol inside a larger agent system

Another implementation should be able to preserve the same work semantics without copying a particular Python library, MCP tool list or product.

| Layer | Responsibility |
|---|---|
| **Core** | C1–C8: identity, envelopes, lifecycle, relations, convergence, authorization, create idempotency and atomic recovery. |
| **Specification** | Define the fields, state transitions, errors and observable behavior. |
| **Conformance** | Check implementations against those contracts using fixtures, vectors and behavioral tests. |
| **Toolkit** | Implement and expose the protocol; this repository supplies Python and the MCP adapter. |
| **Profile** | Supply organizational policy and issuer authority; fixed PM/DEV/QA roles are not universal Core rules. |
| **Runtime** | Run models and tools, manage sessions, schedule work and provide the user interface. |

**Read the design explanation: [English](docs/architecture.en.md) · [简体中文](docs/architecture.zh.md).** It develops the reasoning behind files, separate delivery and acceptance, parallel work, and the boundaries between FCoP, MCP and a Runtime.

**Architecture principles: five full essays in Chinese**, published September 10, 2026 and revised against 4.0:

1. [Work beyond the model context: why files?](docs/fcop-architecture-series/01-work-beyond-context.zh.md)
2. [Extracting the minimal FCoP Core](docs/fcop-architecture-series/02-minimal-core.zh.md)
3. [Separating Core, Specification, Toolkit, Profile and Runtime](docs/fcop-architecture-series/03-architecture-layers.zh.md)
4. [Parallel work through ordered task lifecycles](docs/fcop-architecture-series/04-parallel-work.zh.md)
5. [How FCoP, MCP, A2A and CodeFlowMu fit together](docs/fcop-architecture-series/05-mcp-a2a-runtime.zh.md)

[Series guide (中文)](docs/fcop-architecture-series/README.md) · [All five essays (中文)](docs/fcop-architecture-series/collected.zh.md)

4.0 also distributes **nine bilingual rule modules** with versioned manifests and `sequential`, `parallel` and `repository-development` assemblies. Adoption, deployment planning, receipts and rollback are explicit. Host projections use `reference` or `bounded_embed`; installing a package does not silently rewrite host rules. [Rule distribution contract](docs/fcop-4.0/rule-distribution-contract.md) · [中文契约](docs/fcop-4.0/rule-distribution-contract.zh.md).

<a id="research"></a>

## Papers, evidence and citation

These resources are directly accessible; reading the essay collection is optional.

| Resource | Read or cite |
|---|---|
| **Architecture whitepaper** | [English](essays/from-coordination-to-governance.en.md) · [中文](essays/from-coordination-to-governance.md) — historical research context |
| **3.2.5 archive** | [Zenodo DOI 10.5281/zenodo.20457285](https://doi.org/10.5281/zenodo.20457285) · [OSF DOI 10.17605/OSF.IO/92NWM](https://doi.org/10.17605/OSF.IO/92NWM) |
| **April 2026 research snapshot** | [Zenodo DOI 10.5281/zenodo.19886036](https://doi.org/10.5281/zenodo.19886036) · [Citation metadata](CITATION.cff) |
| **17 field reports and design essays** | [Complete index](essays/README.md) · [中文目录](essays/README.zh.md), including original publication and evidence links |

Choose the archive matching the version you studied. The historical DOIs above are not identifiers for 4.0.0; use the versioned release and specification when discussing current behavior.

## Three repositories, three entry points

| Repository | Start here for |
|---|---|
| **[FCoP](https://github.com/joinwell52-AI/FCoP)** | **Flagship open-source project:** protocol, Python library and MCP server; use, implement or contribute to the coordination layer. |
| **[joinwell52](https://github.com/joinwell52-AI/joinwell52)** | **Research and communication:** AI Agents, digital employees and engineering studies. |
| **[CodeflowMu-Distribution](https://github.com/joinwell52-AI/CodeflowMu-Distribution)** | **Product experience:** packaged application and [downloads](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases); check its release notes for supported versions. |

FCoP is independently usable under the [MIT license](LICENSE). The product distribution has its own licensing and release schedule.

**Star FCoP to bookmark the protocol and its implementation.** To help it improve, share a reproducible integration issue, an example from your host, or a test of the protocol's public behavior through [Issues](https://github.com/joinwell52-AI/FCoP/issues) or a pull request.

## Versions and existing installations

- **4.0.0:** [Release notes](docs/releases/4.0.0.md) · [Changelog](CHANGELOG.md) · [Architecture decisions](adr/README.md). Publication followed the recorded `FCOP_4_STABLE_RELEASE_READY` gate; users install the stable PyPI pair above.
- **Release candidate: 4.0.0rc1** — retained as a [historical prerelease](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0rc1).
- **3.x workspaces:** retain their original semantics until explicit migration. [Legacy specification EN](spec/fcop-v3-spec.md) · [ZH](spec/fcop-v3-spec.zh.md). `finish_task` and legacy history tools remain discoverable but reject v4 workspaces.
- **Legacy installation prompts:** [EN](src/fcop/rules/_data/agent-install-prompt.en.md) · [ZH](src/fcop/rules/_data/agent-install-prompt.zh.md), also available at `fcop://prompt/install`. These are historical setup material; use the 4.0 guide above for the current version.
