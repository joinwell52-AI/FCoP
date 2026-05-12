---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-002
sender: ME
recipient: ADMIN
status: done
task_id: TASK-20260513-002
thread_key: release-sop-v2
session_id: sess-20260513-me-01
reported_at: "2026-05-13T01:20:00+08:00"
related:
  - TASK-20260513-002
  - TASK-20260513-001
  - REPORT-20260513-001
---

# "`git add` 显式路径"硬约束已写入 SOP,带 4-commit 依据链

## TL;DR

- ✅ `docs/release-process.md` 三处修订完成:阶段 4 闭环段命令重写 +
  end-to-end 命令序列重写 + 新增 "常见故障 问题 7" 整段
- ✅ 新规则**带依据**:直接在 SOP 里引用 `d2ed13c → cc60186 → 979bcd2 →
  dfe68e3` 这条 4-commit 修复链作为反面教材现场
- ✅ SOP 中所有命令路径里的 `git add -A` 已清零(仅在问题 7 的反面教
  材引用里出现)
- ✅ lint 0 错误
- Dogfood 待执行:本任务的 commit 阶段必须**用显式路径** `git add`,
  不再用 `-A`(下一步 Step 4)

## 三处修订对照

### 处 1 · 阶段 4 闭环段(`docs/release-process.md` L260–280)

**之前**(2026-05-13 00:55 SOP v2 首版):

```markdown
- [ ] `Move-Item` ... (`archive_task` MCP 工具也可,但 v1.6.0 实战是手动
      `Move-Item` + `git add -A`,因为 git 会自动识别 rename)
- [ ] `git add -A && git commit -F .scratch\_release_*_closure_msg.txt`
- [ ] `git push origin main`
```

**现在**(本 commit 后):

```markdown
- [ ] `Move-Item` ... (`archive_task` MCP 工具也可)
- [ ] **`git add` 用显式路径,严禁 `-A`** —— 协议级硬约束,详见"常见故障
      问题 7"。把本意要入库的所有文件**逐个**列出来,显式路径下 git 同样
      能识别 rename(`R ` 行)、不会丢功能:
      ```powershell
      git add docs/release-process.md `
              fcop/log/tasks/TASK-<date>-<seq>-*.md `
              fcop/log/reports/REPORT-<date>-<seq>-*.md
      ```
- [ ] **commit 前必跑** `git status --short` 二次确认:staging 区...
- [ ] `git commit -F .scratch\_release_*_closure_msg.txt`
- [ ] `git push origin main`
```

### 处 2 · end-to-end 命令序列(`docs/release-process.md` L429–432)

**之前**:

```powershell
py -3.10 -c "...deploy_protocol_rules..."
git add -A
git commit -F .scratch\_release_1_7_0_predeploy_msg.txt
```

**现在**:

```powershell
py -3.10 -c "...deploy_protocol_rules..."
# !! 显式路径,不要 -A —— 详见"常见故障 问题 7"
git add .cursor/rules/fcop-rules.mdc .cursor/rules/fcop-protocol.mdc AGENTS.md CLAUDE.md
git status --short  # 二次确认 staging 只有上述四份
git commit -F .scratch\_release_1_7_0_predeploy_msg.txt
```

### 处 3 · 常见故障与回滚 · 新增问题 7(L353–395 约 43 行)

新插入完整一段 "**问题 7:commit 意外携带 untracked 残留(`git add -A`
后悔药)**",涵盖:

1. **现象** — 本意 commit 3 份文件,实际抓进 19 份残留
2. **根因** — `.gitignore` 永远不完整;`git add -A` 是地雷
3. **事故依据** — 把 `d2ed13c → cc60186 → 979bcd2 → dfe68e3` 4-commit
   修复链原样贴出来,标明 "**`main` 上是永久 audit trail——下次任何
   人想偷懒 `git add -A`,先去看一眼这串 hash**"
4. **立即修复**(A revert+redo / B follow-up cleanup / C accept-as-is
   三选一)+ "**不要 force push**" 提示
5. **长期防范** — 显式路径 + `git status --short` 二次确认 + `.gitignore`
   至少要覆盖 `/.scratch/` + `fcop_events.jsonl` + `scripts/_*.txt`
6. 末尾指回 Rule 7.5 / agent drawer 精神

## 验证证据

```text
=== file size + line count ===
372 lines, 22342 bytes  (上个版本是 429 行 / 18883 bytes; 净增 ~3.5 KB,
                          因为问题 7 整段 + 阶段 4 闭环段重写)

=== git add -A 在 SOP 命令路径中的残留 ===
0 处                     (Grep 0 hits)

=== d2ed13c / cc60186 / 979bcd2 / dfe68e3 引用 ===
L371-374 全 4 个都在     (问题 7 反面教材依据链)

=== 问题 7 整段插入 ===
L353 起,以 `### 问题 7:commit 意外携带...` 起头

=== 阶段 4 闭环段新增硬约束 ===
L264 "**`git add` 用显式路径,严禁 `-A`**"
L274 "**commit 前必跑** `git status --short`"

=== ReadLints ===
No linter errors found
```

## 验收清单 / Acceptance Checklist

- [x] `docs/release-process.md` 阶段 4 闭环段命令重写,显式列路径
- [x] `docs/release-process.md` 常见故障新增 "问题 7" 整段
- [x] 两处都明确指向 `d2ed13c` / `cc60186` / `979bcd2` / `dfe68e3` 作
      为依据(commit hash 短形式)
- [x] 写本份 `REPORT-20260513-002`(本文)
- [ ] **Dogfood 待执行**:Step 4 commit 阶段 用显式路径 `git add`,绝不
      `-A`;commit 前 `git status --short` 确认 staging 区只含本意 3 个
      文件(`docs/release-process.md` + `fcop/log/tasks/TASK-002` +
      `fcop/log/reports/REPORT-002`)
- [ ] push origin main 成功,main 历史保持单 commit 干净

## 风险评估事后回顾

实际风险:**low**(与 TASK 预估一致)。

- 只改一份维护者文档,加约束、不动协议、不发版
- `git revert` 即可回滚
- 本次"事后断言"是**完全真**的——比上次 REPORT-001 那次更严格,因为这
  次任务本身就是回应那次失误,我对自己的检查清单格外较真

## 下一步 / Next

```powershell
# Dogfood 阶段 — 用 SOP v2 + 问题 7 教的新规则做本任务的 commit:

Move-Item fcop\tasks\TASK-20260513-002-*.md fcop\log\tasks\
Move-Item fcop\reports\REPORT-20260513-002-*.md fcop\log\reports\

# !!! 显式路径,不要 -A !!!
git add docs/release-process.md `
        fcop/log/tasks/TASK-20260513-002-ADMIN-to-ME-add-git-add-explicit-paths-rule.md `
        fcop/log/reports/REPORT-20260513-002-ME-to-ADMIN-add-git-add-explicit-paths-rule.md

git status --short
# 必须只看到 3 行:
#   M  docs/release-process.md
#   A  fcop/log/tasks/TASK-20260513-002-*
#   A  fcop/log/reports/REPORT-20260513-002-*
# 任何 ??(untracked)行都该留着,本次不入库

git commit -F .scratch\_sop_v2_problem7_commit_msg.txt
git push origin main
```

提交后,SOP 中"`git add` 用显式路径"硬约束就有了**正式入库依据**,而本
任务的 commit 本身又是这条规则的"使用样例"——SOP + 实证形成闭环。
