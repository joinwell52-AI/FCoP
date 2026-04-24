# ADR-0001: `fcop` Library API（`import fcop`）

- **Status**: Accepted (2026-04-23, ratified with 0.6.0 release)
- **Date**: 2026-04-22
- **Deciders**: ADMIN
- **Related**: [ADR-0002](./ADR-0002-package-split-and-migration.md)（拆包与迁移）

## Context

### 今天的 `fcop`

截至 0.5.4，PyPI 上的 `fcop` 包是一个 **MCP 服务器**：

- 唯一入口 `[project.scripts] fcop = "fcop.server:main"` 启动 stdio MCP 服务器
- `src/fcop/server.py` ~3500 行，22 个 `@mcp.tool`、10 个 `@mcp.resource`
- 所有"能做的事"都只暴露给 MCP 客户端（Cursor / Claude Desktop / 支持 MCP 的 IDE 和框架）
- `import fcop` 实际拿到的只有 `main`（MCP 入口）和一个 `__version__`
  （后者在 0.5.x 全程忘了 bump，仍是 `0.4.1`）

如果要"作为 Python 库"直接使用，唯一出路是走脏后门：

```python
from fcop.server import write_task, list_tasks, _read_fcop_json
```

这些函数被 `@mcp.tool` 装饰过，**返回值是人类可读字符串而不是结构化数据**，
并且依赖模块级全局（`PROJECT_DIR`、`TASKS_DIR`），多项目并发会撞车。
这条路能走但难受，而且没有版本语义承诺。

### 为什么要开库 API

当前定位只服务于"跑在 MCP 宿主里的 AI agent"。但 FCoP 本身是**文件协议**，
天然应该服务更广的场景：

1. **直接对接大模型 API 的应用**：用户自己写 Python 应用，用 OpenAI / Anthropic /
   Gemini SDK，需要一个"处理 FCoP 任务文件"的库，而**不想**起 MCP server。
2. **CLI 工具**：`fcop task new --to DEV --priority P1`，无 LLM 也能对文件做协议操作。
3. **CI / 自动化**：GitHub Actions 里校验仓库的 `docs/agents/` 符合 FCoP 规则。
4. **可观测性 / 仪表盘**：读 `docs/agents/` 渲染一个团队状态 Web UI。
5. **其他 MCP 实现**：基于 `fcop` 这个库，用其他 MCP SDK（非 FastMCP）写等价服务器。

这些场景**都不需要 MCP**。把它们强行塞 MCP 是架构错位。

### 约束

库 API 必须满足：

1. **零 LLM 耦合**：库代码不调用任何 LLM，不依赖 OpenAI / Anthropic SDK。
2. **零 MCP 耦合**：库代码不 `import mcp`、不 `import fastmcp`。
3. **零全局状态**：不读环境变量、不使用模块级可变全局。所有配置通过依赖注入。
4. **结构化数据**：返回 dataclass（或 Pydantic model），**不返回**拼好的 Markdown/文本。
5. **线程/进程安全**：多个 `Project` 实例并存不干扰。
6. **跨平台**：Windows / macOS / Linux；Python >= 3.10。
7. **semver 承诺**：从 0.6.0 起，公开 API 的破坏性变更只能发生在 minor 版（0.x.0）。
8. **协议一致**：库内部操作**必须**和 `fcop-rules.mdc` 描述的规则一致，
   不能出现"库能做但协议不允许"或"协议要求但库做不到"的错位。

### 约束不是什么

- 库**不负责**驱动 agent 对话。这是使用者的事。
- 库**不负责**UI 渲染。返回 dataclass，UI 自己拼。
- 库**不内置** LLM 提示词模板。需要用 `fcop-rules.mdc` 注入 prompt 的使用者自己去
  `fcop.rules.get_rules()` 拿到字符串，爱怎么用怎么用。
- 库**不是** MCP 的替代品。MCP 和库是两条并行的使用方式，各有场景。

## Decision

**拆出纯 Python 库层 `fcop.core`，并在顶层 `fcop` 包中公开五类门面**：

1. **`fcop.Project`** —— 绑定一个项目根目录的对象，承载所有"会产生副作用"的操作
   （创建任务、归档、部署模板、读写配置）。
2. **`fcop.models`** —— 所有只读的数据结构：`Task`、`Report`、`Issue`、`TeamConfig`、
   `ProjectStatus`、`ValidationIssue`。均为 `@dataclass(frozen=True)` 或 Pydantic model。
3. **`fcop.teams`** —— 无状态模块，访问打包在 wheel 里的团队模板（`_data/teams/*`）。
4. **`fcop.rules`** —— 无状态模块，访问打包的协议规则文档（`fcop-rules.mdc` /
   `fcop-protocol.mdc` / `letter-to-admin.*.md`）。
5. **`fcop.errors`** —— 异常体系，基类 `FcopError`，具体异常如 `ProtocolViolation`、
   `ValidationError`、`ProjectNotFoundError` 等。

现有 `src/fcop/server.py` **重构为 `fcop-mcp` 包的薄壳**（见 ADR-0002），
每个 MCP tool 调用 `fcop.core` 拿结构化结果，再格式化成字符串。
业务逻辑归库，表达层归 MCP 壳。

## Design Details

### 包结构

```
src/fcop/
├── __init__.py           ← 公开 Project / models / 常用门面
├── _version.py           ← 单一版本源（pyproject.toml 用 dynamic = ["version"] 读它）
├── core/
│   ├── __init__.py
│   ├── project.py        ← Project 类
│   ├── task.py           ← Task / TaskFrontmatter 相关逻辑
│   ├── report.py         ← Report 相关逻辑
│   ├── issue.py          ← Issue 相关逻辑
│   ├── config.py         ← fcop.json 读写
│   ├── filename.py       ← 文件名生成/解析（TASK-YYYYMMDD-NNN-A-to-B.md）
│   ├── frontmatter.py    ← YAML frontmatter 解析与校验
│   ├── schema.py         ← 协议规则常量（role 正则、优先级枚举、allowed keys…）
│   ├── deploy.py         ← 模板部署（init_project / deploy_role_templates 的核心逻辑）
│   └── archive.py        ← 归档逻辑
├── models.py             ← 所有公开 dataclass
├── errors.py             ← 异常体系
├── teams/
│   ├── __init__.py       ← get_available_teams / get_template 等
│   └── _data/            ← 迁自原 _data/teams/
└── rules/
    ├── __init__.py       ← get_rules / get_protocol_commentary / get_letter
    └── _data/            ← 迁自原 _data/（fcop-rules.mdc、fcop-protocol.mdc、letter-to-admin.*）
```

原 `src/fcop/server.py` **不在此包**（见 ADR-0002，它成为 `fcop-mcp` 包的内容）。

### 公开 API 全貌（`fcop` 顶层命名空间）

以下是 `from fcop import ...` 能拿到的所有名字，**此清单即公共契约**。
0.x 期间可增可改可删；1.0 之后只能增。

```python
# 主入口
from fcop import Project

# 数据结构（只读）
from fcop import (
    Task, TaskFrontmatter,
    Report, Issue,
    TeamConfig, ProjectStatus,
    ValidationIssue,
    Priority, Severity,  # 枚举
)

# 异常
from fcop import (
    FcopError,
    ProtocolViolation,
    ValidationError,
    ProjectNotFoundError,
    ProjectAlreadyInitializedError,
    TaskNotFoundError,
    TeamNotFoundError,
    RoleNotFoundError,
    ConfigError,
)

# 子模块
from fcop import teams, rules

# 版本
from fcop import __version__
```

### `fcop.Project` 类

```python
class Project:
    """Represents an FCoP-managed project rooted at `path`."""

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        strict: bool = True,
    ) -> None:
        """
        Args:
            path: Absolute or relative path to project root (containing
                  `docs/agents/` when initialized).
            strict: If True, every operation validates against FCoP rules
                    and raises ProtocolViolation on any breach. If False,
                    best-effort mode (used by migration tools).

        Does NOT touch the filesystem. Use .init() or .is_initialized()
        to interact with the project.
        """

    # ── Identity ──────────────────────────────────────────────────

    @property
    def path(self) -> pathlib.Path: ...

    @property
    def tasks_dir(self) -> pathlib.Path: ...

    @property
    def reports_dir(self) -> pathlib.Path: ...

    @property
    def issues_dir(self) -> pathlib.Path: ...

    @property
    def shared_dir(self) -> pathlib.Path: ...

    @property
    def log_dir(self) -> pathlib.Path: ...

    # ── Lifecycle ─────────────────────────────────────────────────

    def is_initialized(self) -> bool:
        """True if `docs/agents/fcop.json` exists."""

    def init(
        self,
        *,
        team: str = "dev-team",
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """
        Create `docs/agents/{tasks,reports,issues,shared,log}/`, write
        `fcop.json`, deploy `.cursor/rules/fcop-rules.mdc` +
        `fcop-protocol.mdc`, deploy the team template and a welcome task.

        Raises:
            ProjectAlreadyInitializedError: if fcop.json exists and not force.
            TeamNotFoundError: if `team` is not a preset name.
        """

    def init_solo(
        self,
        *,
        role_code: str = "ME",
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize in Solo mode (single role, directly interfacing with ADMIN)."""

    def init_custom(
        self,
        *,
        team_name: str,
        roles: Sequence[str],
        leader: str,
        lang: str = "zh",
        force: bool = False,
    ) -> ProjectStatus:
        """Initialize with a custom role set. Equivalent of create_custom_team()."""

    @staticmethod
    def validate_team(
        *,
        roles: Sequence[str],
        leader: str,
    ) -> list[ValidationIssue]:
        """
        Dry-run validation of a custom team config. Returns issues.
        Empty list means the config is valid.
        """

    # ── Config ────────────────────────────────────────────────────

    @property
    def config(self) -> TeamConfig:
        """Read-only snapshot of docs/agents/fcop.json. Cached per-call."""

    # ── Status ────────────────────────────────────────────────────

    def status(self) -> ProjectStatus:
        """Counts and recent activity."""

    # ── Tasks ─────────────────────────────────────────────────────

    def write_task(
        self,
        *,
        sender: str,
        recipient: str,
        priority: Priority | str,
        subject: str,
        body: str,
        references: Sequence[str] = (),
        thread_key: str | None = None,
    ) -> Task:
        """
        Create a new task file. Returns the created Task.

        Filename is generated as TASK-YYYYMMDD-NNN-{sender}-to-{recipient}.md.
        NNN is auto-assigned based on today's existing task count + 1.

        Raises:
            ProtocolViolation: if sender→recipient breaks Rule 4 (role chain).
            ValidationError: if priority/subject/body missing or malformed.
        """

    def list_tasks(
        self,
        *,
        sender: str | None = None,
        recipient: str | None = None,
        status: Literal["open", "archived", "all"] = "open",
        date: str | None = None,   # YYYYMMDD filter
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Task]:
        """List tasks, optionally filtered."""

    def read_task(self, filename_or_id: str) -> Task:
        """
        Read a task by filename (TASK-…-A-to-B.md) or by task id (TASK-…-NNN).

        Raises:
            TaskNotFoundError: if no matching file.
        """

    def archive_task(self, filename_or_id: str) -> Task:
        """Move task (and matching report if any) to log/. Returns archived Task."""

    def inspect_task(self, filename_or_id: str) -> list[ValidationIssue]:
        """Validate a task file against FCoP schema. Empty list = valid."""

    # ── Reports ───────────────────────────────────────────────────

    def write_report(
        self,
        *,
        task_id: str,
        reporter: str,
        recipient: str,
        body: str,
        status: Literal["done", "blocked", "in_progress"] = "done",
    ) -> Report:
        """Create a report responding to a task."""

    def list_reports(
        self,
        *,
        reporter: str | None = None,
        task_id: str | None = None,
        limit: int | None = None,
    ) -> list[Report]:
        ...

    def read_report(self, filename_or_id: str) -> Report: ...

    # ── Issues ────────────────────────────────────────────────────

    def write_issue(
        self,
        *,
        reporter: str,
        summary: str,
        body: str,
        severity: Severity | str = "medium",
    ) -> Issue: ...

    def list_issues(self, *, limit: int | None = None) -> list[Issue]: ...

    def read_issue(self, filename_or_id: str) -> Issue: ...

    # ── Templates ─────────────────────────────────────────────────

    def deploy_role_templates(
        self,
        *,
        team: str | None = None,
        lang: str | None = None,
        force: bool = True,
    ) -> DeploymentReport:
        """
        Deploy three-layer team templates into docs/agents/shared/.

        If team/lang is None, reads from self.config. force=True uses the
        aggressive migration strategy (archive conflicting files to
        .fcop/migrations/<timestamp>/).

        Returns a DeploymentReport listing what was deployed, skipped,
        and archived.
        """

    # ── Suggestions ───────────────────────────────────────────────

    def drop_suggestion(
        self,
        *,
        content: str,
        context: str = "",
    ) -> pathlib.Path:
        """Append a proposal under .fcop/proposals/. Returns the written path."""
```

### 数据结构（`fcop.models`）

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal


class Priority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class TaskFrontmatter:
    protocol: str        # 'fcop'
    version: int         # 1
    sender: str          # role code
    recipient: str       # role code
    priority: Priority
    thread_key: str | None = None
    subject: str | None = None
    references: tuple[str, ...] = ()
    # Any extra YAML keys end up in `extra` for forward compat
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Task:
    path: Path                     # absolute path on disk
    filename: str                  # TASK-YYYYMMDD-NNN-A-to-B.md
    task_id: str                   # TASK-YYYYMMDD-NNN (without sender/recipient)
    date: str                      # YYYYMMDD
    sequence: int                  # NNN as int
    frontmatter: TaskFrontmatter
    body: str                      # markdown body (without frontmatter)
    is_archived: bool
    mtime: datetime

    @property
    def sender(self) -> str: return self.frontmatter.sender

    @property
    def recipient(self) -> str: return self.frontmatter.recipient

    @property
    def priority(self) -> Priority: return self.frontmatter.priority

    @property
    def subject(self) -> str | None: return self.frontmatter.subject


@dataclass(frozen=True, slots=True)
class Report:
    path: Path
    filename: str
    task_id: str                   # which TASK this report responds to
    reporter: str                  # role code
    recipient: str
    status: Literal["done", "blocked", "in_progress"]
    body: str
    is_archived: bool
    mtime: datetime


@dataclass(frozen=True, slots=True)
class Issue:
    path: Path
    filename: str                  # ISSUE-YYYYMMDD-NNN-summary.md
    issue_id: str
    summary: str
    severity: Severity
    reporter: str
    body: str
    mtime: datetime


@dataclass(frozen=True, slots=True)
class TeamConfig:
    mode: Literal["solo", "preset", "custom"]
    team: str                      # 'dev-team' / 'solo' / a custom name
    leader: str                    # role code
    roles: tuple[str, ...]         # all role codes (excluding ADMIN)
    lang: str                      # 'zh' | 'en'
    version: int                   # fcop.json schema version
    extra: dict[str, object] = field(default_factory=dict)

    @property
    def is_solo(self) -> bool: return self.mode == "solo"


@dataclass(frozen=True, slots=True)
class ProjectStatus:
    path: Path
    is_initialized: bool
    config: TeamConfig | None
    tasks_open: int
    tasks_archived: int
    reports_count: int
    issues_count: int
    recent_activity: tuple["RecentActivityEntry", ...]


@dataclass(frozen=True, slots=True)
class RecentActivityEntry:
    kind: Literal["task", "report", "issue"]
    filename: str
    mtime: datetime
    summary: str


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: Literal["error", "warning", "info"]
    field: str                     # e.g. 'frontmatter.recipient' or 'filename'
    message: str
    path: Path | None = None


@dataclass(frozen=True, slots=True)
class DeploymentReport:
    deployed: tuple[Path, ...]     # paths written
    skipped: tuple[Path, ...]      # paths skipped because existed (force=False)
    archived: tuple[Path, ...]     # paths moved to .fcop/migrations/
    migration_dir: Path | None     # the .fcop/migrations/<ts>/ dir if any
```

### 无状态模块：`fcop.teams`

```python
def get_available_teams() -> list[TeamInfo]:
    """List all bundled preset teams with their roles and descriptions."""


def get_team_info(team: str) -> TeamInfo:
    """
    Args:
        team: 'dev-team' | 'media-team' | 'mvp-team' | 'qa-team' | …

    Raises:
        TeamNotFoundError: if `team` is not bundled.
    """


def get_template(team: str, lang: str = "zh") -> TeamTemplate:
    """Fetch the full four-layer documentation for a bundled team."""


@dataclass(frozen=True, slots=True)
class TeamInfo:
    name: str                      # 'dev-team'
    display_name: str              # '开发团队' (zh) / 'Dev Team' (en)
    leader: str                    # 'PM'
    roles: tuple[str, ...]         # ('PM', 'DEV', 'QA', 'OPS')
    description_zh: str
    description_en: str


@dataclass(frozen=True, slots=True)
class TeamTemplate:
    name: str
    lang: str
    readme: str                    # TEAM-README.md content
    team_roles: str                # TEAM-ROLES.md content
    operating_rules: str           # TEAM-OPERATING-RULES.md content
    roles: dict[str, str]          # role_code -> role markdown
```

### 无状态模块：`fcop.rules`

```python
def get_rules() -> str:
    """
    Return the content of fcop-rules.mdc (the 9 core rules).
    Suitable for injecting into LLM system prompts.
    """


def get_protocol_commentary() -> str:
    """Return the content of fcop-protocol.mdc (the 'how to apply' commentary)."""


def get_letter(lang: Literal["zh", "en"] = "zh") -> str:
    """Return the Letter-to-ADMIN user manual in the requested language."""


def get_rules_version() -> str:
    """e.g. '1.4.0' — the semver of the shipped rules document."""
```

### 异常体系（`fcop.errors`）

```python
class FcopError(Exception):
    """Base class for all FCoP library errors."""


class ProtocolViolation(FcopError):
    """A requested operation would violate FCoP protocol rules."""
    rule: str                      # e.g. 'Rule 4.1' — the violated rule id


class ValidationError(FcopError):
    """Input failed validation."""
    issues: list[ValidationIssue]


class ProjectNotFoundError(FcopError):
    """The project root does not contain a valid FCoP structure."""
    path: Path


class ProjectAlreadyInitializedError(FcopError):
    """init() called on an already-initialized project (without force=True)."""


class TaskNotFoundError(FcopError):
    """No task file matches the given filename or id."""
    query: str


class TeamNotFoundError(FcopError):
    """The requested team is not bundled and not in the project config."""
    team: str


class RoleNotFoundError(FcopError):
    """The requested role code is not registered in the project config."""
    role: str


class ConfigError(FcopError):
    """docs/agents/fcop.json is missing, malformed, or inconsistent."""
    path: Path
```

### 使用示例

**场景 A：自己对接 LLM API**

```python
import anthropic
from fcop import Project, Priority
from fcop.rules import get_rules


def run_pm_turn(project: Project, admin_message: str) -> str:
    client = anthropic.Anthropic()

    tools = [
        {
            "name": "write_task",
            "description": "向指定角色派单。",
            "input_schema": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["P0", "P1", "P2", "P3"],
                    },
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["recipient", "priority", "subject", "body"],
            },
        },
    ]

    system = f"{get_rules()}\n\n你是 {project.config.leader}，角色是 PM。"

    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4096,
        system=system,
        tools=tools,
        messages=[{"role": "user", "content": admin_message}],
    )

    for block in resp.content:
        if block.type == "tool_use" and block.name == "write_task":
            task = project.write_task(
                sender="PM",
                recipient=block.input["recipient"],
                priority=Priority(block.input["priority"]),
                subject=block.input["subject"],
                body=block.input["body"],
            )
            return f"已派单：{task.filename}"

    return resp.content[0].text


project = Project("./myproject")
if not project.is_initialized():
    project.init(team="dev-team", lang="zh")

print(run_pm_turn(project, "给 DEV 派个 P1：登录模块偶发 500"))
```

**场景 B：CI 仓库协议校验**

```python
from fcop import Project, ProtocolViolation

project = Project(".")

failed = False
for task in project.list_tasks(status="all"):
    issues = project.inspect_task(task.filename)
    for issue in issues:
        if issue.severity == "error":
            print(f"::error file={task.path}::{issue.field}: {issue.message}")
            failed = True

raise SystemExit(1 if failed else 0)
```

**场景 C：用户界面展示**

```python
from fcop import Project

project = Project("./myproject")
status = project.status()

print(f"团队：{status.config.team}（{status.config.lang}）")
print(f"未归档任务：{status.tasks_open}")
print(f"最近活动：")
for entry in status.recent_activity[:5]:
    print(f"  [{entry.kind}] {entry.filename} · {entry.mtime:%Y-%m-%d %H:%M}")
```

### 版本号管理

- `src/fcop/_version.py` 是**单一版本源**：

  ```python
  __version__ = "0.6.0"
  ```

- `pyproject.toml` 用 hatch dynamic 读取：

  ```toml
  [project]
  dynamic = ["version"]

  [tool.hatch.version]
  path = "src/fcop/_version.py"
  ```

- `src/fcop/__init__.py` re-export：`from ._version import __version__`
- CI 增加一个 check，确认 `pyproject.toml` 能读到版本，且 `import fcop` 后
  `fcop.__version__` 与 `tag` 一致。**永远避免 0.4.1 卡在 `__init__.py`
  这种事**。

### semver 承诺

| 变化 | 允许的版本升级 |
|---|---|
| 新增公开符号（class/method/field/enum value）| patch（0.6.0 → 0.6.1）|
| 新增可选参数（有默认值）| patch |
| 修复 bug 但不改行为契约 | patch |
| 修复 bug 但改行为契约（原行为有 bug）| minor（0.6.x → 0.7.0）|
| 删除或改名公开符号 | minor |
| 改变函数签名（参数顺序、必填/可选变化）| minor |
| 改变 dataclass 字段（删除/改名/改类型）| minor |
| 改变异常类层级 | minor |
| 1.0 之后删除 / 改签名 | major |

0.x 期间 minor bump 允许破坏性变更。**1.0 之后只能 major bump 才能破坏**。

### 环境变量策略

**库代码**（`fcop.core.*` 和 `fcop.teams` / `fcop.rules`）：
- **不读任何环境变量**。所有路径、配置通过参数传入。
- 0.5.x 时代的 `FCOP_PROJECT_DIR`、`CODEFLOW_PROJECT_DIR` 只在 MCP 壳里处理。

**`fcop-mcp` 壳**（见 ADR-0002）：
- 继续支持 `FCOP_PROJECT_DIR`（自动发现项目根）
- 继续支持 `FCOP_RELAY_WS_URL` 等桥接相关
- `CODEFLOW_PROJECT_DIR` 在 0.6.0 开始抛硬错误（不再兼容），0.5.x 已弃用两轮

### 线程安全

- `Project` 实例本身不维护可变状态（除了内部缓存的 config 快照）
- 每次 `.status()` / `.list_tasks()` / `.read_task()` 都直接走文件系统，
  避免"缓存陈旧"问题
- 多进程并发写同一个项目时，**不做全局锁**。依赖文件系统 rename 原子性
  来保证文件要么存在要么不存在（Unix 和 Windows NTFS 均满足）
- 文件名序号 NNN 在并发写入时可能冲突——`write_task` 遇到冲突时
  **自动递增重试**（最多 10 次，然后 `RuntimeError`）。这个行为需要写进
  docstring，并在测试里覆盖

### 路径规范

- `Project.path` 是 `Path.resolve()` 过的绝对路径
- 所有返回的 `Path` 都是绝对路径
- 所有传入的路径参数同时接受 `str` 和 `os.PathLike[str]`
- 所有文件写入用 `utf-8` + `newline='\n'`（即使在 Windows 也强制 LF），
  和当前 `.cursor/rules/fcop-*.mdc` 的 "用 Python 读写中文文件" 规约一致

## Non-Goals

这份 ADR **不**涵盖：

- **异步 API**：当前全部 sync。`AsyncProject` 如果需要，走 ADR-0003+。
- **CLI 工具 `fcop` 命令**：本 ADR 只定义库。CLI 是基于库的上层应用，独立 ADR。
  （注：由于 PyPI 包名 `fcop` 对应库，CLI 入口如果要 `fcop` 命令，则放在
  `fcop` 包里是合理的；但 CLI 的具体子命令、交互设计是另一份 ADR。）
- **Plugin / Extension 机制**：暂不支持第三方扩展 Project 方法。1.0 之后再议。
- **Typed Python subset**：mypy strict / pyright 兼容性是品质目标，不是这份 ADR
  的硬性要求。
- **i18n**：错误消息暂用英文，不做多语言。`get_letter(lang)` 是特例，因为 letter
  本身就是双语文档。

## Alternatives Considered

### Alt-1：不开库，保持 MCP-only

- **方案**：继续把 `fcop` 定位成 MCP 服务器，用户想在 Python 里用就走 MCP client SDK。
- **否决原因**：用户明确要 `import fcop`；强行走 MCP client 相当于"本地 RPC 调自己
  的代码"，性能差、调试复杂、违背"文件协议"的初衷。

### Alt-2：一个包含所有入口的单包（库 + MCP 同住 `fcop`）

- **方案**：`fcop` 包里既有 `fcop.core` 也有 `fcop.server`（MCP），`fastmcp` 是可选
  依赖（extras）。
- **否决原因**：见 ADR-0002。简述：名字已经有了（`fcop-mcp` 占位成功），分两个
  包在发布节奏和依赖声明上更干净；库用户不应被迫装 `fastmcp`。

### Alt-3：Pydantic model 而非 dataclass

- **方案**：所有 model 用 Pydantic（v2）。好处：JSON 序列化、校验器、Schema 生成免费。
- **否决原因**：
  - Pydantic v2 是重型依赖（~几 MB），只为了几个数据类不值当
  - Python 标准库 `dataclass` + `typing` 已足够
  - 未来如果需要 JSON schema（比如给 CLI 或 API 用），可加一个可选 extras
    `fcop[pydantic]` 提供 Pydantic 镜像，不强制
- **决定**：先用 `@dataclass(frozen=True, slots=True)`。保留未来切 Pydantic 的口子。

### Alt-4：把业务逻辑放在 `fcop.core` 而公开面 `fcop.*` 直接 `from fcop.core import *`

- **方案**：`fcop/__init__.py` 透明转发 `fcop.core` 的一切。
- **否决原因**：公开 API 必须显式列出，才能稳定做 semver。让子模块 `fcop.core`
  保留"非公开、可随意改"的语义，是给未来重构留口子。

### Alt-5：类继承层级更深（`BaseProject` → `FileSystemProject` → `GitBackedProject`）

- **方案**：Project 分层，支持不同存储后端。
- **否决原因**：YAGNI。FCoP 的"文件驱动"是核心设计，非文件系统后端违背协议
  初衷。如果真有需要（比如 S3 后端），那是 2.0 级别的事。

## Consequences

### Positive

- **对接 LLM API 的项目终于能轻装上阵**：30 行代码能起一个 FCoP-compliant
  的多 agent 应用，完全不依赖 MCP。
- **CI / CLI / 仪表盘生态的口子打开了**：有了结构化数据，围绕 FCoP 做工具链
  变得容易。
- **协议规则和工具实现分层明确**：`fcop.rules` 能独立于库逻辑迭代（比如
  rules 版本号和包版本号可以解耦）。
- **测试性大幅提升**：业务逻辑不再缠在 MCP 装饰器里，pytest 可以直接调
  `Project` 方法断言，不用起 MCP 客户端。
- **并发安全**：没有模块级全局，多 `Project` 实例并存不互相影响，未来
  SaaS 场景可用。
- **逼着代码质量提升**：返回 dataclass 就不能再偷懒往字符串里拼信息，所有
  数据必须结构化描述；异常不能再返回"ERROR: xxx"字符串，必须抛具体类。

### Negative

- **开发成本**：~1800 行改动和新增代码（~400 新增 core、~500 dataclass 迁移、
  ~500 测试、~400 文档）。估 5-8 天专注工作。
- **一次性破坏 0.5.x 用户**（参见 ADR-0002 迁移计划）。不过"还没真用户"使这
  代价几乎为零。
- **双层 API 同时维护**：`fcop.core` 和 `fcop-mcp` 必须同步。工具新增 / 字段变化
  两边都要改。
- **`fcop.teams._data/` 和 `fcop.rules._data/` 会增加 wheel 体积**：已经 210KB
  的 wheel 大概会增长到 300-350KB。单位仍是"小"。

### Neutral

- 需要起一套完整的 pytest 测试（目前代码库还没有测试目录）
- 需要写迁移手册 `MIGRATION-0.6.md`（见 ADR-0002）
- `fcop-mcp` 的 MCP tool 薄壳改造要保证行为 1:1，工作量不可忽略但机械

## Timeline

假设 ADR-0001 accepted 之后开始：

| 日 | 产出 |
|---|---|
| D1 | 建新仓库 `joinwell52-AI/fcop`（空仓，README + LICENSE），搭 `fcop` + `fcop-mcp` 双包骨架，打通双 CI |
| D2 | 从 `server.py` 拆出 `fcop.core.filename` / `.frontmatter` / `.schema`，写对应测试 |
| D3 | `fcop.core.task` + `fcop.core.report` + `fcop.core.issue` + `Project.{write,list,read}_task / _report / _issue` |
| D4 | `fcop.core.config` + `fcop.core.deploy`（`init` / `init_solo` / `init_custom` / `deploy_role_templates`）+ 对应 `ProjectStatus` / `DeploymentReport` |
| D5 | `fcop.teams` + `fcop.rules` 无状态模块；包资源 discovery 用 `importlib.resources` |
| D6 | `fcop.errors` 完整异常体系；`ProtocolViolation` 在 Project 各方法中抛出点明确标注 Rule XX.Y |
| D7 | 重写 `fcop-mcp` 包：22 个 MCP tool 改为调 `fcop.core` 的薄壳 |
| D8 | 集成测试 + 文档 + `MIGRATION-0.6.md` 收尾，发布 `fcop 0.6.0` + `fcop-mcp 0.6.0` |

D8 之后，0.6.x patch 循环正常开展。

## Sign-off

- ADMIN: _待签字_
- PM: _待指派_

---

_Last edited: 2026-04-22. Status changes go in the table at the top; body content is frozen._
