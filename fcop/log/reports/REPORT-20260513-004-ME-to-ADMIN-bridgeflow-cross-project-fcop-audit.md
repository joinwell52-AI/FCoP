---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-004
sender: ME
recipient: ADMIN
in_reply_to: TASK-20260513-004
priority: P1
thread_key: bridgeflow-cross-project-audit-20260513
session_id: sess-20260513-me-01
status: done
created_at: "2026-05-13T07:35:00+08:00"
audit_target: D:\Bridgeflow
audit_scope: read-only-cross-project
---

# Bridgeflow 项目 FCoP 跨项目只读合规审计报告

## TL;DR

**结论:Bridgeflow 处在 "Mode 1 sprint 中后期",大多数协议主干已合规,
但仍有 1 个 P0、5 个 P1、6 个 P2 待处理。** 建议处理顺序:P0 → P1.A
(`.gitignore` 补洞)→ P1.B(`tasks/_archive/` 改归正典 `log/`)→
其余。**没有任何 `AMEND-*` / `*-v2.md` 幽灵前缀,没有任何 sender 跨项目
冒用情况,Rule 4.5 三层文档双语模范实现** —— 主干很稳。

| 维度 | 数 |
|---|---|
| `fcop/**/*.md` 总量 | **295** |
| canonical TASK/REPORT/ISSUE/REVIEW 命名匹配 | **271 / 295** (≈92%,剩余 24 为合规 `shared/*` UPPERCASE 前缀) |
| TASK/REPORT/ISSUE/REVIEW 前缀但**非** canonical | **0 ⭐** |
| 历史归档量(`fcop/log/`) | 229 文件(2026-04: 4,2026-05: 225) |
| v1.0 / v1.1 新能力(REVIEW + needs_human + human_approval) | **已在用 ⭐** |

---

## 绿区 / Compliant baseline(11 项)

- ✓ `fcop_rules_version: 2.4.0` 与 D:\FCoP 包内 `2.4.0` 同步(
  `D:\Bridgeflow\.cursor\rules\fcop-rules.mdc:3`)
- ✓ ADR-0006 host-neutral 四件套齐全:
  `.cursor/rules/fcop-rules.mdc` (52,666B) + `.cursor/rules/fcop-protocol.mdc` (88,044B) +
  `AGENTS.md` (140,141B) + `CLAUDE.md` (140,141B)
- ✓ `AGENTS.md` 与 `CLAUDE.md` SHA-256 完全相同(
  `21925A58D2FEDD48977BEA2230FF01B5071885DE07B45AA4A1A2C487F4B57FBD`)
- ✓ Canonical `fcop/` 路径(无 `docs/agents/` legacy)
- ✓ 五桶齐全(`tasks/` `reports/` `issues/` `shared/` `log/`)
- ✓ **Rule 4.5 三层模范实现**:
  - Layer 0 `TEAM-README.md` ✓
  - Layer 1 `TEAM-ROLES.md` ✓
  - Layer 2 `TEAM-OPERATING-RULES.md` ✓
  - Layer 3 `roles/{PM,DEV,QA,OPS}.md` + `.en.md` **8 份双语角色文档** ⭐⭐⭐
  - `roles/ADMIN.md` **不存在** ✓(ADMIN 不进 roles/)
- ✓ `fcop.json` 合规:`mode: preset` + `team: dev-team` + `leader: PM` +
  `roles: ["PM","DEV","QA","OPS"]`(fcop 库 `Literal["solo","preset","custom"]`
  + `tuple[str, ...]` schema 支持,见 `D:\FCoP\src\fcop\models.py:760, 763`)
- ✓ **Rule 5 append-only 0 违规**:无任何 `AMEND-*` / `*-v2.md` 等幽灵前缀
- ✓ **v1.0 第四类 IPC + v1.1 needs_human 已在用**(见 `fcop/reviews/REVIEW-20260512-001-QA-...md`):
  `decision: needs_human` + `human_approval: {approver: ADMIN, decision: approve,
  approved_at, channel: cli, comment}` 完整子结构落盘 ⭐
- ✓ **Rule 4 路由分布合规**(sender/recipient 统计推断):
  PM 作为 leader 共 sender 146 / recipient 114;ADMIN 共 sender 14 / recipient 51;
  完全符合 `ADMIN ↔ PM` 唯一对外接口 + PM 扇出/扇入扇形流转
- ✓ **TEMPLATE 没有出现在 sender/recipient 配对的"对外"轨迹**(只在 14 个
  归档模板文件里出现,属合规模板而非协议消息)

---

## P0 · 阻断 Mode 1 ALL GREEN(1 条)

### P0-1 · `fcop/reports/` 整个目录在 git 里 untracked

**事实出处**:`git status --short`(在 `D:\Bridgeflow` 下执行)输出:

```text
?? fcop/reports/
?? fcop_events.jsonl
?? .scratch/
?? .venv-fcop-1.4.0/
?? .venv-fcop-1.5.1/
... (略)
```

`fcop/reports/` 整个目录是 **untracked**,意味着里面两份 REPORT
(`REPORT-20260512-021-DEV-to-PM-day1-fcop-upgrade.md` 与
`REPORT-20260512-030-OPS-to-PM-daily-archive-retry.md`)**没入版本库**。

按 Rule 0.a "land it as a file" 的字面,REPORT 已**落到磁盘**;但按
Rule 5 "版本控制不是备忘录,是证据链" 的精神,**未 commit 的 REPORT
不算证据**,下次 fcop_audit 复盘时不可追溯。

**建议处置**:`git add fcop/reports/`(显式路径)+ `git commit`,
按 SOP v2 问题 7 的"显式路径,严禁 -A" 规则。

**严重性**:阻断 ALL GREEN — `fcop_audit` 的 `git diff vs FCoP ledger`
对照会显示"产物落盘但未 commit",在 ADR-0006 等价检查里会爆 P0。

---

## P1 · 协议偏离 / 卫生洞(5 条)

### P1-1 · `tasks/_archive/` 第二归档点(协议正典是 `log/`)

**事实出处**:`D:\Bridgeflow\fcop\tasks\_archive\2026-04\`(目录存在,
内含 25 份 TASK + REPORT 历史文件),例如:

```text
fcop/tasks/_archive/2026-04/TASK-20260420-001-ADMIN-to-PM.md
fcop/tasks/_archive/2026-04/REPORT-20260421-001-PM-to-ADMIN.md
... (共 25 份)
```

**违规依据**:Rule 5 + 协议解释 "Leader archives completed threads —
move finished task+report pairs to `log/`" —— 归档目标是 **五桶之一的
`log/`**,不是 `tasks/_archive/`。当前 Bridgeflow 同时有两套归档:

- 协议正典 `fcop/log/2026-04/` (4 files) + `fcop/log/2026-05/` (225 files)
- 自创 `fcop/tasks/_archive/2026-04/` (25 files)

**P1 而非 P0**:这只是"归档点放错了",归档文件本身命名 + frontmatter
合规,不影响协议解析。

**建议处置**:`Move-Item fcop\tasks\_archive\* fcop\log\` 并保留 `2026-04/`
月份子目录(协议允许子目录分组),然后 `Remove-Item fcop\tasks\_archive`。

### P1-2 · `.gitignore` 漏洞:5 类 untracked 噪音随时可能 `git add -A` 入库

**事实出处**:`git status --short` + `.gitignore` 比对

| 项 | git 现状 | .gitignore 状态 |
|---|---|---|
| `.scratch/` | `??` untracked | **未覆盖** ✗ |
| `fcop_events.jsonl` | `??` untracked | **未覆盖** ✗ |
| `.venv-fcop-1.4.0/` | `??` | `.gitignore:12` 只写 `.venv/`,不匹配 `.venv-fcop-*` ✗ |
| `.venv-fcop-1.5.1/` | `??` | 同上 ✗ |
| `.smoke-beta3-nomodel ` (尾空格) | `??` | `.gitignore:68` 写 `.smoke-*/` 但 **不匹配尾空格名** ✗ |
| `.smoke-beta3-withmodel ` (尾空格) | `??` | 同上 ✗ |

**风险**:之前在 D:\FCoP 仓库就踩过雷 — `git add -A` 把 19 个临时文件
扫进 commit `d2ed13c`,后被 revert `cc60186` + 重做 `979bcd2`(见 D:\FCoP
仓库 `docs/release-process.md` 常见故障问题 7)。Bridgeflow 同样的雷
**还在**,只是 ADMIN 至今没用 `-A`。

**建议处置**:补 `.gitignore` 三行 +重命名两个尾空格目录:

```gitignore
.scratch/
fcop_events.jsonl
.venv*
```

```powershell
Rename-Item ".smoke-beta3-nomodel "    ".smoke-beta3-nomodel-typo"  # 之后删
Rename-Item ".smoke-beta3-withmodel "  ".smoke-beta3-withmodel-typo"
```

### P1-3 · Rule 7.5 工作区违反 · 4 个产物子项目在项目根

**事实出处**:`Get-ChildItem D:\Bridgeflow -Directory` 输出含:

```text
bridgeflow-nudger/
codeflow-desktop/
codeflow-plugin/
codeflow-shell/
```

而 `workspace/` 目录虽存在,**0 slug 子目录**。Rule 7.5 要求所有产物
进 `workspace/<slug>/`。

**软约束**:Rule 7.5 原文 "soft convention",老项目 0.4.6 以下没
`workspace/` 仍合规;Bridgeflow 是早期老项目 + 主力工程,4 个子项目
是已建立的产物分支,**重命名搬迁会引发巨量 git rename 与 import 路径
重写**。

**建议处置(分阶段)**:
- 阶段 1:补 `workspace/README.md` 注记这 4 个子项目为"legacy product
  trees,Rule 7.5 已知例外"
- 阶段 2:新建产物**默认**走 `new_workspace(slug)`
- 阶段 3:重大 refactor 窗口期再考虑批量搬迁

### P1-4 · `_patch_*.py` × 7 在项目根

**事实出处**:`D:\Bridgeflow\` 根:

```text
_patch_hero.py        _patch_hero2.py
_patch_monitor.py     _patch_monitor2.py
_patch_monitor3.py    _patch_monitor_final.py
_patch_switch_state.py
```

`.gitignore:93+136` 已用 `_patch_*.py` 兜底(两次,**重复**),所以 git
不会跟踪。**但根目录卫生** + Rule 7.5(产物进 workspace/)双重违反。

**建议处置**:`mkdir scripts/legacy-patches; mv _patch_*.py scripts/legacy-patches/`
+ 在 `.gitignore` 里调整对应规则(若要继续 `.gitignore` 这些则改成
`scripts/legacy-patches/_patch_*.py`)+ 删除 `.gitignore` 里 `_patch_*.py`
的重复行(L93 与 L136 完全一样)

### P1-5 · `fcop_protocol_version` 漂移 `2.3.0 → 2.4.0`(rules 已同步)

**事实出处**:
- Bridgeflow `.cursor/rules/fcop-protocol.mdc:3` → `fcop_protocol_version: 2.3.0`
- D:\FCoP `.cursor/rules/fcop-protocol.mdc:3` → `fcop_protocol_version: 2.4.0`
- Rules 双向同步:`fcop_rules_version: 2.4.0` 一致

**协议规定**:`fcop_report()` 会自动比对并提醒 ADMIN 调 `redeploy_rules()`。
Agent 不得自行调用(Rule 8 + ADR-0006)。这条**预期需要 ADMIN 显式处理**,
Bridgeflow agent 没违规,但**该 redeploy 而未 redeploy**就是一项漂移。

**建议处置**:ADMIN 在 Bridgeflow 执行:

```python
from pathlib import Path
from fcop.project import Project
Project(Path(r"D:\Bridgeflow")).deploy_protocol_rules(force=True, archive=True)
```

旧文件会自动归档到 `.fcop/migrations/<时间戳>/rules/`。

---

## P2 · 卫生 / 改进建议(6 条)

### P2-1 · `fcop/reviews/` 第六桶(协议未明确定义)

**事实出处**:`D:\Bridgeflow\fcop\reviews\REVIEW-20260512-001-QA-on-task-20260511-020-pm-to-ops.md`

Rule 9.1 只规定 REVIEW 命名 `REVIEW-{date}-{seq}-{reviewer}.md`,**没规定
放哪个目录**。fcop 库源码(`D:\FCoP\src\fcop\`)Grep `reviews` 无匹配——
**协议层 + 库层都没把 REVIEW 文件的目录位置定死**。

Bridgeflow 自创 `fcop/reviews/` 是合理实践,但**全协议生态没统一**。
**这其实是 FCoP 自己的协议覆盖空白**,Bridgeflow 在前面试水。

**建议处置(归属 FCoP 项目)**:ADR 补章把 `fcop/reviews/` 列为"五桶
+REVIEW 桶 → 六桶"标准布局(或建议把 REVIEW-*.md 放进 `fcop/reports/`
作为 audit-style 报告子类)。

### P2-2 · `fcop/internal/` 第七桶(协议未定义,但 Rule 2 允许)

**事实出处**:`D:\Bridgeflow\fcop\internal\` 含:

```text
emergence-log.md
p4-day5-schema-drift.md
p4-schema-mapping.md
path-backup-20260512-2137.txt
path-machine-backup-20260512-2138.txt
```

**评估**:这些是 Bridgeflow 自创的"内部观察 / spike note",不在
协议消息流(无 frontmatter / 无 sender / 无 recipient)。Rule 2 允许
开子目录 + 留 README;Bridgeflow 这里**没留 README**说明此桶用途,
新 agent 接手会困惑。

**建议处置**:补 `fcop/internal/README.md` 说明此目录定位。

### P2-3 · `HANDOVER-20260406.md` 在项目根

**事实出处**:`D:\Bridgeflow\HANDOVER-20260406.md`

属协议文档应在 `fcop/shared/` 下用 `RETRO-` 或 `DECISION-` 前缀
(协议规定的 UPPERCASE shared 前缀清单见 `fcop-protocol.mdc` "Shared
Documents"节)。

**建议处置**:`Move-Item HANDOVER-20260406.md fcop\shared\RETRO-20260406-001-handover.md`
+ 在原内容前面加一行 frontmatter 块(`shared/` 推荐写但不强制)。

### P2-4 · `tasks/_archive/2026-04/REPORT-20260425-001-FCoP-在-Bridgeflow-...-总结.md`

**事实出处**:`D:\Bridgeflow\fcop\tasks\_archive\2026-04\` 列表

文件名第 4 段(应为 `{sender}-to-{recipient}`)被中文短语替换,
**不符合 canonical 模式** `REPORT-{date}-{seq}-{sender}-to-{recipient}.md`,
对 fcop 库 `_TASK_FILENAME_RE` 解析器是"幽灵文件"。

但因属**老归档**(2026-04),P0/P1 不波及当前 sprint。

**建议处置**:Rule 5 "下一序号同前缀"修正——新落一条
`REPORT-{date}-001-PM-to-ADMIN.md` 引用此文,正文说明"修正自(中文名)";
**或者**因属老归档接受现状,在 `fcop/log/legacy-non-protocol/` 给它专门挪过去。

### P2-5 · 历史归档里出现老格式 role code `PM-01 / DEV-01 / ...-01`

**事实出处**:全库 sender/recipient 频次扫描:

```text
sender:     PM-01 : 14   DEV-01 : 1   (老命名)
recipient:  ADMIN-01 : 6  PM-01 : 2   OPS-01 : 4   QA-01 : 2   DEV-01 : 1
```

这些是 FCoP 早期 `init_project` 模板曾用过的 `*-01` 形式(2026-04 之前),
现在 `fcop.json.roles = ["PM","DEV","QA","OPS"]` 已不含 `-01`。Bridgeflow
当时已迁移到新格式,但**老 TASK/REPORT 文件名 + frontmatter 还保留**——
属合规的"历史快照",Rule 5 append-only 不应改。

**建议处置**:**无需处理**,留作历史证据。

### P2-6 · `fcop_protocol_version` 在 commentary 与 rules 之间的语义偏差(归属 FCoP 自己)

**事实出处**:`fcop-protocol.mdc` 第 4 节 "Project Mode & Identity" 写
`mode: team`,但实际 `fcop.json` 落盘值是 `mode: preset`(对应
`init_project(team=...)`)。Bridgeflow 用 `preset` **合规**(`src/fcop/models.py:760`
`Literal["solo","preset","custom"]`),但 commentary 用 `team` 作示意造成
**初次接触 FCoP 的 agent 易困惑**。

**归属**:这是 FCoP 自己的协议解释表述歧义,不是 Bridgeflow 的问题。
建议在 D:\FCoP 仓库下落 proposal:

```
.fcop/proposals/20260513-mode-name-clarification.md
```

或在 commentary 里加一句 "实际 `fcop.json` 字段值是 `preset` /
`custom` / `solo`;`team` 是讲解抽象类别"。

---

## Reciprocity / 互惠回执(Rule 6)状态

**事实出处**:当前 `fcop/tasks/` 5 条 + `fcop/reports/` 2 条:

| TASK | thread_key | status | 配对 REPORT |
|---|---|---|---|
| TASK-018 PM→DEV pc-pwa-sprint | v1-0-public-release-sprint | active | (无 — in-flight) |
| TASK-019 PM→OPS public-release | v1-0-public-release-sprint | (未读 body) | (无 — in-flight) |
| TASK-020 PM→QA rolling-regression | v1-0-public-release-sprint | (未读 body) | (无 — in-flight) |
| TASK-021 PM→DEV fcop-1.4.0-upgrade | v1-0-public-release-sprint | drafted-pending-admin-notify | **REPORT-021 DEV→PM ✓** |
| TASK-030 PM→OPS daily-archive-retry | (未读) | (未读 body) | **REPORT-030 OPS→PM ✓** |

**评估**:`status: active` 与 `drafted-pending-admin-notify` 表明 018/019/020
是"进行中",Rule 6 允许沉默-as-in-flight(只有 ≥7 天 + 无 status 变更才算
"沉默 = 违约")。今天是 2026-05-13,任务都是 2026-05-12 落的,**24 小时
窗口内**——属合规 in-flight。

---

## v1.0 / v1.1 新能力使用统计

- **REVIEW envelope**(Rule 9.1):1 条已落盘 ✓
- **decision = needs_human**(v1.1):1 条已用 ✓
- **human_approval 子结构**(v1.1):1 条已落盘,字段齐全
  (`approver, decision, approved_at, channel, comment`)✓
- **risk_level**(v1.1):在 TASK 中已用(TASK-021 `risk_level: high`,
  TASK-018 `risk_level: medium`)✓
- **layer**(v1.0 boundary):TASK frontmatter 写 `layer: dispatch`(不在
  schema 4 值枚举 `worker/governance/admin` 内 —— 这是 TASK 字段而非
  role 字段,可能是 Bridgeflow 自定义 layer,**不构成违规**,但与 v1.0
  schema 命名空间撞车,P2 改进项可考虑改字段名为 `task_layer`)

---

## 综合评分

| 项 | 评分 |
|---|---|
| 主干合规度(规则部署 + 命名 + frontmatter + 双语角色) | **A+** (≈95%) |
| Rule 5 append-only | **A+** (0 ghost prefix) |
| Rule 4 路由分布 | **A** (路由清晰) |
| v1.0 / v1.1 新能力实践 | **A** (已落盘) |
| Rule 7.5 工作区 | **C** (软约束违反,产物在根) |
| Git 卫生 | **C+** (P0-1 + P1-2 都关于 git) |
| 协议未定义边界(reviews / internal / tasks/_archive) | **B-** (自创合理但与协议有不一致) |

**总评:B+(≈85分),距离 Mode 1 ALL GREEN 还需修 1 P0 + 优先 P1.2 P1.1
两条;P1.3 P1.4 可分阶段;P2 全部建议留作改进 backlog。**

---

## 给 ADMIN 的执行建议(优先级排序)

```text
1. 立刻 (P0-1)        : git add fcop/reports/ + commit + push
2. 当天 (P1-2)        : 补 .gitignore 三行 + 改名两个尾空格目录
3. 当天 (P1-5)        : 在 D:\Bridgeflow 跑 deploy_protocol_rules(force=True)
4. 本周 (P1-1)        : 把 tasks/_archive/* 搬到 log/
5. 本周 (P1-3, P1-4)  : 制定 workspace/ 搬迁路线 + 整理 _patch_*.py
6. 改进 backlog (P2)  : reviews/ ADR 补章、HANDOVER 搬迁、internal/ README 等
```

执行任一 P0/P1 时**严格走 SOP v2 问题 7**:`git add` 显式路径,
`git status --short` 二次确认,严禁 `-A`。

---

## 出处声明(Rule 0.c)

- 所有路径都是绝对路径,可在 `D:\Bridgeflow\` 下原样验证
- 数值来源:`Get-ChildItem`(递归计数)+ `Select-String`(frontmatter)
  + `git status --short`(working tree)
- fcop 库 schema 引用:`D:\FCoP\src\fcop\models.py:760, 763`
- 协议规则引用:`D:\FCoP\.cursor\rules\fcop-rules.mdc` Rule 0-9
- 协议解释引用:`D:\FCoP\.cursor\rules\fcop-protocol.mdc`
- 跨项目身份:本报告由 FCoP 项目的 ME 出具,**未在 Bridgeflow 仓库写
  任何文件**(Rule 1 sub-agent identity 继承 + Rule 4 跨项目)
- 项目身份纠错:前序 `TASK-20260513-003` 走错项目(codeflow-3),
  本 TASK-004 supersedes 之 — 历史按 Rule 5 append-only 保留
