---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-013
sender: ADMIN
recipient: ME
priority: P0
risk_level: medium
parent: TASK-20260513-012
related: [TASK-20260513-012, REPORT-20260513-012]
thread_key: release-sync-discipline
session_id: sess-20260513-me-05
---

# "一条龙发版+备份"+ 发版文件分类总清单 —— 协议级严谨

## ADMIN 三条原话(按时间顺序)

1. **22:28** "**一条龙发版+备份!**"
   ——刚确认 FCoP-backup mirror push 完成。

2. **22:31** "**发版本前的各项文件检查;发版本的准备,发版本的备份;
   都要详细;你前面统计那些文件,都要分类记录。**"
   ——要求把散落在 SOP §C/§G/§阶段 4.5 各处的文件枚举,独立成一份
   分类清单,作为长期纪律的物理化沉淀。

3. **22:32** "**如果未来 FCoP 成为一种标准,我们现在要非常认真才行。**"
   ——元红线,凌驾本 TASK 的所有具体产出之上,定位整份工作的态度
   坐标系。

## 设计基调 · "未来标准"级严谨

ADMIN 第 3 条不是新规则,是**态度坐标系**:本 TASK 落下的每一行,
都按"未来某天被一个外部团队、某个 IDE 厂商、某份学术论文引用"的
标准写——

- 命名风格能被外部直接引用(`Inventory §C` 而不是 `release-files-list`)
- 表格结构稳定,字段定义一致,可被工具自动校验
- 每个引用必带精确出处(文件路径 + 行号 / SOP § + 子段),
  禁止"差不多在那一段"(Rule 0.c)
- 双语意识:中文主版优先(团队主语言),en 副版可由后续 TASK 跟进
- 文件本身落 FCoP frontmatter,本身就是 FCoP 协议产物 —— 让协议
  自描述、自审计、自演化(这是 FCoP 区别于 LangGraph/Temporal 的
  关键)

## 三个具体产出

### 1. 主交付:`fcop/shared/RULES-release-file-inventory.md`(新建)

按 **12 类别(A–L)** 罗列发版涉及的全部文件。每类 6 字段固定:

| 字段 | 含义 |
|---|---|
| **类别代号** | A–L,长期稳定,可被外部引用 |
| **类别名(zh / en)** | 双语标题 |
| **描述** | 这一类是什么,为何独立成类 |
| **文件枚举** | 精确路径,不写通配符 |
| **改动义务** | every release / on protocol change / on essay add / on team template change |
| **锁版风险** | none / CDN-cacheable / **PyPI long_description ⚠** / **Git tag ⚠** / Zenodo DOI ⚠ |
| **SOP 对应行** | §C.1 第 N 项 / §G 第 M 条 / §阶段 4.5 |

12 类别(初稿):
- A · 包源版本号(`_version.py` × 2)
- B · 协议规则文件(包内 `src/fcop/rules/_data/*.mdc` + `letter-to-admin.*.md`)
- C · 协议规则镜像(项目根 `.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`)
- D · 公网可见文档(`README*.md` × 3 + `docs/index.html` + `essays/README.md` + `CITATION.cff`)
- E · CHANGELOG(`CHANGELOG.md`)
- F · Hardcoded 断言 / 测试(精确到行号:`server.py:779`、`test_rules.py:104`、`test_server.py:163/182/196`)
- G · ADR(`adr/ADR-*.md` + `adr/README.md` 索引)
- H · 迁移指南(`docs/MIGRATION-*.md`)
- I · 包内样板与团队模板(`src/fcop/rules/_data/teams/` + `fcop/shared/TEAM-*.md`)
- J · CI / Workflow(`.github/workflows/release.yml`)
- K · 备份链路(Git remote `backup` → `joinwell52-AI/FCoP-backup`)
- L · ADMIN 仪式(`.scratch/_*_msg.txt` + `fcop/tasks/` + `fcop/log/`)

### 2. 升级:`fcop/shared/RULES-release-sync-checklist.md`

- 顶部:三条 ADMIN 红线引用块(对应上面 22:28 / 22:31 / 22:32)
- **三硬约束 → 四硬约束**:新增"**一条龙发版+备份**"
- 顶部新增"完整文件清单见 `RULES-release-file-inventory.md`"指针
- 历史教训表加一行 v2.0.0 后建 FCoP-backup 的来龙

### 3. SOP `docs/release-process.md` 校正

- §C 顶部加 inventory 指针
- §C.3 误报修正:`test_server.py` 实际有 **3 处** `"v2.0.0 摘要" in out` 断言
  (行 163 / 182 / 196,Rule 0.c 现场校对发现),SOP 之前写"若有"是
  模糊措辞,精确改为"3 处"
- §C.3 精确化:`server.py:779` 是唯一硬编码版本号位置,SOP 之前
  写"若 init_* 工具回执的 prompt 里写死"是含糊措辞,精确到行号

## 验收标准

- [ ] TASK 升格完成,设计基调段落明确写出"未来标准"级严谨态度
- [ ] `fcop/shared/RULES-release-file-inventory.md` 新建,12 类 6 字段
      全部填实,文件本身带 FCoP frontmatter
- [ ] `fcop/shared/RULES-release-sync-checklist.md` 升级到四硬约束 +
      顶部元红线 + 顶部 inventory 指针 + 历史教训表加 backup 行
- [ ] SOP §C 顶部加 inventory 指针;§C.3 行号精确化
- [ ] ReadLints 干净(本 TASK 不引入 lint 问题)
- [ ] §G 6 条扫描全部通过自检(0 hit + #4 1hit + #6 2hit)
- [ ] **本次自身就是"一条龙"实证** —— 本 TASK + REPORT 的 closure
      commit 必须 push origin → push backup main → push backup --tags,
      在 REPORT 里贴出三方 SHA 字节级一致的输出
- [ ] archive TASK + REPORT,同样走双发

## 设计目标

发版动作的**最后一步必须**是同步 backup remote。任何漏了 backup 同步
的发版都算未完成。具体:

- `docs/release-process.md` §Release Steps 阶段 4 加 **§阶段 4.5 ·
  备份镜像同步**,作为发版"一条龙"的不可分割部分,**append-only push**
  (非 mirror,见下方设计选择)
- `docs/release-process.md` §G 加第 6 条:`git remote -v | Select-String '^backup'`
  扫描 backup remote 仍配置
- `fcop/shared/RULES-release-sync-checklist.md` "三条永久硬约束"扩
  为四条,新增"**发版即备份**"
- 历史教训表加一行:TASK-013 的来龙去脉(为什么本仓需要二级镜像、
  ADMIN 红线的来源)

## 设计选择 · 为什么不用 `--mirror`(防 force push 反备份)

每次发版同步 backup,有两种命令路径:

| 命令 | 行为 | 风险 |
|---|---|---|
| `git push backup --mirror` | 字节同步(包含强制覆盖) | 若 origin 被恶意 force push,backup 同步把破坏过去 → **反备份** |
| `git push backup main` + `git push backup --tags` | append-only,非 force | origin 被 force push → backup push 失败 → **触发警报,备份保住** ✅ |

**SOP 钦定后者**。备份的哲学不是"字节一致",是"**防灾难**"——抗 force
push 是备份层的核心价值,值得为它放弃 mirror 的极简。首次 mirror 已
经完成,之后只 append-only 推。

## 验收标准

- [ ] `docs/release-process.md` §阶段 4.5 就位(2 行命令 + 验证)
- [ ] §G 第 6 条 `backup remote` 扫描就位
- [ ] `fcop/shared/RULES-release-sync-checklist.md` 四条硬约束 + 历史
  教训表加 backup 行
- [ ] **本次自身就是"一条龙"实证** — 本 TASK + REPORT 的 closure commit
  必须 push origin 之后立即 push backup,在 REPORT 里贴出双发输出
- [ ] commit + push origin/main + push backup main + push backup --tags
- [ ] archive TASK + REPORT 同样双发
