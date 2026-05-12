---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260512-009
sender: ADMIN
recipient: ME
priority: P0
thread_key: release-1-6-0
risk_level: irreversible
created_at: "2026-05-12T23:47:00+08:00"
---

# Release fcop / fcop-mcp 1.6.0 · 一条龙发版(B 选项)

## ADMIN 决策来源

- 2026-05-12 23:33 · "X"(收 ADR-0033 sprint metadata)→ ✅ a669ea3 + a8ff07c
- 2026-05-12 23:44 · "B,全部做掉;按一条龙要求发版,发版前全面检查"

## 范围 · What

按 `docs/release-process.md` 一条龙走 1.6.0 正式版发布,含:

1. **本仓 P=E 修复**:`redeploy_rules()` 同步项目根四件套到 protocol 2.4.0
2. **发布前全面检查**:清单 A/B/C/D 全部跑过(任一失败立刻停)
3. **本地 build + smoke install**(`docs/release-process.md` §Phase 1)
4. **打 tag v1.6.0**(Rule 7,ADMIN 触发)
5. **`git push origin main + v1.6.0`**(Rule 7,触发 GitHub Actions `release.yml`)
6. **Actions 自动化**:verify → build → publish-fcop → publish-fcop-mcp → github-release
7. **发布后验证**:真 PyPI 装新环境冒烟

## Rule 7 / Rule 9.5.1 风险标记

本任务 `risk_level: irreversible` —— **PyPI 不允许同版本号覆盖**(发布即永久占坑)。
回滚方案 = `twine yank` 警告标记(不删除,只是标红 + 立刻 bump 1.6.1 重发)。

按 Rule 9.5.1 / ADR-0024,`irreversible` 写任务后**应自动写 REVIEW
`decision=needs_human`**——本任务由 ADMIN 显式拍板(2026-05-12 23:44
"B,全部做掉;按一条龙要求发版"),**人工审批前置满足**,等价于
`mark_human_approved`。无需再写 REVIEW 走 needs_human 流程。

## Rule 0.a.1 子步骤拆分

| Step | 动作 | Rule | 谁触发 |
|---|---|---|---|
| 1 | 落本 TASK-009 | 0.a.1 第 1 步 | ME |
| 2 | 检查清单 A · 代码层 | 7 前置 | ME(本地) |
| 3 | 检查清单 B · 测试/lint/mypy/snapshots | 7 前置 | ME(本地) |
| 4 | 检查清单 C · CHANGELOG/ADR/README | 7 前置 | ME(本地) |
| 5 | 检查清单 D · Git 状态 | 7 前置 | ME(本地) |
| 6 | 本地 build + smoke install | 7 前置 | ME(本地) |
| 7 | 汇总检查报告 → 等 ADMIN 拍续发 | — | ME 汇报 → ADMIN 拍 |
| 8a | `redeploy_rules()` 修本仓 P=E | 8 + ADR-0006 | **ADMIN 触发(MCP 工具)** |
| 8b | commit P=E 修复产物(如有 diff) | 0.a.1 | ME(本地) |
| 9 | `git tag -a v1.6.0 -m "Release 1.6.0"` | 7 | **ADMIN 触发** |
| 10 | `git push origin main v1.6.0` | 7 | **ADMIN 触发**(触发 Actions) |
| 11 | 等 Actions 跑完 verify→build→publish→release | — | GitHub Actions |
| 12 | 真 PyPI smoke install 验证 | — | ME(本地) |
| 13 | 写 REPORT-009 + archive TASK-009 | 0.a.1 闭环 | ME |

## 已知风险点(发版前必须澄清)

### R1 · test_tool_surface fcop_audit snapshot 漂移

**预先存在**问题(详见 `.fcop/drawer/ME/pending-snapshot-drift.md`)。
ADMIN 之前决定"等 codeflow Mode 1 收尾后再起独立 task"。

但**发版前检查清单 B 要求 `tests/test_fcop_mcp` 全绿**——这个漂移
会让 B 失败,**直接阻塞发版**。

ME 推荐处置:**先 regenerate snapshot 把漂移修复**——这是 1.6.0 发版
的**必要修复**(否则 CI verify 阶段就会挂)。修复方式取决于漂移性质:

- 若 snapshot 内容是 fcop_audit 工具签名的合法演进 → 重新生成 snapshot
- 若 snapshot 是 fcop_audit 代码 bug 引起的 → 改代码恢复

需在 Step 3 检查时**实测确认**漂移性质,然后向 ADMIN 报告。

### R2 · 11 件历史 untracked 噪音

REPORT-008 已列。**不在发版范围**,**不阻塞**(`git status` 在
Phase 1 build 时会忽略这些 untracked,Actions verify 也不查 working
tree untracked)。

### R3 · `fcop_rules_version` vs `fcop_protocol_version` 现状

- wheel 内 `src/fcop/rules/_data/fcop-rules.mdc` `fcop_rules_version: 2.4.0`
  (与 ADR-0033 同期到位,可能是早先 ADR 已升)
- wheel 内 `src/fcop/rules/_data/fcop-protocol.mdc` `fcop_protocol_version: 2.4.0`
  (本次 ADR-0033 升)
- 项目根 `.cursor/rules/fcop-protocol.mdc` `fcop_protocol_version: 2.3.0` ← 漂移
- 项目根 `.cursor/rules/fcop-rules.mdc` `fcop_rules_version: 2.4.0`

需 Step 8a `redeploy_rules()` 把项目根 protocol.mdc 同步到 2.4.0。

## 验收 · DoD

- [ ] 检查清单 A/B/C/D 全绿(任一失败暂停)
- [ ] 本地 build 成功 + smoke install 通过
- [ ] ADMIN 触发 `redeploy_rules()` 后本仓 P=E 一致(`.cursor/rules/` 全 2.4.0)
- [ ] GitHub Actions verify→build→publish-fcop→publish-fcop-mcp→github-release 全绿
- [ ] PyPI 上 `fcop@1.6.0` + `fcop-mcp@1.6.0` 可见 + 可装
- [ ] 真 PyPI 新环境冒烟:`import fcop, fcop_mcp; print(version)` = 1.6.0
- [ ] `fcop-mcp --help` 输出正常
- [ ] REPORT-009 落 + archive 闭环

## 协议合规守则

- Rule 7:tag / push / publish 三步 **全部由 ADMIN 触发**,ME 不自决
- Rule 8 + ADR-0006:`redeploy_rules()` ADMIN 触发
- Rule 9.5.1:irreversible 风险,人工审批前置已满足
- Rule 0.a.1:四步走 + Step 13 闭环
- Rule 0.c:任一检查失败 = 立刻报告 ADMIN,不掩盖

---

**status**:IN_PROGRESS(Step 2 开始)
**closes_on**:Step 13 完成 + REPORT-009 含 PyPI 真实可装确证
