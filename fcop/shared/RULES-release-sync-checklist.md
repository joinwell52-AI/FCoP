---
protocol: fcop
version: 1
kind: shared
prefix: RULES
sender: ME
recipient: TEAM
related: [REPORT-20260513-011, TASK-20260513-012, TASK-20260513-013]
thread_key: release-sync-discipline
---

# RULES · 发版前文档同步纪律 / Release-Sync Discipline

> **Scope**: FCoP 自仓发版纪律,不是 FCoP 协议本身。本文件写"为什么、
> 底线在哪、态度坐标系";配套文件 [`RULES-release-file-inventory.md`](RULES-release-file-inventory.md)
> 写"具体动哪些文件、怎么动、怎么验"。两份一前一后,把红线钉住。
>
> **Discipline level**: 按 FCoP 未来可能成为外部协作协议标准的严谨度
> 写——任何接手的 agent / 任何一次 `fcop_report()` 后都看得见(Rule 2:
> Folders are the organization,`fcop/shared/` 是团队内部第一时间看见
> 的位置)。

## 0. 元红线 / Meta Line(凌驾本文所有具体规则之上)

> **"如果未来 FCoP 成为一种标准,我们现在要非常认真才行。"**
>
> —— ADMIN, 2026-05-13 22:32 +08:00。
>
> 这不是新规则,是**态度坐标系**:本文件、配套清单、SOP §C/§G/
> §阶段 4.5,每一行都按"被外部团队 / IDE 厂商 / 学术论文引用一次"
> 的成本写——禁止"差不多""大概那一段"(Rule 0.c 反面)。

## 1. ADMIN 红线 1 / Line 1 · 文档同步

> **FCoP 在短期内会有很多发版,所以各处的文档一定要同步;发版前不要
> 遗漏,因为 PyPI 不能补发**。
>
> —— ADMIN, 2026-05-13 21:55 +08:00,紧接 REPORT-20260513-011 的反思
> 段被升格为永久纪律。

## 2. ADMIN 红线 2 / Line 2 · 一条龙发版+备份

> **一条龙发版+备份!**
>
> —— ADMIN, 2026-05-13 22:28 +08:00,在确认 FCoP-backup mirror push
> 成功后立即指令。**发版动作的最后一步必须是同步 backup remote**——
> 任何漏了 backup 同步的发版都算未完成(详见 SOP §阶段 4.5)。

## 为什么这条要单独立一份(而不是只埋在 SOP 里)

`docs/release-process.md` 是 SOP 权威源,但**发版的 agent 第一巡检
路径是 `fcop_report()` → `fcop/shared/`**,不一定记得 `docs/` 下有个
SOP。把这条红线钉在 `fcop/shared/` 里,任何接手的 agent / 任何一次
`fcop_report()` 后都看得见。

"Files are the protocol. Folders are the organization."(Rule 2):
SOP 在 `docs/`(外部贡献者也读);纪律书在 `fcop/shared/`(团队
内部第一时间看见)。两份指向同一权威源,**避免漂移**。

## 3. 权威源 · 不在这里复制 / Authoritative sources

发版纪律的**三层结构**(本文件 + 配套清单 + SOP)各管一段:

| 文件 | 管什么 | 权威等级 |
|---|---|---|
| **本文件**(`RULES-release-sync-checklist.md`) | **为什么、底线、态度坐标系** | 纪律书 |
| [`RULES-release-file-inventory.md`](RULES-release-file-inventory.md) | **具体动哪些文件 + 12 类 6 字段全枚举** | 文件清单 |
| `docs/release-process.md` | **流程怎么走 + §C/§G/§阶段 4.5 执行命令** | SOP 权威源 |

发版的 agent 顺序:
1. **先读本文件**——理解红线和态度
2. **再读 inventory**——本次发版要动哪几类(用第 3 节速查矩阵)
3. **最后读 SOP**——一步一步走

三份指向同一目标,**禁止互抄**——本文件 / inventory 可能滞后,SOP
改了不需要回改本文件 / inventory(Rule 5 历史只增不改)。

## 4. 四条不会变的硬约束 / Four things that won't change

1. **`mcp/README.md` = PyPI `long_description`,锁版** ⚠
   `twine upload` 成功即永久定格——版本号 / 历史段 / 亮点描述错了 /
   漏了,**只能 yank + bump 下一版重发**。Rule 7 适用。
   (Inventory §D)
2. **`README.zh.md` 和 `README.md` 同等重要**——历版 SOP 只列前者
   导致 v2.0.0 发版时它停滞在 `1.2.1`(4 个版本前)。两者并列,无主次。
   (Inventory §D)
3. **`docs/index.html` = GitHub Pages**——它是项目的脸,流量比 GitHub
   仓库首页 README 都大,version pill / "What is FCoP" / essays-grid
   不同步 = 对外撒谎(Rule 0.c 反面)。
   (Inventory §D)
4. **一条龙发版+备份**——`git push origin` 后,**最后一步**必须是
   `git push backup main && git push backup --tags`。append-only,
   **禁用** `--mirror`(防"反备份":origin 被 force push,backup 跟着
   把破坏同步过去)。Rule 7 适用。
   (Inventory §K · SOP §阶段 4.5)

## 5. 自检入口 · 发版前最后 30 秒 / 30-second self-audit

发完 §A–§F(SOP 6 段)之后、敲 `git tag` 之前:

```text
跳到 docs/release-process.md §G,把那 6 条 rg / git 命令按顺序跑一遍。
判定:#1/#2/#5 = 0 hit  #3 = 打印 versions aligned  #4 = 1 hit  #6 = 2 hit
全部通过 = 文档同步 + 备份链路就位,进 §Release Steps。
任何不通过 = 立即修 → 重新跑 §G,直到通过。这条 loop 不允许跳过。
```

## 6. 历史教训 / Lessons from the wreckage

| 发版 | 漏的位置 | 后果 | 修复 |
|---|---|---|---|
| `v2.0.0` 同步 (TASK-010) | `README.zh.md` 停在 `1.2.1` × 4 版 | 中文用户在 GitHub 看到错版本号 | SOP §C 加 `README.zh.md` 行 |
| `v2.0.0` 同步 (TASK-011) | `docs/index.html` essays 停在 06 张 | GitHub Pages 公网"半成品" | SOP §C 加 `docs/index.html` 行 |
| 历版 SOP | `mcp/README.md` 从未单独列出 | 险些把错的 long_description 永久锁进 PyPI | SOP §C 加 ⚠ 警告框 + 单独行 |
| 历版 SOP | 本仓只有 origin 单点,无二级镜像 | 本机磁盘损坏 + GitHub 账户事故 → 仓库灭失 | 2026-05-13 v2.0.0 后建 `FCoP-backup` private 仓 + SOP §阶段 4.5 |
| v2.0.0 SOP §C.3 | `test_server.py` 断言数量措辞"若有"含糊 | 实际 3 处不是 1 处,改版本号易漏改 | TASK-013 精确化到行号 163/182/196 |

这五条踩雷的实际 commit / TASK / REPORT 都在 `fcop/log/` 里,是
**永久 audit trail**——下次想偷懒"差不多就行"的时候,先去翻一眼。

---

> 见也见 / See also:
> - [`RULES-release-file-inventory.md`](RULES-release-file-inventory.md)(配套文件清单)
> - `docs/release-process.md`(SOP 权威源)
> - `fcop/log/reports/REPORT-20260513-011-ME-to-ADMIN.md`(红线 1 源头)
> - `fcop/log/reports/REPORT-20260513-013-ME-to-ADMIN.md`(红线 2 + 元红线源头,待落档)
> - Rule 7(高危 / 不可回滚操作 — PyPI 锁版 + force push 的协议层依据)
> - Rule 0.c(只落真话 — 文档没同步 = 落假话)
