---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-014
sender: ME
recipient: ADMIN
status: in_progress
reporter: ME
priority: P0
thread_key: v2-0-2-double-pack-bump-and-mcp-registry-doc
session_id: sess-20260513-ME-014
related:
  - TASK-20260513-014
  - REPORT-20260513-013
---

# REPORT-014 第一段 · v2.0.2 文档冻结完成,等 ADMIN 三件手工

> **状态(本段)**:`in_progress` —— 这是 v2.0.2 release 的**第一段 commit**
> 的报告。
> 待 ADMIN 完成 PyPI 双包上传、Zenodo 拿新 DOI、`.\mcp-publisher.exe publish`
> 这三件手工后,我会在**第二段 commit** 写 REPORT-014 收尾段补完
> CITATION.cff + tag v2.0.2 + 三方 push,届时把本 report 的 `status` 改
> `done`(via 同前缀下一序号 REPORT,per Rule 5 append-only),并 archive
> TASK-014 + REPORT-014。

## 摘要 / Abstract

按 TASK-014 的两段式接力计划,**第一段 agent 独立完成的工作已经全部落地**:

- 双包 `_version.py` + `mcp/server.json` 都 bump 到 `2.0.2`
- `CHANGELOG.md` 写入 `[2.0.2] — 2026-05-13` 完整条目(合并 fcop-mcp@2.0.1 子集)
- 四份对外门面文件(`README.md` / `README.zh.md` / `docs/index.html` / `mcp/README.md`)
  全部同步 v2.0.2 + MCP registry 入驻段落
- 新文件 `fcop/shared/RULES-mcp-registry-release.md` 落档,把 ADMIN 给的
  "未来三步升级路径"从聊天窗口落进文件(Rule 0.a)
- ReadLints 零错;§G 六条扫描通过

**下一步**:等 ADMIN 三件手工(详见末段),完成后我接第二段 commit。

## 决策来源 / Decision provenance

ADMIN 在 TASK-014 上下文给出三个决策,verbatim:

| 决策 | 选项 | 实现 |
|---|---|---|
| 1 · 双包同步 | **A** | `src/fcop/_version.py` 2.0.0→2.0.2;`fcop` 库代码与 v2.0.0 完全一致(`git diff` 实测) |
| 2 · v2.0.1 处理 | **B · 合并进 [2.0.2]** | CHANGELOG 不为 2.0.1 单列条目;`[2.0.2]` 条目正文明确说明"fcop-mcp@2.0.1 是 PyPI 上永久存在的同日子集 patch,FCoP 仓库账本 release 是 2.0.2——一个超集" |
| 3 · Zenodo | **A · 触发** | 计划文件 TASK-014 已声明,本段 commit 不动 `CITATION.cff`,留待 ADMIN 拿到新 DOI 后第二段 commit 更新 |

加速令:`全部升级到 2.0.2 !!!` (ADMIN, 2026-05-13 23:04 +08:00)。

## 第一段交付物 / Deliverables (this commit)

### 类 A · 包源版本

- `src/fcop/_version.py`:`2.0.0` → `2.0.2`(双对齐已自检)
- `mcp/src/fcop_mcp/_version.py`:`2.0.1` → `2.0.2`

### 类 H · MCP registry server.json

- `mcp/server.json`:顶层 `version` + `packages[0].version` 双双 `2.0.1` → `2.0.2`

### 类 C · CHANGELOG

- `CHANGELOG.md` 顶部新增 `## [2.0.2] — 2026-05-13` 条目,含五小节:
  概述 / 版本号策略表 / feat(mcp-registry) / docs(rules) / docs(public) +
  docs(citation)(显式声明为"第二段 commit 写入"占位)+ 验收清单
  (分"第一段已实证"和"第二段待实证"两组,Rule 0.c 时序声明已写入)
- `[2.0.0]` 历史条目位置不变,保留在 L121

### 类 D · 双语 README

- `README.md` L37:badge 升 `release-2.0.2`;紧邻添加紫色 `MCP Registry: io.github.joinwell52-AI/fcop` badge
- `README.md` L210:版本表新增 `**2.0.2**` 首行,引用 MCP registry 入驻里程碑;`2.0.0` 历史行保留
- `README.md` L312:`Status & versioning · Current release` 段整段重写,首句强调入驻 MCP registry
- `README.zh.md` 同位置三处中文版同步

### 类 E · GitHub Pages

- `docs/index.html` L723-724:顶部 latest 链接中英双语都升 v2.0.2,副标题改"official MCP registry · uvx fcop-mcp"
- `docs/index.html` L781/786:v2.0 段落中英双语整体重写,把 MCP registry 入驻放在最显著位置;v2.0.0 两图对偶纪元降级为"早期版本"段

### 类 M · PyPI long_description(fcop-mcp)

- `mcp/README.md` L14:**新增 v2.0.2 章节**作为 PyPI 长描述首段,
  使用 🎯 emoji 突出 "Now in the official MCP registry"
- 关键考量:`mcp/README.md` 一旦随 fcop-mcp@2.0.2 上传 PyPI 即**永久不可改**,
  这次改动是把 MCP registry 入驻这个里程碑写进 PyPI 包页面的**唯一窗口**

### 类 K · 新规则文件

- **新建 `fcop/shared/RULES-mcp-registry-release.md`**:
  把 ADMIN 在 TASK-014 上下文给出的"未来三步升级路径"
  (改版本号 → `python -m build` + `twine upload` → `mcp-publisher publish`)
  落进文件,涵盖:适用范围 / 前提清单 / 三步详细命令 / lockstep 决策点 /
  失败回退矩阵 / 一条龙最后一里(`git push backup`)/ 变更日志。
- 这是对 Rule 0.a 的实践:聊天里的"未来怎么升级"如果不落文件,
  下一次升级时就会重新发明轮子。

### 类 I · FCoP 账本

- `fcop/tasks/TASK-20260513-014-ADMIN-to-ME-double-pack-bump-v2-0-2-and-mcp-registry-doc.md`(新)
- `fcop/reports/REPORT-20260513-014-ME-to-ADMIN.md`(本文件,第一段)

### 类 B · git tag(**第一段 commit 不打**)

按 TASK-014 接力计划,**v2.0.2 tag 在第二段 commit 时打**,这样 tag 才对
应"真实发版到 PyPI/MCP registry/Zenodo 后的完整快照",而不是文档冻结
的中间态。

## 自检结果 / Self-audit

### ReadLints

10 个新改动文件 → **0 错误,0 警告**。

### §G 6 条扫描

| # | 项 | 结果 |
|---|---|---|
| G.2 | 双 `_version.py` 对齐 | ✅ 都是 `2.0.2` |
| G.3 | CHANGELOG 顶部条目 | ✅ `[2.0.2] — 2026-05-13` 在第一位,`[2.0.0]` 退到第二位 |
| G.6 | `backup` remote 配置 | ✅ `https://github.com/joinwell52-AI/FCoP-backup.git` |
| bonus | `mcp/server.json` version 字段双对齐 | ✅ 两处都是 `2.0.2` |
| bonus | 残留 `2.0.0` / `2.0.1` 引用 | ✅ 全部是"历史对比 / 早期版本说明"合法用法,零非法残留 |

注:G.1 / G.4 / G.5 三条本次没改动相关文件(`fcop_rules_version` /
ADR `Proposed` 状态 / spec 文件),不在本次发版改动范围内,跳过。

## Rule 0.c 时序张力自报 / Rule 0.c temporal tension self-disclosure

**问题**:CHANGELOG `[2.0.2]` 条目里有几项内容**在第一段 commit 时尚未发生**,
但描述用了"已经做了"的现在时——这有可能被读者误以为是"全部完成"。

**已采取的对策**(三层声明,深度遵循 Rule 0.c):

1. **CHANGELOG 内显式声明**:`### docs(citation)` 节顶部加 Rule 0.c
   时序声明 blockquote,明确写"本节内容在第一段 commit 时尚未发生,
   待第二段 commit 写入"。`### 验收 / Acceptance` 节分两组:
   `[x] 第一段 commit 已实证` vs `[ ] 第二段 commit 待实证`。
2. **TASK-014 计划文件已声明**:见 TASK-014 § "接力流程"+§ "风险登记"
   `Rule 5 张力`条目,提前披露 CITATION.cff 必须等 ADMIN 拿 DOI 才能填,
   "这是已知中间态,不是 Rule 0.c 违规"。
3. **本 REPORT 第一段标题就写 `status: in_progress`** + 顶部 blockquote,
   明确告诉读者"REPORT 的 done 状态在第二段 commit 才发生"。

**未尝试用占位符填 CITATION.cff**:这是有意识的选择。占位符
(如 `doi: 10.5281/zenodo.XXXXXXXX`)如果 commit 进仓库,会让 GitHub
渲染 "Cite this repository" 时给出无效 DOI 链接,违反 Rule 0.c 比
"现在时描述"更严重。

## 等待 ADMIN 的三件手工 / Waiting on ADMIN

按 TASK-014 § "第二段 · ADMIN 介入(三件手工)" 列出的顺序:

### 手工 ① · PyPI 双包上传

```powershell
# fcop-mcp
cd mcp
python -m build
python -m twine upload --disable-progress-bar dist/fcop_mcp-2.0.2*

# fcop(双包 lockstep,本次代码零变更但版本号需要 PyPI 上有 2.0.2)
cd ..
python -m build
python -m twine upload --disable-progress-bar dist/fcop-2.0.2*
```

**红线**:上传前**最后一次**核对 `mcp/README.md` v2.0.2 章节,因为这段
会成为 fcop-mcp@2.0.2 PyPI 页面长描述,**永久不可改**。

### 手工 ② · Zenodo 触发新快照

ADMIN 通过 Zenodo `releases` integration(基于 GitHub release 自动触发,
或手工上传 source archive),拿到新 DOI 后**告诉 agent**(可在聊天里
报新 DOI 数字)。

### 手工 ③ · MCP registry publish

```powershell
.\mcp-publisher.exe publish
# 期望输出:
# ✓ Server io.github.joinwell52-AI/fcop version 2.0.2
#   registry.modelcontextprotocol.io
```

## Agent 第二段步骤 / Agent second-leg checklist(等 ADMIN 后)

1. 用 ADMIN 给的新 Zenodo DOI 更新 `CITATION.cff`(version + doi +
   date-released + identifiers + preferred-citation)
2. 同步更新 `README.md` / `README.zh.md` 的 "How to cite" 节 + BibTeX 块
3. 写 REPORT-15 收尾段(per Rule 5 append-only,**不**原地改本 REPORT),
   补 PyPI URL + Zenodo DOI + MCP registry URL 实证 + 第二段 commit SHA + 三方 SHA
4. **第二次 commit** `release: v2.0.2 — Zenodo DOI bump + final closure`
5. **打 tag** `v2.0.2` 指向第二次 commit
6. **三方 push**:`git push origin main` + `git push origin v2.0.2` +
   `git push backup main` + `git push backup --tags`
7. 验证三方 SHA(local / origin / backup)字节级一致 +
   `gh api .../tags/v2.0.2` 字节对齐
8. archive TASK-014 + REPORT-014 + REPORT-15 到 `fcop/log/`
9. 三方 push 归档后的最终状态

## 第一段验收 / Stage-1 acceptance

- [x] 双 `_version.py` = `2.0.2`
- [x] `mcp/server.json` 两处 version = `2.0.2`
- [x] `CHANGELOG.md` 加 `[2.0.2]` 条目,含 Rule 0.c 时序声明
- [x] README.md / README.zh.md / docs/index.html / mcp/README.md 同步
- [x] 新文件 `fcop/shared/RULES-mcp-registry-release.md` 落档
- [x] TASK-014 + REPORT-014 第一段落档
- [x] ReadLints 0 错;§G 关键扫描通过(G.2/G.3/G.6 + bonus)
- [x] 残留 v2.0.0 / v2.0.1 引用全部是合法历史对比,零非法残留
- [x] Rule 0.c 时序张力三层声明(CHANGELOG + TASK + REPORT)
- [ ] 第一段 commit + push origin + push backup main(本 commit 后做)

## See also

- `TASK-20260513-014-ADMIN-to-ME-double-pack-bump-v2-0-2-and-mcp-registry-doc.md`
- `fcop/shared/RULES-mcp-registry-release.md`(本版本新建)
- `fcop/shared/RULES-release-file-inventory.md`(12 类清单,本次发版的"地图")
- `fcop/shared/RULES-release-sync-checklist.md`(四硬约束)
- `docs/release-process.md`(SOP §C / §G / §阶段 4.5)
- `CHANGELOG.md` `[2.0.2]` 条目
