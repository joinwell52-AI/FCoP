---
protocol: fcop
version: 1
kind: shared
prefix: RULES
sender: ME
recipient: TEAM
related: [REPORT-20260513-011, TASK-20260513-012]
thread_key: release-sync-discipline
---

# RULES · 发版前文档同步纪律 / Release-Sync Discipline

> **Scope**: FCoP 自仓发版纪律,不是 FCoP 协议本身的一部分。
> 协议本身已经在 Rule 7(高危 / 不可回滚操作)里覆盖了 PyPI 锁版。
> 本文件只是把它**对 fcop / fcop-mcp 这两个包**的具体落地写清楚,
> 让下一次发版的 agent 巡检 `fcop/shared/` 时一眼能看见。

## ADMIN 红线 / The line ADMIN drew

> **FCoP 在短期内会有很多发版,所以各处的文档一定要同步;发版前不要
> 遗漏,因为 PyPI 不能补发**。
>
> —— ADMIN, 2026-05-13 21:55 +08:00,
> 紧接 REPORT-20260513-011 的反思段被升格为永久纪律。

## 为什么这条要单独立一份(而不是只埋在 SOP 里)

`docs/release-process.md` 是 SOP 权威源,但**发版的 agent 第一巡检
路径是 `fcop_report()` → `fcop/shared/`**,不一定记得 `docs/` 下有个
SOP。把这条红线钉在 `fcop/shared/` 里,任何接手的 agent / 任何一次
`fcop_report()` 后都看得见。

"Files are the protocol. Folders are the organization."(Rule 2):
SOP 在 `docs/`(外部贡献者也读);纪律书在 `fcop/shared/`(团队
内部第一时间看见)。两份指向同一权威源,**避免漂移**。

## 权威源 · 不在这里复制 / Authoritative source — not duplicated here

完整的发版前文档同步清单和扫描命令在:

- **`docs/release-process.md §C 文档层 — 全部同步,PyPI 不可补发`**
  · 12 项 checkbox,分 3 个子段(公网可见 / agent 部署后会读 / hardcoded 断言)
- **`docs/release-process.md §G 发版前文档同步扫描`**
  · 5 条 `rg` 命令,30 秒跑完,任何旧版本号残留立即暴露

发版的 agent 必须**直接读上面两节,不从本文件抄**——本文件可能滞后,
SOP 是单一权威源(Rule 5 历史只增不改,SOP 改了本文件不需要回改)。

## 三条不会变的硬约束 / Three things that won't change

1. **`mcp/README.md` = PyPI `long_description`,锁版** ⚠
   `twine upload` 成功即永久定格——版本号 / 历史段 / 亮点描述错了 /
   漏了,**只能 yank + bump 下一版重发**。Rule 7 适用。
2. **`README.zh.md` 和 `README.md` 同等重要**——历版 SOP 只列前者
   导致 v2.0.0 发版时它停滞在 `1.2.1`(4 个版本前)。两者并列,无主次。
3. **`docs/index.html` = GitHub Pages**——它是项目的脸,流量比 GitHub
   仓库首页 README 都大,version pill / "What is FCoP" / essays-grid
   不同步 = 对外撒谎(Rule 0.c 反面)。

## 自检入口 · 发版前最后 30 秒 / 30-second self-audit

发完 §A–§F(SOP 6 段)之后、敲 `git tag` 之前:

```text
跳到 docs/release-process.md §G,把那 5 条 rg 命令复制下来按顺序跑一遍。
全部 0 hit(除 CHANGELOG 历史段命中可忽略)= 文档同步通过,进 §Release Steps。
任何命中 = 立即修 → 重新跑 §G,直到 0 hit。这条 loop 不允许跳过。
```

## 历史教训 / Lessons from the wreckage

| 发版 | 漏的位置 | 后果 | 修复 |
|---|---|---|---|
| `v2.0.0` 同步 (TASK-010) | `README.zh.md` 停在 `1.2.1` × 4 版 | 中文用户在 GitHub 看到错版本号 | SOP §C 加 `README.zh.md` 行 |
| `v2.0.0` 同步 (TASK-011) | `docs/index.html` essays 停在 06 张 | GitHub Pages 公网"半成品" | SOP §C 加 `docs/index.html` 行 |
| (历版 SOP) | `mcp/README.md` 从未单独列出 | 险些把错的 long_description 永久锁进 PyPI | SOP §C 加 ⚠ 警告框 + 单独行 |

这三条踩雷的实际 commit / TASK / REPORT 都在 `fcop/log/` 里,是
**永久 audit trail**——下次想偷懒"差不多就行"的时候,先去翻一眼。

---

> 见也见 / See also:
> - `docs/release-process.md`(SOP 权威源)
> - `fcop/log/reports/REPORT-20260513-011-ME-to-ADMIN.md`(反思的源头)
> - Rule 7(高危 / 不可回滚操作 — PyPI 锁版的协议层依据)
> - Rule 0.c(只落真话 — 文档没同步 = 落假话)
