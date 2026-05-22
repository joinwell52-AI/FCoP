---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260522-005
sender: ADMIN
recipient: ME
priority: P0
related: [TASK-20260522-004, REPORT-20260513-011, REPORT-20260513-013]
thread_key: release-sync-discipline
session_id: sess-20260522-me-01
risk_level: medium
---

# 把"一条龙发版"做成可执行清单 + 自动化扫描

## 背景 / Background

ADMIN 钦定原话(2026-05-22 13:49 +08:00):

> 发版一条龙里,把应该有的检查补起来;从协议到工具,到目录文件夹,
> 还要双语翻译,都不能错过;现在每次更新都是漏洞百出。

3.0.2 发版前现场实测:

- `mcp/server.json` version 没跟上 → 漏了
- `CITATION.cff` `date-released` 没跟上 → 漏了
- `README.md` / `README.zh.md` "近期发版"表 / "Current release" 段没跟上 → 漏了

`fcop/shared/RULES-release-file-inventory.md` 已经把 12 类文件清单写齐
(2026-05-13 v1.0 落档,§4 也写了 audit hook 名字)——但是**审计 hook
"未来实现 P3"四个字躺了 9 天没动**。每次发版靠脑子记 = 每次漏。

根因:**清单只在文档里,不在代码里**。`§G` 6 条 powershell 扫描命令需要
人手动复制到终端,人不复制 = 不跑 = 不报错 = 发漏版。

## 目标 / Goal

把 inventory §4 钦定的两个 audit hook 落地为**可一键执行的检查器**:

1. **`audit.inventory_drift()`**——扫 inventory §2 列出的 12 类文件,
   对照 `git ls-files` 找出"清单有 / 仓库无"、"仓库有 / 清单无"、
   "路径漂移"三类警告。
2. **`audit.release_sync_check(new_version, old_version)`**——把
   `docs/release-process.md` §G 的 6 条 `rg` / `python` 扫描翻译成
   Python,一次跑完,任何一项不通过立即 `exit 1`。

外加把这两个 hook **接进 `release.yml` 的 `verify` job**——CI 不通过
则 tag push 不会触发 publish job(`§阶段 3` 的 dry-run 已经有这个机制,
本次只是把扫描内容补上)。

## 必做项 / Requirements

### 1. 新增 `scripts/release_audit.py`(本仓发版 audit 入口)

**所在位置**:`scripts/release_audit.py`(本仓 utility,不打包进 wheel)。

**接口**:

```bash
# 扫一切,与目标版本号比对
py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1

# 只跑某几类
py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1 --only versions,changelog,public-docs

# CI 模式(任何 P0 不通过 exit 1)
py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1 --ci
```

**必做的扫描类别**(对应 inventory 12 类):

| ID | 扫什么 | 对应 inventory | P 级 |
|---|---|---|---|
| **R1** version-source-pair | `src/fcop/_version.py` 与 `mcp/src/fcop_mcp/_version.py` 完全一致且 == `--new` | A | P0 |
| **R2** mcp-server-json | `mcp/server.json` 顶层 `version` 与 `packages[].version` 都 == `--new` | A | P0 |
| **R3** changelog-block | `CHANGELOG.md` 含 `## [X.Y.Z] — YYYY-MM-DD`(em-dash,不是 hyphen),日期为今日 | E | P0 |
| **R4** public-docs-stale | `README.md` / `README.zh.md` / `mcp/README.md` / `docs/index.html` / `essays/README.md` 中**不再**含 `--old` 字面量(允许 CHANGELOG 历史段命中) | D | P0 |
| **R5** mcp-readme-pair | `README.md`(英)/ `README.zh.md`(中)的"近期发版"表 / "Recent releases" 表都含 `--new` 一行 | D | P0 |
| **R6** citation-cff | `CITATION.cff` 的 `version` == `v--new`,`date-released` == 今日 | D | P0 |
| **R7** letter-to-admin | `src/fcop/rules/_data/letter-to-admin.{zh,en}.md` 摘要块顶部含 `v--new`(zh + en 双份必齐) | B | P0 |
| **R8** hardcoded-assertions | inventory §F 列举的 5 处行号(server.py:779 + 4 处 test 断言)的 `vX.Y.Z` 字面量 == `v--new` | F | P0 |
| **R9** adr-no-proposed | `adr/ADR-*.md` 不含 `^Status: Proposed`(可由 `--allow-proposed adr-NNNN,adr-MMMM` 白名单豁免特定草案) | G | P1 |
| **R10** backup-remote | `git remote -v` 含 `^backup\s` 两行(fetch + push) | K | P1 |
| **R11** mcp-pyproject-pin | `mcp/pyproject.toml` 的 `dependencies` 含 `fcop>={MAJOR}.{MINOR}.0,<{MAJOR}.{MINOR+1}.0`(ADR-0002 同 MINOR pin)| A | P1 |
| **R12** bilingual-pairing | inventory §B `letter-to-admin` / `agent-install-prompt` / `internal-readme` / `fcop-spec-v*` 全部存在 zh + en 配对(任何一份单边 = P1) | B | P1 |

**输出格式**:与 `fcop_audit()` 的 INSPECTION 报告靠拢——`structured-findings`
+ `suggested-remediation`(命令行复制粘贴可执行)。

### 2. 新增 `scripts/inventory_drift.py`(对应 inventory §4 第一条 hook)

扫 `RULES-release-file-inventory.md` §2 每行 "**文件枚举**" 列举的精确路径,
对照 `git ls-files` 输出三段:

- **Clipboard-orphan**(清单有,仓库无):文件被删但清单忘改 → P1
- **Repo-orphan**(仓库有,但符合发版资产模式却不在清单):新增文件未纳入纪律 → P1 提示
- **Path-drift**(同名文件出现在不同路径):文件被重命名但清单没跟 → P0

**实现思路**:解析 inventory.md 的 markdown 列表,提取 backtick 包围的相对路径;
然后递归匹配 12 类各自的路径模式。第一版接受**正则模式**(`adr/ADR-*.md`、
`docs/MIGRATION-*.md`),不要求 100% 精确——**先有一道闸,再优化**。

### 3. 把这两个脚本接进 `release.yml` `verify` job

`release.yml` 的 `verify` job 在 tag push 时跑(以及 `workflow_dispatch dry_run=true`)。
在它现有的"双包版本一致校验"之后追加两步:

```yaml
- name: Release sync audit (G1-G12)
  run: |
    py -3.10 scripts/release_audit.py --new "${{ steps.tag.outputs.version }}" --old "${{ steps.last_tag.outputs.version }}" --ci

- name: Inventory drift scan
  run: |
    py -3.10 scripts/inventory_drift.py --ci
```

### 4. 把 inventory §4 "未来实现 P3" 改成 "v3.0.3 实现"

inventory.md 第 299-311 行从"待办"段挪到"已实现"段,加链接指向上述
两个脚本。同时更新 §6 变更日志:

```
| 2026-05-22 | v1.1 | §4 audit hook 落地为 scripts/release_audit.py 与 scripts/inventory_drift.py | TASK-20260522-005 |
```

### 5. 双语翻译义务 / Bilingual

ADMIN 红线 3 强调"双语翻译不能错过"。本次实现里:

- 脚本输出**中英文双语**(每条 finding 都有 `zh:` + `en:` 两行,与
  `fcop_audit()` violation 风格一致)。
- inventory.md / RULES-release-sync-checklist.md / docs/release-process.md
  本轮**先不**翻成英文(`Discipline level §5` 已说明 en 副版触发条件
  未到),但**脚本本身**输出双语,确保外部读者也能看懂 CI failure。

### 6. 不做的事 / Out of scope

- **不**新增 `fcop` 库内的 `_scan_*`(协议 audit 与发版 audit 关注面不同;
  混着写 = 把"包内审计"和"仓库管理"耦合)。`scripts/` 是发版仓 utility。
- **不**把 audit hook 嵌进 `release.yml` 之外的工作流(test-fcop / test-fcop-mcp
  保持单一职责)。
- **不**改 `RULES-release-file-inventory.md` §2 的 12 类划分——只补 §4 实现。

## 验收标准 / Acceptance Criteria

1. `py -3.10 scripts/release_audit.py --new 3.0.3 --old 3.0.2 --ci` 在
   3.0.2 已发版的现状下**全绿**(因为现状已对齐到 3.0.2)。
2. 故意把 `mcp/server.json` 的版本退回到 `3.0.1`,再跑 R2 → 必须**报红**
   并指出具体行号 + 修复命令。
3. `py -3.10 scripts/inventory_drift.py` 在当前仓库**至多 P1 警告**
   (允许新增 essay 未列入清单这种漂移),无 P0。
4. `release.yml` `workflow_dispatch dry_run=true` 触发跑过新两步
   (CI 日志可见 R1–R12 全绿 + drift = 0)。
5. `fcop/shared/RULES-release-file-inventory.md` §4 / §6 已更新。
6. 本 TASK 走完 Rule 0.a.1 四步循环:`task → 做 → REPORT-005 → archive`。

## 备注 / Notes

- **风险等级 medium**:本次涉及 `release.yml` 修改(Rule 7 高危行为之一),
  必须先用 `workflow_dispatch dry_run=true` 验证;不允许直接 push 到 main。
- 实现期间**不要顺手改其他文件**(Rule 0.a.1):任何超出本 TASK 范围的
  必要改动 → 停下,drop_suggestion 到 `.fcop/proposals/`,再起新 TASK。
- 若发现 §G 6 条扫描命令本身有 bug(例如 R3 em-dash 那一条 SOP 写的
  regex 不命中),应**先**在本 TASK 修脚本(脚本是新代码),**再**回头
  写一份 follow-up TASK 改 SOP §G,保持权威源更新链路清晰。

