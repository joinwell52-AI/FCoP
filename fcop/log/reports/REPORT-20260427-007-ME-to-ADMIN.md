---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260427-007
sender: ME
recipient: ADMIN
related_task: TASK-20260427-006
related_issues: [ISSUE-20260427-007]
session_id: sess-20260427-me-072
---

# 0.7.2 元数据 hotfix done — 同类 bug 第三次也是最后一次

## 完成清单（按 TASK-006 验收逐条核）

### A. 全表面元数据扫描 + 修复

- [x] `src/fcop/_version.py` `0.7.1` → `0.7.2` ✓
- [x] `mcp/src/fcop_mcp/_version.py` `0.7.1` → `0.7.2` ✓
- [x] `pyproject.toml` 根 — version 走 `dynamic` 从 `_version.py` 读，
  自动跟随，无需独立改 ✓
- [x] `mcp/pyproject.toml` 同上（dynamic version）✓
- [x] `mcp/pyproject.toml` description 仍含 "fcop 0.7.x" ✓
- [x] `mcp/pyproject.toml` dependencies `fcop>=0.7,<0.8` ✓（0.7.1
  已修，本次复查保持）
- [x] **`fcop-rules.mdc` frontmatter `1.7.0` → `1.8.0`**（核心 bug）✓
- [x] `fcop-protocol.mdc` `1.6.0` 保持 ✓
- [x] redeploy 同步：`.cursor/rules/{fcop-rules,fcop-protocol}.mdc` +
  `AGENTS.md` + `CLAUDE.md`，4 份旧版自动归档到
  `.fcop/migrations/20260427T203033/rules/` ✓
- [x] README.md / README.zh.md "Recent releases" 表 — 之前停在 0.6.5，
  这次补齐 `0.7.0 / 0.7.1 / 0.7.2` 三行 ✓
- [x] `mcp/README.md` "0.6.x" 化石（line 12 / 158 / 200 / 202）刷成
  "0.6.x 或 0.7.x" + Stability 段刷成 (0.7.x) ✓

### B. 自动化守门（防同类 bug）

- [x] 新建 `tests/test_fcop/test_rules_metadata_consistency.py`，
  3 个测试：
  - `test_fcop_rules_frontmatter_matches_body_changelog`：
    frontmatter `fcop_rules_version` 必等 body 最高
    `**X.Y.Z changes**` ✓
  - `test_fcop_protocol_frontmatter_matches_body_changelog`：
    frontmatter `fcop_protocol_version` 必等 body 最高
    `- **vX.Y** (date)` ✓
  - `test_no_stale_rules_version_anywhere_in_data`：双文件同时
    核（belt-and-braces）✓
- [x] `tests/test_fcop/test_pyproject_pins.py`（0.7.1 已建）复查覆盖
  fcop ↔ fcop-mcp minor lockstep + dep pin lockstep ✓
- [x] `pytest -q`：**620 passed** in 7.90s ✓
- [x] `ruff check src/ mcp/src/ tests/`：All checks passed ✓

### C. 协议账本

- [x] 立 `ISSUE-20260427-007`：rules.mdc frontmatter 跟 body 脱节，
  根因列表归类为"多行编辑漏一处"同 ISSUE-006 一类
- [x] `redeploy_rules` 已落 4 文件，1.8.0 行为 + 1.8.0 元数据双方
  完全一致（`fcop_report()` `项目本地 1.8.0 | 包内 1.8.0 ✓`）
- [x] 本 REPORT 写完即 archive TASK-006；ISSUE-007 同步 closed

### D. 发版

- [x] `CHANGELOG.md` `[0.7.2]` 段：含完整修复+新守门测试说明 +
  "no yank" 决策延续
- [x] `docs/releases/0.7.2.md`：含 third-strike post-mortem +
  "every two-copy version pair has a regression test" 表 +
  PEP 592 "no yank" 决策延续
- [ ] build × 2、twine check × 2、upload PyPI（待执行）
- [ ] `uvx --refresh fcop-mcp@0.7.2` 干净缓存冒烟（待执行）
- [ ] git commit + tag v0.7.2 + push + `gh release create`（待执行）
- [x] 0.7.1 不 yank（同 0.7.0 决策；自动覆盖；`uvx --refresh` /
  `pip install -U` 拿 0.7.2）

## Dogfood 现场（修复后）

```
=== FCoP UNBOUND 报告 ===
项目 / project: D:\FCoP  (来源: session:set_project_dir)
[版本 / Versions]
  fcop-mcp:  0.7.2
  fcop:      0.7.2
  rules:     项目本地 1.8.0 | 包内 1.8.0 ✓
  protocol:  项目本地 1.6.0 | 包内 1.6.0 ✓
```

修复前：`rules: ... | 包内 1.7.0`（错）
修复后：`rules: 项目本地 1.8.0 | 包内 1.8.0 ✓`

`audit_drift()` 仍报告 15 份 working-tree drift——这是本次发版还没
commit 的源码改动（_version.py / _data/*.mdc / README / CHANGELOG /
docs/releases/0.7.2.md / 本份 REPORT 自身），按 Rule 0.a.1 都关联到
TASK-006，commit 后 drift 归零。

## 已知留白（不在本 patch 范围）

1. `audit_drift()` 把 `ADMIN`-via-`ME` 转录模式仍判为
   `session_id ↔ role conflict`（REPORT-006 dogfood 提出）。需要
   ADMIN/SYSTEM 豁免清单——属于行为变更，0.7.2 是 metadata-only
   patch，不动 audit 语义。延后单独 issue 提。
2. `docs/upgrade-fcop-mcp.md` / `docs/release-process.md` 仍 0.6.x
   叙述。RELEASE-CHECKLIST.md 是新权威。延后单独 docs patch。
3. 上述两条已在 `docs/releases/0.7.2.md` "intentionally not in"
   段记录，未来 0.7.3 / 0.8.0 选一个吸收。

## 红线已守

- "实质对、元数据错"二度发生 → **不再可能不被测试发现**：
  - `test_pyproject_pins`（已有，防 ISSUE-006 类）
  - `test_rules_metadata_consistency`（新增 3 道，防 ISSUE-007 类）
- 任何"两份同号字段"对齐都已挂回归测试，写在 `0.7.2.md` 的"every
  two-copy pair"表里——下次再加新对齐点时，照此扩。

`fcop_report()` 不再说谎；`rules: ... | 包内 1.8.0 ✓` 双栏一致。
ISSUE-007 closed；TASK-006 ready for archive。
