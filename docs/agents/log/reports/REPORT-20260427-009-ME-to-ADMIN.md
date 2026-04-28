---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
references:
- TASK-20260427-007
status: done
---

# v1 中文教程接入真实 dogfood 素材完成

## 结论

`TASK-20260427-007` 验收项全部达标：v1 教程以另一台机器的真实 dogfood 为背书重写完成，含 15 张代表性真实截图 + 一章「陷阱与对策」事故复盘。

## 交付物

### 新增

- `docs/tutorials/assets/snake-solo-to-duo/`：从 39 张原始截图中精选 15 张，语义化命名为 01..16（中间 02 未采用的"未装 fcop" 对照图已删除）。
  - 第 0 章安装：01-mcp-installed.png
  - 第 1 章 solo：03-solo-init.png / 04-solo-files.png / 05-solo-task-running.png / 06-snake-solo.png
  - 第 2 章切团队：07-switch-to-duo.png / 08-team-status.png
  - 第 4 章陷阱（5 张完整事故）：09-trap-planner-coding.png → 10-trap-user-challenge.png → 11-trap-self-reflection.png → 12-trap-strict-mode.png → 13-trap-issue-recorded.png
  - 第 5 章接手 + 成片：14-coder-handoff.png / 15-team-final.png / 16-orbit-game.png

### 重写

- `docs/tutorials/snake-solo-to-duo.zh.md`（326 行 → 440 行）：
  - 第 1 章任务描述对齐 dogfood 原话（零依赖单文件 + 圆角分段 + 足头有眼睛 + 呼吸光晕 + 粒子）。
  - 第 2 章角色名从 "PM/DEV" 改为 dogfood 实际用的 PLANNER/CODER，与 FCoP 原生概念对齐。
  - 第 3 章新增：PLANNER 完整设计《星轨织者 NEON ORBIT》（3 皮肤 + 5 道具 + 参数面板）。
  - 第 4 章新增「⚠️ 真实陷阱：PLANNER 越界冒充 CODER」：以 5 张事故图 + ISSUE-001 原文节选 + FCoP 三层防护表格（协议层 / 审计层 / MCP 层）。
  - 第 5 章最终成片与第 1 章基础版两张图并面对比，体现 "同一代码笼子、从贪吃蛇到原创宇宙游戏" 的演进。
  - FAQ 新增两项："agent 越界能不能完全避免" / "单 agent 顺序扮多角色会怎么样"，明确 0.7.1 软锁 + 证据留存的设计取舍。

### 更新

- `docs/tutorials/README.md`："演示了什么" 列从原 "solo → 两人团队" 升级为包含《星轨织者》、越界事故、三层防护的完整描述；时长 35min → 45min。

## 验收自检

| 项 | 状态 |
|---|---|
| `assets/snake-solo-to-duo/*.png` 17 处引用、文件全部存在 | OK |
| 15 处相对 markdown 链接（`../releases/0.6.4..0.7.2.md` / `../../adr/...` / `../agents/log/` 等）全部可解析 | OK |
| `ReadLints` 对 zh.md 和 README.md | 无错误 |
| 陷阱章节 5 张事故图按时间顺序串起 | OK |
| solo 阶段成片 vs 团队阶段成片双幅对比 | OK |
| 桌面 dogfood 原始目录未被修改、未被纳入 git | OK |

## 已知边界

- 英文版仍为 "即将上线"。考虑到 ADMIN 后续的 "教材级" 重定位（参下节），英文版宜等 v2 定稿后再一次性产出。
- 未加封面图 / elevator pitch / 分发友好的 SEO 标题；这些由 ADMIN 在选项 E 中未勾选，收进 v2 范围调整到二期。

## 下一步 ADMIN 决策输入

ADMIN 在本 TASK 验收后明确重新定位为「免费开源·多 agent 实战教材·教你怎么指挥 agent」，并提供三段心法：

1. **单 agent 什么都做 → 记忆爆炸**：session 上下文无限拉长，agent 开始忘事、自相矛盾、退化。
2. **MCP 工具是教你做 ADMIN 的**：我们不是码农，是指挥者、领导者；agent 是数字员工。
3. **每个文件落盘 = 管理 / 追溯 / 审计 / 有序 / 有规则**：把记忆从对话卸到文件系统。

同时勾选了加工方向：A（读者画像 + 学习目标） + D（抽象为指挥 agent 的 N 条铁律）。

## 建议

立即开 `TASK-20260427-008-ADMIN-to-ME`，以上述三段心法为 spine + A/D 为加工手段，将 v1 升级为教材级 v2。本 TASK-007 完结后可直接 archive。