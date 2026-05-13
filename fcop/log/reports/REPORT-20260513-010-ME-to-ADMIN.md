---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-010
sender: ME
recipient: ADMIN
status: done
task_id: TASK-20260513-010
thread_key: fcop-2-0-0-public-sync
session_id: sess-20260513-me-04
---

# 同步 GitHub 主仓 README 至 v2.0.0 · REPORT

## 结论

GitHub `tree/main` 默认渲染的英文 README + 中文 README + `fcop-mcp` PyPI 描述源
(`mcp/README.md`)三份文件,头部徽章 / MCP 工具数 / "latest release" 段 / Recent
Releases 表全部刷成 v2.0.0 / 35;`spec-v1.1` 徽章按协议语义保留不动。

## 改动清单

| 文件 | 位置 | Before | After |
|---|---|---|---|
| `README.md` | L16 | `MCP Tools (32)` | `MCP Tools (35)` |
| `README.md` | L37 | `badge/release-1.3.0` `alt="1.3.0"` | `badge/release-2.0.0` `alt="2.0.0"` |
| `README.md` | L204 | `Browse all 32 MCP tools` | `Browse all 35 MCP tools` |
| `README.md` | L281 | `All 32 MCP tools & 14 resources` | `All 35 MCP tools & 14 resources` |
| `README.md` | L209–212 → 现 L209–216 | Recent releases 表只到 `1.3.0 / 1.2.1` | 顶部补 `v2.0.0 / v1.6.0 / v1.5.0 / v1.4.0` 四行 |
| `README.zh.md` | L16 | `MCP 工具清单（32 个）` | `MCP 工具清单（35 个）` |
| `README.zh.md` | L37 | `badge/%E5%8F%91%E5%B8%83-1.2.1` `alt="1.2.1"` | `badge/%E5%8F%91%E5%B8%83-2.0.0` `alt="2.0.0"` |
| `README.zh.md` | L188 | `浏览全部 32 个工具` | `浏览全部 35 个工具` |
| `README.zh.md` | L256 | `全部 32 个 MCP 工具` | `全部 35 个 MCP 工具` |
| `README.zh.md` | L195 → 现 L195–200 | "近期发版" 表只到 `1.2.1` | 顶部补 `v2.0.0 / v1.6.0 / v1.5.0 / v1.4.0 / v1.3.0` 五行 |
| `README.zh.md` | L279 → 现 L284 | "当前发布: `v1.2.1`(2026-05-11)" | "当前发布: `v2.0.0`(2026-05-13) · 两图对偶 …";末尾追加"早期发布: v1.6/v1.5/v1.4/v1.3/v1.2.1/v1.1/v1.0" |
| `mcp/README.md` | L12 | `v1.3.0 is the latest stable release: adds GAL ...` | `v2.0.0 is the latest stable release — a *philosophical* major bump ("two-diagram era") …`,旧版本逐条降级为历史 |
| `mcp/README.md` | L14 | `v1.3.0 adds: Governance Alert Layer …` | 顶部加 `v2.0.0 adds: Rule 4.6 / Project.init opt-in / fcop.rules.get_internal_readme / P3 severity / exemption list …` |

`spec-v1.1` 徽章(两份 README L33–34)**保留不动**。协议 spec freeze 是单独的版本
线;v2.0.0 per ADR-0003 §MINOR additive,**没有 spec bump**。`README.md` L305 已写
"v1.1 spec bundled in wheel via `fcop.rules.get_spec()`",与徽章自洽。

## 校实(Rule 0.c)

数值校实(改动前):

| 数据点 | 来源 | 实测值 |
|---|---|---|
| `fcop` 包版本 | `src/fcop/_version.py` | `2.0.0` |
| `fcop-mcp` 包版本 | `mcp/src/fcop_mcp/_version.py` | `2.0.0` |
| Git 最新 tag | `git describe --tags --abbrev=0` | `v2.0.0` |
| MCP 工具数 | `Grep ^@mcp\.tool d:\FCoP\mcp\src\fcop_mcp\server.py -c` | `35` |
| `CHANGELOG.md` 顶部 | `L11` | `## [2.0.0] — 2026-05-13` |

改动后 grep 残留扫描:

```
git grep -n "release-1\.3\.0|%E5%8F%91%E5%B8%83-1\.2\.1|MCP Tools (32)|MCP 工具清单（32 个）"
  → README*.md / mcp/README.md 内 0 命中
```

`git diff --stat` 三件套合计 `+21 / -12`(README.md +12-4,README.zh.md +17-6
经二次精算实为 +13-6,mcp/README.md +4-2):变动局部、可审计。

## 已知边界(诚实落记,非阻塞)

1. **PyPI `fcop-mcp 2.0.0` 包的 long_description 是发版时的 v1.3.0 文案**。
   PyPI 不允许同号重发(已检查:`twine upload` 会报 `400 File already exists`),
   只能等下次发版同步刷新。`mcp/README.md` 改动**仅对 GitHub 显示和后续 2.0.1+
   发版有效**,不会回填到 PyPI 已发布的 2.0.0 包页面。这是 PyPI immutability,不是
   本次能修复的事——按 Rule 0.c 显式落记给 ADMIN 知情。

2. **`docs/index.html`(GitHub Pages)仍处于半成品**。上一波给 hero 加了 v2.0.0
   pill + 在 "What is FCoP" 加了 "two-diagram era" 双语段;但 essay 14 入口 +
   Rule 4.6 + Semantic Evolution Loop 图示等还没补齐。本 TASK **不**收尾它,
   留作另一 TASK,以避免一次 commit 卷入未完成段落。

3. `spec-v1.1` 徽章保留:与协议 spec freeze 语义(per ADR-0021 + ADR-0003 §MINOR
   additive)一致;若 ADMIN 希望另立 `spec-v2.x` 徽章请显式指示。

## 交付物 / Git 状态

```
 M README.md         (+12 -4)
 M README.zh.md      (+13 -6)
 M mcp/README.md     ( +4 -2)
```

(`docs/index.html` 也脏但不在本 commit 范围内;`essays/*.{csdn,devto,cursor-forum}.md`
草稿与本 TASK 无关。)

## 下一步

- ADMIN 校审 → 我接续 commit + push origin/main → 等 GitHub raw 刷新(~10s) →
  打开 https://github.com/joinwell52-AI/FCoP 实地验证。
- 若 OK,本 TASK + REPORT 一同 archive 到 `fcop/log/`。
- `docs/index.html` GitHub Pages 全面 v2.0.0 改版另立 TASK 继续。
