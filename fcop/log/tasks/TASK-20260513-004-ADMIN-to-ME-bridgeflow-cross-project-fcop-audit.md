---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-004
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: bridgeflow-cross-project-audit-20260513
session_id: sess-20260513-me-01
supersedes: TASK-20260513-003
created_at: "2026-05-13T07:22:00+08:00"
---

# Bridgeflow 项目 FCoP 跨项目只读合规审计(修正 TASK-003 走错项目)

## Rule 0.c 账改 / Amendment

**修正自 `TASK-20260513-003`**。我在收到 ADMIN 指令"检查下,codeflow
项目的 FCoP 是否完全合规!"后,**误把 `D:\codeflow-3` 当成目标**,理由是
它是 `D:\` 下唯一带 `fcop.json` 的"codeflow-*"目录。ADMIN 紧接着用 3 个
感叹号纠正:

> **Bridgeflow 目录D盘!!!**

正确目标是 **`D:\Bridgeflow`**。

**Rule 5 处理**:TASK-003 不删、不改,作为"agent 走错路径"的历史账本
留在 `tasks/` → `log/tasks/`,与本 TASK-004 一起归档。这正是 Rule 5
"append-only history" 在小事故上的标准用法:**用下一序号同前缀新文件
修正,不抹掉错误本身**。

**Rule 0.c 自检**:我之所以走错,根因是看到 `codeflow-3/docs/agents/fcop.json`
一个事实命中后,**没核实 ADMIN 真正的 target**——典型"我以为是这样"。
SOP 沉淀:跨项目审计第 0 步应当是 **明确确认审计对象 path**,不要因
为某个候选项目"看起来像"就直接奔过去。

## 背景 / Background

`D:\Bridgeflow` 是 ADMIN 主力工程,最近一直在做 FCoP "Mode 1 sprint"
冲刺 ALL GREEN(`fcop_audit(scope=takeover)` 三色全绿,P0=P1=P2=0)。
最近 git log 自述:

```text
890ff3c  chore(fcop): daily archive batch 2026-05-12 v2 retry (D52=A / PM #71 fix)
0d1bab4  chore(fcop): Mode 1 sprint Phase D metadata sweep (D51=A)
6d1b108  chore(fcop): Mode 1 Phase B T2.7 (Lane 1) - archive 20 cursor-rules to migration bucket
```

ADMIN 此次"检查"指令在这条主线上 — 不是头一回检查,而是**周期性审
计 checkpoint**:验证 Mode 1 冲刺是否还在 ALL GREEN,有没有新出现的
回退。

### 基线快查(已扫)

| 项目 | 现状 | 评估 |
|---|---|---|
| Canonical `fcop/` 路径 | 存在 | ✓ |
| 四件套(`.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`) | 全部存在 | ✓ |
| Git repo | 是,branch=main | ✓ |
| `.fcop/` drawer | 存在 | ✓ |
| `workspace/` | 存在 | 需查 slug 合规 |
| `fcop_events.jsonl` 在根目录 | 是 — 需查是否被 git tracked(应 untracked) | 🟡 |
| `bridgeflow-nudger` / `codeflow-desktop` / `codeflow-plugin` / `codeflow-shell` 直接在根 | 是 | ❌ Rule 7.5(产物应在 workspace/<slug>/) |
| `_patch_*.py` 7 个脚本在根目录 | 是 | ❌ Rule 7.5 |
| `.smoke-*` 12 个目录在根 | 是 | ❌ Rule 7.5 (或合理 sandbox?需核) |
| **`.smoke-beta3-nomodel` 和 `.smoke-beta3-nomodel `(带尾空格)** | 两个并存 | ❌ 文件系统脏数据 / typo 残留 |
| **`.smoke-beta3-withmodel` 同上** | 两个并存 | ❌ 同上 |
| 两个 venv `.venv-fcop-1.4.0` / `.venv-fcop-1.5.1` 在根 | 是 | 🟡 应 .gitignore;不一定违规 |
| `HANDOVER-20260406.md` 在根 | 是 | 🟡 协议文档建议进 `fcop/shared/` |

## 跨项目审计约束 / Cross-project audit constraints

(沿用 TASK-003 同款约束,不重复说理。要点:)

- 不在 Bridgeflow 仓库下写任何 FCoP 协议文件
- 只读文件名 + frontmatter,**不读 task body / report body / issue body**
- 本 carrier 落在 `D:\FCoP\fcop\tasks\` 由 FCoP 的 ME 出具

## 要做的事 / Deliverables

按以下 11 章扫描,出**分级合规报告**:

### A. 协议规则部署 / Protocol Rules Deployment

- [ ] 4 件套版本读取:`fcop_rules_version` / `fcop_protocol_version`
      与 D:\FCoP 仓库内最新版本对比(P=E 漂移)
- [ ] `.fcop/migrations/` 历史(有几代旧规则被归档)

### B. 目录结构 / Directory Layout

- [ ] `fcop/` 五桶(`tasks/` `reports/` `issues/` `shared/` `log/`)齐全
- [ ] 是否多团队(`fcop/{team}/`)还是扁平
- [ ] `workspace/` slug 合规(Rule 7.5)

### C. 团队文档三层 / Three-layer Team Docs(Rule 4.5)

- [ ] Layer 0 / 1 / 2 / 3 齐全(`TEAM-README` / `TEAM-ROLES` /
      `TEAM-OPERATING-RULES` / `roles/{ROLE}.md`)
- [ ] 不含 `roles/ADMIN.md`

### D. `fcop.json` 完整性 / fcop.json Integrity

- [ ] `mode` / `team` / `roles` / `leader` 齐全且自洽
- [ ] 不含 `ADMIN` / `SYSTEM` role code
- [ ] v1.0 字段:`layer` / `can` / `cannot`(可选,有则需正确)

### E. 文件命名 + frontmatter / Naming + Frontmatter

- [ ] `TASK-` / `REPORT-` / `ISSUE-` / `REVIEW-` 命名 4 种合规
- [ ] 是否出现 `AMEND-*` / `*-v2.md` 等幽灵前缀
- [ ] frontmatter 必填字段(`protocol` / `version` / `sender` / `recipient`)
- [ ] sender / recipient 角色码在 `fcop.json` roles 内
- [ ] **取样**:每个 dir 取头 5 / 尾 5 / 中间随机 5 份,出抽样合规率

### F. 路由 / Routing(Rule 4)

- [ ] team 模式下是否 ADMIN ↔ leader 唯一对外接口(从 sender/recipient 分布推断)
- [ ] 是否存在 leader 短路(`PM-to-ADMIN`-非 leader 的横向)

### G. Reciprocity(Rule 6)/ 互惠回执

- [ ] 每条 `tasks/TASK-*.md` 是否有匹配的 `reports/REPORT-*.md` 或
      follow-up TASK(按 `thread_key` 配对)
- [ ] 哑火清单(任务 ≥7 天无回应)

### H. Append-only(Rule 5)/ 历史只增不改

- [ ] 序号冲突(同日同序号多文件)
- [ ] `log/` 归档量级(总条数 / 最近 30 天)
- [ ] 是否有跑 `git diff` 与 FCoP 账本对照时的"未挂任务的产物变更"
      (0.7.1+ `fcop_check()` 等价检查)

### I. Rule 7.5 工作区约定 / Workspace Convention

- [ ] 项目根的非协议产物清单(本次基线已发现 6+ 类违规)
- [ ] 每条违规产物是否能归到 `workspace/<slug>/`
- [ ] 重复目录(尾空格 typo)清单及处置建议

### J. v1.0 / v1.1 新能力使用情况

- [ ] `REVIEW-*` 文件统计 + decision 5 值合规检查
- [ ] `risk_level` 字段使用频次
- [ ] `needs_human` + `human_approval` 使用合规

### K. `git` 账本与 FCoP 账本一致性

- [ ] 项目根上 `fcop_events.jsonl` 是否在 git 跟踪范围(应 untracked)
- [ ] `.scratch/` / venv / `_*` 临时文件是否在 .gitignore
- [ ] `git status` working tree 噪音清单

## 输出格式 / Output Format

REPORT 按 **P0 / P1 / P2 三级**+ **绿区**列出:

- **P0**:阻断 Mode 1 ALL GREEN 的硬违规(例:`AGENTS.md` 缺失、frontmatter 非法等)
- **P1**:协议偏离但不致命(例:Rule 7.5 软约定违反、版本漂移)
- **P2**:卫生 / 改进建议(例:HANDOVER-* 在根目录、典型 mtime 异常)
- **绿区**:已合规的关键点(给 ADMIN 看到进展)

每条结论必须附**事实出处**(路径 + 文件名 / 字段名)。Rule 0.c 不允许
"我以为是这样",写"unverified"也合法。

## 验收 / Acceptance

- [ ] `REPORT-20260513-004-ME-to-ADMIN-bridgeflow-cross-project-fcop-audit.md`
- [ ] 不在 Bridgeflow 仓库下写任何文件
- [ ] commit 阶段严格走 SOP v2 问题 7:显式路径 `git add`,`git status --short`
      二次确认
- [ ] TASK-003 与 TASK-004 一起归档到 `log/tasks/`,二者作为线程
      `bridgeflow-cross-project-audit-20260513` 的完整证据链留存

## 风险 / Risk

risk_level: low。只读跨项目审计,绝不修改 Bridgeflow 任何文件。
