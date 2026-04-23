---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# mvp-team — 创业 MVP 团队

**适用**:产品从 0 到 1、快速验证想法、做 MVP 并测试市场。
**leader**:`MARKETER`
**角色**:`MARKETER` · `RESEARCHER` · `DESIGNER` · `BUILDER`(4 个)

## 团队定位

`mvp-team` 是 FCoP 自带的"创业小队"样板,面向早期验证阶段:一个想法 →
需不需要做 → 怎么做最小 → 能不能跑通市场。四个角色各管一个关卡,
`MARKETER` 负责把所有信息收拢成"是否进入下一轮"的决策点。

之所以 leader 是 `MARKETER` 而不是 `BUILDER`,是因为 MVP 阶段的瓶颈是
"有没有市场"而不是"能不能写出来"。

## ADMIN 是谁

`ADMIN` 是**真人管理员**(通常就是创始人本人),不是 AI 角色,**不进 `roles/` 目录**。

- `ADMIN` 是团队对外的唯一输入来源:产品愿景、目标市场、资源约束都来自 `ADMIN`。
- `ADMIN` **不写进 `fcop.json.roles`**,FCoP 在协议层已为它保留。
- 团队不直接跟 `ADMIN` 对话,全部走 `ADMIN ↔ MARKETER` 的任务文件。
- 方向只有两条:
  - `ADMIN -> MARKETER`:发愿景/约束/决策,用 `TASK-*-ADMIN-to-MARKETER.md`
  - `MARKETER -> ADMIN`:回里程碑/阻塞/成果,用 `TASK-*-MARKETER-to-ADMIN.md`

所以本团队的 AI 成员是 4 个(`MARKETER / RESEARCHER / DESIGNER / BUILDER`),
加上真人 `ADMIN`,一共 5 方协作。

## 协作链路

```
ADMIN ──发愿景/约束──▶  MARKETER ──派调研──▶  RESEARCHER
  ▲                    │
  │                    ├──派设计(带调研结论)──▶  DESIGNER
  │                    │
  │                    └──派构建(带 PRD)──▶     BUILDER
  │
  └──里程碑/增长结果──  MARKETER
```

`MARKETER` 是团队唯一对外入口,也是"是否进入下一阶段"的决策人。
`RESEARCHER / DESIGNER / BUILDER` 的产出一律回到 `MARKETER`,
不直接对 `ADMIN`,也不横向直交(所有跨岗流转由 `MARKETER` 汇总后再派发)。

## 文档分层(三层)

| 层次 | 文件 | 作用 |
|---|---|---|
| 入口 | `README.md`(本文) | 团队定位、ADMIN 说明、协作链路 |
| 第 1 层 | `TEAM-ROLES.md` | 每个角色负责什么、不负责什么 |
| 第 2 层 | `TEAM-OPERATING-RULES.md` | 什么时候派、怎么回执、何时升级 |
| 第 3 层 | `roles/{MARKETER,RESEARCHER,DESIGNER,BUILDER}.md` | 单角色深度说明 |

## 快速上手

### ADMIN 想用这套班子初始化项目

> 用预设团队 `mvp-team` 初始化项目。

Agent 会调 `init_project(team="mvp-team", lang="zh")`,部署三层文档并建 `fcop.json`。

### Agent 被指派为本团队的某个角色

依次读:`README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<你的角色>.md`。

## 和其他预设团队的关系

- `dev-team` = 软件开发(leader: `PM`)
- `media-team` = 内容创作(leader: `PUBLISHER`)
- `mvp-team` = 创业 MVP(本团队)
- `qa-team` = 专项测试(leader: `LEAD-QA`)

`mvp-team` 与 `dev-team` 的差别:`dev-team` 默认产品方向已定、任务清楚;
`mvp-team` 默认方向未定、要边做边验证,因此 leader 是做增长的 `MARKETER`,不是 `BUILDER`。
