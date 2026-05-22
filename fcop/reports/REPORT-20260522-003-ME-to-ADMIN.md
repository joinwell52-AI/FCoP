---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P0
references:
- TASK-20260522-003
status: done
---

## TL;DR

**FCoP 3.0 init 路径与 spec 不对齐**——任何全新项目跑 `Project.init_*()` 之后**都不会**得到 `_lifecycle/`，违反 `spec/fcop-3.0-spec.zh.md` §1.1 的 MUST 条款。`migrate --to-v3` 设计上**只能**迁已有 v2 项目，对全新项目判 `EMPTY` → no-op。结论：**全新项目当前没有任何代码路径能产生 spec 要求的 v3 拓扑**。

本次任务严守『只查不改』，未动任何源文件。

---

## Q1 · `_lifecycle/` 应该由谁生成？

**结论：spec 期望 `init_*` 直接落 v3，但代码里 `init_*` 只落 v2。**

证据：

- `src/fcop/lifecycle/migrate.py:289-295` EMPTY 分支注释原文：
  > "Workspace is empty — no v2 or v3 evidence. **A fresh `init` would create a v3 layout directly**; no migration needed."
  作者本人在 migrate 引擎里**预期 init 落 v3**。
- `src/fcop/project.py:924-931` `_apply_init` 实际行为：
  ```
  for directory in (self.tasks_dir, self.reports_dir, self.issues_dir,
                    self.shared_dir, self.log_dir):
      directory.mkdir(parents=True, exist_ok=True)
  ```
  只 mkdir v2 五桶。**全文 grep 不到 `ensure_lifecycle_dirs(` 在 `_apply_init` / `init` / `init_solo` / `init_custom` 任一处的调用。**
- `src/fcop/lifecycle/state.py:43` 提供了 `ensure_lifecycle_dirs()` 公共 API，但**无人调用**它来完成 init。

现场实测（ADMIN 在另一台机器 `E:\fcop3.0-test\` 跑 `python -c "from fcop import Project; Project('.').init()"` 后）：

```
PS> dir fcop\_lifecycle
dir : 找不到路径...因为该路径不存在
```

## Q2 · 当前仓库为什么没有 `_lifecycle/`？

**结论：本仓库的 `fcop/` 是 v3.0 之前 init 的，且 `_apply_init` 一直没有 v3 拓扑路径，所以从未被创建。**

证据：

- `fcop/fcop.json:10` `created_at: 2026-04-27T13:04:04` —— 早于 v3.0.0 release（`CHANGELOG.md:47` 的 2026-05-21）将近一个月。
- `git log --oneline` 里 v3.0 相关 4 个 commit（`10d078f` PR-1 / `4ac139e` PR-2 / `357fe37` PR-3a / `65892ea` PR-3b）只动 `src/fcop/lifecycle/` 与 `Project` facade 的读路径，**没有动 `_apply_init`**。
- `Get-ChildItem fcop -Directory` 实测当前桶：`tasks/ reports/ issues/ shared/ log/ reviews/`，**无 `_lifecycle/`**。
- `.fcop/migrations/` 没有 v3 迁移痕迹（之前只有 0.6.x 升级痕迹，未列出）。

现状定性：**『该跑 migrate 但没跑』和『init 应该落但没落』两条解释，证据偏向后者**——因为本仓库即便明天跑 `migrate --to-v3 --apply` 也只是把现有 `tasks/log/` 迁过去，未来 init 新项目还是同样不会产生 `_lifecycle/`。

## Q3 · v3.0 spec 与代码实现一致吗？

**结论：spec 与 lifecycle 子包高度一致；与 `Project.init_*` 严重不一致。**

证据：

- 五桶名一致：`spec/fcop-3.0-spec.zh.md:67-77` 的 `inbox/active/review/done/archive` 与 `src/fcop/lifecycle/state.py:72-76` `Stage` 枚举逐字对齐。
- `_events.jsonl` 实现存在：`src/fcop/lifecycle/events.py` 全模块就是为它而写；`src/fcop/lifecycle/atomic.py` `commit()` 把事件落盘。
- spec MUST 条款（§1.1 "合规实现必须在项目根目录维护以下结构"）**当前没有任何 init 入口能满足**——这是 spec ↔ 实现的硬不一致。
- 不一致点收口：
  - `_apply_init` 不创建 `_lifecycle/`（最大问题）
  - `LETTER-TO-ADMIN.md` 里 `init_*` 落盘清单写的是 v2 五桶（昨天 ME 重写时按现状写的，但与 spec 期望相反）

## Q4 · 我之前重写的 LETTER-TO-ADMIN.md 哪些段涉嫌 Rule 0.c 风险？

**结论：有但不严重，关键风险段已标红如下。**

通读 `fcop/LETTER-TO-ADMIN.md`（759 行）后划分类：

| 类别 | 状态 | 行号样本 |
|---|---|---|
| spec 已定义（合法引用） | ✅ 真 | v3.0.1 摘要里 "`_lifecycle/` 五桶 + 7 类 transition + 三层规则集"（说的是 spec 而非本仓库现状）|
| CLI 已存在（合法引用） | ✅ 真 | `python -m fcop migrate --to-v3` 描述（命令真实存在，行为如所述）|
| **暗示『装上 fcop 就有 v3 拓扑』** | ⚠️ 0.c 风险 | 顶部摘要 "v3.0.0，BREAKING"+ 目录章节『v3.0 标准拓扑』即便加了双轨说明，**整体语气仍让人以为 init 直接落 v3**——而事实（Q1）是 init 永远不落 v3。 |
| 双轨节兜底声明 | ✅ 真 | 双轨节里『本仓库当前实际状态』那段是真的——但放在『v3.0 标准拓扑』之后，读者很容易先信前者。 |

严格按 0.c：**没有一句话明文撒谎**，但**整体结构暗示了一个不存在的能力**。修一封信的正确方式不是删段落，而是在顶部摘要 + 目录章节都加 "⚠️ 当前 init 不落 _lifecycle/，需先 init v2 再 migrate；这是 v3.0 的已知缺口（见 ISSUE-001）" 之类的诚实声明。

## 附带发现 / Incidental findings（不在本任务范围内，留给 ADMIN 决定）

1. `Project.init_*` 里 `tasks_dir` / `reports_dir` 等 property（在 v3 项目下指向 `_lifecycle/inbox/`）与 `_apply_init` 直接 `mkdir` 的物理路径**在 v2 拓扑下重合、v3 拓扑下不重合**——一旦修 `_apply_init` 加 v3 路径，这套 property 的双轨语义需要顺带核一遍。
2. `migrate --to-v3` 默认 dry-run（`migrate_v3.py:72-75`），需 `--apply` 才真迁——这件事 LETTER 现在没说。
3. README.md / README.zh.md 没有 v3.0 安装/快速开始章节（ADMIN 之前提到的问题 ②）——独立任务，留给后续。

## 下一步建议 / Recommendations

按 0.b（决策与执行不能同一人闭环），下面三件事**全部需要 ADMIN 单独下 TASK 才能执行**，本报告只列选项：

- **甲 · 修代码**：让 `_apply_init` 默认调 `ensure_lifecycle_dirs()`，让 `init_*` 直接落 v3。需要：
  - 改 `src/fcop/project.py:_apply_init`
  - 决定 v2 五桶要不要继续创建（reports/issues/shared 还要；tasks/log 在 v3 下属于 v2 残留）
  - 加测试覆盖
  - 走 Rule 7 发版流程
- **乙 · 改一封信**：在顶部摘要 + 目录章节加诚实声明，引用 ISSUE-001。在甲完成前，乙是不可少的——否则 LETTER 持续撒结构性谎。
- **丙 · 改 README**：加 v3.0 安装 + 现状声明。优先级低于甲乙。

ME 倾向顺序：**ISSUE 落档 → 甲（修代码）→ 乙（更新一封信）→ 丙（更新 README）→ 发 patch**。理由：先把代码修对，文档跟着真实行为走，避免文档先于代码到位再次撒谎。

## 验证 / Self-check

- [x] 未修改任何 `.md` / `.py` 源文件
- [x] 每条结论附了文件路径 + 行号 / 命令 + 输出
- [x] 无法验证项标记『现状定性』而非断言
- [x] 附带发现单独成段，未与主结论混淆
