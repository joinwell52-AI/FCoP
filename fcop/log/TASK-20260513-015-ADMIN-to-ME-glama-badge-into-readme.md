---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-015
sender: ADMIN
recipient: ME
priority: P2
thread_key: v2-0-2-glama-badge
session_id: sess-20260513-ME-015
related:
  - TASK-20260513-014   # 双包 lockstep 升级 v2.0.2 + MCP registry 入驻文档化(主线 stage-1)
risk_level: low
---

# Glama AI 收录 badge 入双语 README(stage-1.5)

## ADMIN 原话 / ADMIN's verbatim

> **2026-05-13 23:25 +08:00 · 里程碑播报**
>
> "今晚总结:官方 MCP 注册表 ✅ + Glama 收录 ✅ + 4 个 PR ✅;
> FCoP 的 MCP 服务器已经上了 Glama.ai 的目录了!这是个很好的信号。
> Glama.ai 是目前最主要的 MCP Server 聚合目录,上了这个目录意味着:
> fcop-mcp 已被公开收录,任何人都可以搜到 / 页面内容展示了 FCoP 的
> 完整架构层级图、核心理念('tasks over folders')、以及涌现故事 /
> badge 可以直接贴到 GitHub README,增加可信度和曝光。
> 你现在可以把这个 badge 加到 FCoP 和 CodeFlow 两个仓库的 README 里。"

ADMIN 提供的 badge markdown:

```md
[![FCoP MCP server](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/badges/card.svg)](https://glama.ai/mcp/servers/joinwell52-AI/FCoP)
```

## 范围 / Scope

本任务**只覆盖 FCoP 仓库**(本工作区)。CodeFlow 仓库是另一个项目,不归本会话/本角色管。

## 事实核验 / Reality check(Rule 0.c)

执行前 WebFetch `https://glama.ai/mcp/servers/joinwell52-AI/FCoP`,确认:

1. 页面真实可达(HTTP 200),返回 33.7 KB / 528 行内容。
2. 页面正文是 Glama AI 抓取的 `mcp/README.md`(PyPI long_description 同步源),
   包含 FCoP 完整架构层级图、"tasks over folders" 核心理念、essay 14 链接、
   ADR-0029 / ADR-0021 链接等。
3. 因此"Glama 已收录 fcop-mcp"是**经验证的事实**,可落盘。

## 放置决策 / Placement decision

### 改动的 / What changes

| 文件 | 改动 | 理由 |
|---|---|---|
| `README.md` | 在 MCP Registry badge 之后 / Zenodo DOI 之前插入 Glama badge(HTML 形态) | ADMIN 明确指派 + 与 MCP 生态收录类 badge 聚合 |
| `README.zh.md` | 同上,alt 文案改中文 | 中英双语项目,README 一律双语同步(已成惯例) |

### 不动的 / What stays untouched

| 文件 | 不动理由 |
|---|---|
| `CHANGELOG.md` | v2.0.2 段已 commit + push 到 origin / backup(stage-1 d79d438),不回填(append-only 精神) |
| `docs/index.html` | ADMIN 指派范围只有 README;不擅自扩张 |
| `mcp/README.md`(PyPI long_description) | 加进去会形成"Glama 抓我的描述 → 我的描述说我在 Glama"自指;且只有 fcop-mcp@2.0.2 上传后才生效。留 stage-2 决定 |
| 其他文档 | 同上 — 本轮仅落 ADMIN 字面要求的 README 改动 |

## 时序决策 / Timing decision

**独立 stage-1.5 commit + 立即三方 push**,理由:

- ADMIN 给出明确指派,Rule 0.a 要求立即落文件,不应拖到 stage-2(可能需多日)
- stage-1(`d79d438`)已冻结,不 amend(不 force-push,不破坏 origin/backup 已对齐的状态)
- stage-1.5 不打 tag,正式 release tag `v2.0.2` 仍留给 stage-2(等 ADMIN PyPI/Zenodo/registry 三件齐活)
- stage-1.5 三方 push(origin + backup),延续"一条龙发版 + 备份"SOP

## 执行步骤 / Execution

1. 改 `README.md`:在第 41 行后(MCP Registry `</a>` 后) / 第 42 行前(Zenodo `<a href=...zenodo...>` 前)插入 Glama HTML 段
2. 改 `README.zh.md`:同上,alt 文案双语对齐
3. ReadLints `README.md` + `README.zh.md`
4. §G 6 条扫描自检(无新版本号引入,不应触发 violation)
5. 落 `REPORT-20260513-015-ME-to-ADMIN.md`
6. `git add` 仅本 task 改动的 4 个文件(2 README + 1 TASK + 1 REPORT)
7. commit(消息含 stage-1.5 标识 + 关联 d79d438 + 关联 TASK-015)
8. `git push origin main` + `git push backup main`
9. SHA 三方验证(local HEAD == origin/main == backup/main)
10. 归档 TASK-015(本任务自归档,无 ADMIN 显式归档指令时按 Rule 0.a.1 第 4 步自驱)

## 验收 / Acceptance

- [ ] 两份 README 各有一个 Glama `<a><img></a>` 段,URL 完全等于 ADMIN 给的 markdown
- [ ] 两份 README 其它部分零变动(diff 干净)
- [ ] ReadLints 0 error / 0 warning
- [ ] §G 扫描通过(版本号、Proposed ADR、backup remote 三项)
- [ ] commit message 明确标注"stage-1.5"+ 关联 stage-1 commit hash + 不动 mcp/README 的 Rule 0.c 自陈
- [ ] origin/main 与 backup/main SHA 字节一致

## 风险与回滚 / Risks & rollback

- 风险 1:Glama `card.svg` 是大尺寸 SVG,塞 small badge 行可能视觉不协调
  - 回滚:若 ADMIN 反馈视觉问题,下一次 commit 把它从 small badge 行抽出来,独立成段,或换成 small badge 风格的 URL(若 Glama 有提供)
- 风险 2:Glama 的 badge URL 后续可能改版(第三方控制)
  - 回滚:URL 失效时,下次 commit 替换或移除
- 风险 3:CodeFlow 仓库的 README 没在本任务处理
  - 缓解:本任务已在"范围"节明确声明 — CodeFlow 由另一会话/角色处理
