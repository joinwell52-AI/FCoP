---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-008
sender: ADMIN
recipient: ME
priority: P0
risk_level: high
thread_key: fcop-2.0.0-release-sprint
session_id: sess-20260513-ME-04
parent: TASK-20260513-006
related:
  - TASK-20260513-005
  - TASK-20260513-006
  - TASK-20260513-007
  - REPORT-20260513-006
  - REPORT-20260513-007
  - adr/ADR-0034-fcop-internal-external-document-convention.md
  - fcop/shared/SPRINT-fcop-2.0.0-release.md
created_at: "2026-05-13T13:35:00+08:00"
---

# fcop / fcop-mcp 2.0.0 哲学双图时代发版 sprint

## 1. 来源 / Provenance

ADMIN 2026-05-13T13:06+08:00 在聊天里给出明确决策:

> 我想全部完成,然后升级为 2.0.0

完整上下文:本会话先完成 ADR-0034 v2.1.1 + essay #13 中英版 +
FCOP-2.0.png 三件套交付(commit `523d81e` / `d2e0967`),REPORT-006
回执已落(commit `92980c7`),ADR-0034 Status 已 Proposed → Accepted
(commit `cbe6adb`)。ADMIN 13:06 这条指令触发 `fcop` 包发版 SOP
(`docs/release-process.md`)启动,版本目标 **fcop / fcop-mcp 2.0.0**。

## 2. 范围 / Scope

按 `fcop/shared/SPRINT-fcop-2.0.0-release.md` 规划,12 个 sub-changes
(C1-C12)+ 4 个 D 阶段 + 3 个 E 阶段。详见 SPRINT 文档 §2 表格。

## 3. risk_level: high 依据 / High-Risk Justification

按 Rule 9.5.1 + Rule 7,本 sprint 触及高危动作:

- **PyPI 发布**:`fcop` + `fcop-mcp` 2.0.0 推送到公网 PyPI,符合 Rule 7
  "发布到公网制品仓库"高危条款
- **主干分支 tag push**:`v2.0.0` tag 在 origin/main 上,符合 Rule 7
  "推送到主干分支"高危条款
- **MAJOR bump**:语义上是协议哲学时代的里程碑,生态层面影响所有下游
  用户

按 Rule 9.5.1,risk_level=high 应自动写出 `decision=needs_human` REVIEW
——本仓未装 fcop-mcp 工具,故由本任务文件 §4 显式声明 D2 守门点
等价 needs_human 语义,等 ADMIN 在聊天里二次确认。

## 4. Rule 7 守门点 / Rule 7 Gate

```
                                      ┌─────────────────────────┐
   C1-C12 finished + dry-run pass ───►│  ⚠️ STOP — Rule 7 gate  │
                                      │  ADMIN second confirm   │ ────► D3 tag push
                                      │  required for PyPI +    │
                                      │  main-branch tag push   │
                                      └─────────────────────────┘
```

**ADMIN 13:06 那条指令是 sprint 启动**(第一次 confirm),**不构成 D2
二次 confirm**。Rule 7 死规则要求 destruction-class 动作必须分两次
确认,这是 Rule 8 优先级里"协议规则不被单条 ADMIN 指令覆写"的典型
应用。

## 5. 验收标准 / Acceptance Criteria

### 5.1 C 阶段(代码 + 协议层)

- [ ] C1 · `fcop-rules.mdc` 加 Rule 4.6 + rules 2.4.0 → 3.0.0
- [ ] C2 · 第二张哲学图(FCoP Semantic Evolution Loop)入"七大核心概念"末尾,严格原文不改一字
- [ ] C3 · `fcop-protocol.mdc` 加 §Internal/External Document Convention commentary + protocol 2.4.0 → 3.0.0
- [ ] C4 · 同 mdc 加 §双图对偶 commentary
- [ ] C5 · `Project.init(deploy_internal_template: bool = False)` opt-in
- [ ] C6 · `INTERNAL-README.md` 模板新增
- [ ] C7 · 4 个 preset team `TEAM-OPERATING-RULES.md`(zh + en)加 §internal-only 声明语法
- [ ] C8 · `audit.py` 加 internal-only 检查(P3 non-blocking)
- [ ] C9 · `_version.py × 2` bump 1.6.0 → 2.0.0 + `AGENTS.md`/`CLAUDE.md`/`.cursor/rules/*.mdc` 镜像同步
- [ ] C10 · CHANGELOG.md 加 [2.0.0] 段(显式标"No API breaking despite MAJOR")
- [ ] C11 · 新 unit tests + 1061+ 旧 test 全过 + ruff/mypy/pip_audit 全清
- [ ] C12 · README + LETTER-TO-ADMIN(zh/en)版本 sync + ADR 索引补 ADR-0034 Accepted 行

### 5.2 D 阶段(release)

- [ ] D1 · dry-run + 本地全测 pass
- [ ] D2 · ⚠️ Rule 7 守门:agent 停手,等 ADMIN 二次确认
- [ ] D3 · ADMIN 二次确认后 tag v2.0.0 + push,触发 GitHub Actions 5/5 jobs
- [ ] D4 · 验证 PyPI 上 `fcop==2.0.0` + `fcop-mcp==2.0.0` + GitHub Release v2.0.0 含 4 assets

### 5.3 E 阶段(release 后)

- [ ] E1 · ADMIN 在本仓 + Bridgeflow + codeflow 调 `redeploy_rules()`(agent 不调,Rule 8 + ADR-0006)
- [ ] E2 · ADR-0034 Status: Accepted → Implemented + commit
- [ ] E3 · 写 REPORT-008(整个 sprint 闭环报告)+ archive TASK-008 + commit

## 6. 不在本 TASK 范围 / Out of Scope

- ✗ 候选 ADR-0035 / 0036 / 0037(下次 sprint)— 注:0037 候选实际被本 sprint 吸收(C2 已含)
- ✗ Bridgeflow / codeflow 仓内任何文件改动(Rule 1 跨项目边界)
- ✗ `docs/release-process.md` SOP 修订(已 v2,本 sprint 不动)
- ✗ workspace/ 路径或 Rule 7.5 的修订
- ✗ 任何不在 SPRINT §2 表格内的 sub-change

## 7. 回滚方案 / Rollback Plan

按 Rule 7"无回滚方案 = 不得执行":

- **C 阶段单 commit 回滚**:每个子 commit 独立可 `git revert`,不影响其它子 commit
- **D 阶段 tag 已 push 但 GitHub Actions 失败**:沿用 `docs/release-process.md` v2 §6 的 5-job 失败处理 SOP
- **PyPI 已发但需 yank**:`twine upload` 后只能 yank 不能删,2.0.0 yank 后 ADMIN 决定下次版本号(2.0.1 / 2.1.0 / 3.0.0,SemVer 不允许重用)
- **协议规则升级回滚**:rules 3.0.0 → 2.4.0 由 ADMIN 调 `redeploy_rules()` 完成,旧文件已自动归档到 `.fcop/migrations/<时间戳>/rules/`

## 8. References

- `fcop/shared/SPRINT-fcop-2.0.0-release.md`(本 sprint 详细规划 + 决策点)
- `adr/ADR-0034-fcop-internal-external-document-convention.md` §5.2(中期升级清单源材料)
- `docs/release-process.md` v2(release SOP)
- `fcop/log/tasks/TASK-20260512-009-ADMIN-to-ME-release-1-6-0-full-pipeline.md`(v1.6.0 sprint 经验,可对照)
