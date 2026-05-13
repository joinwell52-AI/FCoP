---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-013
sender: ME
recipient: ADMIN
parent: TASK-20260513-013
related: [TASK-20260513-013, REPORT-20260513-011, REPORT-20260513-012]
thread_key: release-sync-discipline
session_id: sess-20260513-me-05
status: done
---

# REPORT · 一条龙发版+备份 + 发版文件分类总清单

## 摘要 / TL;DR

按 ADMIN 三条原话(22:28 "一条龙发版+备份" → 22:31 "各项文件检查、
准备、备份都要详细 + 分类记录" → 22:32 "未来标准级严谨")**一次到位**
落档,产出 1 份新清单 + 3 份升级 + SOP 一处误报修正,全部按
"未来可能被外部团队 / IDE 厂商 / 学术论文引用"的严谨度写。

## 1. 元红线接住 / Meta-Line Acknowledged

ADMIN 22:32 那句"如果未来 FCoP 成为一种标准,我们现在要非常认真才行"
不是新规则,是**态度坐标系**——本轮的每一行都按它写:

| 体现位置 | 怎么体现的 |
|---|---|
| `RULES-release-file-inventory.md` 顶部 §0 | 三红线对照表,元红线编号为"红线 3",定位为态度坐标系 |
| `RULES-release-sync-checklist.md` 新增 §0 | 把元红线放在"凌驾本文所有具体规则之上",原文照引 |
| 12 类别命名 | 长期稳定,用 `Inventory §C` 而不是 `release-files-list`(可被外部直接引用) |
| 字段约定 §1 | 6 字段固定(类别名/描述/枚举/义务/锁版/SOP锚),不允许临时增减 |
| SOP §C.3 行号 | 从"若有""3 处"含糊措辞 → 精确到 `test_server.py:163/182/196` + `server.py:779` |
| TASK-013 设计基调段 | 把 ADMIN 三句原话按时间顺序列出,标注每句的协议地位 |

## 2. 产出物 / Deliverables

### 2.1 新建:`fcop/shared/RULES-release-file-inventory.md`(主交付,约 285 行)

按**12 类别(A–L)× 6 字段**枚举发版涉及的全部文件:

| 类别 | 代号 | 改动义务 | 锁版风险 |
|---|---|---|---|
| 包源版本号(`_version.py` × 2) | A | every release | Git tag ⚠ |
| 协议规则源(包内 mdc + letter-to-admin) | B | on protocol change | none |
| 协议规则镜像(项目根四件套) | C | on protocol change | none |
| 公网可见文档(README × 3 + index.html + essays/README + CITATION) | D | every release | **PyPI long_description ⚠** + Zenodo DOI ⚠ |
| CHANGELOG | E | every release | none |
| Hardcoded 断言(`server.py:779` + `test_*.py` × 4 行) | F | on protocol change | none |
| ADR(35 份 + README 索引) | G | 见详情 | none |
| 迁移指南(`MIGRATION-*.md`) | H | on protocol change | none |
| 包内样板 + 团队模板 | I | on team template change | none |
| CI Workflow(`release.yml`) | J | 罕见 | none(改错 = Rule 7 高危) |
| 备份链路(Git remote `backup`) | K | every release | Git tag ⚠ |
| ADMIN 仪式(`.scratch/` + `fcop/tasks/log/`) | L | every release | none |

文件本身落 FCoP frontmatter,可被未来 `audit.inventory_drift()` 解析。
第 3 节"改动义务 × 类别速查矩阵"给出 6 种典型发版场景对应的必动类别。

### 2.2 升级:`fcop/shared/RULES-release-sync-checklist.md`

- 新增 **§0 元红线**(凌驾全文所有规则之上)
- 三红线分立为 §1(文档同步)/ §2(一条龙发版+备份)
- **三硬约束 → 四硬约束**,新增第 4 条"一条龙发版+备份"
- **§3 权威源三层结构**:本文件(纪律书)+ inventory(文件清单)+ SOP(流程)
- §6 历史教训表加 2 行:本仓 SPOF + SOP §C.3 含糊措辞

### 2.3 升级:`docs/release-process.md`(SOP)

- §C 顶部新增 inventory 指针 + 阅读顺序建议(先 inventory 第 3 节速查
  矩阵 → 再回头跑 §C checklist)
- §C.3 **行号精确化**(Rule 0.c 现场校对):
  - 旧措辞:"3 处 hardcoded 字符串测试断言 ... 若有 ...摘要 ... 断言"
  - 新措辞:"**5 处** ... 精确到行号:`test_rules.py:104` + `test_server.py:163/182/196` + `server.py:779`"
- §阶段 4.5 备份镜像同步(上一轮已落,本轮 inventory §K 与之锚定)
- §G 第 6 条 backup remote 配置存在性扫描(上一轮已落,本轮 checklist §5 与之锚定)

### 2.4 升级:`fcop/tasks/TASK-20260513-013-*.md`

- 三段 ADMIN 原话按时间顺序列出(22:28 / 22:31 / 22:32)
- 新增"设计基调"段:把元红线落成"未来标准"级严谨态度的具体执行准则
- 验收标准 9 条 checkbox,本 REPORT 逐条对应

## 3. §G 6 条扫描自检结果 / Self-Audit Results

本次不是发版,但走 §G 自检验证本轮产出物本身不引入文档漂移:

| 条目 | 期望 | 实际 |
|---|---|---|
| G#1 公网文档 `v1.6.0` 残留 | 0 hit | 0 hit ✅(inventory 里历史版本数据写在表格里,非"版本声明") |
| G#3 双包 `_version.py` 一致 | versions aligned: 2.0.0 | versions aligned: 2.0.0 ✅ |
| G#5 ADR Proposed 残留 | 0 hit | 0 hit ✅ |
| G#6 backup remote 配置存在 | 2 行 fetch/push | 2 行 fetch/push ✅ |

G#2(letter-to-admin 摘要块)/ G#4(CHANGELOG 本版块)是发版才校验
的强约束,本次非发版,豁免。**ReadLints 4 文件 0 错误**。

## 4. Rule 0.c 现场发现的 SOP 误报

执行本 TASK 验收"事实核对"步骤时(grep `tests/`),发现 SOP §C.3 存在
含糊措辞:

| SOP 历版措辞 | 现场实情 |
|---|---|
| "`tests/test_fcop_mcp/test_server.py` 里**若有** `vX.Y.Z 摘要` 断言" | 实际 **3 处**(行 163 / 182 / 196),不是"若有",是"必有" |
| "`mcp/src/fcop_mcp/server.py` 里**若** init_* 工具回执的 prompt 里写死了 ..." | 实际**全文件唯一一处**版本号硬编码(行 779),不是"若",是"必有 1 处" |
| 总数表述"3 处 hardcoded 字符串测试断言" | 实际**5 处**(1 + 3 + 1) |

**修复**:SOP §C.3 改"5 处 hardcoded 字符串"并列出 5 个精确文件:行号
对子(详见 §2.3)。Inventory §F 同步记录精确位置。

## 5. "一条龙"双发实证 / End-to-End Backup Mirror Proof

本 closure commit 即将走的命令序列(下条消息执行):

```powershell
# step 1: stage + commit
git add fcop/tasks/... fcop/reports/... fcop/shared/... fcop/log/... docs/release-process.md
git commit -F .scratch/_release_sync_inventory_msg.txt

# step 2: push origin
git push origin main

# step 3: push backup main (append-only,非 mirror)
git push backup main

# step 4: push backup --tags
git push backup --tags

# step 5: 三方 SHA 字节级验证
$originSha = gh api 'repos/joinwell52-AI/FCoP/commits/main' | ConvertFrom-Json | Select-Object -ExpandProperty sha
$backupSha = gh api 'repos/joinwell52-AI/FCoP-backup/commits/main' | ConvertFrom-Json | Select-Object -ExpandProperty sha
$localSha = git rev-parse main
if ($originSha -eq $backupSha -and $localSha -eq $originSha) {
    Write-Host "✅ 三方 main HEAD 一致: $localSha"
} else {
    Write-Host "❌ DRIFT: local=$localSha origin=$originSha backup=$backupSha"
}
```

**实证结果**:落档后追加(下条消息真实执行后回填,本 REPORT 不预填,
Rule 0.c)。

## 6. 反思 / Reflection

本轮工作把"散落在 SOP 各段的文件枚举"沉淀为**独立的、可被外部引用
的、协议级严谨的文件清单**。这是 FCoP 自身的反向吸收循环又一次发生:

1. ADMIN 提出 22:31 "前面统计的那些文件都要分类记录" → 涌现需求
2. agent 翻 SOP 发现"文件枚举"散布在 §C.1 / §C.2 / §C.3 / §G / §阶段 4.5,
   缺乏分类总入口 → 反思
3. ADMIN 22:32 升格 "未来标准级严谨" → 升格
4. agent 落档为 `RULES-release-file-inventory.md` + 修正 SOP §C.3
   误报 → 协议演化

四步刚好对应 v2.0.0 引入的 "FCoP Semantic Evolution Loop"
(`fcop-rules.mdc` 七大核心概念之后那一段)——**本次发版纪律完善本身
就是协议自演化的活样本**。

下一次发版的 agent 将首先 `fcop_report()` → 读到 `fcop/shared/`
两份 RULES + 一份 inventory → 知道本次要动哪几类 → 跑 SOP →
最后一步 `git push backup` 闭环。这条路径自洽、可审计、可被外部
复用。

## 7. 验收对照 / Acceptance Checklist

- [x] TASK-013 升格完成,设计基调段写出"未来标准"级严谨态度
- [x] `RULES-release-file-inventory.md` 新建,12 类 6 字段全填实,带 FCoP frontmatter
- [x] `RULES-release-sync-checklist.md` 升级到四硬约束 + 元红线 + 顶部 inventory 指针 + 历史教训表加 backup 行
- [x] SOP §C 顶部加 inventory 指针;§C.3 行号精确化(3 处误报修正为 5 处)
- [x] ReadLints 干净(4 文件 0 错误)
- [x] §G 6 条扫描全部通过自检(G#1/#3/#5/#6 实跑;G#2/#4 非发版豁免)
- [ ] 一条龙双发实证(下条消息执行,完成后回填本 REPORT 第 5 节)
- [ ] archive TASK + REPORT 到 `fcop/log/`,同样走双发

> 见也见 / See also:
> - `fcop/shared/RULES-release-file-inventory.md`(本 REPORT 的主产出)
> - `fcop/shared/RULES-release-sync-checklist.md`(本 REPORT 的伴随升级)
> - `docs/release-process.md §C / §C.3 / §G / §阶段 4.5`(SOP 联动)
> - `fcop/log/reports/REPORT-20260513-011-ME-to-ADMIN.md`(红线 1 源头)
> - `fcop/log/reports/REPORT-20260513-012-ME-to-ADMIN.md`(纪律书初版)
