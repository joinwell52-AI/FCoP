---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-008
sender: ME
recipient: ADMIN
task_id: TASK-20260512-008
priority: P1
status: done
thread_key: adr-0033-trailing-slug-adoption
risk_level: low
created_at: "2026-05-12T23:42:00+08:00"
---

# REPORT · ADR-0033 sprint atomic commit 闭环

> 回执 `TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md`。
> ADMIN 决策(2026-05-12 23:33):排期 X · 收 ADR-0033 sprint metadata。

## TL;DR

**Commit #1 已落地。Commit #2(本 REPORT + archive 入历史)在 step 5 落,
hash 等 commit 完成后由 ADMIN 在 `git log` 直接查看。**

`git status` 在 sprint 全闭环后将只剩 ADR-0033 范围外的 11 件历史
untracked 噪音,**已列清单 + 处置建议**附在 §"历史噪音清单"小节。

## Commit #1 · ADR-0033 sprint 物理产物 ✅

- **hash**:`a669ea3`
- **subject**:`feat(filename): adopt trailing-slug grammar (ADR-0033 · fcop 1.6.0)`
- **stats**:11 files changed, 1442 insertions(+), 19 deletions(-)
- **branch**:`main`(本地)
- **push**:**未**推送 origin(Rule 7,需 ADMIN 二次确认)
- **tag**:**未**打 tag(同上)

### 含文件清单(11 件)

```
M  CHANGELOG.md
M  adr/README.md
A  adr/ADR-0033-trailing-slug-filename-adoption.md
M  mcp/src/fcop_mcp/_version.py
M  src/fcop/_version.py
M  src/fcop/core/filename.py
M  src/fcop/rules/_data/fcop-protocol.mdc
M  tests/test_fcop/test_core_filename.py
A  fcop/log/tasks/TASK-20260512-006-ADMIN-to-ME.md
A  fcop/reports/REPORT-20260512-007-ME-to-ADMIN-adr-0033-trailing-slug.md
A  fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md
```

### Commit message 风格核查 ✅

- 单行 subject + 空行 + body(参照仓库历史 `feat(<scope>): <subject>`)
- Body 含 protocol layer 版本对账、grammar 公式、code/tests/docs 变更
  清单、companion envelopes、刻意不含项 5 类、refs。
- 无 emoji(参照仓库历史风格)
- 无 `Co-authored-by` 等水印(参照仓库 git config + 项目惯例)

## Commit #2 · Rule 0.a.1 sprint 元数据收口(进行中)

本 REPORT 写完后:

1. `Move-Item fcop/tasks/TASK-008 → fcop/log/tasks/TASK-008`(archive)
2. `git add` 三件:
   - `D  fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md`
   - `A  fcop/log/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md`
   - `A  fcop/reports/REPORT-20260512-008-ME-to-ADMIN-adr-0033-sprint-commit.md`
3. `git commit -F` 落 commit #2:
   `chore(fcop): rule 0.a.1 closure for ADR-0033 sprint (TASK-008 archive + REPORT-008)`

> Rule 0.c 真话原则:本 REPORT 写下时,自身 commit #2 还在路上。
> 这不是矛盾——是 Rule 0.a.1 四步走必然出现的"报告写在归档前"时序,
> ADMIN 可在 `git log --oneline -5` 看到两个 commit 实际入历史。

## 与 TASK-008 计划的对照 · DoD 核对

| 验收项 | 状态 |
|---|---|
| Commit #1 落盘 + hash 记入 REPORT-008 | ✅ `a669ea3` |
| Commit #2 落盘 + hash 记入 REPORT-008 | ⏳(写完本 REPORT 即落,见上) |
| `git status` 两 commit 后只剩 ADR-0033 范围外的历史 untracked | ⏳(commit #2 后核验) |
| Commit message 严格遵守仓库历史风格,无 emoji | ✅ |
| 不打 tag v1.6.0 | ✅(未触发) |
| 不 push origin | ✅(未触发) |

## 历史噪音清单 · 排除在 ADR-0033 sprint 之外

`git status` 在 commit #1 之后显示如下 11 件 untracked,**全部不在 ADR-0033
范围内**,**不**混入本次 commit(白名单原则):

| 路径 | 性质 | ME 建议处置 |
|---|---|---|
| `.scratch/_msg_commit1_adr0033.txt` | 本次 commit message 草稿 | 加入 `.gitignore` 的 `.scratch/` 规则,或者按需删除 |
| `.scratch/`(目录) | 临时草稿目录 | 同上,`.gitignore` 候选 |
| `fcop_events.jsonl` | FCoP runtime 事件日志(根) | `.gitignore` 强候选 — 这是运行时副产品,不应入版本库 |
| `mcp/fcop_events.jsonl` | 同上(mcp 子包) | 同上 |
| `scripts/_commit_msg.txt` | 历史 commit message 草稿(1.5.0?) | 评估去留;若保留作历史参考,改名 + 提交;否则删除 |
| `scripts/_docs_commit_msg.txt` | 历史 commit message 草稿 | 同上 |
| `scripts/_v150_commit_msg.txt` | 历史 commit message 草稿(1.5.0) | 同上 |
| `scripts/_v151_commit_msg.txt` | 历史 commit message 草稿(1.5.1) | 同上 |
| `scripts/patch_protocol_version.py` | 历史一次性升级脚本 | 评估去留;一次性脚本归档到 `scripts/migrations/` 或删除 |
| `scripts/patch_rules_version.py` | 同上 | 同上 |
| `scripts/patch_tags.py` | 同上 | 同上 |
| `scripts/patch_write_guard.py` | 同上 | 同上 |

**建议另起 task**:
`TASK-{date}-{seq}-ADMIN-to-ME-cleanup-untracked-noise.md` —— 一次性
评估 + 处置这 11 件遗留物,改进 `.gitignore` + 决定一次性脚本去留。
**不在本 sprint 范围**,**不强求今晚做**。

## 后续 · Next

### ADR-0033 sprint 完全收口后(commit #2 落地后)

1. ✅ TASK-008 archive 入历史
2. ✅ REPORT-008 入历史
3. ⏳ 等 ADMIN 决定:
   - 是否打 `v1.6.0` tag(Rule 7,destructive op,需二次确认)
   - 是否 push origin
   - 是否触发 `redeploy_rules()`(把 host-neutral 四件套同步到 2.4.0)
   - 是否发 PyPI(`fcop@1.6.0` + `fcop-mcp@1.6.0`)
   - 是否启 codeflow 5/13 早会上报的 4-5 件 FCoP 上游 ISSUE 处理

### 仍挂账(详见 todo + drawer)

- snapshot-drift 独立 task(等 codeflow Mode 1 完全收尾 + 5/13 早通报后再起)

## 引用 · Citations

- TASK-006 task body(已 archive):`fcop/log/tasks/TASK-20260512-006-ADMIN-to-ME.md`
- TASK-008 task body(commit #1 含,即将 archive):`fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md`
- REPORT-007:`fcop/reports/REPORT-20260512-007-ME-to-ADMIN-adr-0033-trailing-slug.md`
- ADR-0033:`adr/ADR-0033-trailing-slug-filename-adoption.md`
- commit #1 hash:`a669ea3`(`git show a669ea3` 可见全部 11 件 diff)
- commit message file:`.scratch/_msg_commit1_adr0033.txt`(留作审计,见历史噪音清单建议处置)
- ADMIN 决策点(2026-05-12 23:33):"X"(排期 X · 收 ADR-0033 sprint metadata)

---

**status**:DONE(本 REPORT 自身落档完成)
**closes**:TASK-20260512-008(commit #2 后物理闭环)
**next**:archive TASK-008 + commit #2
