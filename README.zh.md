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
│   └── when-ai-vacates-its-own-seat-evidence/
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

**给最终用户的安装（分步、多平台、自检）**：见 **[`mcp/README.md`](mcp/README.md)**（英文；步骤与 `mcp.json` 模板可直接照抄）。**已在使用 0.6.x 时的升级**（`pip` 同环境升两包、钉版本、重启与自检；**0.6.3+** 还多了协议规则文件的 host-neutral 升级流）：**[`docs/upgrade-fcop-mcp.md`](docs/upgrade-fcop-mcp.md)**。**MCP 工具与资源清单（26 个工具、10 个资源）**：**[`docs/mcp-tools.md`](docs/mcp-tools.md)** —— 每个工具是干嘛的、什么时候调、参数要点一表看清。**0.6.3 亮点**（[`docs/releases/0.6.3.md`](docs/releases/0.6.3.md)）：新增 `fcop_report`（每会话首调、报告头自带 `[版本]` 漂移检测段）、新增 `redeploy_rules`（ADMIN 专用，把协议规则 host-neutral 写到 `.cursor/rules/` + `AGENTS.md` + `CLAUDE.md`，背景见 [ADR-0006](adr/ADR-0006-host-neutral-rule-distribution.md)）；`unbound_report` 改名为 `fcop_report`，老名字保留为 deprecation 别名（0.7.0 移除）。官方包须来自**本仓库对应的 PyPI 发行**；若 `pip install fcop` 后 `from fcop import Project, Issue` 仍失败，多半是装到了错误发行物或被本机其他工程的可编辑包抢名 —— 说明文中有「干净 venv + 验证命令」的修法。

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
