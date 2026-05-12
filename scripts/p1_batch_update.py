"""P1 Batch Update — append v1.0~v1.4 protocol update sections to team/role docs.

Covers:
  - Non-leader role docs (DEV/QA/OPS/WRITER/TESTER etc.) × zh+en
  - TEAM-ROLES.md × all teams × zh+en
  - TEAM-OPERATING-RULES.md × all teams × zh+en
  - team README.md × all teams × zh+en
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEAMS_DATA = ROOT / "src" / "fcop" / "teams" / "_data"
TODAY = "2026-05-12"

# ── content blocks ───────────────────────────────────────────────────────────

ROLE_UPDATE_ZH = """
---

## v1.0 ~ v1.4 协议更新速查

> 本节汇总 v1.0 起协议层面引入的重要变化，执行角色需了解的关键点。
> 详细说明见 `.cursor/rules/fcop-protocol.mdc` 和 `docs/releases/`。

### REVIEW envelope（v1.0）

高风险任务由 leader（`PM` / `LEAD-QA` 等）标注 `risk_level: high` 时，
会自动生成 `REVIEW-*.md` 待审批文件。执行角色须知：

- 任务带有 `needs_human: true` 时，**必须等待 ADMIN 批准**后再执行
- 批准动作：ADMIN 调 `mark_human_approved(review_id=...)`
- 未获批准**不得越权执行**，等 leader 通知继续

### risk_level 字段（v1.1）

TASK 文件中可含 `risk_level: low / medium / high`（由 leader 在派单时标注）：

- `high` → 自动生成 REVIEW，需 ADMIN 批准方可执行
- 执行角色**以 leader 标注为准**，不自行升降级
- 收到 `needs_human: true` 的 TASK → 停手，等 ADMIN / leader 通知

### fcop_audit 与 INSPECTION（v1.3）

`fcop_audit()` 由 **leader 或 ADMIN** 运行，你无需主动调用。但需了解：

- `INSPECTION-*.md` 体检报告出现在 `fcop/shared/` 后，可能派发整改 TASK 给你
- 在回执里引用 INSPECTION 报告 ID（`references=["INSPECTION-..."]`）
- 如收到来自 INSPECTION 的整改任务，正常走"四步流程"即可

### supersedes 字段（v1.4）

如果你的 TASK / REPORT 文件**修正**了某份历史文件，可加可选字段：

```yaml
supersedes: TASK-20260418-010   # 本文件替代该历史文件
# 或多个：
supersedes:
  - TASK-20260418-010
  - REPORT-20260418-005
```

`list_tasks` / `list_reports` 工具会自动双向标注 `[supersedes X]` / `[superseded by X]`。
"""

ROLE_UPDATE_EN = """
---

## Protocol Updates v1.0 ~ v1.4

> Quick reference for key protocol changes introduced since v1.0.
> Full details in `.cursor/rules/fcop-protocol.mdc` and `docs/releases/`.

### REVIEW envelope (v1.0)

When a leader (`PM`, `LEAD-QA`, etc.) marks a task with `risk_level: high`,
a `REVIEW-*.md` approval file is automatically generated. What you need to know:

- If a task has `needs_human: true`, **wait for ADMIN approval** before acting
- Approval action: ADMIN calls `mark_human_approved(review_id=...)`
- Do **not** proceed without approval — wait for the leader to notify you

### risk_level field (v1.1)

TASK files may contain `risk_level: low / medium / high` (set by the leader):

- `high` → automatically generates a REVIEW; requires ADMIN approval to proceed
- Execution roles **follow the leader's rating**; do not change it yourself
- If you see `needs_human: true` → stop and wait for ADMIN / leader

### fcop_audit and INSPECTION (v1.3)

`fcop_audit()` is run by the **leader or ADMIN** — you don't need to call it.
But you should know:

- `INSPECTION-*.md` reports appear in `fcop/shared/`; they may produce remediation
  tasks assigned to you
- Reference the INSPECTION ID in your report (`references=["INSPECTION-..."]`)
- If you receive a task that originates from an INSPECTION finding, follow the
  standard four-step workflow

### supersedes field (v1.4)

If your TASK / REPORT **replaces** a historical file, add the optional field:

```yaml
supersedes: TASK-20260418-010   # this file replaces the referenced file
# or multiple:
supersedes:
  - TASK-20260418-010
  - REPORT-20260418-005
```

`list_tasks` / `list_reports` will automatically annotate both directions:
`[supersedes X]` and `[superseded by X]`.
"""

TEAM_ROLES_EVOLUTION_ZH = """
---

## 协议演进说明（v1.0 ~ v1.4）

| 版本 | 变更 | 影响角色 |
|---|---|---|
| v1.0 | REVIEW envelope：高风险任务生成 `REVIEW-*.md`，需 ADMIN 批准 | leader / 全部 |
| v1.1 | `risk_level` 字段：`low / medium / high`；`needs_human` 自动触发人工审批 | leader 派单时设置 |
| v1.3 | `fcop_audit()`：协议体检工具，生成 `INSPECTION-*.md` 报告 | leader / ADMIN |
| v1.3 | GAL（治理告警层）：`fcop_create_alert` / `fcop_list_alerts` | leader |
| v1.4 | `supersedes:` 字段：文件级修正链（区别于 `parent:` 派生）| 全部 |
| v1.4 | write-side 工具须显式绑定项目路径（`set_project_dir()`）| MCP Server 层 |

> leader 角色的详细工具速查见对应 `roles/` 文件。
"""

TEAM_ROLES_EVOLUTION_EN = """
---

## Protocol Evolution (v1.0 ~ v1.4)

| Version | Change | Affected roles |
|---|---|---|
| v1.0 | REVIEW envelope: high-risk tasks generate `REVIEW-*.md`, require ADMIN approval | leader / all |
| v1.1 | `risk_level` field: `low / medium / high`; `needs_human` triggers human approval | leader (on dispatch) |
| v1.3 | `fcop_audit()`: protocol health-check tool, produces `INSPECTION-*.md` | leader / ADMIN |
| v1.3 | GAL (Governance Alert Layer): `fcop_create_alert` / `fcop_list_alerts` | leader |
| v1.4 | `supersedes:` field: file-level correction link (distinct from `parent:` derivation) | all |
| v1.4 | Write-side tools require explicit project binding (`set_project_dir()`) | MCP Server layer |

> See the corresponding `roles/` file for each leader's detailed tool quick reference.
"""

TEAM_OPERATING_RULES_EVOLUTION_ZH = """
---

## 协议演进补记（v1.0 ~ v1.4）

本节补记协议演进带来的运行规则变化：

### 高风险任务审批（v1.0 引入）

- `PM`（leader）派单时标注 `risk_level: high`，系统自动生成 `REVIEW-*.md`
- 带 `needs_human: true` 的任务：执行角色**停手**，等 ADMIN 调 `mark_human_approved()`
- 未批准不得执行 → 此约束优先级高于任何"进度压力"

### fcop_audit 整改任务处理（v1.3 引入）

- ADMIN 或 leader 运行 `fcop_audit()` 后，`INSPECTION-*.md` 报告会记录协议缺口
- 对应整改任务（`TASK-*-ADMIN-to-PM.md`）可批量授权（`scope: batch-remediation`）
- 处理整改任务时同样走"四步流程"，并在回执中引用 INSPECTION ID

### 发布绑定规则（v1.4 引入）

- MCP Server 层：write-side 工具必须显式绑定项目路径
- 配置方式：在 MCP config 中设置 `FCOP_PROJECT_DIR`，或会话开始时调 `set_project_dir()`
- 未绑定时调用任何写入工具，将抛出 `WriteRefused` 错误
"""

TEAM_OPERATING_RULES_EVOLUTION_EN = """
---

## Protocol Evolution Addendum (v1.0 ~ v1.4)

Key operating rule changes introduced in recent protocol versions:

### High-risk task approval (introduced v1.0)

- Leader marks dispatch with `risk_level: high`; system generates `REVIEW-*.md`
- Tasks with `needs_human: true`: execution roles **stop and wait** for ADMIN
  to call `mark_human_approved()`
- No approval → no execution; this overrides any schedule pressure

### Handling fcop_audit remediation tasks (introduced v1.3)

- After ADMIN / leader runs `fcop_audit()`, `INSPECTION-*.md` records compliance gaps
- Remediation tasks (`TASK-*-ADMIN-to-PM.md`) may be batch-authorized
  (`scope: batch-remediation` in proposal frontmatter)
- Handle remediation tasks with the standard four-step workflow; reference the
  INSPECTION ID in your report

### Write-side binding requirement (introduced v1.4)

- Write-side MCP tools now require an explicit project path binding
- Configure via `FCOP_PROJECT_DIR` env var in MCP config, or call
  `set_project_dir()` at session start
- Calling any write tool without binding raises `WriteRefused`
"""

README_QUICKREF_ZH = """
---

## 工具速查链接

| 工具 | 场景 |
|---|---|
| `fcop_audit(scope="new")` | 新项目 `init_*` 完成后自检 |
| `fcop_audit(scope="upgrade")` | `pip install -U fcop` 升级后验收 |
| `fcop_audit(scope="takeover")` | 接手陌生老项目时第一步 |
| `fcop_report()` | 查看项目绑定、版本、告警摘要 |
| `fcop_list_alerts(status="open")` | 查看治理告警收件箱 |

> leader 角色详细工具速查见 `roles/<leader>.md` 末尾的"工具速查"节。
"""

README_QUICKREF_EN = """
---

## Tool Quick Reference

| Tool | Scenario |
|---|---|
| `fcop_audit(scope="new")` | Self-check after `init_*` on a new project |
| `fcop_audit(scope="upgrade")` | Verify after `pip install -U fcop` upgrade |
| `fcop_audit(scope="takeover")` | First step when inheriting an unfamiliar project |
| `fcop_report()` | View project binding, version, and alert summary |
| `fcop_list_alerts(status="open")` | View governance alert inbox |

> For detailed leader tool quick reference, see the "Tool Quick Reference" section
> at the end of `roles/<leader>.md`.
"""

# ── helpers ──────────────────────────────────────────────────────────────────

def update_frontmatter_date(text: str, new_date: str) -> str:
    return re.sub(r"(updated_at:\s*)\S+", rf"\g<1>{new_date}", text, count=1)


def append_section(path: Path, block: str, marker: str) -> None:
    """Append block to path unless marker already present."""
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"  SKIP (already has marker): {path.name}")
        return
    text = update_frontmatter_date(text, TODAY)
    text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")
    print(f"  UPDATED: {path.relative_to(ROOT)}")


# ── leader roles already updated in P0 ──────────────────────────────────────
LEADER_ROLES = {"PM", "ME", "LEAD-QA", "MARKETER", "PUBLISHER"}

# ── P1-1: non-leader role docs ───────────────────────────────────────────────

def update_role_docs() -> None:
    print("\n=== P1-1: Non-leader role docs ===")
    for role_dir in TEAMS_DATA.rglob("roles"):
        for f in sorted(role_dir.iterdir()):
            if not f.name.endswith(".md"):
                continue
            stem = f.stem  # e.g. DEV, DEV.en
            base = stem.split(".")[0]  # e.g. DEV
            if base in LEADER_ROLES:
                continue
            is_en = ".en" in stem
            block = ROLE_UPDATE_EN if is_en else ROLE_UPDATE_ZH
            marker = "Protocol Updates v1.0" if is_en else "v1.0 ~ v1.4 协议更新速查"
            append_section(f, block, marker)


# ── P1-2: TEAM-ROLES + TEAM-OPERATING-RULES ─────────────────────────────────

def update_team_docs() -> None:
    print("\n=== P1-2: TEAM-ROLES + TEAM-OPERATING-RULES ===")
    for team_dir in TEAMS_DATA.iterdir():
        if not team_dir.is_dir():
            continue
        for f in sorted(team_dir.iterdir()):
            if not f.is_file() or not f.name.endswith(".md"):
                continue
            is_en = ".en" in f.stem
            if "TEAM-ROLES" in f.name:
                block = TEAM_ROLES_EVOLUTION_EN if is_en else TEAM_ROLES_EVOLUTION_ZH
                marker = "Protocol Evolution" if is_en else "协议演进说明"
                append_section(f, block, marker)
            elif "TEAM-OPERATING-RULES" in f.name:
                block = TEAM_OPERATING_RULES_EVOLUTION_EN if is_en else TEAM_OPERATING_RULES_EVOLUTION_ZH
                marker = "Protocol Evolution Addendum" if is_en else "协议演进补记"
                append_section(f, block, marker)


# ── P1-3: team README files ──────────────────────────────────────────────────

def update_readme_files() -> None:
    print("\n=== P1-3: Team README files ===")
    for team_dir in TEAMS_DATA.iterdir():
        if not team_dir.is_dir():
            continue
        for f in sorted(team_dir.iterdir()):
            if not f.is_file():
                continue
            if f.name == "README.md":
                append_section(f, README_QUICKREF_ZH, "工具速查链接")
            elif f.name == "README.en.md":
                append_section(f, README_QUICKREF_EN, "Tool Quick Reference")


# ── main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    update_role_docs()
    update_team_docs()
    update_readme_files()
    print("\nDone. Now handle P1-4 (getting-started) and P1-5 (agent-install-prompt) manually.")
