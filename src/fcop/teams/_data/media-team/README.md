---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: media-team
doc_id: TEAM-README
updated_at: 2026-04-17
---

# media-team — 自媒体团队

**适用**:内容选题、素材采集、撰写、编校、发布全链路。
**leader**:`PUBLISHER`
**角色**:`PUBLISHER` · `COLLECTOR` · `WRITER` · `EDITOR`(4 个)

## 团队定位

`media-team` 是 FCoP 自带的"标准内容班子"样板,面向公众号、博客、新闻通讯、短视频文案等内容产线。
从选题到成稿到发布,每一步都落文件,便于溯源、改稿、复盘和归档。

## ADMIN 是谁

`ADMIN` 是**真人管理员**,不是 AI 角色,**不进 `roles/` 目录**。

- `ADMIN` 是团队对外的唯一输入来源:所有选题、方向、品牌要求、审批都来自 `ADMIN`。
- `ADMIN` **不写进 `fcop.json.roles`**,FCoP 在协议层已为它保留。
- 团队不直接跟 `ADMIN` 对话,全部走 `ADMIN ↔ PUBLISHER` 的任务文件。
- 方向只有两条:
  - `ADMIN -> PUBLISHER`:发选题/需求,用 `TASK-*-ADMIN-to-PUBLISHER.md`
  - `PUBLISHER -> ADMIN`:回稿件/状态,用 `TASK-*-PUBLISHER-to-ADMIN.md`

所以本团队的 AI 成员是 4 个(`PUBLISHER / COLLECTOR / WRITER / EDITOR`),加上真人 `ADMIN`,一共 5 方协作。

## 协作链路

```
ADMIN ──发选题──▶  PUBLISHER ──派采集──▶  COLLECTOR
  ▲                  │
  │                  ├──派撰写(带素材)──▶  WRITER
  │                  │
  │                  └──派编校──▶          EDITOR
  │
  └──终审后发布/回执──  PUBLISHER
```

`PUBLISHER` 是团队唯一对外入口,也是内容发布的最终把关人。
`COLLECTOR / WRITER / EDITOR` 的产出一律回到 `PUBLISHER`,不直接对 `ADMIN`,
也不横向交接稿件(所有跨岗流转由 `PUBLISHER` 汇总后再派发)。

## 文档分层(三层)

| 层次 | 文件 | 作用 |
|---|---|---|
| 入口 | `README.md`(本文) | 团队定位、ADMIN 说明、协作链路 |
| 第 1 层 | `TEAM-ROLES.md` | 每个角色负责什么、不负责什么 |
| 第 2 层 | `TEAM-OPERATING-RULES.md` | 什么时候派、怎么回执、何时升级 |
| 第 3 层 | `roles/{PUBLISHER,COLLECTOR,WRITER,EDITOR}.md` | 单角色深度说明 |

## 快速上手

### ADMIN 想用这套班子初始化项目

> 用预设团队 `media-team` 初始化项目。

Agent 会调 `init_project(team="media-team", lang="zh")`,把本目录的三层文档部署到
`docs/agents/shared/`,并建好 `fcop.json`。

### Agent 被指派为本团队的某个角色

依次读:`README.md` → `TEAM-ROLES.md` → `TEAM-OPERATING-RULES.md` → `roles/<你的角色>.md`。

## 和其他预设团队的关系

- `dev-team` = 软件开发(leader: `PM`)
- `media-team` = 内容创作(本团队)
- `mvp-team` = 创业 MVP(leader: `MARKETER`)
- `qa-team` = 专项测试(leader: `LEAD-QA`)
