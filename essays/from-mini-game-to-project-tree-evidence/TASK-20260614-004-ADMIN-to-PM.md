---
protocol: fcop
version: 1
sender: ADMIN
recipient: PM
priority: P2
thread_key: panel-task-020
subject: Grid Runner Phase 2：产品化升级（多关/道具/特效）
references:
  - TASK-20260613-020
task_id: TASK-20260614-004
transitions:
  - at: 2026-06-14T03:03:59.214738+00:00
    from: null
    to: inbox
    by: ADMIN
    tool: create_task
  - at: 2026-06-14T12:08:38+08:00
    from: inbox
    to: active
    by: CodeFlowMu
    action: runtime_dispatch
  - at: 2026-06-14T12:08:38+08:00
    from: active
    to: review
    by: PM
    action: submit_review
    report: REPORT-20260614-016-PM-to-ADMIN.md
  - at: 2026-06-14T12:38:51+08:00
    from: review
    to: done
    by: ADMIN
    action: approve_review
    reason: 验收通过
    decision: approved
  - at: 2026-06-14T12:38:58+08:00
    from: done
    to: archive
    by: ADMIN
    action: archive_task
    reason: 任务已完成
    decision: archived
display_status: archived
pm_attention_reason: PM 自动审查未通过，需 PM 人工处理
state: archive
lifecycle_path: fcop/_lifecycle/archive
review_status: approved
submitted_at: 2026-06-14T04:08:38.398Z
approved_by: ADMIN
approved_at: 2026-06-14T04:38:51.864Z
lifecycle_projection: archive
frozen: true
archived_by: ADMIN
archived_at: 2026-06-14T04:38:58.883Z
archive_reason: 任务已完成
---

## 背景

`TASK-20260613-020` **Grid Runner v0.1** 已验收（纯 HTML/CSS/JS · `file://` 可运行）。ADMIN 要求 **Phase 2 产品化升级**：从功能 demo 升级为可玩 15–30 分钟的轻量产品。

## 硬约束（继承 v0.1）

- 纯 **HTML + CSS + JavaScript**
- **禁止** TypeScript、Vite、npm、`npm install` / `npm run dev`
- 运行方式：**双击 `index.html`** 或浏览器 `file://` 直接打开
- 产物目录：`workspace/grid-runner/`（原地升级，不修改 codeflowmu 本体）

## Phase 2 产品目标

| 模块 | P0 要求 |
|------|--------|
| 流程 | 主菜单 → 选关 → 游戏 → 结算 → 下一关/重试 |
| 关卡 | **≥5 关**，`levels.js` 数据驱动，难度递进 |
| 道具 | **≥3 种**：加速靴 / 护盾 / 磁铁（拾取有 UI + 持续时间） |
| 敌人 | **≥2 种行为**：巡逻怪 + 追击怪（或固定炮台） |
| 进度 | `localStorage`：关卡解锁、最佳时间、1–3 星 |
| HUD | 分数、时间、关卡号、道具状态、Playing/Paused/Win/Lose |
| 操作 | WASD/方向键、R 重开、P 暂停、Esc 回菜单 |
| 视觉 | CSS 主题 UI；Canvas 粒子（收币/死亡/过关）；非「几个灰方块」 |

## 交付文件

```
workspace/grid-runner/
├── index.html
├── style.css
├── main.js          # 状态机：menu | play | pause | result
├── levels.js        # ≥5 关数据
├── game.js          # 核心循环、碰撞、胜负
├── entities.js      # 玩家/怪/道具
├── effects.js       # 粒子与动画
└── README.md
```

## 关卡草案

1. 新手村 — 移动/收币/出口
2. 迷宫 — 墙体绕路
3. 初遇怪 — 巡逻怪
4. 道具关 — 磁铁+加速
5. 综合 — 追击怪+护盾

## 分工

- **PM**：派 DEV/OPS/QA，汇总后 submit_review
- **DEV**：实现 Phase 2 全部 P0
- **OPS**：验 `file://` 打开，5 关可进入
- **QA**：30min 试玩，5 关通关 + 3 道具 + 存档

## 完成标准

OPS + QA 均 **done**；`file://` 下可玩、有产品感、非单关 demo。

## 引用

- 前置：`TASK-20260613-020`（v0.1 技术验证）

---

## state_history (auto-appended by runtime)

- **2026-06-14T11:03:59+08:00** | by `runtime` | `inbox` → `rejected_busy` recipient=PM, agent_status=running
