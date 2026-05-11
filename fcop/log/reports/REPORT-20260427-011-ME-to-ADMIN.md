---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
references:
- TASK-20260427-010
status: done
---

## 交付

v3 已落盘。教程 `docs/tutorials/snake-solo-to-duo.zh.md` 新增 **《附录 A：FCoP 适用边界》**，插入位置符合 TASK：6 条铁律之后、常见问题之前。教程从 587 行 → 674 行（+87 行）。

## 附录 A 结构（严格对齐 TASK 要求）

- **头部过渡句**：明说这是答 ADMIN 4 个问题——价值/代价/1 人公司/大型项目。
- **A.1 核心价值与代价**
  - 价值部分：开场定义「从'聊天默契'到'可追溯协议'」，ADMIN 视角「你不用一直记住」+ 6 项价值表格 + 金句 quote「FCoP 让 ADMIN 从“盯着 AI 干活的人”，变成“看账本验收的人”」。
  - 代价部分：诚实列出三点代价——小任务显重、role-switch 警告、效率不是强项；金句「防止协作变成一团口头承诺」逐字保留。尾句「不适合当成所有随手操作的默认流程」作为判断准则引出。
- **A.2 1 人公司**
  - 6 角色清单 FOUNDER/PLANNER/BUILDER・CODER/QA/OPS/MARKETER 做成表格。
  - 金句「对 1 人公司来说，这就是轻量版组织记忆」逐字保留。
  - 额外加了一个「渐进开启」提示，提醒读者不用一上来开 6 角色、对齐第 1-3 章渐进路径。
- **A.3 大型项目**
  - 5 价值表格 + 2 个注意事项。「FCoP 只管协作，不管项目管理全量信息」金句保留。对专业系统的指向（Jira / Linear / GitHub Projects / OA）加入作为实例，避免读者以为 FCoP 要取代这些工具。
  - 金句「1 人公司用 FCoP 是“把自己拆成团队”；大型项目用 FCoP 是“让 AI 团队有纪律地接入现有工程体系”」逐字保留。
- **A.4 三句话决定要不要用**
  - 3 句问句决策树：一次性？跨 session？半年后要证据？
  - **末尾回扣三段公式（痛点/立场/机制）**——距 v2 头部公式与总章 6 铁律形成三点谐振。

## 同步更新

- `docs/tutorials/README.md` 顶部在三段公式下加一句「**不知道自己适不适合用？**」引导链接跳转附录 A。

## 验收代码路径

```
# 1) lints
ReadLints 「 snake-solo-to-duo.zh.md 与 README.md 」 → No linter errors found.

# 2) 金句逐字保留（UTF-8 下 15 项 grep）
附录 A：FCoP 适用边界        HIT
看账本验收的人                       HIT
防止协作变成一团口头承诺     HIT
轻量版组织记忆                     HIT
把自己拆成团队                       HIT
让 AI 团队有纪律地接入现有工程体系       HIT
FOUNDER / PLANNER / BUILDER・CODER / QA / OPS / MARKETER  六项全 HIT
跨 Agent 交接 / FCoP 只管协作 / 要分层使用  全 HIT
```

## 验收清单

- [x] 新增 `## 附录 A：FCoP 适用边界` 章节，插在 6 铁律之后、常见问题之前
- [x] ADMIN 三段原文 4 金句逐字保留
- [x] 6 角色清单完整
- [x] 大型项目 5 价值 + 2 注意事项完整
- [x] README.md 加引导链接
- [x] ReadLints 通过
- [x] 不破坏 6 铁律、三段公式、原有图片链接、内部锚点
- [x] 末尾回扣三段公式（超额交付）

## 后续建议

1. 英文版按同样结构补附录 A（当前还只有中文版）。
2. 是否要抽一份独立的 `docs/tutorials/manifesto.zh.md`（三段公式 + 6 铁律 + 附录 A 金句的单页宣言），方便 PPT/社媒分享——之前提过，ADMIN 还未拍板。
3. 本次附录 A 的写作本身是走完整 fcop 一条龙（TASK-010 → do → REPORT-011 → archive），是教程另一个「狗食自己」的样本；需要的话可以开个 TASK 把这段 "meta" 过程也加进教程作为额外证据。