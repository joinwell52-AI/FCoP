---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260522-009
sender: ADMIN
recipient: ME
priority: P0
parent: TASK-20260522-007
related: [REPORT-20260522-007]
thread_key: bringup-prompt-defects
session_id: sess-20260522-me-09
---

# TASK-009 · 修 `agent-bringup-prompt.{zh,en}.md` §5 两处事实错（防呆 prompt 自己翻车）

## 背景

ADMIN 在另一台电脑用主页 banner 第 5 个链接「起项目 prompt」（即
`agent-bringup-prompt.zh.md`）让 agent 起 FCoP 3.0.2 项目。

agent 按 §5 做物理验证时**错判 init 失败**——因为 prompt 里写的"v3 五桶"
名字与 fcop 库实际落盘的目录名**不一致**。这不是 fcop 库的 bug，是这份
prompt 本身的 bug——TASK-007 写 prompt 时抄错。

参见本会话上下文中对 `src/fcop/lifecycle/state.py` 的实证验证：

```
class Stage(str, Enum):
    INBOX = "inbox"
    ACTIVE = "active"
    REVIEW = "review"
    DONE = "done"
    ARCHIVE = "archive"
```

以及本地 `init_solo()` / `init(team="dev-team")` 双路径实测均落
`_lifecycle/{inbox,active,review,done,archive}/`，且 3.0.2 起 fresh init
**不再创建** `tasks/`、`log/`（spec §6 钦定退场，commit `5ab9e73` 实现）。

## 必须修的两处事实错

### 错 1 · 五桶名字写错

**位置**：`agent-bringup-prompt.zh.md` §5 line 148–152、对应
`agent-bringup-prompt.en.md` 同位置。

**当前（错）**：

```
├── _lifecycle/                    ← v3 五桶（必查）
│   ├── intent/
│   ├── plan/
│   ├── execution/
│   ├── verification/
│   └── archive/
```

**应改为（对，按 spec §1.1 + state.py 钦定）**：

```
├── _lifecycle/                    ← v3 五桶（必查）
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
```

§5 末"特别检查"小节里若有桶名引用，同步改。

### 错 2 · 误称 v3 仍保留 v2 五桶

**位置**：`agent-bringup-prompt.zh.md` §5 line 158、英文同位置。

**当前（错）**：

```
└── (兼容五桶: tasks/ reports/ issues/ shared/ log/ —— v3 仍保留)
```

**应改为**：删掉这一行，并在 §5 顶部"应该能看到（v3 拓扑）"之前加一段
正面挡话——

> ⚠️ **3.0.2 fresh init 不再创建 `fcop/tasks/` 和 `fcop/log/`**——
> spec §6 钦定退场，已搬到 `_lifecycle/inbox/` 与 `_lifecycle/archive/`。
> 看到这两个目录不存在是**正常的**，不是 init 失败。
> 老 v2 项目走 `python -m fcop migrate --to-v3` 升迁。

英文同步翻译。

## 验收标准

1. zh + en 两份 prompt §5 桶名全部 = `inbox/active/review/done/archive`
2. 两份都不再出现"v3 仍保留 tasks/ + log/"或英文同义
3. 两份在 §5 顶部都加了 v2 目录退场的正面提示
4. 改完 grep 验证：

   ```
   rg "intent/|plan/|execution/|verification/" src/fcop/rules/_data/agent-bringup-prompt.{zh,en}.md
   ```

   应零命中。
5. ReadLints 无新增警告。
6. 双 commit 推 main：
   - commit A（产品）：`docs(prompt): fix bringup prompt §5 lifecycle bucket names + drop v2 dirs`
   - commit B（治理）：`fcop: archive TASK-009 + REPORT-009`

## 不在本 task 范围

- `agent-install-prompt.{zh,en}.md` 加 `--no-cache-dir` / `uv tool upgrade` 防 uvx 缓存
  踩坑——单独走 TASK-010。
- 老 v2 项目 `d:\FCoP` 自身的 v3 迁移——单独走 Rule 7 destructive flow。
- fcop 库或 fcop-mcp 任何代码变更——本 task 只动 prompt 文档。

## thread_key

`bringup-prompt-defects` —— 后续若发现 prompt 还有别的事实错，沿用此线程。
