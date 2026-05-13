---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-014
sender: ADMIN
recipient: ME
priority: P0
thread_key: v2-0-2-double-pack-bump-and-mcp-registry-doc
session_id: sess-20260513-ME-014
related:
  - TASK-20260513-013   # 一条龙发版+备份 SOP + inventory
  - TASK-20260513-012   # release-sync checklist permanent rule
  - TASK-20260513-010   # v2.0.0 README sync
  - TASK-20260513-011   # v2.0.0 docs/index.html sync
risk_level: medium
---

# 双包 lockstep 升级 v2.0.2 + MCP registry 入驻文档化

## ADMIN 原话 / ADMIN's verbatim

> **2026-05-13 22:50 +08:00 · 里程碑播报**
>
> "PyPI 2.0.1 上传成功!现在提交到官方注册表:注册成功!最后把这些变更
> commit 进 FCoP 仓库:全部完成!fcop-mcp 已正式入驻官方 MCP 注册表 ……
> Server io.github.joinwell52-AI/fcop version 2.0.1, registry.modelcontextprotocol.io"

> **2026-05-13 23:00 +08:00 · 补课指令**
>
> "现在又要补课,一个是完善文档,记录这个入驻 Anthropic / GitHub / Microsoft
> 联合背书的官方 MCP 注册表,从此 Claude Desktop / Cursor / PulseMCP 全栈
> 可达;另一个是补课,把另一半补上;我记得原来就有遗漏的,对吗?
> 如果有,全部升级到 2.0.2"

> **2026-05-13 23:04 +08:00 · 三决策拍板**
>
> "A;B,合并进 [2.0.2];A · 触发;Zenodo 学术快照很旧了"
>
> **2026-05-13 23:04 +08:00 · 加速令**
>
> "全部升级到 2.0.2 !!!"

## 决策矩阵 / Decision matrix(三个拍板)

| 决策 | 选项 | 含义 |
|---|---|---|
| **1 · 双包同步** | **A · `fcop` 也升 v2.0.2** | 代码零变更的 administrative bump,与 `fcop-mcp` lockstep,符合 ADR-0002 |
| **2 · v2.0.1 处理** | **B · 合并进 [2.0.2]** | CHANGELOG 只写 `[2.0.2]` 主条目,正文说明 fcop-mcp@2.0.1 是同日子集 patch |
| **3 · Zenodo** | **A · 触发新快照** | 旧快照 2026-04-29(commit 7f59395)太旧;拿新 DOI 后更新 CITATION.cff |

## 背景事实(Rule 0.c 实测,2026-05-13 22:50 数据)

1. **`fcop` 主库代码自 v2.0.0 后零改动**——`git diff --stat v2.0.0..HEAD -- src/fcop/ pyproject.toml` 输出为空。v2.0.2 是纯版本号 bump。
2. **`fcop-mcp` 自 v2.0.0 后改动 3 处文件**(35 行)——`mcp/README.md` 加 mcp-name 标记、`mcp/server.json` 新建、`mcp/src/fcop_mcp/_version.py` 2.0.0→2.0.1。
3. **CITATION.cff 当前状态**——`version: research-snapshot-2026-04-29`, `doi: 10.5281/zenodo.19886036`(commit `7f59395`)。指向 14 天前的研究快照。
4. **CHANGELOG.md 最顶**——`[2.0.0] — 2026-05-13`,无 v2.0.1 条目。
5. **MCP registry 现状**——`io.github.joinwell52-AI/fcop` 已在 `registry.modelcontextprotocol.io` 注册,版本 2.0.1,从此 Claude Desktop / Cursor / PulseMCP 全栈可达。

## 设计基调 / Design Posture

延续 TASK-013 立的"未来标准"红线 —— **如果 FCoP 成为标准,我们现在必须非常认真**。
v2.0.2 是 FCoP 第一次"双包 + MCP registry + Zenodo 三联动"发版,本任务交付物
将成为后续每一次同形态发版的模板。

## 12 类清单 · v2.0.2 改动项(对照 `RULES-release-file-inventory.md`)

| 类 | 文件 | 改动 | 谁做 |
|---|---|---|---|
| **A.1** | `src/fcop/_version.py` | `2.0.0` → `2.0.2` | agent |
| **A.2** | `mcp/src/fcop_mcp/_version.py` | `2.0.1` → `2.0.2` | agent |
| **A.3** | `mcp/server.json` 两处 version | `2.0.1` → `2.0.2` | agent |
| **B** | git tag `v2.0.2` | 新建,指向 release commit | agent(在第二次 commit 后)|
| **C** | `CHANGELOG.md` | 新增 `[2.0.2] — 2026-05-13` 条目(合并 v2.0.1)| agent |
| **D.1** | `README.md` | badge / 版本表 / 加 MCP registry 入驻段 | agent |
| **D.2** | `README.zh.md` | 中文版同步 | agent |
| **E** | `docs/index.html` | 中英双语版本号 + 加 MCP registry 入驻段 | agent |
| **F** | `CITATION.cff` | 用**新 Zenodo DOI** 更新 version + doi + description | agent(第二次 commit,**必须先有 ADMIN 给的新 DOI**)|
| **G** | `mcp/README.md` | 顶部加 v2.0.2 章节 + 强调 mcp-name 验证标记 | agent |
| **H** | `mcp/server.json` | (已在 A.3 处理) | — |
| **I** | FCoP 账本 | TASK-014 + REPORT-014 | agent |
| **J** | `docs/release-process.md` | (本次不大改;在 `RULES-mcp-registry-release.md` 新建)| agent |
| **K** | `fcop/shared/RULES-mcp-registry-release.md`(**新建**) | 把 ADMIN 三步升级路径落文件 | agent |
| **L** | Zenodo DOI | 上传 source archive 到 Zenodo 拿新 DOI | **ADMIN 手工** |
| **M** | PyPI 上传 `fcop-2.0.2` + `fcop-mcp-2.0.2` | `python -m build` + `twine upload` | **ADMIN 手工** |
| **N** | MCP registry publish | `.\mcp-publisher.exe publish` | **ADMIN 手工** |
| **O** | git push origin + push backup main + push backup tags | 一条龙红线 2 | agent(双方 commit 后)|

## 接力流程 / Relay Plan(分两段 commit)

**为什么分两段**:CITATION.cff 必须等 ADMIN 拿到新 Zenodo DOI 后才能写真实值。
不能在第一段 commit 里塞占位符,那违反 Rule 0.c。

### 第一段 · agent 独立完成(无需 ADMIN 介入)

1. 双 `_version.py` + `mcp/server.json` bump 到 2.0.2
2. `CHANGELOG.md` 加 `[2.0.2]` 条目(合并 v2.0.1 子集,写 MCP registry 入驻里程碑)
3. README.md / README.zh.md / docs/index.html 三处版本号 + MCP registry 段
4. `mcp/README.md` 顶部加 v2.0.2 章节
5. **新建** `fcop/shared/RULES-mcp-registry-release.md`(ADMIN 三步升级路径落文件)
6. ReadLints 0 错 + `docs/release-process.md §G` 6 条扫描通过
7. REPORT-014 写到"等 ADMIN PyPI/Zenodo/registry 三件手工"为止
8. **第一次 commit** `release: prepare v2.0.2 — docs + double-pack version bump`
9. **push origin** + **push backup main**(本次**不打 tag**,等 ADMIN 完成 PyPI 上传后再 tag)

### 第二段 · ADMIN 介入(三件手工)

10. **ADMIN**:`python -m build` 双包 + `twine upload` 双包到 PyPI
11. **ADMIN**:上传 source archive 到 Zenodo,**告诉 agent 新 DOI**
12. **ADMIN**:`.\mcp-publisher.exe publish` 注册 `fcop-mcp@2.0.2` 到 modelcontextprotocol.io

### 第三段 · agent 收尾

13. 用 ADMIN 给的新 Zenodo DOI 更新 `CITATION.cff`(version + doi + date-released + description)
14. **第二次 commit** `release: v2.0.2 — Zenodo DOI bump (XXX) + final closure`
15. **打 tag** `v2.0.2` 指向第二次 commit
16. **三方 push**:push origin + push backup main + push backup --tags
17. **验证**:三方 SHA 字节级一致 + `gh api .../tags/v2.0.2` 字节对齐
18. REPORT-014 收尾段补"双包 PyPI URL + Zenodo DOI + MCP registry URL"实证 + 三方 SHA
19. archive TASK-014 + REPORT-014

## 风险登记 / Risk register

- **Rule 5 张力**:CITATION.cff 必须等 ADMIN 拿 DOI 才能填,所以第一段 REPORT
  落档时 CITATION.cff 还指向旧 DOI(2026-04-29)。这是**已知中间态**,
  不是 Rule 0.c 违规——REPORT 第一段会显式标注"CITATION.cff 待第二段更新"。
- **PyPI 不可补发**:fcop-mcp@2.0.1 已永久存在于 PyPI,**不能撤回**。
  CHANGELOG 用"合并进 [2.0.2]"的写法是承认 2.0.1 真实存在但是同日子集 patch。
- **mcp-publisher 注册失败的回退**:如果 MCP registry publish 失败,2.0.2 仍是有效的
  PyPI 双包发版,只是注册表停留在 2.0.1。这种情况下 v2.0.2 仍可 closure,
  另起 hotfix 任务处理 registry 同步。
- **Zenodo 触发失败**:如果 Zenodo 拿不到新 DOI,CITATION.cff 保持指向旧快照,
  v2.0.2 降级为"软件双包发版,无新学术快照"——但这会让决策 3 落空,
  需要在 REPORT-014 显式声明"决策 3 推迟到 v2.0.3"。

## 验收标准 / Acceptance criteria

- [ ] `src/fcop/_version.py` 与 `mcp/src/fcop_mcp/_version.py` 都是 `2.0.2`
- [ ] `mcp/server.json` 两处 version 都是 `2.0.2`
- [ ] git tag `v2.0.2` 存在,指向第二次 release commit
- [ ] CHANGELOG.md 顶部有 `[2.0.2] — 2026-05-13` 完整条目(覆盖 fcop-mcp@2.0.1 子集)
- [ ] README.md badge 显示 v2.0.2,版本表加 v2.0.2 行,加 MCP registry 入驻段
- [ ] README.zh.md 中文版同步
- [ ] docs/index.html 中英双语版本号 v2.0.2 + MCP registry 段
- [ ] mcp/README.md 顶部 v2.0.2 章节存在
- [ ] CITATION.cff 已用新 Zenodo DOI 更新(必须真实 DOI,不接受占位符)
- [ ] 新文件 `fcop/shared/RULES-mcp-registry-release.md` 存在,内含 ADMIN 三步升级路径
- [ ] PyPI 双包均可见 `fcop@2.0.2` / `fcop-mcp@2.0.2`(ADMIN 实证)
- [ ] modelcontextprotocol.io 上 `io.github.joinwell52-AI/fcop` 版本 = 2.0.2(ADMIN 实证)
- [ ] Zenodo 新 DOI 可访问(ADMIN 实证)
- [ ] git tag v2.0.2 在 origin + backup 三方 SHA 字节级一致
- [ ] TASK-014 + REPORT-014 落 + archive

## See also

- `fcop/shared/RULES-release-file-inventory.md`(12 类清单)
- `fcop/shared/RULES-release-sync-checklist.md`(四硬约束)
- `docs/release-process.md`(SOP §阶段 4.5 一条龙最后一里)
- TASK-20260513-013(本任务的直接前序)
