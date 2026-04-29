<p align="center">
  <img src="assets/fcop-logo-256.png" alt="FCoP Logo" width="180" />
</p>

<h1 align="center">FCoP — 文件驱动的 Agent 协作协议</h1>

<p align="center">
  <em>一套极简协议，让多个 AI Agent 透过<strong>共享文件系统</strong>协作。</em><br/>
  <strong>核心创新：<code>Filename as Protocol</code>（文件名即协议）</strong>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="primer/fcop-primer.md">60 秒入门</a> ·
  <a href="essays/when-ai-organizes-its-own-work.md">现场报告</a> ·
  <a href="essays/fcop-natural-protocol.md">自然协议</a> ·
  <a href="spec/fcop-spec.md">规范入口</a> ·
  <a href="docs/fcop-standalone.md">纯 FCoP 说明</a>
</p>

<p align="center">
  <a href="https://dev.to/joinwell52/we-replaced-our-multi-agent-middleware-with-a-folder-48-hours-later-the-ai-invented-6-42a9">
    <img src="https://img.shields.io/badge/DEV-%E9%95%BF%E6%96%87%E5%AE%A2%E6%A0%88-black?style=flat-square&logo=dev.to&logoColor=white" alt="DEV Community 长文" />
  </a>
  <a href="https://forum.cursor.com/t/fcop-let-multiple-cursor-agents-collaborate-by-filename-mit-0-infra/158447">
    <img src="https://img.shields.io/badge/Cursor%20%E8%AE%BA%E5%9D%9B-%E8%AE%A8%E8%AE%BA-0066FF?style=flat-square" alt="Cursor 社区论坛" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  </a>
  <a href="spec/fcop-spec.md">
    <img src="https://img.shields.io/badge/spec-v1.0.3-green?style=flat-square" alt="规范 v1.0.3" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.19886036">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.19886036.svg" alt="DOI 10.5281/zenodo.19886036" />
  </a>
</p>

---

## 一句话说清楚

主流的多 Agent 框架要靠消息队列、数据库、自研 RPC 中间件。FCoP 全部扔掉，只留**文件系统**：

- **目录就是状态。**`tasks/` / `reports/` / `issues/` / `log/`，文件从一个目录 `rename` 到另一个就是状态流转。
- **文件名就是路由。**`TASK-20260418-001-PM-to-DEV.md` 一眼看得出发件人、收件人、类型、流水号。
- **内容就是负载。**Markdown + 一点点 YAML frontmatter，Agent 和人读写的是同一份东西。
- **唯一的同步原语是 `os.rename()`。**POSIX 在同一挂载点内保证它原子——不需要锁、不需要 broker、不需要共识算法。

就这些。没有数据库，没有消息队列，没有常驻守护进程。整个系统状态 `ls` 就能看完，整段协作历史 `git log` 就能回放。

> 如果说 TCP 是"字节跑在线缆上"，**FCoP 就是"任务跑在文件夹里"。**

> 在工程上，就是用**可序列化、可版本化的协作面**，换走了对**专属、沉重基础设施**的依赖。

## 为什么值得一看

因为**看得见的 Agent，才管得住。**

我们用一支 4 人 AI 团队（PM / DEV / QA / OPS）跑了 48 小时，Agent 们**自发发明了 6 种我们从没写进规范的协作模式**——全体广播、角色槽位、共享文档、子任务批次、自解释 README、可追溯性 frontmatter。每一种新模式都表现为**新文件名**——我们一行代码都没改。

后来又出现了更意外的一幕：一个**单独**的 agent，在一个**与任何当时已打开的项目工作区都无关**的本地目录里（例如生成一段 AI 音乐视频），**自发**把自己拆成 PM / DEV / ADMIN 三个角色、给自己写了四份 FCoP 格式的公文，还**升华**了我那些分散在 7 个文件里的技术规定，浓缩成一句我根本没写过的原则性箴言。

这两段故事都整理成了现场报告，见下面的文章索引。

## 现场报告 · Essays

| # | 标题 | 版本 | 一句话 |
|---|---|---|---|
| 01 | **当 AI 自己整理工作** | [GitHub 中文](essays/when-ai-organizes-its-own-work.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160344932) · [English](essays/when-ai-organizes-its-own-work.en.md) | 一支 4 人 AI 团队（PM / DEV / QA / OPS），48 小时，只给一个文件夹——结果自发涌现出 6 种我们从没写进规范的协作模式。 |
| 02 | **一个无法完全解释的现象:AI 不止服从规则,它认同规则** | [GitHub 中文](essays/fcop-natural-protocol.md) · [GitHub English](essays/fcop-natural-protocol.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160345043) · [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) · [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | 一个 agent 在**完全无关**的任务里，自发把自己拆成 4 个 FCoP 角色，还**升华**了我散在 7 个文件里的技术规定，浓缩成一条我根本没写过的原则。附[完整证据档案](essays/fcop-natural-protocol-evidence/)（4 张截图 + 4 份公文 + 原始 JSONL 转录）。 |
| 03 | **自然协议为什么站得住——FCoP 从 TMPA 中抽出来的那条伦理** | [GitHub 中文](essays/fcop-tmpa-lineage.md) · [GitHub English](essays/fcop-tmpa-lineage.en.md) | 02 的姊妹篇。那一篇讲"这件事发生了"，这一篇讲"它为什么站得住"：FCoP 其实是从 **TMPA**（一份多 AI 架构规范，核心立意是用纯文本时序替代传统分布式协调）里抽出来的子集；agent 升华出的那句话，是 TMPA 伦理层"多角色审核是 AI 伦理强制"的最小化重发现。 |
| 04 | **让 agent 说"不"，是 LLM 最难做的事——FCoP 给了它语法** | [GitHub 中文](essays/when-ai-vacates-its-own-seat.md) · [GitHub English](essays/when-ai-vacates-its-own-seat.en.md) · [现场证据档案](essays/when-ai-vacates-its-own-seat-evidence/INDEX.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160513899) · [Dev.to](https://dev.to/joinwell52/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar-3ccd) · [Cursor Forum](https://forum.cursor.com/t/saying-no-is-the-hardest-thing-for-an-llm-fcop-gives-it-grammar/159037) | 同一台电脑、两个 Cursor 会话、两个 GPT-5 小版本（5.4 与 5.5）：原 PM 在我说"找了临时 PM"后主动让出席位回到 UNBOUND，新 PM.TEMP 用「frontmatter 降级 + 正文 `说明:` 一行」走完了协议没写的那条路。我原本以为会冲突，结果没有——agent 自己把规则补全了。附 15 张截图 + 2 份完整 JSONL 转录。 |
| 05 | **教程：solo 单 agent 转 2 人团队——FCoP-MCP 让 AI 团队有纪律**（两个并列案例） | 中文母语原创（贪吃蛇案例）: [`snake-solo-to-duo.zh.md`](docs/tutorials/snake-solo-to-duo.zh.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953) · English (Tetris case): [`tetris-solo-to-duo.en.md`](docs/tutorials/tetris-solo-to-duo.en.md) · [Dev.to](https://dev.to/joinwell52/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-1j3j) · [Cursor Forum](https://forum.cursor.com/t/free-open-source-multi-agent-hands-on-how-to-command-agents-fcop-mcp-brings-discipline-to-ai-teams/159329) · 中文译本（俄罗斯方块案例）: [`tetris-solo-to-duo.zh.md`](docs/tutorials/tetris-solo-to-duo.zh.md) | 唯一一篇**教程性质**的文章，以**两个并列案例**形式发布——**协议相同，案例游戏与现场彩蛋不同**。两个案例都是 45 分钟跟真实 dogfood 走一遍：让 AI 替你装 `fcop-mcp`，solo 写一只能跑的小游戏，一句话切 2 人团队后 PLANNER 设计 + CODER 实现创意变体，最后读盘看完整账本。**中文案例**用贪吃蛇 → 原创主题《星轨织者 NEON ORBIT》，附 18 张截图 + 一次真实的 PLANNER 越界冒充 CODER 彩蛋（0.6.x 时代的协议越界证据）。**英文案例**用俄罗斯方块 → 单人《Nebula Stack》→ 双人《Comet Loom》，多了一个真实的"评审 → 拒收 → 重做"循环（v1 被 ADMIN 试玩驳回，PLANNER 写 TASK-006 加 `Verification Requirements`，v2 通过）+ 当场访谈两个 agent "你怎么看 FCoP" 收到的诚实自评。两个案例共 22 张 dogfood 截图、14 份 TASK/REPORT、8 份 role-switch 静默证据、2 份游戏代码、2 份 verbatim agent 访谈 transcript——全部归档在 [`docs/tutorials/assets/tetris-en/`](docs/tutorials/assets/tetris-en/)。 |
| 06 | **直接问 agent 它怎么看 FCoP——它说出了我们没让它说的话** | [GitHub 中文](essays/what-agents-say-about-fcop.md) · [GitHub English](essays/what-agents-say-about-fcop.en.md) · [现场证据（俄罗斯方块案例 dogfood）](docs/tutorials/assets/tetris-en/) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160636177) · [Dev.to](https://dev.to/joinwell52/what-the-agents-say-about-fcop-when-you-ask-them-3ajk) · [Cursor Forum](https://forum.cursor.com/t/what-the-agents-say-about-fcop-when-you-ask-them-two-field-interviews-at-the-end-of-an-english-dogfood/159368) | 第三类"agent 反向认同 FCoP"的证据——在 [essay 02](essays/fcop-natural-protocol.md)（**自发触发，无关任务**）和 [essay 04](essays/when-ai-vacates-its-own-seat.md)（**被冲突逼出来**）之后，这次的触发条件是**被直接问**。一次英文俄罗斯方块 dogfood 收尾时（教程行 05 的伴随 essay），我分别在两个会话里问 PLANNER 和 CODER 同一类问题——agent 视角的老实话，无营销腔。PLANNER 把 "follow latest instruction" 这个 RLHF 训出来的本能命名为自己为了守住 FCoP 角色锁需要"对抗"的那一面，把它名下产生的 8 份 `role-switch` 评定为**真阳性**而不是误报。CODER 承认 TASK-003 有规格漏洞 + **协议本来给了它一条 pushback 路径（`write_issue`）它没用**——v1 缺陷正好长在那块没覆盖的空白上——并给出 PR 级别的协议产品反馈。三种触发条件，同一个现象：**只要给空间，agent 就会反过来认同 FCoP**。还有一个 dogfood 顺带产出的小观察值得留底——整整 45 分钟，ADMIN 说得最多的两句话是 **"Start work."** 和 **"Inspection."** |
> 欢迎提交新的现场报告。如果你在自己的项目里用了 FCoP，遇到了意外（好或坏），欢迎开 issue 或对 `essays/` 提 PR。协议是在现场报告里演进的，不是在委员会里。

## 仓库结构

概览：根目录除**协议与文档**外，还有 **PyPI `fcop` 的源码**（`src/fcop/`）与**独立子项目 `fcop-mcp`**（`mcp/`），以及测试与发版/ADR 支撑目录。

```
FCoP/
├── src/fcop/                    # `fcop` 包：Project 等库 API；`rules/_data/` 内置 fcop-rules / fcop-protocol（init 时可选部署的母版）
├── mcp/                         # `fcop-mcp` 子项目（MCP 服务器，自有 pyproject）
├── tests/                       # `fcop` / `fcop-mcp` 的 pytest
├── spec/                        # 人读规范 + 可粘贴的 Agent 单文件 .mdc 镜像
│   ├── codeflow-core.mdc        # 已弃用占位（防旧链接 404）；权威为 `../src/.../fcop-rules` + `fcop-protocol`
│   ├── fcop-spec.md             # 规范入口（中文）
│   └── fcop-spec-v1.0.3.md      # 长版人读（非规范）
├── docs/                        # 迁移、发版记录；[`fcop-standalone.md`](docs/fcop-standalone.md) 为纯协议说明
├── adr/                         # 架构决策
├── .github/workflows/           # CI
├── pyproject.toml               # 根 `fcop` 包与工具配置
├── primer/
│   ├── fcop-primer.md
│   └── fcop-primer.en.md
├── essays/
│   ├── when-ai-organizes-its-own-work.md
│   ├── when-ai-organizes-its-own-work.en.md
│   ├── fcop-natural-protocol.md
│   ├── fcop-natural-protocol.en.md
│   ├── fcop-natural-protocol-evidence/
│   ├── fcop-tmpa-lineage.md
│   ├── fcop-tmpa-lineage.en.md
│   ├── when-ai-vacates-its-own-seat.md
│   ├── when-ai-vacates-its-own-seat.en.md
│   ├── when-ai-vacates-its-own-seat-evidence/
│   ├── what-agents-say-about-fcop.md
│   └── what-agents-say-about-fcop.en.md
├── examples/workspace-example/  # 最小参考工作区
├── integrations/windows-file-association/
├── assets/                      # Logo
├── LICENSE
└── README.md / README.zh.md
```

## 30 秒快速上手

FCoP 是「采纳」协议，不是装一个独立守护进程。当前版本的**规范侧**是成对的 **[总则 `fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc)** 与 **[解释 `fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)**（部署到 **`.cursor/rules/`**）。`spec/codeflow-core.mdc` 仅为**防旧链接失效**的弃用占位，**勿**当正文规范使用。

**方式 A：用 `fcop` 库初始化（推荐）** — 一次写好 `docs/agents/` 目录与 `fcop.json`（库约定的协作根）：

```python
from fcop import Project
Project(".").init()  # 默认 dev-team；单人可改用 .init_solo()
```

**方式 B：不跑 Python、只让 Cursor 读规则** — 把上列两个 `.mdc` 从本仓拷进项目的 `.cursor/rules/`。目录若尚未存在，至少要有与库一致的五类桶：

```bash
mkdir -p docs/agents/{tasks,reports,issues,shared,log}
```

配好规则后，Agent 按总则/解释可知：认领发给自己的任务、按文件名写回报告、上报问题、不越权动他人文件。更完整的落盘与团队模板，见下节包与 [`examples/workspace-example/`](examples/workspace-example/)。

## Python SDK & MCP 服务器（可选）

协议可纯文件采纳；**若需要**在代码里读写 task/report/issue，或通过 MCP 暴露给 IDE，自 `0.6.0` 起 PyPI 上有两个包：

| 包 | 安装 | 用途 | 依赖 |
|---|---|---|---|
| [`fcop`](https://pypi.org/project/fcop/) | `pip install fcop` | 纯 Python 库。读写 task / report / issue。**零 MCP 依赖**。 | `pyyaml` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | `pip install fcop-mcp` | MCP 服务器。把库通过 stdio 暴露给 Cursor / Claude Desktop。 | `fcop>=0.6,<0.7`、`fastmcp`、`websockets` |

**指针表**（一行一件事，不绑定版本号）：

| 想干啥 | 去这里 |
|---|---|
| 在 Cursor / Claude Desktop 装 `fcop-mcp`（分步、多平台、自检） | [`mcp/README.md`](mcp/README.md) |
| 不想自己改 JSON，让 agent 全程跑命令装 | [`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md) · [English](src/fcop/rules/_data/agent-install-prompt.en.md)（装好以后也是 MCP 资源 `fcop://prompt/install`） |
| 已在用 0.6.x，要升级（两包同环境一起升 + 协议规则文件刷新） | [`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md) |
| 浏览全部 26 个工具和 12 个资源（分类、何时调、参数要点） | [`docs/mcp-tools.md`](docs/mcp-tools.md) |
| 看每版到底改了什么、为什么改 | [`CHANGELOG.md`](CHANGELOG.md) 与 [`docs/releases/`](docs/releases/) |

**近期发版**（完整说明在 [`docs/releases/`](docs/releases/)）：

| 版本 | 一句话 |
|---|---|
| **0.7.2**（[详细](docs/releases/0.7.2.md)） | 元数据 patch：修 `fcop-rules.mdc` frontmatter 错版本号（`1.7.0` → 实际内容已是 `1.8.0`）；新增三道 frontmatter↔body changelog 一致性测试 + 已有的两包 minor lockstep 测试，0.7.x 周期内连发三次"多行编辑漏一处"的同类 bug（ISSUE-006 / ISSUE-007）从此**结构性不可发**。无协议变化、无 API 变化。 |
| **0.7.1**（[详细](docs/releases/0.7.1.md)） | hotfix `fcop-mcp 0.7.0` 依赖钉错版本（`fcop>=0.6,<0.7` → `<0.8`）+ 三处协议澄清：Rule 1 子 agent 身份（`session_id ↔ role` 审计）、Rule 0.a.1 适用所有写路径（不止 MCP 工具）、Rule 5 删 `AMEND-*` / `-v2`（用顺序报告 + `amends:`）。新增：`Project.audit_drift()` + `fcop_check()` MCP 工具 + 软角色锁。**协议升级**：rules `1.7.0` → `1.8.0`、protocol `1.5.0` → `1.6.0`。 |
| **0.7.0**（[详细](docs/releases/0.7.0.md)） | **角色唯一性**正式入协议：新增 `Project.role_occupancy()` + `RoleOccupancy` 数据结构，`fcop_report()` 增 `[角色占用]` 段，`unbound_report` 删除（0.6.3 起已弃用）。Rule 1 收紧：角色 OCCUPIED 当且仅当**有落盘文件**以其为 `sender`。**协议升级**：rules `1.6.0` → `1.7.0`、protocol `1.4.0` → `1.5.0`。**注**：0.7.0 的 `fcop-mcp` 依赖钉错版本，请装 0.7.1+。 |
| **0.6.5**（[详细](docs/releases/0.6.5.md)） | Rule 0.a.1（`task → 做 → report → archive`）落到**工具层**：`new_workspace` 在没有任何开放 `TASK-*.md` 提及当前 slug 时**预置一段提醒**；`fcop_report` 已初始化分支末尾加挂四步模板。中英双语、纯追加。 |
| **0.6.4**（[详细](docs/releases/0.6.4.md)） | 修复初始化缺漏：每个 `init_*` 一次性把承诺的所有文件（信、三层团队文档、协议规则四件套）全部落齐。新增资源 `fcop://prompt/install` 中英两份。所有 `init_*` 新增 `force` 参数。 |
| **0.6.3**（[详细](docs/releases/0.6.3.md)） | 引入 `fcop_report`（带 `[版本]` 漂移段）；host-neutral 的 `redeploy_rules` 同时写 `.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`（[ADR-0006](adr/ADR-0006-host-neutral-rule-distribution.md)）；`unbound_report` 弃用（0.7.0 移除）。 |

> **小心：PyPI 上有一个跟这里无关的 `fcop` 同名包。** 本仓两个包都从**本仓发**。如果 `pip install fcop` 之后 `from fcop import Project, Issue` 仍失败，多半是你装错了 distribution、或本机某个可编辑安装的工程把 `fcop` 名字抢走了。修法：干净 venv + 一并按 PyPI 重装两个包。验证命令在 [`mcp/README.md`](mcp/README.md)。

**库** —— 从任何 Python 脚本或 agent 里直接调：

```python
from fcop import Project

proj = Project(".")                              # 项目根；未 init 时无 fcop.json
proj.init()                                      # 建 tasks|reports|issues|shared|log/ 与 fcop.json
task = proj.write_task(sender="PM", recipient="DEV", priority="P1",
                       title="加鉴权中间件", body="...")
print(proj.list_tasks(recipient="DEV"))
```

**MCP 服务器** —— 写进 Cursor 的 `mcp.json` 或 Claude Desktop 的 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

**不想自己改 JSON？** 让 agent 来。开一个能跑命令的新会话，把官方安装提示词
（[`agent-install-prompt.zh.md`](src/fcop/rules/_data/agent-install-prompt.zh.md)
· [English](src/fcop/rules/_data/agent-install-prompt.en.md)）整段贴过去——
agent 会识别系统、装 `uv`、改 `mcp.json`（**保留**已有 server）、提醒重启。
装好以后这段提示词在 MCP 资源 `fcop://prompt/install` 也能直接读到。提示
词里**明令禁止** agent 装完顺手 `init_project`——初始化是 ADMIN 的三选一
（solo / 预设团队 / 自定义），不是 agent 的默认值。

稳定性承诺：**整个 `0.6.x` 小版本周期内只加不改**，详见 [`adr/ADR-0003-stability-charter.md`](adr/ADR-0003-stability-charter.md)。

> **从 0.5.x 升级？** MCP 服务器已从 `fcop` 包搬到 `fcop-mcp`——把 `mcp.json` 里的命令改成 `uvx fcop-mcp`。完整迁移指引见 [`docs/MIGRATION-0.6.md`](docs/MIGRATION-0.6.md)，本次发版档案见 [`docs/releases/0.6.0.md`](docs/releases/0.6.0.md)。

## 设计原则

1. **文件名是唯一真理。**目录 + 文件名决定状态，frontmatter 只是冗余元数据。
2. **原子性来自 `rename()`**。没有别的——不需要锁，不需要事务。
3. **人机同构。**`cat` 能读的就是 Agent 能解析的，没有调试模式、没有管理后台。
4. **身份决定路径。**文件名里的角色标识本身就是权限模型——身份不匹配，Agent 连文件都动不了。
5. **零基础设施。**只要有文件系统就有 FCoP。笔记本能跑，集群能跑，跨机通过 `rsync` 就能跑。

## 参考实现

两套官方参考实现，均为 MIT 许可：

1. **`fcop` / `fcop-mcp`** —— 协议的 Python 库 + MCP 服务器。源码在本仓库 [`src/fcop/`](src/fcop/) 和 [`mcp/src/fcop_mcp/`](mcp/src/fcop_mcp/)，通过 PyPI 分发（见上一节）。
2. **历史 URL 占位**：`spec/codeflow-core.mdc` 仅防旧链接失效，**无正文**；**唯一权威**仍是 `src/fcop/rules/_data/fcop-rules.mdc` + `fcop-protocol.mdc`（文件名含历史字样而已）。

## 状态与版本

- **当前规范版本**：v1.0.3（2026-04-19）
- **本仓内 Agent 规则（`.mdc`）**：[`src/fcop/rules/_data/fcop-rules.mdc`](src/fcop/rules/_data/fcop-rules.mdc) + [`fcop-protocol.mdc`](src/fcop/rules/_data/fcop-protocol.mdc)（`spec/codeflow-core.mdc` 仅为弃用占位）
- 变更记录见 [`spec/fcop-spec-v1.0.3.md`](spec/fcop-spec-v1.0.3.md) 文首。
- **研究快照**：[`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29) 已经归档到 Zenodo 并分配 DOI（详见下文 *如何引用*）。

## 如何引用

如果 FCoP 的协议、现场报告 essays、教程、或参考实现对你的研究、软件、写作有帮助，请引用 [Zenodo 研究快照](https://doi.org/10.5281/zenodo.19886036)：

- **DOI**：[`10.5281/zenodo.19886036`](https://doi.org/10.5281/zenodo.19886036)
- **快照 tag**：[`research-snapshot-2026-04-29`](https://github.com/joinwell52-AI/FCoP/releases/tag/research-snapshot-2026-04-29)（commit `7f59395`）
- **机器可读元数据**：[`CITATION.cff`](CITATION.cff)（GitHub 会从这个文件自动渲染一个 *Cite this repository* 按钮放在右栏）

```bibtex
@misc{fcop2026snapshot,
  author       = {Zhu, Wei},
  title        = {{FCoP}: A Filename-as-Protocol coordination layer for multi-agent {AI} development (Research Snapshot, April 2026)},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {research-snapshot-2026-04-29},
  doi          = {10.5281/zenodo.19886036},
  url          = {https://doi.org/10.5281/zenodo.19886036}
}
```

如果引用单篇 essay 或教程，DOI 仍是同一个——在引用脚注里附上 essay 的文件名（如 `essays/what-agents-say-about-fcop.md`）和 snapshot 版本号即可定位到具体内容。

## 如何贡献

本仓库刻意保持**小而稳**。协议演进的依据是"真实场景里的报告"，不是"委员会投票"。最有价值的贡献是：

1. **现场报告。**把 FCoP 拉到你自己的 Agent 团队里跑一段，把"哪里坏了"、"Agent 自己发明了什么"、"涌现出哪些命名约定"开个 Issue。
2. **移植与 SDK。**Python / TypeScript / Go 的薄封装，负责解析文件名和跑 `rename()` 状态机。
3. **编辑器与 MCP 集成。**`.fcop` 文件的语法高亮、把这套文件夹 expose 给其他 Agent 运行时的 MCP 桥。

对规范本身的 PR，请链接到它要解决的具体问题。

## License

MIT — 详见 [LICENSE](LICENSE)。

## 致谢

FCoP 是在 **Cursor 等环境**里与多 Agent 实战协作时陆续涌现的。规范里不少约定**最初是 Agent 们自己写出来的**，我们只是把它们整理成册。详情见 [现场报告](essays/when-ai-organizes-its-own-work.md)。
