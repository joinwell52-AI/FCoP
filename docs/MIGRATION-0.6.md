# 0.5.x → 0.6.0 迁移指南

> 面向 **现有 `fcop` 用户**（包括 0.5.3 / 0.5.4 的 MCP 使用者和 Python 库使用者）。  
> 如果你是从 0 开始用 FCoP，直接看 [README](../README.md)，不必读本文。

---

## TL;DR

| 你是怎么用的 | 需要做什么 |
|---|---|
| `uvx fcop` 或 `pip install fcop` 当 MCP 服务器 | **改安装 `fcop-mcp`**，MCP 配置里把命令从 `fcop` 换成 `fcop-mcp` |
| `from fcop.server import ...`（私有 API） | 迁到 `from fcop import Project`（[ADR-0001](../adr/ADR-0001-library-api.md)） |
| 只写过任务文件，从来没装 Python 包 | **啥也不用做**，老 task 文件继续可读 |
| 用 `docs/agents/tasks/` 里的 0.5.3 老 task 文件 | **啥也不用做**，Grandfather 条款保护（见 Section 4.1） |
| 有 `docs/agents/reports/TASK-*.md` 这种 0.5 老 report（非 `REPORT-` 开头） | 人依然能看，**但 agent `list_reports()` 不认**。想纳管就改名；不改也没事 |
| 有 0.5 的 issue 文件（用 `severity: P0-P3` 或缺 `kind/protocol`） | 同上：人能看、agent 不认，按需手改（见 Section 4.3） |

0.6 的大方向是**协议不变、包拆了、API 变稳了**，并且**从 0.6 起 agent 视角下的解析开始严格**。

---

## 0. 心智模型：人视角 ≠ Agent 视角

0.6 对「老文件 / 不合规文件」有两种**完全不同**的态度。读下面任何章节前请先把这张表刻进脑子：

| 视角 | 看得见什么 | 0.6 的立场 |
|---|---|---|
| **人** —— `ls` / `cat` / `git log` / IDE 文件树 | 100% 历史文件全在，一个都没丢 | 不管，也管不着 |
| **Agent** —— 走 `fcop` 库的 `list_*` / `read_*` 或 `fcop-mcp` 工具 | 只看得见**符合 0.6 规范**的文件 | **严格**。不合规 = 库视角下不存在 |

**为什么这么分**：

- 协议的消费者**不是人**，是 **agent**。Agent 协同需要**无歧义契约**——面对 `reports/TASK-xxx.md`，agent 没法自己判断"这是误命名还是刻意的"，容忍就是埋雷
- 人**不需要**库来保护。文件原样躺在磁盘上，`git log --follow` 随时考古，改不改、清不清是人的决定
- 0.5.x 那种「能读就读、读不了就 WARN」的宽容心态从 0.6 起**退役**。这是 0.6 进入"稳定版"的核心承诺，也是 ADR-0003 稳定性宪章的题中之义

所以下面章节里说的「0.6 看不见」「0.6 不认」，**全部指 agent/库视角**。你的文件没丢、也不会丢。

---

## 1. 包拆分：`fcop` → `fcop` + `fcop-mcp`

0.5.x 是一个包同时做两件事：

- Python 库（读写任务文件）
- MCP 服务器（暴露给 Cursor / Claude Desktop）

0.6 把这两个身份拆成两个包（[ADR-0002](../adr/ADR-0002-package-split-and-migration.md)）：

| 包名 | 做什么 | 谁会装 |
|---|---|---|
| `fcop` | 纯 Python 库，零 MCP 依赖，只依赖 `pyyaml` | 写脚本、写自定义 agent、做自动化 |
| `fcop-mcp` | MCP 服务器，依赖 `fcop` + `fastmcp` | 在 Cursor / Claude Desktop 里用 |

### 1.1 MCP 用户（最常见的场景）

**之前（0.5.x）**：
```bash
uvx fcop   # 或 pip install fcop && fcop
```

MCP 客户端配置类似：
```jsonc
{
  "mcpServers": {
    "fcop": { "command": "uvx", "args": ["fcop"] }
  }
}
```

**现在（0.6）**：
```bash
uvx fcop-mcp   # 或 pip install fcop-mcp && fcop-mcp
```

MCP 配置改成：
```jsonc
{
  "mcpServers": {
    "fcop": { "command": "uvx", "args": ["fcop-mcp"] }
  }
}
```

**服务器名字**可以保留 `"fcop"` 不变（这是 MCP 客户端内部的 key，你的所有工具调用代码不用改）。只是**命令名**从 `fcop` 变成了 `fcop-mcp`。

### 1.2 MCP Tool Surface 没变

`fcop-mcp 0.6.0` 的 24 个工具（`write_task` / `read_task` / `list_tasks` / …）和 10 个资源（`fcop://status` 等）**完全兼容 0.5.4**。ADR-0003 稳定性宪章第 2 条把这个接口面锁死了——名字、参数、必填性、返回格式任何变化都会被 CI 挡下。

如果你的 agent prompt 里写死了 `write_task(...)` 的调用，**不用改**。

### 1.3 Python 库用户

0.5.x 没有官方 Python API。如果你直接从 `fcop.server` 或 `fcop.fileio` 之类的模块里 import 东西，**那都是私有 API**，0.6 全部重写了。

0.6 提供一个官方公共 API：

```python
from fcop import Project

proj = Project("/path/to/my/workspace")
proj.init(team="dev-team")
task = proj.write_task(
    sender="PM",
    recipient="DEV",
    priority="P1",
    subject="Fix login bug",
    body="...",
)
print(task.task_id)         # TASK-20260423-001
print(task.frontmatter.priority)  # Priority.P1
```

完整 API 见 [ADR-0001](../adr/ADR-0001-library-api.md)。这个接口面从 0.6 起进入 ADR-0003 的「只进不出」模式——0.6.x 周期内不会发生签名破坏。

---

## 2. Frontmatter 格式差异

### 2.1 `protocol: agent_bridge` → `protocol: fcop`

0.5 早期（2026-04-20 前）：
```yaml
protocol: agent_bridge
version: 1.0
```

0.5.4 / 0.6：
```yaml
protocol: fcop
version: 1
```

**老文件怎么办**：Grandfather 条款覆盖——0.6 的 `read_task` 能正常读 `protocol: agent_bridge`，`inspect_task` 只会发 WARN 不会 FAIL。**不要改老文件**（Rule 5 文件不可变），旧的就让它旧下去，新写的文件自动用新格式。

### 2.2 `kind` 字段新增

0.6 要求（0.5 没这一条）：
```yaml
kind: task      # 或 report / issue
```

文件名前缀（`TASK-` / `REPORT-` / `ISSUE-`）本来就能告诉你 kind，但 `kind:` 字段让 frontmatter 自包含，不依赖文件名。

**老文件怎么办**：缺 `kind:` 的 0.5 老文件 `inspect_task` 会 WARN，不会 FAIL。新文件由 `Project.write_*` 自动写。

### 2.3 `created_at` 字段——从"写"变成"不写"（ADR-0004）

0.5.x 的 `write_task`：

```yaml
created_at: 2026-04-21 19:43:00
```

0.6：**不再写**。task/report 文件从此不带时间字段。

**为什么**：文件名里已经有 `YYYYMMDD`，真实精确时间由 `git log` 和文件系统 `mtime` 提供（这两个 agent 伪造不了），frontmatter 再记一份是冗余而且容易错。详见 [ADR-0004](../adr/ADR-0004-time-is-filesystem.md)。

**老文件怎么办**：

- 老的 `created_at` 字段：读取时保留在 `TaskFrontmatter.extra["created_at"]`，**不报错**
- `inspect_task`：看到 `created_at` 在 task/report 里 → WARN（「0.6 不鼓励，但容忍」），**不会 FAIL**

**例外：Issue 仍需 `created_at`**。Issue 是唯一允许合法编辑的文件类型（`open → closed`），`mtime` 语义被污染，所以必须在 frontmatter 显式记。0.6.0 起 `write_issue` 自动写入。

### 2.4 sender/recipient 角色码大小写

0.5 早期允许角色码混合大小写（`PM-01`、`ADMIN-01`）。0.6 的文件名语法要求**全大写** ASCII + 连字符（`PM`、`DEV-BACKEND`）。

**老文件怎么办**：文件名里如果已经是大写的，frontmatter 里写小写或带后缀无所谓——读取时大小写不敏感。新文件由 `Project.write_*` 自动大写。

---

## 3. 文件名规则

0.6 的合法文件名：

```
TASK-YYYYMMDD-NNN-SENDER-to-RECIPIENT.md
REPORT-YYYYMMDD-NNN-REPORTER-to-RECIPIENT.md
ISSUE-YYYYMMDD-NNN-REPORTER.md
```

其中：

- `YYYYMMDD` 是日期（如 `20260423`）
- `NNN` 是当天该类文件的 3 位序号（`001` – `999`）
- `SENDER` / `RECIPIENT` / `REPORTER` 是大写 ASCII + 连字符，可选带 `.SLOT`（如 `DEV.BACKEND`）

### 0.5 兼容的差异

如果你用 0.5.x 写了形如 `REPORT-20260421-003-FINAL-PM-to-ADMIN.md` 这种带**自定义中间段**的文件名（FINAL / DRAFT / V2 等），0.6 的严格 regex 不认。

**方案**：Grandfather 条款——老文件留着，新文件按新语法写。如果确实需要在文件名里表达「这是最终版」之类的含义，推荐改用：

- 文件级策略：REPORT 本来就是 append-only 的（Rule 5），直接写新的 report 文件表达最新状态
- 或：用 frontmatter 的 `status:` 字段（`done` / `blocked` / `in_progress`）

---

## 4. Grandfather 条款（只对 Task 宽容）

**一句话**：**Task 文件**的 frontmatter 容忍度比较高（protocol/kind/created_at 都能缺），**Report / Issue 的不合规文件在 agent 视角下直接消失**。

### 4.1 Task（宽容）

0.5 的老任务文件基本都能被 0.6 读到：

- ✅ `read_task` / `list_tasks` 正常返回
- ⚠️ `inspect_task` 对 `protocol: agent_bridge` / 缺 `kind` / 带 `created_at` 报 WARN，**不拒绝**
- ❌ 不自动改写（Rule 5 文件不可变）

前提：文件名匹配 `TASK-YYYYMMDD-NNN-SENDER-to-RECIPIENT.md` 这个严格 regex。带 `FINAL` / `V2` 之类自定义段的文件名 0.6 不认（见 Section 3）。

### 4.2 Report（严格）

0.6 只承认**正确命名的 report**：

| 情况 | 0.6 agent 视角 |
|---|---|
| 文件名 `REPORT-YYYYMMDD-NNN-X-to-Y.md` + 合规 frontmatter | ✅ 读得到 |
| 文件名 `TASK-*` 但放在 `reports/` 目录 | ❌ `list_reports()` 看不见 |
| 缺 `kind: report` 或 `protocol` | ❌ 解析失败 |

**真实场景**：0.5.x 的 MCP 某些路径会把 report 写成 `reports/TASK-*.md`。这些文件**人能看，agent 看不见**。接受它，或者手动把文件改名。

### 4.3 Issue（严格）

0.6 对 issue 要求 frontmatter 必须有 `protocol` / `version` / `kind: issue` / `reporter` / `severity ∈ {low, medium, high, critical}` / `summary`：

| 情况 | 0.6 agent 视角 |
|---|---|
| 上述字段齐全 | ✅ 读得到 |
| 缺 `protocol` / `version` / `kind` | ❌ 解析失败 |
| `severity: P0 / P1 / P2 / P3`（0.5 遗留值） | ❌ 解析失败（0.6 不做 P0-P3 → severity 的映射） |

从 0.6.0 起，`Project.write_issue` 自动写 `created_at` + `status: open`（[ADR-0004](../adr/ADR-0004-time-is-filesystem.md)）。老 issue 不加这两个字段的话，0.6.1 的 `close_issue` 等状态机操作会不认。

### 4.4 心态

- 人视角：老文件**全都在**，git 有全量历史
- Agent 视角：**只有合规的那部分存在**
- 想让 agent「看见」老 report/issue？**自己改文件**（重命名 / 补 frontmatter）——这属于人在自己仓库里的正常编辑，Rule 5 约束的是协议级别的不可变性，不是禁止你修你的磁盘
- 不想改也没关系：测试数据就让它躺着，新写的文件用 0.6 格式即可

### 4.5 Agent 运行时文件的归宿（新）

0.5.x 里有些 agent 把运行时状态（`.runtime-qa-*.json`、session/cache/checkpoint）写在 `docs/agents/` 根下或其他奇怪位置，污染了协议命名空间。

0.6 通过 [ADR-0005](../adr/ADR-0005-agent-output-layering.md) 一次性定规：

| Agent 产出物的类型 | 0.6 归宿 |
|---|---|
| 瞬时诊断返回值（如 `inspect_task` 结果）| 不落盘，MCP 返回 JSON |
| 巡检/审计快照（跨 agent 可读）| `docs/agents/log/AUDIT-YYYYMMDDTHHMMSS-*.json` |
| 需他人跟进的问题 | `docs/agents/issues/`（走 `write_issue`）|
| **Agent 私有运行时（`runtime-*.json` 之类）** | **`docs/agents/.runtime/{AGENT_CODE}/`** |
| 人本地一次性脚本输出 | `_ignore/`（入 `.gitignore`）|

**老用户迁移策略**：

- 老的 `.runtime-qa-*.json`：人视角永远保留（git 历史 + 磁盘）；agent 视角从 0.6 起不扫描，相当于不存在
- 想让 agent 新版本能用这些 state：手动挪到 `docs/agents/.runtime/QA/` 下（人的编辑不违反 Rule 5）
- 想直接抛弃：删掉即可，或者加到 `.gitignore` 里让它从仓库消失
- 0.6.0 库**不提供**自动迁移工具。`Project.agent_runtime_dir()` 等 helper 规划在 0.6.1 加（additive，符合 ADR-0003）

---

## 5. 典型迁移流程（3 步）

### 场景：我是 Cursor 用户，0.5.4 MCP + docs/agents/ 一堆老任务

**Step 1. 升级 MCP 命令**

```bash
pip uninstall fcop
pip install fcop-mcp
```

或者 `uvx` 用户直接改调用名（下次 uvx 自动拉 `fcop-mcp` 最新版）。

**Step 2. 改 MCP 客户端配置**

找到 Cursor / Claude Desktop 的 `mcp.json`，把：

```jsonc
"fcop": { "command": "uvx", "args": ["fcop"] }
```

改成：

```jsonc
"fcop": { "command": "uvx", "args": ["fcop-mcp"] }
```

**Step 3. 重启 MCP 客户端，啥也不用改别的**

工具名、参数、返回格式全跟 0.5.4 兼容。`docs/agents/tasks/` 下的老文件继续可读。新写的任务自动用 0.6 格式。

---

## 6. 常见问题

### Q: 我手工改过老任务文件的 frontmatter，0.6 是不是不认了？

只要 `protocol` / `version` / `sender` / `recipient` 四个字段在，0.6 基本都能读。实在不行 `inspect_task` 会告诉你哪里出问题。

### Q: 我能不能让 0.6 的 `write_task` 继续像 0.5.x 那样写 `created_at`？

不能（也不应该）——ADR-0004 是协议级决定，不是可配置项。如果你需要时间戳，靠 `git commit` 或 `os.stat().st_mtime`。

### Q: Issue 文件我 0.5 写的没有 `created_at` / `status` / `kind`，0.6 怎么处理？

**对人**：文件原样在磁盘，`cat` / `git log` 随时看。
**对 agent**：如果缺 `protocol` / `version` / `kind` 或用 `severity: P0-P3` 这种 0.5 遗留值，`list_issues()` / `read_issue()` 不会把它纳入结果——属于 Section 4.3 说的「严格」行为。

想让 agent 认它，自己手动补齐 frontmatter（人视角的编辑不违反 Rule 5）。不想补就留着——它在 agent 的世界里不存在，但在你的 git 历史里永远存在。

### Q: 0.6 的 `fcop` 包还能当 MCP 服务器跑吗？

**不能**。0.6 的 `fcop` 是纯 Python 库，没有 MCP 入口。想要 MCP 要装 `fcop-mcp`（它内部 `import fcop` 做所有实际工作）。

### Q: 我之前 `pip install fcop` 装的版本在哪？

两个包是同一个 PyPI 命名空间下的不同项目。`pip show fcop` 能看到你现在装的是哪个版本；`pip install fcop==0.5.4` 仍然可以装回老版本（有生之年都会存档在 PyPI 上），但新功能只会进 `fcop-mcp`。

### Q: `fcop 0.6.x` 什么时候会再加新 tool/方法？

ADR-0003 允许**加**（additive），禁止**改/删**（breaking）。新 tool 会在 minor 版本里陆续加，每次在 CHANGELOG 里单独标注 `(additive)`。你的老代码永远不会因为升级 0.6.N → 0.6.N+1 而坏。

---

## 参考链接

- [README](../README.md) — 新用户入门
- [ADR-0001](../adr/ADR-0001-library-api.md) — 库 API 契约
- [ADR-0002](../adr/ADR-0002-package-split-and-migration.md) — 包拆分决策
- [ADR-0003](../adr/ADR-0003-stability-charter.md) — 稳定性宪章
- [ADR-0004](../adr/ADR-0004-time-is-filesystem.md) — 时间交给文件系统
- [CHANGELOG](../CHANGELOG.md) — 详细变更列表
