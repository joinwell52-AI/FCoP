# FCoP 是什么（独立说明）

**FCoP**（**F**ile-based **Co**ordination **P**rotocol，文件驱动协调协议）是一套**开放、与具体产品解耦**的约定：让多个 AI Agent（以及 human）**只通过共享工作区里的文件**完成协作，不依赖消息队列、业务数据库、专用中间件或常驻 broker。

本文只描述 **FCoP 协议本身**（定位、权威文档、工作区形态、如何采纳）。不讲具体商业产品、不讲外部未公开规范的血缘，也不展开田野故事；那些见仓库内 `essays/` 等文。

---

## 核心思想（四件事）

1. **目录即状态** — 任务、报告、问题、归档分桶存放；在桶之间移动文件即状态转移。  
2. **文件名即路由** — 从 `TASK-…-PM-to-DEV.md` 等文件名即可读出发件人、收件人、类型与序号。  
3. **正文即负载** — Markdown + 受约束的 YAML frontmatter，人机读同一套文件。  
4. **同步靠文件系统** — 同一挂载点内依赖 `rename` 等原子操作即可协调并发；无需分布式锁/队列共识。

人话版：**可序列化、可 diff、可回放的协作面全部落在盘上的文件上**。

---

## 规范写在哪（权威来源）

| 作用 | 路径 | 说明 |
|------|------|------|
| **总则（规则）** | [`src/fcop/rules/_data/fcop-rules.mdc`](../src/fcop/rules/_data/fcop-rules.mdc) | Agent 必须遵守的条文级规则 |
| **解释（协议）** | [`src/fcop/rules/_data/fcop-protocol.mdc`](../src/fcop/rules/_data/fcop-protocol.mdc) | 总则的落地说明：命名、frontmatter、目录、巡检等 |
| **人读长规范（非单文件强制）** | [`spec/fcop-spec-v1.0.3.md`](../spec/fcop-spec-v1.0.3.md) | 中文长文，与版本号绑定 |
| **规范稳定入口** | [`spec/fcop-spec.md`](../spec/fcop-spec.md) | 指向上列正式版的导航页 |

在 Cursor 等环境中，**请将** `fcop-rules.mdc` 与 `fcop-protocol.mdc` **成对**放入项目 `.cursor/rules/`。二者冲突时，**以 `fcop-rules.mdc` 为准**（`fcop-protocol` 自述）。

> `spec/codeflow-core.mdc` 在仓库中仅保留**历史 URL 占位**；**不要**把它当作 0.6+ 的权威正文。

---

## 工作区长什么样

- **根**：你选定的项目根目录。  
- **协调根**：`docs/agents/`，下含 `tasks/`、`reports/`、`issues/`、`shared/`、`log/` 等（由库 `init` 或按规范自建）。  
- **身份与角色**：`docs/agents/fcop.json` 为**唯一权威**（`roles`、`leader` 等），Agent 不凭聊天自称角色绕过该文件。  

具体子目录、归档规则、多团队前缀等以 **`fcop-rules` + `fcop-protocol`** 为准。

---

## 怎么采纳（三选一或组合）

1. **Python 库** — `pip install fcop`，在项目根 `Project(".").init()` 等，生成目录与 `fcop.json`（可配合团队模板等 API）。  
2. **只配规则** — 无 Python 时，从本仓复制 `fcop-rules.mdc` + `fcop-protocol.mdc` 到 `.cursor/rules/`，并自建 `docs/agents/…` 与 `fcop.json`（可手写最小合法 JSON，详见规范）。  
3. **MCP** — `fcop-mcp` 在 IDE 里暴露与初始化、读写任务等工具；**MCP 可选**，纯库不依赖 MCP。

---

## 配套发行物（可选）

- **`fcop`**：协议 Python 实现（读写作业、archive、suggestion 等）。  
- **`fcop-mcp`**：把 `fcop` 通过 MCP 接到 Cursor / Claude Desktop 等。  

两包在 PyPI 上拆分自 0.6+；**协议本身不绑定任何一门语言**。

---

## 许可

仓库根目录 [LICENSE](../LICENSE)（MIT）。

---

## 延伸阅读（协议之外的叙事）

- [60 秒入门](../primer/fcop-primer.md)  
- [规范入口](../spec/fcop-spec.md)  
- [现场报告与随笔](../essays/)（演进而非委员会投票）

若你只需要**可转载的“纯协议”单页本文**，请链接本文件；若需**版本与条款**，请以 `fcop-rules` / `fcop-protocol` 与 `fcop-spec-v*` 为准。

---

- [English / 英文版](fcop-standalone.en.md)
