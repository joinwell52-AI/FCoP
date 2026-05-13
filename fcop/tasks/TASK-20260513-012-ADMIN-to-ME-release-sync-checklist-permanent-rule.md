---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-012
sender: ADMIN
recipient: ME
priority: P0
risk_level: medium
parent: TASK-20260513-011
related: [TASK-20260513-010, TASK-20260513-011, REPORT-20260513-011]
thread_key: release-sync-discipline
session_id: sess-20260513-me-04
---

# 把"发版前文档全同步"升级为永久规则(SOP §C 扩展 + 本仓纪律书)

## 背景 / ADMIN 原话

> FCoP 在短期内,会有很多的发版,所以各处的文档,一定要同步;
> 发版前不要遗漏,因为 PYPI 不能补发;
> ——ADMIN, 2026-05-13 21:55 +08:00

这是把 REPORT-20260513-011 末尾的"反思"段(本是我对自己 0.c 反面教材的
内部检讨)**升格为面向所有未来发版的程序性约束**。

## 现状盘点

`docs/release-process.md` 已是 v1.6.0 起的 SOP,§Pre-Release Checklist
A–F 段已覆盖代码 / 测试 / 文档 / Git / P=E / Rule 0.a.1 闭环。但 §C
文档层(L84–L106)对照过去 2 次发版实际踩雷的位置,**漏列 5 处**:

| 缺漏项 | PyPI 不可补发? | 触发它的踩雷次 |
|---|---|---|
| `README.zh.md` | 否 | TASK-010(发现时停在 `1.2.1` × 4 个版本) |
| **`mcp/README.md`** | **是** = PyPI `long_description`,版本号一旦发即永久定格 | 险些漏(被 TASK-010 抓住) |
| `docs/index.html` | 否(GitHub Pages,流量大) | TASK-011("半成品做完") |
| `essays/README.md` | 否 | 加新 essay 后停滞 |
| `CITATION.cff` | 否 | 一般不动但 v2 须扫 |

## 改动计划

### A · `docs/release-process.md` 主修(单文件,SOP 权威源)

A1. **§C 文档层 标题升级 + 警告段**:
    标题改为 `C. 文档层 / Docs — 全部同步,PyPI 不可补发`。
    第一段加突出框:**`mcp/README.md` = PyPI long_description,发版即永久
    定格**(PyPI 规则 unique-per-version,等同 Rule 7 不可回滚)。

A2. **§C 拆 3 个子段**,把当前 7 项 + 新增 5 项分组:
    - **C.1 · Visible-on-the-web 类**(读者最多,bump 漏=对外撒谎):
      `README.md` / `README.zh.md` / **`mcp/README.md`**(PyPI 锁版,标红) /
      `docs/index.html`(GitHub Pages)/ `essays/README.md`(若加 essay)/
      `CITATION.cff`(若需要)
    - **C.2 · Agent-touch 类**(agent 部署后会读到):
      `letter-to-admin.zh.md` / `letter-to-admin.en.md` /
      `fcop-rules.mdc` 协议版 / `fcop-protocol.mdc` 协议解释版 /
      `CHANGELOG.md` 新版块
    - **C.3 · Hardcoded 断言类**(测试和 server 里写死的字符串):
      原 SOP "3 处 hardcoded 字符串" + ADR `Status: Accepted`
      检查 / `docs/MIGRATION-*.md`(若本版改了迁移路径)

A3. **§G 新增 · 发版前文档同步扫描 / Pre-Release Documentation Sync
    Audit**:
    在 §F Rule 0.a.1 Carrier 之后、§Release Steps 之前插入一个 30 秒
    "扫一眼"命令清单。一条 `rg` 把所有面向公众的位置扫一遍,任何
    残留的"旧版本号"立即可见,这是 ADMIN 这条规则的**自动化检查
    入口**:

    ```powershell
    # 扫所有面向公众文档里是否还含上一版号(应为 0 hit)
    rg --hidden -g '!.git' -g '!fcop/log' -g '!*.lock' '\b1\.6\.0\b'
    # 扫 fcop/fcop-mcp 包元数据里是否对齐
    py -3.10 -c "import importlib.metadata as m; print(m.version('fcop'), m.version('fcop-mcp'))"
    # 扫 PyPI 上一版本号有没有意外残留在 README × 3
    rg -e 'Current release: `v1\.6\.0`' -e 'v1\.6\.0' README.md README.zh.md mcp/README.md
    ```

    grep 命中 = 漏了,立即修;0 命中 = 通过。

### B · `fcop/shared/RULES-release-sync-checklist.md`(新建,本仓纪律书)

把 ADMIN 这句话作为**协议级红线引文**钉在文件顶部,然后**只放指针**指向
`docs/release-process.md §C / §G`(避免两处冗余、避免漂移)。

这份文件的存在价值是:**下一次发版的 agent 在 `fcop/shared/` 巡检时
能一眼看见这条纪律**,而不是要先翻 `docs/` 目录才找得到。
"文件即协议,文件夹即组织"。

### C · 不在本任务范围

- 把 §C "3 处 hardcoded 字符串"做成 `scripts/check_release_docs.py`
  自动化 lint(SOP §Automation Roadmap TODO 4 项)。这是更大工作,
  另立 TASK。本次先**把 checklist 落到位**;自动化是下一阶段。
- 改 FCoP 协议本身(`fcop-rules.mdc` / `fcop-protocol.mdc`)。这是
  本仓的发版纪律,不是协议层问题。Rule 7 已经覆盖"破坏性 / 不可
  回滚操作 = 必走 ADMIN 二次确认",PyPI 锁版本身就属于 Rule 7
  适用范围,不需要新规则。

## 验收标准

- [ ] `docs/release-process.md` §C 三段拆完,12 项 checkbox 齐 + PyPI
  不可补发警告框就位
- [ ] `docs/release-process.md` §G 新增,30 秒文档同步扫描命令清单到位
- [ ] `fcop/shared/RULES-release-sync-checklist.md` 新建,引文 + 指针
- [ ] 改动只在上述 2 个文件 + 本 TASK + 配套 REPORT 内
- [ ] commit + push origin/main
- [ ] 写 REPORT-20260513-012 + archive

## Rule 0.c 自审承诺

REPORT-20260513-012 末尾必须按 Rule 0.c **直话**记一笔:本任务的来源
就是 REPORT-011 的反思被 ADMIN 升格成永久规则——既是 0.c "落真话"的
成功兑现(反思真的进入了改动),也是 0.c "下次怎么不再翻车"的具体落地。
