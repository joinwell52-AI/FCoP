# FCoP 预设团队样板库 / Preset Team Templates

本目录是 `fcop` Python 包内置的**样板库**,给手头没有角色文档、但想立刻按 FCoP 协议开干的用户一个可以复制即用的起点。

This directory ships the stock **template library** bundled inside the `fcop`
Python package, so users without role docs can start working to the FCoP
protocol right away.

## 目录结构 / Layout

```
teams/
├── README.md          # 本文件 / this file
├── index.json         # 机器可读索引 / machine-readable index
├── dev-team/          # 软件开发 / software development
├── media-team/        # 自媒体 / content media
├── mvp-team/          # 创业 MVP / startup MVP
└── qa-team/           # 专项测试 / dedicated testing
```

## 每个团队的三层结构 / Three-Layer Docs Per Team

```
<team>/
├── README.md / README.en.md                     # 入口:定位 / ADMIN / 协作链路
├── TEAM-ROLES.md / TEAM-ROLES.en.md             # 第 1 层:谁负责什么
├── TEAM-OPERATING-RULES.md / .en.md             # 第 2 层:什么时候派、怎么回、何时升级
└── roles/
    ├── {LEADER}.md / .en.md                     # 第 3 层:主控角色(leader)
    ├── {ROLE-2}.md / .en.md
    ├── {ROLE-3}.md / .en.md
    └── {ROLE-4}.md / .en.md
```

- **入口**:快速理解团队是干什么的、ADMIN 在哪里、链路怎么走。
- **第 1 层**:角色分工与边界。
- **第 2 层**:运行规则(派发、回执、升级、高危动作)。
- **第 3 层**:单个角色的深度职责说明。

泛化程度递减,细节递增。读完前两层就能跑协作;第 3 层只在扮演该角色时深读。

## 四个预设团队 / Four Preset Teams

| 团队 | leader | 角色(AI) | 场景 |
|------|--------|---------|------|
| `dev-team` | `PM` | `PM / DEV / QA / OPS` | 软件开发、修复发布 |
| `media-team` | `PUBLISHER` | `PUBLISHER / COLLECTOR / WRITER / EDITOR` | 内容选题、撰写、发布 |
| `mvp-team` | `MARKETER` | `MARKETER / RESEARCHER / DESIGNER / BUILDER` | 创业 MVP、想法验证 |
| `qa-team` | `LEAD-QA` | `LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER` | 独立测试、多战线并行 |

每个团队的 AI 角色是 4 个,加上真人 `ADMIN`,一共 5 方协作。

`ADMIN` 是**真人管理员**,FCoP 在协议层已为它保留,**不写入 `fcop.json.roles`**,也**不放在 `roles/` 目录**。关于 ADMIN 的说明请看每个团队自己的 `README.md`。

## 怎么用 / How to Use

两条路径,按需选:

### A. 初始化新项目 / Initialize a new project

一句话告诉 agent:

> 用预设团队 `<team-id>` 初始化项目。

Agent 会调 `init_project(team="<team-id>", lang="zh" or "en")`,把对应团队的三层文档部署到
你的项目 `docs/agents/shared/`,并建好 `fcop.json`。

### B. 已有项目,只部署/升级角色文档 / Existing project — deploy or upgrade role docs only

一句话告诉 agent:

> 把 `<team-id>` 的角色文档部署到本项目。

Agent 会调 `deploy_role_templates(team="<team-id>", lang="zh" or "en")`。已有的旧版扁平角色文档(例如 `PM-01.md`)会被自动归档到 `.fcop/migrations/<timestamp>/`,新版三层结构覆盖上去,覆盖前有归档,可回退。

## URI 访问约定 / URI Conventions

预设文档也作为 MCP resource 暴露:

- `fcop://teams` — 索引
- `fcop://teams/{team}` — 团队 README
- `fcop://teams/{team}/TEAM-ROLES` — 角色分工(第 1 层)
- `fcop://teams/{team}/TEAM-OPERATING-RULES` — 运行规则(第 2 层)
- `fcop://teams/{team}/{role}` — 单角色深度(第 3 层)
  - 例如:`fcop://teams/dev-team/PM`、`fcop://teams/qa-team/LEAD-QA`
  - 旧 URI 如 `fcop://teams/dev-team/PM-01` 仍然解析(向后兼容)

所有 URI 支持语言后缀:`?lang=zh`(默认)或 `?lang=en`。

## 不在这里的东西 / Not in here

- 真实任务文件(`TASK-*.md`)—— 运行期才产生,放在 `docs/agents/tasks/` 等。
- 真实回执文件(`REPORT-*.md` / `ISSUE-*.md`)—— 同上。
- 项目自己的规范文档 —— 建议放项目自己的 `docs/agents/shared/`,不要改这里的样板。

这份样板库的目标是**让 FCoP 开箱即用**,不是规定每个项目必须长成这个样子。真正跑起来以后,
每个项目会演化出自己的具体规范,但入口、边界、出口这三件事应尽量保持 FCoP 的形态。
