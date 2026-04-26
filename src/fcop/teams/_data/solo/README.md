---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: solo
doc_id: TEAM-README
updated_at: 2026-04-26
---

# solo — 单 AI 协作模式

**适用**：一个 AI 帮你做事；不需要拆班子、不需要派单。
**leader**：`ME`（兼 leader、兼唯一执行者）
**角色**：`ME`（1 个 AI）+ `ADMIN`（你，真人）

## 团队定位

`solo` 是 FCoP 协议里 **一等的协作模式**——不是 "团队的简化版"。它解决的是
"我就一个人，但仍然要 FCoP 的文件纪律" 这种最常见场景：

- 不用养四个 Cursor 窗口；
- 不用记 leader / member 的派单顺序；
- **但 Rule 0.a / Rule 0.b / Rule 0.c 一条都不打折**——所有指令仍然落
  `TASK-*-ADMIN-to-ME.md`，所有结果仍然落 `REPORT-*-ME-to-ADMIN.md`，
  所有质疑/异议仍然走 `ISSUE-*` 或 `.fcop/proposals/`。

> Solo 不是 "省协议"；solo 是 "协议两个角色都到位（ADMIN + ME），
> 但同一台机器上只装一个 AI 客户端"。

## ADMIN 是谁

`ADMIN` 是**真人管理员**，不是 AI 角色，**不进 `roles/` 目录**。

- `ADMIN` 是团队对外唯一输入来源：所有需求、目标、决策、授权都来自 `ADMIN`。
- `ADMIN` **不写进 `fcop.json.roles`**，FCoP 在协议层已为它保留。
- 在 solo 模式下 `ADMIN ↔ ME` 是**直接对接**——没有 PM/Leader 中转，但
  仍然走文件协议（不许口头派单 / 口头结论）。

## 协作链路

```
ADMIN  ──发任务──▶  ME  ──写产物──▶  workspace/<slug>/
  ▲                  │
  │                  └──回执──▶  REPORT-*-ME-to-ADMIN.md
  │                                         │
  └──读 / 验收 / 反馈 / 下一单 ◀────────────┘
```

`ADMIN` 唯一对接 `ME`；`ME` 对每条任务必须有对应回执。

## 文档分层（三层）

| 层次 | 文件 | 作用 |
|---|---|---|
| 入口 | `README.md`（本文） | 团队定位、ADMIN 说明、协作链路 |
| 第 1 层 | `TEAM-ROLES.md` | `ME` 负责什么、不负责什么；`ADMIN` 边界 |
| 第 2 层 | `TEAM-OPERATING-RULES.md` | 任务怎么派、回执怎么写、什么时候升级、跨"自审" |
| 第 3 层 | `roles/ME.md` | `ME` 的核心职责（含**工作流硬约束**：先 task → 做 → report → archive） |

solo 也分三层不是为了"凑齐"。`ME.md` 里专门写了 **Rule 0.a 在单角色场景下
怎么自审**——这是 solo 模式区别于"无协议"的唯一硬约束，不读这一份会把
solo 用回成 "AI 自由发挥"。

## 快速上手

### 情况 A：ADMIN 想用 solo 模式初始化项目

一句话告诉 Agent：

> 用 solo 模式初始化项目，角色代码叫 `ME`。

Agent 会调 `init_solo(role_code="ME", lang="zh")`，把本目录的三层文档部署到
`docs/agents/shared/`，并建好 `fcop.json` / `LETTER-TO-ADMIN.md` /
`workspace/`。

### 情况 B：Agent 被指派为本团队的 `ME`

你应该按顺序读：

1. 本文 `README.md`（团队大图）
2. `TEAM-ROLES.md`（角色边界 / ADMIN 边界）
3. `TEAM-OPERATING-RULES.md`（运作规则、自审）
4. `roles/ME.md`（**工作流硬约束** + 深度职责）

四份读完就能按协议干活。出现"这件事我直接做就行了吧"的念头时，
回到 `roles/ME.md` § "核心工作流（硬约束）" 复查。

## 和其他预设团队的关系

- **solo** = 单 AI（本团队）
- `dev-team` = 软件开发四人组（PM / DEV / QA / OPS）
- `media-team` = 内容创作四人组（PUBLISHER / COLLECTOR / WRITER / EDITOR）
- `mvp-team` = 创业 MVP 四人组（MARKETER / RESEARCHER / DESIGNER / BUILDER）
- `qa-team` = 专项测试四人组（LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER）

solo 和四套多角色团队是**并列样本**，不是继承关系。从 solo 切到团队请重新
`init_project`，FCoP 会把旧 `shared/` 自动归档到 `.fcop/migrations/<时间戳>/`。
