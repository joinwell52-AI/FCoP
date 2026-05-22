---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260522-010
sender: ADMIN
recipient: ME
priority: P1
parent: TASK-20260522-009
related: [REPORT-20260522-009]
thread_key: agent-bringup-prompt-fix
---

# 修 agent-bringup-prompt §1 —— 让 agent 自己查 PyPI 最新版

## 背景 / Background

ADMIN 在另一台机器跑 §1 时，agent 拿到自己装的 `fcop 3.0.2 / fcop-mcp 3.0.2`
之后说出了一句"目前 PyPI 上最新版可能是 3.0.2 或更高，需要确认墙内是否同步"。
——agent 手里有版本号，PyPI 也有版本号，但它**就是不去查**，凭印象搪塞。

`TASK-009` 修了 §5 的事实错误，但 §1 这条"agent 不查 PyPI"的洞还没补：
prompt 只让 agent 跑 `pip show fcop fcop-mcp`，没要求它对比 PyPI 最新版，
agent 就当然不查。

## 错误的解法（已识别为反模式）

最初的修法是把"当前最新版 = 3.0.2"硬编码进 prompt + 列一个判断树。
被 ADMIN 直接戳穿："什么叫把'当前最新版'写死？？"——

- prompt 是发版冻结的产物，下个 patch 一发版就过时
- 维护负担：每次发版都得改 prompt 里的硬编码版本号
- 版本漂移：硬编码 3.0.2 时如果用户装的是 3.0.3，prompt 反而会误导

正确的解法是**让 agent 自己跑命令查 PyPI**，把"权威答案在哪"写进
prompt，而不是把"权威答案是几"写进 prompt。

## 要求 / Requirements

修改两份 prompt 的 §1：

1. `src/fcop/rules/_data/agent-bringup-prompt.zh.md`
2. `src/fcop/rules/_data/agent-bringup-prompt.en.md`

让 agent 同时跑：

- `pip show fcop fcop-mcp` —— 查本地
- `pip index versions fcop` / `pip index versions fcop-mcp` —— 查 PyPI 最新

老 pip 上 `pip index versions` 不可用时，退路用：

- `python -m pip install --dry-run --upgrade fcop fcop-mcp`

判断规则改成 4 档（local == latest / local < latest / local > latest /
not installed），不再写"3.0.2"这种具体版本号。

明令禁止"可能是 X 或更高"、"需要确认墙内同步"这种**手里有事实却选择
不查**的废话。

## 验收标准 / Acceptance Criteria

- 两份 prompt §1 都包含 `pip index versions` 命令（或同等查询方式）
- 两份 prompt §1 都不再出现硬编码的具体版本号（`3.0.2` 不再作为
  "当前最新"出现，只允许在 §5 / §10 的"v3.0.2 修了什么"历史叙述里出现）
- 两份 prompt 的"判断规则"都改成 local↔latest 比较，不再硬编码版本号
- §5 / §10 等其它章节的 v3.0.2 历史叙述保持不变（`TASK-009` 已修过的
  内容不要回退）
- 两份 prompt 各自在自己语言下读起来自然，不要中英混杂
