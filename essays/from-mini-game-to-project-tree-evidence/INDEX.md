# Evidence for “FCoP Grew a Project Tree / FCoP 跑出了项目树”

This index catalogues the **CodeFlowMu dogfood originals** behind [essay 17](../from-mini-game-to-project-tree.en.md). The TASK / EVAL Markdown files were produced on a local CodeFlowMu workspace and are **not copied into the FCoP repository** in this release. The essay’s workflow figures live under [`essays/assets/`](../assets/) on GitHub.

本索引对应 [第 17 篇随笔](../from-mini-game-to-project-tree.md) 的 CodeFlowMu 狗食现场原件。TASK / EVAL 正文文件仍在本地 CodeFlowMu 工作区，**尚未随 FCoP 公仓一并发布**；正文配图已放在 [`essays/assets/`](../assets/)。

## Figures shipped in this repository / 本仓库已收录的配图

| File | Role |
| --- | --- |
| [from-mini-game-to-project-tree-cover.png](../assets/from-mini-game-to-project-tree-cover.png) | Cover |
| [from-mini-game-to-project-tree-fig2-gameplay.png](../assets/from-mini-game-to-project-tree-fig2-gameplay.png) | Grid Runner gameplay |
| [from-mini-game-to-project-tree-fig3-panel-zh-full.png](../assets/from-mini-game-to-project-tree-fig3-panel-zh-full.png) | CodeFlowMu console archive view |
| [from-mini-game-to-project-tree-fig-chat-pm-tree.png](../assets/from-mini-game-to-project-tree-fig-chat-pm-tree.png) | PM drew 020→004→005–007 in chat |
| [from-mini-game-to-project-tree-fig4-archive-block.png](../assets/from-mini-game-to-project-tree-fig4-archive-block.png) | Archive blocked (`CHILD_TASKS_OPEN`) |
| [from-mini-game-to-project-tree-fig6-eval-gap003.png](../assets/from-mini-game-to-project-tree-fig6-eval-gap003.png) | EVAL Fix-chain slice (GAP-003) |

## Primary ledger excerpts / 主线账本摘录

### task-20260613-020

- **ID:** `TASK-20260613-020` — Grid Runner v0.1  
- **Role path:** `ADMIN → PM`  
- **Key field:** `thread_key: panel-task-020`  
- **Dogfood path (local, not in FCoP repo):** `fcop/_lifecycle/archive/TASK-20260613-020-ADMIN-to-PM.md`  
- **Reading:** later recognised as the **project root** of the Grid Runner product line.

### task-20260614-004

- **ID:** `TASK-20260614-004` — Grid Runner Phase 2  
- **Role path:** `ADMIN → PM`  
- **Key fields:** `references: TASK-20260613-020`, same `thread_key`  
- **Dogfood path (local):** `fcop/_lifecycle/archive/TASK-20260614-004-ADMIN-to-PM.md`  
- **Reading:** **Phase task** under 020; parent of 005–007 execution tasks.

### gap-20260614-004-panel-scan

- **ID:** `GAP-20260614-004-panel-scan`  
- **Kind:** internal EVAL scan triggered from the CodeFlowMu console  
- **Dogfood path (local):** `fcop/internal/eval/GAP-20260614-004-panel-scan.md`  
- **Signal:** `project_tree_emergence` — canonical line `020 → 004 → 005 / 006 / 007 / 008`.

## Compressed field summary / 字段压缩摘要

```text
TASK-20260613-020: thread_key = panel-task-020
TASK-20260614-004: references = TASK-20260613-020
EVAL: project_tree_emergence
Archive guard: CHILD_TASKS_OPEN
```

## Proposed protocol follow-up / 拟议协议收编

Essay conclusion points to additive **[`spec/0003-project-tree-protocol.md`](https://github.com/joinwell52-AI/FCoP/blob/main/spec/0003-project-tree-protocol.md)** (proposed; 0001/0002 unchanged) for **Project / Phase / Execution / Fix / Independent Project**.
