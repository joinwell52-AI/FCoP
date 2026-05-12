---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-003
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: codeflow-cross-project-audit-20260513
session_id: sess-20260513-me-01
created_at: "2026-05-13T07:20:00+08:00"
---

# Codeflow 项目 FCoP 跨项目只读合规审计

## 背景 / Background

ADMIN 直接指令:

> 检查下,codeflow 项目的 FCoP 是否完全合规!

侦察发现项目实体位于 `D:\codeflow-3`(在 `D:\` 下还有 `codeflow-1` /
`codeflow-pwa` / `newflow-3` 等同代项目,但只有 `codeflow-3` 携带可定位
的 `fcop.json`)。基线快查已暴露多条显眼问题:

| 项目 | 现状 | 协议参照 |
|---|---|---|
| `fcop.json` 位置 | `docs/agents/fcop.json` | Rule "2.0.0" 起 canonical 路径为 `fcop/` |
| `fcop/` 目录 | 不存在 | 同上 |
| `.cursor/rules/fcop-*.mdc` | 已部署 | ADR-0006 host-neutral 四件套之 2 |
| `AGENTS.md` / `CLAUDE.md` | **缺失** | ADR-0006 同上,缺另 2 |
| 岗位文件 | 扁平 `PM-01.md` / `DEV-01.md` etc. | Rule 4.5(自 v1.3.0)要求 `roles/{ROLE}.md` 三层 |
| git repo | **不是 git repo** | 0.a.1 tripwire(`fcop_check()` 的 git diff 对照)无法生效 |
| `team` | `dev-team`,`leader: PM` | OK |

但这只是表层。完整合规需要把 fcop@1.1.0 / rules 2.2.0 / protocol commentary
2.0.0 的全部规则点过一遍。

## 跨项目审计约束 / Cross-project audit constraints

**本任务 carrier 落在 FCoP 仓库(`D:\FCoP`),不在 codeflow 仓库下落任
何 FCoP 协议文件。** 理由:

- Rule 1.0 / 1.7.0:角色 ↔ 身份一对一。我是 FCoP 项目里被 ADMIN 指派的
  `ME`;codeflow 项目里**未被指派任何角色**,严禁自命 `codeflow.PM` /
  `codeflow.AUDITOR` 等冒充身份。
- Rule 1.8.0:子 agent 继承呼叫者身份。这次"跨项目检查"在协议视角下
  本质是 FCoP 项目的 ME 用只读方式去看另一仓库——产出物归 FCoP 项目。
- 协议解释 Rule 1 Phase 2:"未获指派前不得读任务**正文**"。所以本次
  对 codeflow 的 `TASK-*.md` / `REPORT-*.md` 只读**文件名 + frontmatter**,
  绝不读正文(这与 `fcop_report()` UNBOUND 时的限制完全对齐)。

## 要做的事 / Deliverables

按以下清单完整扫一遍 codeflow-3,出**分级合规报告**:

### A. 协议规则部署 / Protocol Rules Deployment

- [ ] 四件套(`.cursor/rules/fcop-rules.mdc` + `fcop-protocol.mdc` +
      `AGENTS.md` + `CLAUDE.md`)是否齐全
- [ ] 项目本地 rules 版本 vs 包内最新版本(P=E 漂移检测)
- [ ] 是否调用过 `redeploy_rules()`(从文件 mtime / `.fcop/migrations/` 推
      断)

### B. 目录结构 / Directory Layout

- [ ] canonical `fcop/` 还是 legacy `docs/agents/`
- [ ] 五桶(`tasks/` `reports/` `issues/` `shared/` `log/`)是否齐全
- [ ] `workspace/<slug>/` 工作区约定(Rule 7.5)是否在用

### C. 团队文档三层(Rule 4.5)/ Three-layer Team Docs

- [ ] Layer 0 · `TEAM-README.md`(ADMIN 入口)
- [ ] Layer 1 · `TEAM-ROLES.md`(角色边界)
- [ ] Layer 2 · `TEAM-OPERATING-RULES.md`(运作规则)
- [ ] Layer 3 · `roles/{ROLE}.md`(单岗深度)
- [ ] **没有** `roles/ADMIN.md`(ADMIN 是真人,不入 roles/)

### D. `fcop.json` 完整性 / fcop.json Integrity

- [ ] `mode` / `team` / `roles` / `leader` 齐全
- [ ] roles 含 v1.0 新增的 `layer`(worker / governance / admin)字段?
      可选,但若声明则需正确
- [ ] **不含** `ADMIN` 角色(Rule 1 invariant)

### E. 文件命名 + frontmatter 合规

仅看 frontmatter 与文件名(**不读正文**):

- [ ] 任务命名 `TASK-{YYYYMMDD}-{NNN}-{sender}-to-{recipient}.md`
- [ ] 报告命名 同上模式,在 `reports/`
- [ ] 问题命名 `ISSUE-{YYYYMMDD}-{NNN}-{summary}.md`
- [ ] 是否出现 `AMEND-*` / `*-v2.md` 等幽灵前缀(Rule 5 禁)
- [ ] frontmatter 必填字段:`protocol` / `version` / `sender` /
      `recipient`(Rule 3)
- [ ] `sender` / `recipient` 与 `fcop.json` 中 `roles` 一致(不含未声明的
      角色码,不冒充 `ADMIN`)
- [ ] `leader` 路由是否成立(team 模式下 ADMIN ↔ leader 唯一对外接口,
      Rule 4)——通过统计 sender/recipient pair 间接验证

### F. Reciprocity(Rule 6)

- [ ] 每条 `tasks/TASK-*.md` 是否都有匹配的 `reports/TASK-*.md` 或
      follow-up TASK(按 `thread_key` / 文件名 pair 对照)
- [ ] 哑火(任务存在 ≥7 天无回应)清单

### G. Append-only(Rule 5)/ History Integrity

- [ ] 是否有重名(同前缀同序号)文件 → 暗示原地修改后追加
- [ ] log/ 是否有未归档的 sprint artifact

### H. v1.0 / v1.1 新能力使用情况

- [ ] `REVIEW-*` 文件是否出现(若出现需校验 `decision` 枚举 5 值合规、
      `subject_id` / `reviewer` / `reviewed_at` 齐全)
- [ ] `risk_level` 字段是否在使用
- [ ] `needs_human` / `human_approval` 是否被滥用(`pending` 严禁)

### I. 0.a.1 tripwire 等价检查

- [ ] codeflow-3 不是 git repo → `fcop_check()` 的"git diff vs FCoP 账本"
      事后审计**无法运行**,这本身是 P1 级缺失,需在报告中说明并给出建议
- [ ] 替代方案:统计 `workspace/` 与开放 TASK 的对应关系

## 验收 / Acceptance

- [ ] 写出 `REPORT-20260513-003-ME-to-ADMIN-codeflow-cross-project-fcop-audit.md`,
      按 P0 / P1 / P2 分级列出全部问题
- [ ] 每条结论附**事实出处**(路径 + 文件名 + 行号或字段)。Rule 0.c
      不允许"我以为是这样",写"unverified"也合法
- [ ] 不在 codeflow-3 仓库下写任何文件
- [ ] 本任务 commit 时严格遵守新立的 `git add` 显式路径硬约束(SOP v2
      问题 7,见 `b4dc1f7`)

## 风险 / Risk

risk_level: low。只读跨项目审计,**绝不修改** codeflow-3 任何文件。
回滚:不存在副作用,无需回滚。
