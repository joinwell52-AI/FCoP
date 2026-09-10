# FCoP — File-based Coordination Protocol

[English](README.md) · [简体中文](README.zh.md) · [Homepage](https://joinwell52-ai.github.io/FCoP/)

FCoP governs collaboration through TASK / REPORT / ISSUE / REVIEW files. It is a protocol, not a scheduler, Agent Runtime, broker or database.

- **Stable version: 4.0.0** — release distribution; publication is gated by WP4F.
- **Release candidate: 4.0.0rc1** — published historical prerelease, retained unchanged.
- **4.0 MCP: 46 tools / 12 resources / 4 resource templates**.

## Protocol-level Major upgrade

Python Core (`fcop`) owns validation and filesystem behavior. The optional MCP Adapter (`fcop-mcp`) routes public calls to Core, without independently interpreting or implementing the protocol.

4.0 provides workspace identity, four typed envelopes, Branch, explicit convergence, authorization binding, durable idempotency, concurrent linearization, crash recovery and versioned rule distribution. The eight testable contracts are C1 workspace identity, C2 envelopes, C3 lifecycle, C4 relations, C5 convergence, C6 authorization, C7 idempotency, C8 atomic recovery. The seven historical architecture concepts do not replace C1–C8.

The existing **45 MCP tool names acquire 4.0 version routing and protocol semantics**; the new name is **T6 `reopen_task`**, bringing the total to **46**. T6 is `done → active`, **not a Branch-only tool**. Discovery does not mean every legacy action supports v4: `finish_task` and history tools reject v4; `close_issue` is not added.

Concurrency is a shared write contract, not a standalone tool: atomic writes, linearization, durable `operation_id`, exact retry, conflict rejection, zero-side-effect failure, recovery and consistent `family_digest`. Locks and receipts are required mechanisms; neither an actor field nor a single rename grants authority.

## Stable installation

Use a fresh virtual environment; activate it in your shell before installing:

```bash
python -m venv .venv
python -m pip install fcop==4.0.0 fcop-mcp==4.0.0
```

## Candidate installation

Before Stable publication, obtain the exact artifacts and SHA-256 hashes from the WP4F Manifest and install into a **separate new virtual environment**. The published historical RC remains available separately:

```bash
python -m pip install ./candidate/fcop-4.0.0-py3-none-any.whl ./candidate/fcop_mcp-4.0.0-py3-none-any.whl
python -c "from importlib.metadata import version; print(version('fcop'), version('fcop-mcp'))"
```

The exact Stable pair is `fcop==4.0.0 / fcop-mcp==4.0.0`; the adapter declares `fcop>=4.0.0,<4.1.0`. Do not mix release lines. Existing 3.x workspaces keep their original semantics; installing does not authorize migration, rule redeployment or downstream upgrades.

## Minimal Python entry (verified 4.0)

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from fcop import Project

with TemporaryDirectory(prefix="fcop-demo-") as directory:
    project = Project(Path(directory) / "workspace")
    workspace = project.create_workspace(protocol_version="4.0")
    request = dict(
        workspace_id=workspace["workspace_id"], operation_id="demo-create-1",
        sender="ME", recipient="ME", subject="First task", body="Read-only research",
    )
    first = project.create_task(**request)
    again = project.create_task(**request)
    assert again["existing"] and again["task_id"] == first["task_id"]
    print(first["task_id"])
```

## Minimal MCP entry (verified 4.0)

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

Replace both paths. On Windows use the absolute `.venv/Scripts/fcop-mcp.exe` path. Never point a demo at an existing workspace. Call `init_solo(role_code="ME", protocol_version="4.0")`, then `create_task` with the returned `workspace_id` and an explicit `operation_id`.

The trusted Profile registry defaults to empty. T4–T7 require adopted evaluators registered at **trusted server initialization**. Caller code, YAML, `actor` and `profile_ref` alone cannot grant authority. The [standalone MCP example](examples/v4/third-party/mcp-only/client.py) uses only public stdio JSON-RPC, with no client imports of either package. Its server evaluator is **educational, not production security**.

## Branch and explicit convergence

This is a parameter map, not runnable code that omits required evidence:

```text
create_task(branch_of=...)
inspect_task(include_family_digest=true)
write_report(attempt_id=...)
write_review(review_kind="convergence", family_digest=..., references=...)
archive_task(review_ref=..., family_digest=...)
```

Create a Root and two Branches. Complete each Branch with its current `attempt_id` REPORT and acceptance authorization, then complete the Root. Query the canonical family digest, append a convergence REVIEW referencing Branch REPORT heads, and archive the Root with convergence evidence and a separate digest-bound T7 authorization. Core revalidates under the family lock. Changed digest or reused authorization is rejected. REPORT/REVIEW remain immutable.

## Versioned rules and compatibility

Nine bilingual modules form 18 canonical rule files and one Manifest. Assemblies: `sequential`, `parallel`, `repository-development`. Business-agent rules and repository-development rules are separate. Static Host profiles select deterministic `reference` / `bounded_embed` projections. Adoption, zero-write plan, deployment receipt and rollback are explicit. No Host probing, automatic migration or background service. Disk, index, adoption, Host entry and Runtime consumption are separate facts.

## Documentation and history

- [4.0 EN](spec/fcop-4.0-spec.md) / [4.0 ZH](spec/fcop-4.0-spec.zh.md)
- [3.x EN](spec/fcop-v3-spec.md) / [3.x ZH](spec/fcop-v3-spec.zh.md)
- [MCP tools](docs/mcp-tools.md) / [MCP Adapter](mcp/README.md)
- [RC guide](docs/fcop-4.0/rc-candidate-guide.md) / [Python example](tests/stable/third-party/python-only/app.py)
- [CHANGELOG](CHANGELOG.md) / [ADR index](adr/README.md)
- [Research EN](essays/when-ai-organizes-its-own-work.en.md) / [研究 ZH](essays/when-ai-organizes-its-own-work.md)
- [License](LICENSE) / [Citation](CITATION.cff)
- Legacy installation prompts only: [EN](src/fcop/rules/_data/agent-install-prompt.en.md) / [ZH](src/fcop/rules/_data/agent-install-prompt.zh.md), also discoverable at `fcop://prompt/install`. These historical prompts do not authorize RC installation or migration.

Historical tutorials describe their stated versions, not automatic 4.0 upgrades. The historical 3.2.5 archive is [DOI 10.5281/zenodo.20457285](https://doi.org/10.5281/zenodo.20457285), registered at [OSF 92nwm](https://osf.io/92nwm/). Neither identifies 4.0.0; no new DOI or Registry record is created here.

## Release boundary

WP4F promotes the accepted RC without new protocol or business behavior. Phase A verifies reproducible Stable artifacts and real clients. Publication and the specifically authorized local MCP upgrade require ADMIN's `FCOP_4_STABLE_RELEASE_READY` Gate. The RC is retained; no observation period, automatic workspace migration, Registry or Zenodo update is introduced. See [4.0.0 release notes](docs/releases/4.0.0.md).
