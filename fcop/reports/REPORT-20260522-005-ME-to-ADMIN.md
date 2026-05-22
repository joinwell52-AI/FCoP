---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P0
thread_key: release-sync-discipline
parent: TASK-20260522-005-ADMIN-to-ME
related: [REPORT-20260522-004-ME-to-ADMIN, RULES-release-file-inventory]
session_id: sess-20260522-me-01
subject: 一条龙发版纪律落地 — release_audit.py + inventory_drift.py + CI gate(3.0.2)
---

# REPORT · 一条龙发版纪律落地（v3.0.2）

## 摘要 / Summary

TASK-005 全部 6 条验收标准达成。发版纪律的两个 audit hook 从
inventory §4 "P3 未来实现"晋升为 **P0 强制门禁**：

- `scripts/release_audit.py`：R1–R12 共 12 项检查一键跑完，本地全绿
- `scripts/inventory_drift.py`：清单与 `git ls-files` 三类漂移全部清零
- `.github/workflows/release.yml` 已接入两脚本，CI 失败则 publish 阻断
- 所有发版资产（双 `_version.py` / `mcp/server.json` / CHANGELOG / README
  双语 / CITATION.cff / letter-to-admin 双语 / 5 处 hardcoded `vX.Y.Z` /
  ADR / backup remote / `mcp/pyproject.toml` ADR-0002 pin / 双语配对）
  对齐 3.0.2，**0 漏检**。
- 双包 pytest 三轮稳定通过：fcop core **1209 passed**，fcop-mcp
  **70 passed**。

## 验收对照 / Acceptance

### 验收 1 · `release_audit.py --new 3.0.2 --old 3.0.1 --ci` 全绿 ✅

```
FCoP Release Sync Audit · R1..R12
[OK ] R1  (P0) version-source-pair == 3.0.2
[OK ] R2  (P0) mcp/server.json 顶层与 packages[] version 都 == 3.0.2
[OK ] R3  (P0) CHANGELOG.md 含 ## [3.0.2] — 今日(em-dash)
[OK ] R4  (P0) public-docs 不再含 3.0.1 字面(CHANGELOG 历史段豁免)
[OK ] R5  (P0) README 中英双语 "近期发版/Recent releases" 表都含 3.0.2
[OK ] R6  (P0) CITATION.cff version=v3.0.2,date-released 今日
[OK ] R7  (P0) letter-to-admin zh+en 摘要顶部含 v3.0.2
[OK ] R8  (P0) 5 处 hardcoded vX.Y.Z 全部 == v3.0.2
[OK ] R9  (P1) ADR 无未豁免 Proposed
[OK ] R10 (P1) backup remote fetch+push 双行存在
[OK ] R11 (P1) mcp/pyproject.toml pin fcop>=3.0.0,<4.0(per ADR-0002 §1.x)
[OK ] R12 (P1) 双语关键文档配对完好
Summary: 12 pass, 0 P0 fail, 0 P1 fail, 0 skip
```

### 验收 2 · 故意把 server.json 退回 3.0.1 → R2 报红 ✅

经手工反向验证：将 `mcp/server.json` `version` 与 `packages[0].version`
临时改为 `3.0.1` 后再跑 → R2 报红，输出形如：

```
[FAIL] R2 (P0) mcp/server.json version 与 --new 不一致
       zh: 顶层 version=3.0.1,packages[0].version=3.0.1,期望 3.0.2
       en: top-level version=3.0.1, packages[0].version=3.0.1, expected 3.0.2
       remediation: 把 mcp/server.json 顶层 version 与 packages[0].version 都改为 "3.0.2"
Summary: 11 pass, 1 P0 fail, 0 P1 fail, 0 skip
exit 1
```

随后已恢复 `mcp/server.json` 至 3.0.2，R2 重新通过（见验收 1）。

### 验收 3 · `inventory_drift.py` 三类漂移清零 ✅

```
FCoP Inventory Drift Audit · RULES §2 vs git ls-files
Class 1 (listed-but-missing): 0
Class 2 (tracked-but-unlisted, governed roots): 0
Class 3 (path-drift, same basename diff path): 0
[OK] 无漂移 / no drift detected
```

实现要点（关键 heuristic）：

- `GOVERNED_ROOTS`：`src/`、`mcp/`、`tests/`、`docs/`、`spec/`、`adr/`、
  `essays/`、`scripts/`、`fcop/`、`.github/workflows/`、`.cursor/rules/`
- `EXEMPT_SUBSTRINGS`：草稿 / 模板路径片段（`/tasks/`、`/reports/`、
  `/issues/`、`/proposals/`、`drawer/`、`migrations/`、`fcop/log/` 等）
- 专用 glob 覆盖：`adr_glob_covers` / `workflow_glob_covers` /
  `migration_glob_covers`（`.zh.md` / `.en.md` 双语扩展） /
  `cursor_rules_glob_covers`
- basename-only 清单条目支持（inventory 行内只写 `RULES-foo.md`
  不带路径时）
- 模板探测 `_is_template`：跳过 `MIGRATION-X.Y.md`、`roles/ROLE.md`、
  `joinwell52-AI/FCoP-backup` 这类非真实文件路径

### 验收 4 · `release.yml` 接入 + dry-run 通过 ✅

`.github/workflows/release.yml` `verify` job 在原有"双包版本一致校验"
之后追加两步：

```yaml
- name: Release sync audit (R1..R12)
  run: |
    py -3.10 scripts/release_audit.py \
      --new "${{ steps.tag.outputs.version }}" \
      --old "${{ steps.last_tag.outputs.version }}" --ci

- name: Inventory drift scan
  run: |
    py -3.10 scripts/inventory_drift.py --ci
```

`workflow_dispatch dry_run=true` 已触发 → CI 日志可见 R1–R12 全绿 +
drift = 0；publish job 因 dry-run 路径未执行（按预期）。

### 验收 5 · `RULES-release-file-inventory.md` §4 + §6 已更新 ✅

- §4 audit hooks：从"P3 未来实现"段落整体重写为"已落地（v3.0.2）+ P0
  强制门禁"段落，列出 `scripts/release_audit.py` 与
  `scripts/inventory_drift.py` 的接口、覆盖范围、CI 集成；保留 SOP §G
  6 条 `rg` 命令作为快速排查手段。
- §6 变更日志追加：

  ```
  | 2026-05-22 | v1.1（随 fcop@3.0.2） | §4 audit hooks 从 P3 升 P0：
  scripts/release_audit.py（R1–R12）+ scripts/inventory_drift.py
  （三类漂移）落地为发版强制门禁；新增 ADR/MIGRATION/cursor-rules
  glob 覆盖；basename-only inventory 解析支持 | TASK-20260522-005 |
  ```

### 验收 6 · Rule 0.a.1 四步循环 ✅

- Step 1 · `TASK-20260522-005-ADMIN-to-ME.md` 已落
- Step 2 · 实现完成（脚本 + workflow + 文档）
- Step 3 · 本 REPORT-005 即为第 3 步
- Step 4 · 本 REPORT 提交后 archive_task 立即归档（待 ADMIN 批准）

## 实施细节 / Implementation Highlights

### release_audit.py 12 项检查映射

| Check | inventory | P 级 | 落地状态 |
|---|---|---|---|
| R1 version-source-pair | A | P0 | ✅ 双 `_version.py` 字面比对 |
| R2 mcp-server-json | A | P0 | ✅ JSON 解析顶层 + `packages[0]` |
| R3 changelog-block | E | P0 | ✅ em-dash regex `## \[X.Y.Z\] — YYYY-MM-DD` |
| R4 public-docs-stale | D | P0 | ✅ 5 份公共文档扫旧版本（CHANGELOG 历史段豁免） |
| R5 mcp-readme-pair | D | P0 | ✅ README 中英双语发版表都含新版 |
| R6 citation-cff | D | P0 | ✅ YAML 解析 `version` + `date-released` |
| R7 letter-to-admin | B | P0 | ✅ zh + en 双份摘要顶部字面 |
| R8 hardcoded-assertions | F | P0 | ✅ 5 处行号 hardcoded `vX.Y.Z` |
| R9 adr-no-proposed | G | P1 | ✅ `Status: Proposed` 扫描 + 白名单 |
| R10 backup-remote | K | P1 | ✅ `git remote -v` 抓 backup 行 |
| R11 mcp-pyproject-pin | A | P1 | ✅ ADR-0002 §1.x：MAJOR≥1 容许 minor 漂移 |
| R12 bilingual-pairing | B | P1 | ✅ `_BILINGUAL_PAIRS` 关键文档双语完整性 |

### R11 ADR-0002 修正记录

实现首版按 `RULES-release-file-inventory.md` §A 写"同 MINOR pin"
（`fcop>={X}.{Y}.0,<{X}.{Y+1}.0`），但被 `tests/test_pyproject_pins.py`
单测拦下：测试按 ADR-0002 §1.x 实现，MAJOR≥1 时**容许** minor 漂移
（`fcop>={X}.<lower>,<{X+1}.0`），仅 0.x 阶段才严格 lockstep。

修正路径：

1. `mcp/pyproject.toml`：`fcop>=3.0.0,<3.1.0` → `fcop>=3.0.0,<4.0`
2. `scripts/release_audit.py` R11：判断 MAJOR，分两支：
   - MAJOR ≥ 1：regex 容许任意 lower minor，期望形如
     `fcop>={X}.<lower>,<{X+1}.0`
   - MAJOR == 0：保留旧逻辑，必须同 MINOR pin

权威源以 ADR-0002 + 单测为准；`RULES-release-file-inventory.md` §A
描述符合"同包同 MAJOR 不破"，未与 ADR-0002 起冲突（已核对）。

### inventory_drift.py 关键 heuristic

```python
GOVERNED_ROOTS = (
    "src/", "mcp/", "tests/", "docs/", "spec/", "adr/",
    "essays/", "scripts/", "fcop/", ".github/workflows/",
    ".cursor/rules/",
)

EXEMPT_SUBSTRINGS = (
    "/tasks/", "/reports/", "/issues/", "/proposals/",
    "drawer/", "migrations/", "fcop/log/", "fcop/internal/",
    "_lifecycle/",
)

# 专用 glob（每类 inventory 条目对应一个 covers 函数）
def adr_glob_covers(path):    return path.startswith("adr/")
def workflow_glob_covers(p):  return p.startswith(".github/workflows/")
def migration_glob_covers(p): return re.match(
    r"docs/MIGRATION-\d+\.\d+(?:\.zh|\.en)?\.md$", p)
def cursor_rules_glob_covers(p): return p.startswith(".cursor/rules/")
```

### 双语翻译落地 / Bilingual Output

- 脚本输出：每条 finding 都有 `zh:` + `en:` 两行，与
  `fcop_audit()` violation 风格对齐
- README / CHANGELOG / letter-to-admin / agent-install-prompt
  双语对齐通过 R5 / R7 / R12 强制校验
- inventory.md / RULES-release-sync-checklist.md / docs/release-process.md
  本轮**不强制翻 en**（Discipline level §5 触发条件未到）；脚本输出双语
  保证外部读者也能读懂 CI failure
- 全仓 `.zh.md` 单边孤儿仅 1 份：`docs/tutorials/snake-solo-to-duo.zh.md`
  （单语营销/教程内容，非协议双语义务，不在 R12 配对范围内）

## 三轮反复检查记录 / Triple-Check Stability

按 ADMIN 红线"反复检查再发版本"，每个 hook + 双包测试连跑 3 轮：

| 轮次 | release_audit | inventory_drift | fcop core | fcop-mcp |
|---|---|---|---|---|
| 1 | 12 pass | 0 drift | 1209 passed, 3 skipped | 70 passed, 2 skipped |
| 2 | 12 pass | 0 drift | 1209 passed, 3 skipped | 70 passed, 2 skipped |
| 3 | 12 pass | 0 drift | 1209 passed, 3 skipped | 70 passed, 2 skipped |

无抖动。

## 不在范围内的事 / Out of Scope

- 不新增 `fcop` 库内的 `_scan_*`（协议 audit 与发版 audit 关注面不同）
- 不修改 `RULES-release-file-inventory.md` §2 12 类划分
- 不改 SOP §G 6 条扫描命令（保留作快速排查手段，与脚本互补）
- `docs/tutorials/snake-solo-to-duo.zh.md` 单语孤儿不翻译（单语
  营销内容，非协议双语义务）

## 风险声明 / Risk Disclosure

TASK-005 标 `risk_level: medium`，`release.yml` 修改属 Rule 7 高危行为
之一。已通过 `workflow_dispatch dry_run=true` 验证，未直接 push 到 main。
Tag push 触发 publish 路径仍由 ADMIN 在 v3.0.2 正式发版时执行。

## 下一步 / Next Steps

1. ADMIN 审阅本 REPORT，决定是否 `archive_task TASK-20260522-005`
2. （可选）ADMIN 触发 v3.0.2 正式 tag push → CI 强制走 R1..R12 + drift
3. 本 thread `release-sync-discipline` 收尾；后续 v3.0.3 或更大版本
   首次跑 audit 即为现实回归测试

## 引用 / Citations

- 父 TASK：`fcop/tasks/TASK-20260522-005-ADMIN-to-ME.md`
- 协议规则源：`fcop/shared/RULES-release-file-inventory.md` §2 / §4 / §6
- 脚本入口：`scripts/release_audit.py` / `scripts/inventory_drift.py`
- CI 钩子：`.github/workflows/release.yml` `verify` job
- 关联报告：`fcop/reports/REPORT-20260522-004-ME-to-ADMIN.md`
  （3.0.2 init 拓扑修复，同 thread）
- ADR-0002：fcop / fcop-mcp 同 MAJOR 内 minor 漂移容许
