---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260512-008
sender: ADMIN
recipient: ME
priority: P1
thread_key: adr-0033-trailing-slug-adoption
risk_level: low
created_at: "2026-05-12T23:35:00+08:00"
---

# ADR-0033 sprint atomic commit · 物理收口

> 注:本 task 文件名自带 trailing slug
> `-adr-0033-sprint-commit`,这是 1.6.0 新文法的首次落盘自证。
> ADMIN 当前的 working tree 已含 ADR-0033 全部产物(`fcop` 1.6.0),
> 因此本 task 直接以新文法落档合规。

## 背景 · Why

ADR-0033 五个 Phase 已 ALL GREEN 闭环(详见 `REPORT-20260512-007`),
但**物理产物仍在 working tree、未 commit**。当前 `git status` 含:

```
M  CHANGELOG.md
M  adr/README.md
M  mcp/src/fcop_mcp/_version.py
M  src/fcop/_version.py
M  src/fcop/core/filename.py
M  src/fcop/rules/_data/fcop-protocol.mdc
M  tests/test_fcop/test_core_filename.py
?? adr/ADR-0033-trailing-slug-filename-adoption.md
?? fcop/log/tasks/TASK-20260512-006-ADMIN-to-ME.md           # 已 archive 的 task
?? fcop/reports/REPORT-20260512-007-ME-to-ADMIN-adr-0033-trailing-slug.md
?? fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md  # 本 task
```

ADMIN 决策(2026-05-12 23:33):**排期 X · 收 ADR-0033 sprint metadata
atomic commit**(类比 codeflow PM Phase D collection commit 范式)。

## 范围 · What

**双 atomic commit 闭环**(参照 codeflow 6 件 atomic commit 风格):

### Commit #1 · ADR-0033 sprint 物理产物

`feat(filename): adopt trailing-slug grammar (ADR-0033 · fcop 1.6.0)`

含:
- 7 件 M(代码 + 文档 + 版本号)
- 3 件 ??(`ADR-0033` 本体 + `TASK-006` 已归档形态 + `REPORT-007`)
- **+ 本 TASK-008**(commit 决策载体,与产物同 batch 入历史)

### Commit #2 · Rule 0.a.1 sprint 元数据收口

`chore(fcop): rule 0.a.1 closure for ADR-0033 sprint (TASK-008 archive + REPORT-008)`

含:
- `D fcop/tasks/TASK-20260512-008-...` (commit #1 后从 tasks/ 移走)
- `?? fcop/log/tasks/TASK-20260512-008-...` (archive 落点)
- `?? fcop/reports/REPORT-20260512-008-...` (本 task 的 REPORT)

## 实施步骤 · How(Rule 0.a.1 双层闭环)

| Step | 动作 | git 状态 |
|---|---|---|
| 1 | 写 TASK-008(本文件) | + 1 ?? |
| 2 | `git add <精确清单>` + commit #1 | tree clean except #2 后续产物 |
| 3 | 写 REPORT-008 | + 1 ?? |
| 4 | archive TASK-008 → log/tasks/ | + 1 D + 1 ?? |
| 5 | `git add <精确清单>` + commit #2 | tree clean |

## 精确文件清单 · Whitelist(Rule 7.5 精神 + codeflow PM #69 教训)

### Commit #1 范围(白名单)

```
CHANGELOG.md
adr/README.md
adr/ADR-0033-trailing-slug-filename-adoption.md
mcp/src/fcop_mcp/_version.py
src/fcop/_version.py
src/fcop/core/filename.py
src/fcop/rules/_data/fcop-protocol.mdc
tests/test_fcop/test_core_filename.py
fcop/log/tasks/TASK-20260512-006-ADMIN-to-ME.md
fcop/reports/REPORT-20260512-007-ME-to-ADMIN-adr-0033-trailing-slug.md
fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md
```

### Commit #1 排除(显式不加,留作未来评估)

| 路径 | 性质 | 处置 |
|---|---|---|
| `.scratch/` | 临时草稿目录 | **不加**,改进 `.gitignore` 候选 |
| `fcop_events.jsonl` | 运行时事件日志 | **不加**,改进 `.gitignore` 候选 |
| `mcp/fcop_events.jsonl` | 同上 | **不加**,改进 `.gitignore` 候选 |
| `scripts/_*_commit_msg.txt` | 历史 commit message 草稿 | **不加**,改进 `.gitignore` 候选 |
| `scripts/patch_*.py` | 历史升级 patch 脚本 | **不加**,待 ADMIN 评估去留 |

→ 这五类是历史 untracked 噪音,**不在 ADR-0033 范围内**,要单独评估,
不混进本 sprint commit。会在 commit #2 末尾或 REPORT-008 末尾向 ADMIN
列出"建议另起 task 处理"。

### Commit #2 范围(白名单)

```
fcop/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md  # 状态: deleted
fcop/log/tasks/TASK-20260512-008-ADMIN-to-ME-adr-0033-sprint-commit.md
fcop/reports/REPORT-20260512-008-ME-to-ADMIN-adr-0033-sprint-commit.md
```

## 验收标准 · DoD

- [ ] Commit #1 落盘 + commit hash 记入 REPORT-008
- [ ] Commit #2 落盘 + commit hash 记入 REPORT-008
- [ ] `git status` 在两 commit 之后:**只剩 ADR-0033 范围外的 5 类历史
      untracked**(可向 ADMIN 列出清单 + 处置建议)
- [ ] 两个 commit message 严格遵守仓库历史风格
      (`<type>(<scope>): <subject>`),无 emoji
- [ ] **不**打 tag(tag v1.6.0 推迟到 ADMIN 单独触发,因为 tag 会引发
      CI lockstep + 发布流程,Rule 7 范畴)
- [ ] **不** push origin(本次只本地落 commit,push 由 ADMIN 评估)

## 协议合规守则

- Rule 0.a.1:四步走完整执行(write_task → do → write_report → archive)
- Rule 0.b:本 task 由 ADMIN 提案、ME 执行,文件即代表两个视角
- Rule 0.c:commit message 内容必带出处(commit hash + 文件路径 + ADR-0033)
- Rule 5:TASK-006 + REPORT-007 + ADR-0033 已落,**不**回头改它们的内容
- Rule 7:**不**打 tag、**不** push origin、**不**发布 PyPI ——
  这些都需要 ADMIN 二次确认,本 sprint 不涉及
- Rule 7.5:不向项目根写业务代码(本次只是 commit,无新文件落根)

---

**status**:READY
**closes_on**:两个 commit hash 都进 REPORT-008
