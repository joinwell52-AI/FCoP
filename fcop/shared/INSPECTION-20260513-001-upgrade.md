---
protocol: fcop
version: 1
kind: inspection
inspection_id: INSPECTION-20260513-001
scope: upgrade
project: D:\FCoP
inspector: SYSTEM (fcop_audit 2.0.0)
inspected_at: "2026-05-13T06:35:11.854353+00:00"
fcop_version: 2.0.0
fcop_rules_version_local: 3.0.0
fcop_rules_version_package: 3.0.0
overall_status: needs_remediation
p0_violations: 0
p1_violations: 2
p2_violations: 1
p3_violations: 0
violation_file_count: 7
estimated_total_minutes: 21
---

# 体检报告 · FCoP (scope: upgrade)

## 摘要

- **状态**: 🟠 needs_remediation
- **违规分档**: P0 阻塞性 0 项 / P1 规范性 2 项 / P2 整洁性 1 项 / P3 建议 0 项
- **预估整改时长**: ~21 分钟

## P1 · 规范性违规（本 sprint 内修）

### P1-001 · Rule 4.5 (三层团队文档缺失)

**fcop/shared/ 缺少 4/10 件团队文档**

- **实证**:
  - `fcop/shared/roles/PM.md`
  - `fcop/shared/roles/DEV.md`
  - `fcop/shared/roles/QA.md`
  - `fcop/shared/roles/OPS.md`
- **影响**: 团队职责边界、协作流程、升级路径缺失，agent 无法查阅角色定义

- **整改命令**:
  ```
  deploy_role_templates(team="dev-team", force=True)
  ```
- **执行人**: ADMIN
- **预估**: 1 分钟
- **回滚**: `shared/ 原文件已备份（若 force=True 覆盖则需从包重新提取）`
- **Tier**: 1

### P1-002 · RULE_DOC_DRIFT (角色文档协议漂移)

**2 份已部署角色文档内容滞后已安装的 fcop 2.0.x 超过 1 个 minor 版本**

- **实证**:
  - `fcop\shared\roles\ME.en.md`
  - `fcop\shared\roles\ME.md`
- **影响**: Agent 读取的角色说明书缺少协议新功能描述（REVIEW envelope / risk_level / supersedes: 等），可能导致 Agent 不了解当前 FCoP 能力边界

- **整改命令**:
  ```
  deploy_role_templates(force=True)
  # unix: deploy_role_templates(force=True)
  ```
- **执行人**: PM
- **预估**: 5 分钟
- **回滚**: `git revert HEAD  # 如部署结果有问题`
- **Tier**: 2

## P2 · 整洁性违规（后续清理）

### P2-001 · Rule 5 (幽灵前缀文件)

**发现 1 个幽灵前缀文件**

- **实证**:
  - `fcop\reports\INSPECTION-20260512-v1.4.0-pre-release.md`
- **影响**: 草稿/交接/修订文件未清理，积累协议外文件，干扰审计

- **整改命令**:
  ```
  # DRAFT- → 确认后 git mv 为 TASK- 或删除
# HANDOFF- → 确认交接完成后 git mv 到 fcop/log/archive/
# *-v2.md → 确认合并后 git rm 旧版
  ```
- **执行人**: PM
- **预估**: 15 分钟
- **回滚**: `git revert HEAD`
- **Tier**: 3

---

## ▶ 执行块 · Execution Block

> 按 Tier 顺序执行。每步命令可直接复制；执行前请确认无未提交工作（`git status`）。

### Tier 1 · 立即（今日内，无前置，低风险）（预计 ~1 分钟）

#### 步骤 1 · 部署团队宪法文件
```
deploy_role_templates(team="dev-team", force=True)
```
**执行人**: ADMIN　|　**关联**: P1-001
**回滚**: `shared/ 原文件已备份（若 force=True 覆盖则需从包重新提取）`

### Tier 2 · 本 sprint（1~2 天，有前置依赖）（预计 ~5 分钟）

#### 步骤 1 · 重新部署角色模板，将本地角色文档同步到最新协议版本
```
deploy_role_templates(force=True)
```
```bash
# unix:
deploy_role_templates(force=True)
```
**执行人**: PM　|　**关联**: P1-002
**回滚**: `git revert HEAD  # 如部署结果有问题`

### Tier 3 · 后续清理（下一 sprint，低优先）（预计 ~15 分钟）

#### 步骤 1 · 确认内容后重命名或删除幽灵文件
```
# DRAFT- → 确认后 git mv 为 TASK- 或删除
# HANDOFF- → 确认交接完成后 git mv 到 fcop/log/archive/
# *-v2.md → 确认合并后 git rm 旧版
```
**执行人**: PM　|　**关联**: P2-001
**回滚**: `git revert HEAD`

## 复检建议

完成 Tier 1 后运行：

```
fcop_audit(scope="auto")
```

复检报告将落 `fcop/shared/INSPECTION-20260513-NNN-upgrade.md`，不覆盖本份（append-only）。
