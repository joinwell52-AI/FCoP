---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-011
sender: ADMIN
recipient: ME
priority: P1
parent: TASK-20260513-010
related: [TASK-20260513-010]
thread_key: docs-index-v2-finish
session_id: sess-20260513-me-04
---

# 把 docs/index.html "半成品" 做完(essay 07~14 + 标题修正)

## 背景

`TASK-20260513-010` 同步了 README × 3 → 2.0.0 但故意把 `docs/index.html`
留为"半成品 — 下次另立 TASK"。ADMIN 立刻反馈:

> "说了检查了才发,怎么还是这样呢?半成品要做完;"

— 这是对 Rule 0.c(`Only Land True Things` / "落到文件里的必须是真的")的
直接命中:号称"已同步 GitHub"却把同一 commit 里看得见的 v2.0.0 落地半成品
留在站点首页,等于在文件层撒谎。

## 现场盘点(2026-05-13 21:18 +08:00)

| 项 | 现状 | 评估 |
|---|------|------|
| Hero pill `Latest: v2.0.0 · 2026-05-13` (L723-724) | ✓ 已落 | 上一波改的 |
| "What is FCoP" 段 v2.0.0 双图对偶段(L781,786) | ✓ 已落 | 上一波改的 |
| Field Reports 标题 "Six essays / 六篇 essay"(L870-871) | ✗ 数字过时 | essays/ 目录现有 14 篇 |
| Essay 06 卡片 `Essay 06 · Latest`(L952) | ✗ 不再是 Latest | 应让位给 14 |
| Essay 07~14 卡片(8 张) | ✗ 缺失 | wreckage / short / gate / supersedes / looking / 5-models / evolution / picked-up-tools |
| 站内 1.3.0 / 1.2.1 / 32 工具 残留 | (上一波 grep) 已清 | ✓ |

## 改动清单(单文件 `docs/index.html`)

1. L870 `Six essays. Command the agents — FCoP brings discipline to an AI team.`
   → `Fourteen essays. Command the agents — FCoP brings discipline to an AI team.`
2. L871 `六篇 essay。指挥 agent —— FCoP 让 AI 团队有纪律。`
   → `十四篇 essay。指挥 agent —— FCoP 让 AI 团队有纪律。`
3. L952 `<div class="num">Essay 06 · Latest</div>`
   → `<div class="num">Essay 06</div>`
4. L964(essay-06 卡片闭合 `</div>`)与 L965(essays-grid 闭合 `</div>`)之间,
   按 `essays/README.md` 权威清单插入 8 张卡片:
   - **Essay 07** · 当 agent 从自己的残骸中学习 / When agents learn from their own wreckage
   - **Essay 08** · 协议为什么短,历史为什么长 / Why the protocol stays short
   - **Essay 09** · 当 validator 撞向自己的镜像 / Gate design pitfalls case studies
   - **Essay 10** · 一行 frontmatter 的旅程 / The supersedes field story
   - **Essay 11** · 看,但不动手 / Looking without touching
   - **Essay 12** · 五大 AI 模型眼中的 FCoP / What five AI models say about FCoP
   - **Essay 13** · 演化,反向吸收 / Evolution, reverse absorption
   - **Essay 14 · Latest** · 当 Agent 第一次拿起工具 / When the agent picked up its tools

   每张卡片复用现有 `<div class="essay-card">` 模板,字段:
   - `.num` · Essay NN
   - `<h3 class="en-only">` 英文标题
   - `<h3 class="zh-only">` 中文标题
   - `.hook en-only / zh-only` 一句话钩子(强调词以 `<strong>` 包裹)
   - `.channels` 至少含 GitHub EN + GitHub 中文,有 CSDN 的(07 / 11)补上

## 验收标准

- [ ] 改动只在 `docs/index.html` 内(单文件)
- [ ] 8 张新卡片结构与现有 6 张完全一致(class / 锚点 / 链接四白对齐)
- [ ] 双语都补齐(`en-only` + `zh-only`)
- [ ] 编号与 `essays/README.md` 一致(01 → 14),无跳号、无错号
- [ ] Essay 14 标 `Latest`,Essay 06 摘掉 `Latest`
- [ ] 标题数字从 6 / 六 改成 14 / 十四
- [ ] commit + push,GitHub Pages 渲染 v2.0.0 完整(F12 ctrl+shift+R 复诊)
- [ ] 写 REPORT-20260513-011 + archive TASK + REPORT 到 `fcop/log/`

## 不在本任务范围

- v2.0.0 哲学 hero 段补图(预留 essay 13 / 14 封面图加进首页),后续视觉资源 ready
  再立 TASK
- 顶部 nav 增加 "Releases" / "Evolution Loop" 锚点(那是结构性改,非 v2.0.0 同步)
