---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260427-008
sender: ME
recipient: ADMIN
related_task: TASK-20260427-008
session_id: sess-20260427-me-072
---

# 中文教程骨架 done — Snake solo→duo

## 完成清单（按 TASK-008 验收逐条核）

### A. 文件位置 ✓

- [x] `docs/tutorials/snake-solo-to-duo.zh.md`（10792 字符 / 325 行）
- [x] `docs/tutorials/README.md`（教程目录索引）

### B. 教程章节齐全 ✓

- [x] 第 0 章：5 分钟自动装 fcop-mcp（含完整 install prompt、`fcop_report()`
  首次输出样本、版本号偏差排查）
- [x] 第 1 章：solo 模式 + 贪吃蛇 v1（含 `init_solo` 落盘清单 / 目录树 /
  Rule 0.a.1 四步对照表 / `fcop_report()` 终态样本）
- [x] 第 2 章：`create_custom_team(force=True)` 切 2 人团队（含旧文件命运
  对照表 / 新文件命运对照表 / `.fcop/migrations/` 截图占位 /
  历史角色 vs 当前 roster 解读）
- [x] 第 3 章：PM 拆 task + DEV 实现（含 ADMIN 显式切角色 prompt /
  `.fcop/proposals/role-switch-*.md` 解释 / 软角色锁 0.7.1 取舍）
- [x] 结尾彩蛋：指向本仓 `docs/agents/log/` + 0.7.0/.1/.2 三连发版账本

### C. 每章必含元素 ✓

- [x] 一句话目标 — 以章节副标题或导言段呈现
- [x] 可复制粘贴 prompt — 全部用反引号代码块包裹，半角符号
- [x] 期望工具调用清单 — 第 1 章用表格、第 2/3 章用 prompt 内枚举
- [x] 截图占位符 — 共 9 处 `[截图 X-Y：...]` 占位，覆盖关键时刻
- [x] "FCoP 在做什么" — 每章末尾 3-5 行解说 + 协议条款链接
- [x] "如果出错怎么办" — 文末统一 FAQ 段含 5 条常见问题

### D. 协议账本 ✓

- [x] TASK-008 已立
- [x] 本 REPORT 即 done report
- [x] 写完 archive

### E. 不在范围 — 已标注 ✓

- [x] 真实截图：教程明确说明"如果你看到的是占位标记 `[截图：...]`，
  说明本仓还没上传该截图"，新机器实操后 ADMIN 自行补
- [x] 英文版：教程末尾 README index 已留 "_即将上线_" 占位
- [x] 视频/GIF：未列入

## 验收偏差（透明披露）

### 偏差 1：字数超出 TASK 自定上限（10792 字符 vs 计划 ≤ 2500 字）

**TASK-008 验收里我自己写的**："中文教程 ≥ 800 字、≤ 2500 字（保持轻量；过长读者会跑）"

**实际产出**：10792 字符（约 4500-5000 字正文 + 大量代码块/表格/树结构）。

**原因**：

- 教程跨 4 章 + FAQ + Next steps，每章本身需要"目标 + prompt + 工具
  调用清单 + 截图占位 + 解说 + 协议条款链接"，这套结构是 TASK 自己
  规定的 C 段验收项。
- 大量篇幅是非正文：6 段 prompt 代码块、5 个对照表格、2 处 ASCII
  目录树、9 处截图占位符、章节锚点。**纯正文**（用户阅读那种）估
  计 4500 字，约 11 分钟阅读时间——配 35 分钟实操合理。
- 强压到 2500 字会让"FCoP 在做什么"的解说稀薄，反而损伤教程的
  教学价值。

**取舍判断**：选了"严守 C 段元素齐全"而非"严守字数上限"——前者
是用户实际看不看得懂教程的关键，后者只是我自己定的轻量化指标。
透明披露而非偷偷放过。

**未来纠偏建议**：写下一份教程（如英文版）时，C 段验收应改成"每
章正文（不含代码/表格）≤ 800 字"，比按整文字数总量更精准可控。

### 偏差 2：教程内含截图占位符 9 处，无真实截图

**TASK-008 E 段**已明确说明"真实截图（要新机器跑了才有，先留占位
符）"——这条是预期内的偏差，**不是缺陷**，列在这里只为完整性。

ADMIN 实操新机器时按占位符前缀 `tutorial-assets/snake/<step>.png`
落图即可，路径已在教程顶部 admonition 里给读者交代。

## 链接核查（已自查）

教程位于 `docs/tutorials/`，相对路径分两类：

| 目标 | 正确前缀 | 已用且核对 |
|---|---|---|
| 仓根（`README.md`、`adr/`、`src/`） | `../../` | ✓ |
| docs 同级（`releases/`、`agents/`、`fcop-standalone.md`） | `../` | ✓ |
| 教程内部（`README.md`） | 同目录 | ✓ |

之前一度把 `docs/releases/0.7.X.md` 写成 `../../docs/releases/...`
（多了一层 `docs/`，会 404），4 处全部已修正为 `../releases/...`。

## 给 ADMIN 的"新机器实操 checklist"

接下来在新电脑上跑教程时，按下面顺序补完整套素材：

1. 装 fcop-mcp（教程第 0 章自走）→ 截图 0-1, 0-2
2. 跑 solo + 贪吃蛇 v1 → 截图 1-1, 1-2, 1-3, 1-4
3. 切 2 人团队 → 截图 2-1, 2-2
4. PM 拆 + DEV 实现 v2 → 截图 3-1, 3-2
5. 截图全部存到 `docs/tutorials/tutorial-assets/snake/<step>.png`
6. （可选）回头把教程顶部 admonition 里的"截图缺失"段删掉
7. 教程链接里的 `D:/snake-demo` 改成你新机器实际用的路径

## 关联

- TASK-20260427-008（本任务）
- `docs/tutorials/snake-solo-to-duo.zh.md`
- `docs/tutorials/README.md`
- 下一任务（未立）：英文版 + 实操截图（新机器 dogfood 后）
