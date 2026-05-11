---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
subject: 把另一台机器的真实 dogfood 素材接入中文教程（含 PLANNER 越界陷阱章节）
---

## 背景

用户在另一台电脑上完整跑通了 `docs/tutorials/snake-solo-to-duo.zh.md` 的故事线，把整个 dogfood 项目和 39 张截图拷贝到了 `C:\Users\Administrator\Desktop\test\`：

- `test/fcop-mcp-test/`：完整落盘项目（fcop.json / shared/ / tasks/ / reports/ / issues/ / workspace/snake-game/）
- `test/image/`：39 张截图，覆盖安装、solo、切两人、CODER 接手、**5 张 PLANNER 越界事故现场（two-error-0..4.png）**、最终成片

关键发现：dogfood 中真的复现了 "PLANNER 自言 'CODER 开始实现' 直接改 index.html" 的越界，agent 自我识别后写下 `ISSUE-20260427-001-PLANNER.md` 归档，然后由**新会话的真正 CODER** 接手草稿 + 修复护盾逻辑（`if hitSelf return` 改成 `消费护盾后放行`），形成完整闭环。这一段必须固化到教程里，而不是泛泛地写'可能会发生'。

## 需求

1. **接入真实截图**：从 39 张里挑 12-16 张代表性的，按章节复制到 `docs/tutorials/assets/snake-solo-to-duo/`，用语义化文件名（如 `01-mcp-installed.png` / `04-snake-solo.png` / `08-trap-planner-coder.png` / `09-trap-user-challenge.png` / `12-orbit-final.png`）。
2. **重写 `docs/tutorials/snake-solo-to-duo.zh.md`**：
   - 替换全部占位符为真实图片相对引用。
   - **新增一章「⚠️ 真实陷阱：PLANNER 越界冒充 CODER」**：用 `two-error-0..4` 5 张图 + `ISSUE-20260427-001-PLANNER.md` 真实内容讲清楚"为什么会发生 / FCoP 怎么检测到 / 怎么收住 / 真正的 CODER 怎么接手"。
   - 把第 1 章 solo 阶段的成片（基础贪吃蛇 `game-0.png`）和第 3 章团队阶段的成片（《星轨织者 NEON ORBIT》`newgame.png`）做明显对比，体现"同一个工作区，从基础贪吃蛇到原创主题游戏"的演进。
   - FAQ 增加："agent 自己开了子进程顺序扮演多个角色怎么办？"对应 ISSUE-20260427-004 已经做的护栏（`fcop_check` session_id↔role 一致性 + 软锁）。
3. **结构整洁**：assets 目录用 kebab-case，markdown 引用用相对路径 `assets/snake-solo-to-duo/<file>.png`。
4. **不要给 dogfood 项目本身做 commit**：那是用户的现场证据，原样保留在桌面。我们只是引用其中的截图和事故记录文本。

## 验收

- 教程在 GitHub Web 上能正常显示所有图片（相对路径正确）。
- 「陷阱与对策」章节里 5 张事故图按时间顺序串起来，有 ISSUE-001 引用 + FCoP 三层防护说明。
- solo 章节有 `game-0.png` 成片，team 章节有 `newgame.png` 成片，视觉对比强烈。
- `ReadLints` 无 markdown 错误。
- 完成后按 Rule 0.a.1 走完 `write_report → archive_task`。

## 备注

- 桌面上的 `test/` 目录是用户的现场快照，不要修改也不要纳入 git。
- 英文版本暂缓，仍按 README.md 里的'即将上线'保留。