---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-002
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: release-sop-v2
session_id: sess-20260513-me-01
created_at: "2026-05-13T01:12:00+08:00"
related:
  - TASK-20260513-001   # SOP v2 沉淀主刀(已归档)
  - REPORT-20260513-001
---

# 把"`git add` 用显式路径,不用 `-A`"写进 `docs/release-process.md`(带依据)

## 背景 / Background

上一轮 `TASK-20260513-001` 沉淀 SOP v2 时,我自己在 `Step 4 闭环 commit` 阶
段用 `git add -A` 一把抓,意外把 19 份 untracked 残留(`.scratch/` 临时
msg、`fcop_events.jsonl` 运行时日志、`scripts/_*.txt` 历史 commit msg
等)一起塞进了 `commit d2ed13c`。ADMIN 决策 revert + redo,最终通过
`cc60186 (revert) → 979bcd2 (clean SOP) → dfe68e3 (artifacts + .gitignore
tighten)` 三个 commit 修复。

汇报里我提了一句"下次应在 SOP 里加这条规则",ADMIN 当即回:

> **写到文档中,有依据!!**

意思是:**口头沉淀不算数,必须落文件**——这正是 FCoP 的根原则(Rule 0.a)
本身。同时,有 `d2ed13c → cc60186 → 979bcd2 → dfe68e3` 这条完整的 main
历史作为依据,新规则不是凭空写的"教条",是从实际事故里抽出来的硬约束。

## 要做的事 / Deliverables

在 `docs/release-process.md` **两处**加新条款:

### 处 1 · 阶段 4 "发布后验证 + Rule 0.a.1 闭环" 的 `archive + commit` 子段

把现有 `git add -A && git commit -F ...` 命令**整段重写**,强调:

- ❌ 不要 `git add -A`(会抓所有 untracked 残留)
- ✅ 用显式路径列出所有要入库的文件
- ✅ 在 `git commit` 前先跑 `git status --short` 二次确认 staging 区只
  包含本意文件
- 引用 `d2ed13c → cc60186 → 979bcd2 → dfe68e3` 这串 commit 作为"反面
  教材 + 修复案例"的链接,说明依据

### 处 2 · "常见故障与回滚" 新增 `问题 7`

```
### 问题 7:commit 意外携带 untracked 残留(`git add -A` 后悔药)
```

- 现象、根因、立即修复(revert + redo)、长期防范(显式路径 + `.gitignore`
  补 `.scratch/` / `fcop_events.jsonl` / `scripts/_*.txt`)
- 直接引用本次 4-commit 修复链作为现实案例

## 验收 / Acceptance

- [ ] `docs/release-process.md` 阶段 4 闭环段命令重写,显式列路径
- [ ] `docs/release-process.md` 常见故障新增 "问题 7" 整段
- [ ] 两处都明确指向 `d2ed13c` / `cc60186` / `979bcd2` / `dfe68e3`
      作为依据(commit hash 短)
- [ ] 写 `REPORT-20260513-002-ME-to-ADMIN-add-git-add-explicit-paths-rule.md`
- [ ] **Dogfood**:本任务的 commit 阶段 **必须用显式路径** `git add`,
      不许再用 `-A`;commit 前 `git status --short` 确认 staging 区只
      包含本意 3 个文件(docs + TASK-002 + REPORT-002)
- [ ] push origin main 成功,main 历史保持单 commit 干净

## 风险 / Risk

risk_level: low。只改维护者文档,加约束、不动协议、不发版。
回滚:`git revert` 即可。
