# 0.7.x → 1.0 迁移指南

> 面向 **现有 `fcop@0.7.x` 用户**（包括库使用者、MCP 用户、CodeFlow / Bridgeflow 等下游集成方）。
> 如果你是从 0 开始用 FCoP，直接看 [README](../README.md) + [v1.0 protocol spec](../spec/fcop-runtime-protocol-v1.0.md)，不必读本文。

---

## TL;DR

| 你是怎么用的 | 需要做什么 |
|---|---|
| 0.7.x `Project()` Python 库；项目里已有 `docs/agents/` | 升级到 `fcop>=1.0.0` 后 **一次性**跑 `fcop migrate-workspace --apply`（git-aware，会保留历史）；不想动盘就传 `Project(path, workspace_dir="docs/agents")` 显式锁定 |
| 0.7.x `fcop-mcp` MCP server | 升级到 `fcop-mcp>=1.0.0` + `fcop>=1.0.0`（lockstep），MCP 配置不变 |
| 还没 init 过的全新项目 | 啥也不用做。新 `init_project` / `init_solo` 直接落到顶层 `fcop/` |
| 0.5/0.6/0.7 老 TASK / REPORT / ISSUE 文件 | **零迁移**——frontmatter / filename / 字段全部继续可读（per ADR-0003 稳定性宪章 §0.7→1.0 grandfather 条款）|
| 写过 `from fcop.core.event_log import _emit_event_stub` 这种私有符号 | 改用 `Project.subscribe_events()` / `Project.poll_once()`（per ADR-0018）|
| 用 `docs/agents/` 字符串做过 hard-coded 路径拼接 | 改读 `project.workspace_dir` / `project.tasks_dir` 等 property，不要再拼字面量 |

1.0 的核心 framing 是：**FCoP 不再是 "AI 协作规则"，而是 AI OS 协议层（Agent Runtime Protocol）**——七大核心概念（Agent、IPC、Encoding、Event、Failure、Boundary、Audit）的最小语义契约正式固化为稳定标准。

但**对你的现有文件而言**，1.0 是 **零迁移升级**：所有 0.7.x 文件继续 100% 可读，agent 行为同语义。唯一物理动作是 workspace 目录从 `docs/agents/` → `fcop/`，且**只在你想动的时候动**（escape hatch 永久保留）。

---

## 0. 心智模型：3 个独立的"breaking 维度"

1.0 的 breaking 不是一个整体，而是 3 条独立轴。读下面任何章节前请先看清自己处于哪条轴：

| 维度 | 0.7.x | 1.0 | 你的应对 |
|---|---|---|---|
| **协议 framing** | "AI 协作规则" | "AI OS 协议层 / Agent Runtime Protocol" | 心智更新；文件不动 |
| **workspace 默认目录** | `<root>/docs/agents/` | `<root>/fcop/`（v1.0 默认）；`docs/agents/` 仍合法（escape hatch）| 选 A / B / C 之一（见 §2）|
| **新增 4 抽象**（REVIEW / Failure / Boundary / Event）| 不存在 | 公开 API + JSON Schema + reference impl | 看你要不要用；不用零成本（additive only）|

3 条轴**互相正交**——比如你可以"接受新 framing 但不动 workspace"，或者"动 workspace 但暂不用 4 抽象"。本指南按这 3 条轴分章节展开。

---

## 1. 协议 framing 升级：从"规则"到"协议"

### 1.1 概念变化

0.7.x 的 README / 内部交流里 FCoP 被描述为"AI 协作的 9 条规则"。1.0 起的官方定位是：

> **FCoP 是 AI OS 的协议层 / POSIX 类比**——定义 7 个最小语义合约（Agent / IPC / Encoding / Event / Failure / Boundary / Audit），任何符合合约的 host / runtime / 编辑器都能复用同一套 agent。

这不是营销词——它直接影响 1.0 的版本承诺：

- **协议 = 7 抽象的 minimum semantic contract**（见 [`spec/fcop-runtime-protocol-v1.0.md`](../spec/fcop-runtime-protocol-v1.0.md)）。任何修改协议的变更需要 MAJOR bump（v2.x）
- **reference implementation = `fcop` Python 库 + `fcop-mcp`**。本身遵守 SemVer：MINOR 可加新方法，PATCH 仅 bug fix
- **Rules 9 条**继续作为 `fcop-rules.mdc` 落到用户项目（per ADR-0006），是**协议向 agent 的运行时投影**

### 1.2 你需要做什么

- ✅ 心智更新：以后跟人讲 FCoP 时说"协议层"而不是"规则集"，你写的下游集成会更清晰
- ✅ 阅读 [`spec/fcop-runtime-protocol-v1.0.md`](../spec/fcop-runtime-protocol-v1.0.md)（约 30 分钟），尤其 §"7 抽象"那张总表
- ✅ 更新 README / 文档中对 FCoP 的描述（如果你的项目对外提到 FCoP）
- ❌ **不需要**改一行代码或一份文件

---

## 2. Workspace 默认目录：`docs/agents/` → `fcop/`

这是 1.0 **唯一的物理 breaking**。决议见 [ADR-0022](../adr/ADR-0022-workspace-directory-convention.md)。

### 2.1 为什么改

0.7.x 把 FCoP 工作区放在 `docs/agents/`。问题：

- `docs/` 暗示"文档"语义，遮蔽了"这块目录被 FCoP 占用"的事实
- 主流工具都用自己的命名空间：`.git/` / `.cursor/` / `node_modules/` / `.venv/` / `.next/`——FCoP 应该同族
- 用户的"自然 docs"和"FCoP 协议占用区"混在一起，多 FCoP 项目混合时一眼难识

1.0 起 FCoP 工作区默认住在顶层 `<root>/fcop/`，作为"协议命名空间"占位。

### 2.2 你的 3 个选项

#### 选项 A — 接受新默认（推荐）

跑一次自动迁移工具：

```bash
# 1. 升级到 1.0+
pip install --upgrade fcop fcop-mcp   # 或 uv pip install -U ...

# 2. 先 dry-run 看一眼会动什么
fcop migrate-workspace

# 3. 真改盘（git-aware：tracked path 自动用 git mv 保留历史）
fcop migrate-workspace --apply
```

会发生什么：

- `docs/agents/` 整个 tree 移到 `fcop/`，`git log --follow` 仍能查 0.7.x 时代每个文件
- 落地一份 `fcop/MIGRATED_FROM_DOCS_AGENTS.md` 留痕（含时间戳 + 源 + CLI 版本号）
- 顾问扫描会列出 `.gitignore` / `.cursor/rules/*.mdc` / `AGENTS.md` / `CLAUDE.md` / `README*.md` 中字符串包含 `docs/agents` 的行——**仅列出，不自动改写**（避免误伤你的用户文档）。看到这些 hits 后人工逐个判断：是历史叙述（保留）还是路径引用（手改 → `fcop`）

之后所有 `Project()` 调用、`fcop-mcp` 工具调用都自动看到新位置。

#### 选项 B — 永远锁定 `docs/agents/`（escape hatch）

不想动盘，或者你的 CI / docs site 已经深度依赖 `docs/agents/` 路径：

```python
from fcop import Project

project = Project(repo_root, workspace_dir="docs/agents")
# ↑ 永远合法，永不打 DeprecationWarning，连 v2.x 都保留
```

或者保持不传任何参数——0.7.x 项目检测到 `docs/agents/` 后会**自动用它**，只是会打一次 `DeprecationWarning` 提醒你 migrator 的存在。把 warning 当 lint hint，不影响功能。

如果你用 `fcop-mcp`，目前 MCP 没有暴露 `workspace_dir` 参数（per ADR-0022 §"MCP 表面稳定约束"），所以选 B 时建议直接在调用 `Project()` 处显式传，或者干脆走选项 A。

#### 选项 C — 用自定义路径（罕见，monorepo / 多项目共享）

```python
project = Project(repo_root, workspace_dir="/absolute/path/to/shared-fcop")
# 或相对：workspace_dir="apps/web/agents"
```

适用场景：monorepo 里有多个 sub-project 共享同一个 FCoP 工作区，或者把 FCoP 工作区放在 git submodule 里。

### 2.3 自动 detect 矩阵

不传 `workspace_dir=` 时，`Project()` 按以下规则决定：

| `<root>/fcop/` | `<root>/docs/agents/` | 行为 |
|---|---|---|
| 存在 | 不存在 | 用 `fcop/`（v1.0 默认）|
| 不存在 | 存在 | 用 `docs/agents/` + 打 `DeprecationWarning` 指向 migrator |
| **都存在** | **都存在** | 抛 `ConfigError` ABORT，要求显式 `workspace_dir=` 消歧 |
| 都不存在 | 都不存在 | 默认 `fcop/`（v1.0 fresh init）|

**双存在 = 半迁移状态**，FCoP 拒绝猜测——这种情况要么你迁移卡在中间，要么你刻意保留两套。无论哪种，正确做法是显式选一个。

### 2.4 内省 API

新增 `Project.workspace_layout` property（read-only）：

| 值 | 含义 |
|---|---|
| `"v1"` | 当前用 `<root>/fcop/`（自动 detect 或新 init）|
| `"legacy"` | 当前用 `<root>/docs/agents/`（auto-detect 命中老 layout，已打 warning）|
| `"explicit"` | 用户显式传了 `workspace_dir=`，FCoP 不假设 layout 形态 |

适合 IDE plugin / CI / 下游 wrapper 用来给用户提示。

### 2.5 完全 rollback

如果你跑了 `fcop migrate-workspace --apply` 后想撤销（极少见，通常是想去 `docs/` 子树和别的脚本对齐）：

```bash
# git 项目：直接 revert 那次 commit 即可
git log --diff-filter=R --summary | grep "rename docs/agents" | head
git revert <commit>

# 非 git 项目：手工 mv 回去
mv fcop docs/agents
```

迁移工具不会动 `.git/`，rollback 安全。

---

## 3. 4 个新抽象（REVIEW / Failure / Boundary / Event）—— 加不加随意

1.0 将七大核心概念（Agent、IPC、Encoding、Event、Failure、Boundary、Audit）全部固化，但其中 4 个（除 Agent / IPC / Encoding 之外）在 0.7.x 没有任何 API 表面，是**纯 additive expansion**。你不主动用就**永远碰不到它们**——你的 0.7.x 代码 100% 继续工作。

下面给极简 walkthrough，详细见 each ADR + `spec/schemas/`。

### 3.1 REVIEW — 第 4 类 IPC envelope（per ADR-0017）

让 reviewer 角色写 review 评注，独立于 TASK/REPORT/ISSUE：

```python
project.write_review(
    target_id="REPORT-20260509-007",
    reviewer="REVIEWER",
    body="LGTM with one nit: ...",
    decision="approve",   # approve | reject | needs_changes
)
```

落到 `<workspace>/reviews/REVIEW-20260509-001-REVIEWER-on-REPORT-20260509-007.md`，归档时跟 TASK 一起进 `log/reviews/`。

### 3.2 Failure / Recovery — 失败语义 + 续接（per ADR-0019）

```python
from fcop import FailureKind, RecoveryAction

# Agent 主动报错（recoverable）
project.report_failure(
    task_id="TASK-20260509-013",
    kind=FailureKind.TOOL_TIMEOUT,
    detail="LLM API 504 after 3 retries",
)

# Session 恢复
recovered = project.recover_session(
    session_id="main-2026-05-09",
    action=RecoveryAction.RESUME,   # RESUME | RETRY | ABANDON
)
```

会写一份 `<workspace>/failures/FAILURE-...md` 和（可选）`<workspace>/recoveries/RECOVERY-...md`。

### 3.3 Boundary / Capability — 角色权限边界（per ADR-0020）

```python
from fcop import BoundaryViolation

# 检查某 role 是否被允许做某 action
try:
    project.assert_boundary(
        actor="QA",
        action="write_task",   # write_task | write_report | write_issue | write_review | apply_recovery
    )
except BoundaryViolation as exc:
    print(f"QA cannot write_task: {exc}")
```

边界规则从 `<workspace>/fcop.json` 的 `boundaries` 字段（v1.0 新增字段）读取；不配置 = 全允许（向后兼容）。

### 3.4 Event Model — Polling watcher（per ADR-0018）

```python
from fcop import EventType

def on_change(event):
    print(f"[{event.type}] {event.source.path}")

sub = project.subscribe_events(
    types=[EventType.TASK_CREATED, EventType.REPORT_CREATED],
    callback=on_change,
)

# 显式跑一次 polling 周期（v1.0 不引入后台线程，调度由 caller 决定）
project.poll_once()

# 取消订阅
sub.unsubscribe()
```

12 类事件值域见 `spec/schemas/event.schema.json`。

---

## 4. JSON Schema 形式化（per ADR-0016）—— 给写工具的人

如果你写 IDE plugin / CI 检查 / 替代 host：

```python
from fcop.core.jsonschema_validator import validate_against_schema

errors = validate_against_schema(
    instance=task_dict,            # frontmatter 解析后的 dict
    schema_name="task",            # task | report | issue | review | event | failure | recovery
)
if errors:
    for e in errors:
        print(f"  {e.path}: {e.message}")
```

7 份 schema 在 `spec/schemas/*.schema.json`，wheel 内 `fcop/_data/schemas/` 是 byte-identical 副本（守门测试见 `tests/test_schemas/test_wheel_copies_match.py`）。

`referencing.Registry` 跨文件 `$ref` 解析已就位；自定义 schema 可以 `$ref: ./common.schema.json` 复用枚举值域。

---

## 5. 常见踩坑

### 5.1 我是 0.5/0.6/0.7 任意一个版本，跳级到 1.0 安全吗

安全。0.5 → 0.6 是包拆分（已有 [MIGRATION-0.6.md](./MIGRATION-0.6.md)）；0.6 → 0.7 是协议规则补强（无破坏性变更）；0.7 → 1.0 是本指南覆盖的范围。3 段叠加后：

- 包：必装 `fcop>=1.0.0` + `fcop-mcp>=1.0.0`（如果用 MCP）
- API：`from fcop import Project`（不要再用 `fcop.server` / `fcop.core.*` 私有路径）
- 文件：0.5 时代的 `reports/TASK-xxx.md`（非 `REPORT-` 前缀）从 0.6 起被 agent 视角忽略；想纳管就改名（详见 [MIGRATION-0.6.md §1.2](./MIGRATION-0.6.md)）
- workspace：跑 `fcop migrate-workspace --apply` 一次

### 5.2 我用 `from fcop.core.event_log import ...` 这种私有符号

`fcop.core.*` 一直是**内部模块**（per ADR-0001 库 API 定义），1.0 不保证其稳定性。1.0 起 Event 模型公开走 `from fcop import EventType, EventSource, EventSubscription`，回调走 `Project.subscribe_events`。任何依赖 `fcop.core.event_log` / `fcop.core._private_*` 的代码升 1.0 应迁到公开 API。

### 5.3 CI / pre-commit hook 里写了 `find docs/agents/tasks/`

跑完 `fcop migrate-workspace --apply` 后改成 `find fcop/tasks/`，或者更稳——直接调 `python -c "import fcop; print(fcop.Project('.').tasks_dir)"` 拿真实路径，永不 hard-code。

### 5.4 多 FCoP 项目混跑（monorepo）

每个 `Project()` 实例独立 detect。如果 monorepo 里有些 sub-project 已迁 `fcop/`、有些还在 `docs/agents/`，互不干扰。监控 `Project.workspace_layout` 可以看哪些还需要迁。

### 5.5 fcop-mcp 升级后，老的 `init_project` reply 里说 `docs/agents/LETTER-TO-ADMIN.md`，是 bug 吗

不是。0.7.x reply 是 hard-coded 字符串。1.0 起 reply 中的 LETTER 路径基于 `project.workspace_dir.relative_to(project.path)` **动态生成**：

- 新 init 项目（fcop/ layout）→ reply 显示 `fcop/LETTER-TO-ADMIN.md`
- 老项目（docs/agents/ layout）→ reply 显示 `docs/agents/LETTER-TO-ADMIN.md`
- 自定义 workspace → reply 显示自定义路径

这是 ADR-0022 Phase 2 的一部分（commit `861713b`），保证你看到的路径就是文件实际落地处。

### 5.6 已经在 v1.0 RC 上跑过迁移，要再升 final 时怎么办

啥都不用做。`v1.0.0-rc.1` → `v1.0.0` final 不会有任何破坏性改动（per ADR-0003 §SemVer 仅允许 bug fix / docs / additive deferred-from-RC），你 RC 上的迁移直接继承到 final。

---

## 6. 时间线参考

| 你的项目状态 | 估时 | 包含的步骤 |
|---|---|---|
| 全新项目 | 0 分钟 | 不需要做任何事 |
| 0.7.x、不动 workspace（选项 B）| 5 分钟 | `pip install -U fcop fcop-mcp` + 看一眼 DeprecationWarning |
| 0.7.x、接受新默认（选项 A）| 15-30 分钟 | upgrade + dry-run 检查 + `--apply` + 顾问 hits 人工 review |
| 0.7.x + 重度依赖 `fcop.core.*` 私有符号 | 1-2 小时 | 上面 + 私有符号迁公开 API |
| 0.5/0.6 跳级 | +1 小时 | 上面 + 0.6 包拆分迁移（[MIGRATION-0.6.md](./MIGRATION-0.6.md)）|
| 自己写了 IDE plugin / 替代 host | 2-4 小时 | 上面 + 接 7 个 JSON Schema 校验 + 4 抽象新 API |

---

## 7. 进一步阅读

- [`v1.0 protocol spec`](../spec/fcop-runtime-protocol-v1.0.md) —— 协议本体（normative，~30 分钟）
- [`spec/schemas/`](../spec/schemas/) —— 7 份 JSON Schema（machine-readable）
- [`adr/`](../adr/) —— v1.0 的 8 份 ADR（0015-0022），每份 5-15 分钟
- [`docs/releases/1.0.0-rc.1.md`](./releases/1.0.0-rc.1.md) —— RC 候选版的完整发布说明
- [`CHANGELOG.md`](../CHANGELOG.md) —— 0.7.2 → 1.0 完整变更日志
- [`MIGRATION-0.6.md`](./MIGRATION-0.6.md) —— 0.5.x → 0.6.0 迁移指南（如果你跨更老版本升级）

---

## 8. 出问题？

- GitHub Issues：<https://github.com/joinwell52-AI/FCoP/issues>
- 已知 v1.0 RC issue 列表：<https://github.com/joinwell52-AI/FCoP/issues?q=is%3Aissue+label%3Av1.0>
- 提 issue 时请带：`fcop --version`、`fcop-mcp --version`、Python 版本、OS、复现步骤、期望 vs 实际 behavior
