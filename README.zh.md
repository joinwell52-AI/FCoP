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
  <a href="spec/fcop-spec.md">规范入口</a>
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

## 为什么值得一看

因为**看得见的 Agent，才管得住。**

我们用一支 4 人 AI 团队（PM / DEV / QA / OPS）跑了 48 小时，Agent 们**自发发明了 6 种我们从没写进规范的协作模式**——全体广播、角色槽位、共享文档、子任务批次、自解释 README、可追溯性 frontmatter。每一种新模式都表现为**新文件名**——我们一行代码都没改。

后来又出现了更意外的一幕：一个**单独**的 agent，在一个和 CodeFlow **毫无关系**的目录里（生成一段 AI 音乐视频），**自发**把自己拆成 PM / DEV / ADMIN 三个角色、给自己写了四份 FCoP 格式的公文，还**升华**了我那些分散在 7 个文件里的技术规定，浓缩成一句我根本没写过的原则性箴言。

这两段故事都整理成了现场报告，见下面的文章索引。

## 现场报告 · Essays

| # | 标题 | 版本 | 一句话 |
|---|---|---|---|
| 01 | **当 AI 自己整理工作** | [GitHub 中文](essays/when-ai-organizes-its-own-work.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160344932) · [English](essays/when-ai-organizes-its-own-work.en.md) | 一支 4 人 AI 团队（PM / DEV / QA / OPS），48 小时，只给一个文件夹——结果自发涌现出 6 种我们从没写进规范的协作模式。 |
| 02 | **一个无法完全解释的现象:AI 不止服从规则,它认同规则** | [GitHub 中文](essays/fcop-natural-protocol.md) · [GitHub English](essays/fcop-natural-protocol.en.md) · [CSDN 中文](https://blog.csdn.net/m0_51507544/article/details/160345043) · [Dev.to](https://dev.to/joinwell52/an-unexplainable-thing-i-saw-the-agent-didnt-just-comply-with-rules-it-endorsed-them-5ecd) · [Cursor Forum](https://forum.cursor.com/t/i-asked-cursor-to-make-a-video-it-wrote-itself-4-protocol-memos-field-report-on-rule-internalization/158524) | 一个 agent 在**完全无关**的任务里，自发把自己拆成 4 个 FCoP 角色，还**升华**了我散在 7 个文件里的技术规定，浓缩成一条我根本没写过的原则。附[完整证据档案](essays/fcop-natural-protocol-evidence/)（4 张截图 + 4 份公文 + 原始 JSONL 转录）。 |
| 03 | **自然协议为什么站得住——FCoP 从 TMPA 中抽出来的那条伦理** | [GitHub 中文](essays/fcop-tmpa-lineage.md) · [GitHub English](essays/fcop-tmpa-lineage.en.md) | 02 的姊妹篇。那一篇讲"这件事发生了"，这一篇讲"它为什么站得住"：FCoP 其实是从 **TMPA**（一份多 AI 架构规范，核心立意是用纯文本时序替代传统分布式协调）里抽出来的子集；agent 升华出的那句话，是 TMPA 伦理层"多角色审核是 AI 伦理强制"的最小化重发现。 |

> 欢迎提交新的现场报告。如果你在自己的项目里用了 FCoP，遇到了意外（好或坏），欢迎开 issue 或对 `essays/` 提 PR。协议是在现场报告里演进的，不是在委员会里。

## 仓库结构

```
FCoP/
├── spec/
│   ├── codeflow-core.mdc          # ★ 规范性协议本体（交给 Agent 的 Cursor 规则文件）
│   └── fcop-spec-v1.0.3.md        # 中文长版人读规范（非规范性）
├── primer/
│   ├── fcop-primer.md             # 中文 60 秒入门
│   └── fcop-primer.en.md          # 英文 60 秒入门
├── essays/
│   ├── when-ai-organizes-its-own-work.md       # 中文长文（首篇）
│   ├── when-ai-organizes-its-own-work.en.md    # 英文长文（首篇）
│   ├── fcop-natural-protocol.md                # "自然协议"现象篇（中文）
│   ├── fcop-natural-protocol.en.md             # "自然协议"现象篇（英文）
│   ├── fcop-natural-protocol-evidence/         # 完整证据档案（截图、公文、JSONL 原始转录）
│   ├── fcop-tmpa-lineage.md                    # "为什么站得住" 溯源篇 · TMPA 血缘（中文）
│   └── fcop-tmpa-lineage.en.md                 # "为什么站得住" 溯源篇 · TMPA 血缘（英文）
├── examples/
│   └── workspace-example/         # 最小参考工作区（tasks / results / events）
├── integrations/
│   └── windows-file-association/  # Windows 下注册 .fcop 文件关联 + 图标
├── assets/                        # Logo / 图标
├── LICENSE                        # MIT
└── README.md / README.zh.md
```

## 30 秒快速上手

FCoP 不需要"安装"，而是"采纳"。在任何一个项目里：

```bash
mkdir -p docs/agents/{tasks,reports,issues,log}
```

然后把 [`spec/codeflow-core.mdc`](spec/codeflow-core.mdc) 丢进项目的 `.cursor/rules/` 目录（或你用的 Agent 运行时的等价位置）。任何读了这份规则的 Agent 都会立刻知道怎么：

- 认领发给自己角色的任务；
- 按命名规则写回报告；
- 上报问题；
- 不碰别人的文件。

恭喜——你的 `docs/agents/` 文件夹现在就是一条 agent-to-agent 通信总线了。

更完整的参考请看 [`examples/workspace-example/`](examples/workspace-example/)。

## 设计原则

1. **文件名是唯一真理。**目录 + 文件名决定状态，frontmatter 只是冗余元数据。
2. **原子性来自 `rename()`**。没有别的——不需要锁，不需要事务。
3. **人机同构。**`cat` 能读的就是 Agent 能解析的，没有调试模式、没有管理后台。
4. **身份决定路径。**文件名里的角色标识本身就是权限模型——身份不匹配，Agent 连文件都动不了。
5. **零基础设施。**只要有文件系统就有 FCoP。笔记本能跑，集群能跑，跨机通过 `rsync` 就能跑。

## 参考实现

FCoP 最初是从 [**CodeFlow Desktop**](https://github.com/joinwell52-AI/codeflow-pwa)（为 Cursor IDE 配套的 PC 端 Agent 调度器）里抽离出来的。给 Agent 读的权威规则文件随 CodeFlow 一起发布：

- [`codeflow-desktop/templates/rules/codeflow-core.mdc`](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/codeflow-desktop/templates/rules/codeflow-core.mdc)

本仓库 `spec/` 下的是同一份文件的镜像，独立版本化，便于协议脱离 CodeFlow 单独演进。

## 状态与版本

- **当前规范版本**：v1.0.3（2026-04-19）
- **当前 Agent 规则文件**：对应 CodeFlow Desktop v2.12.17
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

FCoP 是在 Cursor + CodeFlow Desktop 上与 AI Agent 实际协作的过程中涌现出来的。规范里不少约定**最初是 Agent 们自己写出来的**，我们只是把它们整理成册。详情见 [现场报告](essays/when-ai-organizes-its-own-work.md)。
