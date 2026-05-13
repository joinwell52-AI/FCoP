---
protocol: fcop
version: 1
kind: internal-archive
sender: SYSTEM
recipient: TEAM
internal_only: true
fcop_version: "{fcop_version}"
deployed_at: "{deployed_at}"
---

> ⚠️ **INTERNAL ONLY · 内部档案 · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> 本目录（`fcop/internal/`）是团队**内部档案**桶，仅供本协议团队
> 自审 / 复盘 / 决策追溯使用。**对外发布前必须先经审查改写**
> （删除原话引用、敏感人物、未公开决策细节）。
>
> This directory (`fcop/internal/`) is the **team-internal archive
> bucket**: for team self-audit / retrospective / decision trail
> only. **Must be reviewed and rewritten before any external
> publication** (strip raw quotes, sensitive persons, undisclosed
> decisions).

# fcop/internal/ — 团队内部档案桶

## 这是什么 / What this is

本目录由 FCoP `Project.init(deploy_internal_template=True)` 部署，
对应 **Rule 4.6**（fcop-rules.mdc v3.0.0 起 / fcop@2.0.0 起）。
它是 `fcop/` 协作元数据层之外的一个**可选**子层（non-mandatory soft
convention），承载团队**内部**用、不直接对外发布的档案：

This directory is deployed by
`Project.init(deploy_internal_template=True)` and corresponds to
**Rule 4.6** (fcop-rules.mdc v3.0.0 onwards / fcop@2.0.0 onwards).
It is an **optional** sub-layer of `fcop/` (non-mandatory soft
convention) for **team-internal** archive material that is not
directly externalised:

- 涌现观察日志 / emergence-log
- 角色自我披露 / self-disclosure
- 决策审计链 / decision-trail
- 上游 ISSUE 草稿 / upstream-issue drafts
- ADMIN 战略原话保留 / ADMIN strategic quotes
- 任何"草稿期不希望进 git history、定稿后再外发"的过渡材料

## 与项目其它目录的边界 / Boundaries with other directories

| 目录 / Dir | 装什么 / Holds | 强制？ | 对外可见？ |
|---|---|---|---|
| `fcop/{tasks,reports,...}` | 协作流水 | 是（Rule 2） | 是 |
| `fcop/internal/`（本桶） | 团队内部档案 | 否（Rule 4.6 soft） | 可选，团队自定 |
| `docs/` | 项目对外文档 | 否 | 是 |
| `essays/` | 公开随笔 / 哲学叙事 | 否 | 是 |
| `workspace/<slug>/` | 任务产物（代码 / 数据） | 否（Rule 7.5 soft） | 是 |

## 推荐子目录 / Recommended subdirectories

```
fcop/internal/
├── README.md              ← 本文件（含 internal-only 声明）
├── emergence-log/         ← 涌现观察日志（如 codeflow / Bridgeflow 现场）
├── self-disclosure/       ← PM / 角色自我披露
├── decision-trail/        ← 决策审计链（ADMIN 决策原话 + 落地章节）
└── upstream-issues/       ← 上游开源仓库 ISSUE 的草稿池
```

子目录非强制，按需开。

## `internal-only` 声明语法 v1 / Declaration Syntax v1

每份 `fcop/internal/` 下 `.md` 文件**应当**（should）在 frontmatter 之后
加一段醒目的双语声明块：

Every `.md` file under `fcop/internal/` SHOULD carry a bilingual
declaration block right after the YAML frontmatter:

```markdown
---
protocol: fcop
version: 1
kind: internal-archive
sender: PM
recipient: PM
internal_only: true
---

> ⚠️ **INTERNAL ONLY · 内部档案 · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> （本文件用途说明 / file purpose description）

# 正文标题 / Body title
...
```

最低要求（per ADR-0034 §4.3）：

1. 必须是 frontmatter 之后的**第一个 block**（不能埋在正文中段）。
2. 必须包含双语警告字串 `INTERNAL ONLY` / `内部档案`，方便 grep。
3. **建议**配合 frontmatter 写一个 `internal_only: true` 字段
   （机器可读，与 `fcop_audit()` 钩子配合）。

## audit 行为 / Audit behaviour

`fcop_audit()` 在扫描本桶时只生成 **P3 (suggestion)** 提示，不阻塞：

- file 缺声明块或 `internal_only: true` 字段 → P3 提示补全；
- file 携带 `internal_only: true` 但**不在**本桶下 → P3 提示位置错放。

`fcop_audit()` against this bucket only emits **P3 (suggestion)**
hints, never blocks:
- missing declaration block / `internal_only` field → P3 nudge
- carries `internal_only: true` but lives outside `fcop/internal/`
  → P3 misplaced-location flag

## 为什么这是 soft convention / Why soft

Rule 4.6 与 Rule 7.5（`workspace/` 笼子）是同款设计模式：协议**优先
教育，少处罚**——硬规则只立在 Rule 0–4 / Rule 5 / Rule 7 这种"破坏性
/ 真相性"红线上；目录组织 / 命名习惯这种"漂移代价低 + 教育收益高"
的领域全部走 soft，让协议长出**自演化的肌肉**而非僵化的骨骼。

Rule 4.6 mirrors Rule 7.5 (`workspace/` cage) in design pattern:
**prefer education over punishment** — hard rules sit only on Rules
0–4 / 5 / 7's destructive / truth red lines; directory organisation
and naming conventions live entirely under soft conventions, letting
the protocol grow **self-evolving muscle** rather than rigid bone.

## 参考 / References

- 规则源头：`fcop-rules.mdc` Rule 4.6（v3.0.0+）
- 详细 commentary：`fcop-protocol.mdc` §How Rule 4.6 Applies（v3.0+）
- 设计决策：ADR-0034 §4.3 "internal-only declaration syntax v1"
- 相关 essays：`essays/evolution-reverse-absorption.md`（涌现的反向
  吸收范式 · 中文）、`essays/evolution-reverse-absorption.en.md`（英）
