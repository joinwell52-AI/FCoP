---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: dev-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# dev-team — 软件开发团队

**适用**:常规软件开发、功能交付、修复发布。
**leader**:`PM`
**角色**:`PM` · `DEV` · `QA` · `OPS`(4 个)

## 团队定位

`dev-team` 是 FCoP 自带的"标准开发班子"样板,职责分工、派发规则、升级条件全部文件化,
从第一天就让 Agent 知道边界在哪、谁跟谁对接、结论往哪回。

## ADMIN 是谁

`ADMIN` 是**真人管理员**,不是 AI 角色,**不进 `roles/` 目录**。

- `ADMIN` 是团队对外的唯一输入来源:所有需求、目标、决策、授权都来自 `ADMIN`。
- `ADMIN` **不写进 `fcop.json.roles`**,FCoP 在协议层已为它保留。
- 团队不直接跟 `ADMIN` 对话,全部走 `ADMIN ↔ PM` 的任务文件。
- 方向只有两条:
  - `ADMIN -> PM`:发任务,用 `TASK-*-ADMIN-to-PM.md`
  - `PM -> ADMIN`:回结果,用 `TASK-*-PM-to-ADMIN.md`

所以本团队的 AI 成员是 4 个(`PM / DEV / QA / OPS`),加上真人 `ADMIN`,一共 5 方协作。

## 协作链路

```
ADMIN  ──发需求──▶  PM  ──派任务──▶  DEV
  ▲                 │
  │                 ├──派测试──▶  QA
  │                 │
  │                 └──派部署──▶  OPS
  │
  └──阶段回执/最终交付──  PM
```

`PM` 是团队唯一对外回执入口;`DEV / QA / OPS` 的结论一律回到 `PM`,不直接对 `ADMIN`。

## 文档分层(三层)

| 层次 | 文件 | 作用 |
|---|---|---|
| 入口 | `README.md`(本文) | 团队定位、ADMIN 说明、协作链路 |
| 第 1 层 | `TEAM-ROLES.md` | 每个角色负责什么、不负责什么 |
| 第 2 层 | `TEAM-OPERATING-RULES.md` | 什么时候派、怎么回执、何时升级 |
| 第 3 层 | `roles/{PM,DEV,QA,OPS}.md` | 单角色深度说明:使命、输入、输出、交付标准、常见失误 |

泛化程度递减,细节递增。读完前两层就能跑协作;第 3 层只在扮演该角色时深读。

## 快速上手

如果你正在读这份 README,通常有两种情况:

### 情况 A:ADMIN 想用这套班子初始化项目

一句话告诉 Agent:

> 用预设团队 `dev-team` 初始化项目。

Agent 会调 `init_project(team="dev-team", lang="zh")`,把本目录的三层文档部署到
`docs/agents/shared/`,并建好 `fcop.json`。

### 情况 B:Agent 被指派为本团队的某个角色

你应该读:

1. 本文 `README.md`(团队大图)
2. `TEAM-ROLES.md`(边界)
3. `TEAM-OPERATING-RULES.md`(规则)
4. `roles/<你的角色>.md`(深度职责)

四份读完就能按协议干活。遇到边界问题时,回到 `TEAM-OPERATING-RULES.md` 第 1 节和第 5 节复查。

## 和其他预设团队的关系

- `dev-team` = 软件开发(本团队)
- `media-team` = 内容创作(leader: `PUBLISHER`)
- `mvp-team` = 创业 MVP(leader: `MARKETER`)
- `qa-team` = 专项测试(leader: `LEAD-QA`)

四套预设是**并列的样本**,不是继承关系。切换团队请重新 `init_project`,不要在同一项目混用多套角色命名。
