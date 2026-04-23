---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: qa-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# qa-team — 专项测试团队

**适用**:交付前的专项测试、回归、自动化覆盖、性能验证。
**leader**:`LEAD-QA`
**角色**:`LEAD-QA` · `TESTER` · `AUTO-TESTER` · `PERF-TESTER`(4 个)

## 团队定位

`qa-team` 是 FCoP 自带的"独立测试团队"样板,适合规模较大、质量要求高、
需要把测试角色从开发团队中拆出来独立运作的场景。

与 `dev-team` 中单一 `QA` 角色不同,`qa-team` 把测试再拆成**功能测试**、
**自动化测试**、**性能测试**三个专业分工,由 `LEAD-QA` 统一调度。

## ADMIN 是谁

`ADMIN` 是**真人管理员**,不是 AI 角色,**不进 `roles/` 目录**。

- `ADMIN` 是团队对外的唯一输入来源:测试目标、质量门槛、优先级都来自 `ADMIN`。
- `ADMIN` **不写进 `fcop.json.roles`**,FCoP 在协议层已为它保留。
- 团队不直接跟 `ADMIN` 对话,全部走 `ADMIN ↔ LEAD-QA` 的任务文件。
- 方向只有两条:
  - `ADMIN -> LEAD-QA`:发测试任务/质量目标,用 `TASK-*-ADMIN-to-LEAD-QA.md`
  - `LEAD-QA -> ADMIN`:回测试结论/风险评估,用 `TASK-*-LEAD-QA-to-ADMIN.md`

> **跨团队场景**:如果本团队与 `dev-team` 配合(例如接收 `dev-team` 的 `PM` 转发过来的测试任务),
> 在当前项目中 `PM` 也视作"上游入口",但正式结论的对外回执仍由 `LEAD-QA` 负责。

所以本团队的 AI 成员是 4 个(`LEAD-QA / TESTER / AUTO-TESTER / PERF-TESTER`),
加上真人 `ADMIN`,一共 5 方协作。

## 协作链路

```
ADMIN ──发测试目标──▶  LEAD-QA ──派功能测试──▶  TESTER
  ▲                   │
  │                   ├──派自动化──▶          AUTO-TESTER
  │                   │
  │                   └──派性能──▶            PERF-TESTER
  │
  └──测试结论/风险评估──  LEAD-QA
```

`LEAD-QA` 是团队唯一对外入口,也是"是否建议发布"的决策人。
`TESTER / AUTO-TESTER / PERF-TESTER` 的结论一律回到 `LEAD-QA`,
不直接对 `ADMIN`,也不横向直交(所有跨岗协作由 `LEAD-QA` 汇总后再派发)。

## 文档分层(三层)

| 层次 | 文件 | 作用 |
|---|---|---|
| 入口 | `README.md`(本文) | 团队定位、ADMIN 说明、协作链路 |
| 第 1 层 | `TEAM-ROLES.md` | 每个角色负责什么、不负责什么 |
| 第 2 层 | `TEAM-OPERATING-RULES.md` | 什么时候派、怎么回执、何时升级 |
| 第 3 层 | `roles/{LEAD-QA,TESTER,AUTO-TESTER,PERF-TESTER}.md` | 单角色深度说明 |

## 快速上手

### ADMIN 想用这套班子初始化项目

> 用预设团队 `qa-team` 初始化项目。

Agent 会调 `init_project(team="qa-team", lang="zh")`,部署三层文档并建 `fcop.json`。

### Agent 被指派为本团队的某个角色

依次读:`README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<你的角色>.md`。

## 和其他预设团队的关系

- `dev-team` = 软件开发(leader: `PM`,含一个综合性 `QA` 角色)
- `media-team` = 内容创作(leader: `PUBLISHER`)
- `mvp-team` = 创业 MVP(leader: `MARKETER`)
- `qa-team` = 专项测试(本团队)

`dev-team` 的 `QA` 适合小型项目、测试专业分工需求低的场景;
`qa-team` 适合需要独立质量团队、覆盖功能/自动化/性能三条战线的场景。
