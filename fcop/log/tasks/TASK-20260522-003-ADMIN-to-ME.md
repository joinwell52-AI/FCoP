---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
thread_key: v3-reality-check-20260522
subject: 查清 _lifecycle/ 不生成的根因（只查不改）
---

## 背景 / Context

2026-05-22 ADMIN 发现 3 个连锁问题：

1. 本仓库 `fcop/` 下**没有** `_lifecycle/` 五桶，但 `src/fcop/lifecycle/` 模块齐全、`migrate --to-v3` CLI 已注册。
2. `README.md` / `README.zh.md` 缺 v3.0 安装/迁移章节。
3. 我（ME）刚写完的 `fcop/LETTER-TO-ADMIN.md` 自称 v3.0.1，但项目实际没迁移——存在 Rule 0.c（落盘必须真）风险。

③ 的根本原因是 ① 没查清，先把 ① 查实、再动 ②③，避免第二次落假话。

## 任务 / Task

**只查不改**。本任务**禁止**修改任何 `.md` / `.py` 源文件，只产出一份 REPORT-003，回答以下问题：

### Q1 · `_lifecycle/` 应该由谁生成？
- 看 `src/fcop/project.py`、`src/fcop/cli/_main.py`、`src/fcop/cli/migrate_v3.py`、`src/fcop/lifecycle/migrate.py`：
  - `init_solo` / `init_project` / `create_custom_team` 是否在初始化时**默认**落 `_lifecycle/`？
  - 还是设计上必须 ADMIN 显式跑 `python -m fcop migrate --to-v3` 才落？
  - 或者库里有开关（env / 参数）控制？

### Q2 · 当前仓库为什么没有 `_lifecycle/`？
- 看 `fcop/fcop.json`、`CHANGELOG.md`、最近的 `git log`：
  - 这个仓库是 v3.0 之前 init 的吗？init 之后 fcop 包升过几次？
  - 有没有 `.fcop/migrations/` 痕迹显示曾经尝试迁移过？
  - 现状是「该跑 migrate 但没跑」，还是「设计上就不需要 `_lifecycle/`」？

### Q3 · v3.0 spec 与代码实现一致吗？
- 对比 `spec/fcop-3.0-spec.md` 描述的 `_lifecycle/{inbox,active,review,done,archive}/` 与 `src/fcop/lifecycle/state.py`、`src/fcop/lifecycle/migrate.py` 实际实现：
  - 五桶名字一致吗？
  - `_events.jsonl` 真的会被写入吗？
  - 有哪些 spec 里写了但代码还没实现 / 代码做了但 spec 没写的？

### Q4 · 我写的 LETTER-TO-ADMIN.md 哪些段落涉嫌 Rule 0.c 风险？
- 通读 `fcop/LETTER-TO-ADMIN.md`，列出**所有暗示「装上 fcop 就有 v3.0 拓扑」**的句子（行号 + 原文）。
- 区分：
  - 「事实」（spec 已定义、CLI 已存在 → 引用合法）
  - 「现状」（本仓库实际状态 → 与现实不符的就是 0.c 风险）

## 验收标准 / Acceptance

REPORT 必须包含：
- Q1~Q4 各一段结论 + 证据（文件路径 + 行号 / 命令 + 输出）
- 一份「下一步建议」清单，给 ADMIN 三选一/多选：
  - 修代码（让 init 默认落 v3 拓扑）
  - 改一封信（按现状回退 v3 措辞，去掉假设性陈述）
  - 改 README（加 v3.0 安装/迁移章节）
- **不得**自己动手修任何这些文件。

## 越界处理 / Out of scope

查的过程中如果发现别的问题（比如 `migrate --to-v3` 实测失败），**不要现场修**——记到 REPORT 的「附带发现」段，由 ADMIN 决定是否新开 TASK。

## 引用 / Citations rule

按 Rule 0.c：每条结论必带文件路径 + 行号 / 命令 + 输出。查不到 = 写「未验证」，不要填空。