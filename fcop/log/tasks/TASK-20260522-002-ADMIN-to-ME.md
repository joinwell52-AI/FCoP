---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P2
subject: LETTER-TO-ADMIN.md 同步至 v3.0.1（重写）
---

## 背景

ADMIN 通过聊天指出 `fcop/LETTER-TO-ADMIN.md` 落后于当前发版（v3.0.1）。该文件 L9 摘要块仍标 `v2.0.0 (2026-05-13)`，正文多处引用 `32 个工具`，且完全未提 v3.0 的「文件夹即状态」纪元、`_lifecycle/` 五桶、State / Event / Boundary Charter 三层规则、`fcop migrate --to-v3` 等核心新概念。

## 授权

- `scope: batch-remediation`
- `batch_id: letter-3.0-sync-20260522`
- `files: [fcop/LETTER-TO-ADMIN.md]`
- 选项：A（口头批量授权）+ C（按 v3.0 视角整体重写），ADMIN 已选 A 确认。

## 核对过的事实（防 0.c 违规）

| 项 | 当前真值 | 来源 |
|---|---|---|
| 当前发版 | 3.0.1（2026-05-21） | `CHANGELOG.md` L11 |
| 上一发版 | 3.0.0（2026-05-21，BREAKING 协议级） | `CHANGELOG.md` L47 |
| MCP 工具数 | 35 | `docs/mcp-tools.md` L1 + L11 |
| 资源数 | 14 | `docs/mcp-tools.md` L12 |
| 规则版本 | `fcop-rules.mdc 3.0.0` / `fcop-protocol.mdc 3.0.0` | 项目内 `.cursor/rules/` frontmatter |
| 本仓 fcop/ 拓扑 | **仍是 v2.x**（tasks/ reports/ issues/ shared/ log/ reviews/，无 `_lifecycle/`） | `dir fcop` |
| v3.0 spec 五桶 | `_lifecycle/{inbox,active,review,done,archive}/` + `reports/` `issues/` `shared/` | `spec/fcop-3.0-spec.md` §1.1 |
| v3.0 7 类 transition | create / claim / submit / finish / approve / reject / archive | spec §1.3 |

> 本仓 `fcop/` **没有** `_lifecycle/`，LETTER 在描述 "起完之后会落下这些东西" 时必须**双轨**写：1) v3.0 init 后的标准拓扑；2) 老仓库（含本仓）仍是 v2.x，可选 `fcop migrate --to-v3` 升级。

## 重写范围（C 方案）

1. 顶部摘要块由「v2.0.0 摘要」整体替换为「v3.0.1 摘要」，提及 v3.0.0 是协议级 MAJOR、引入「文件夹即状态」纪元，v3.0.1 是文档路径修补 patch。
2. 五桶目录段（"起完之后会落下这些东西"）双轨化：v3.0 标准拓扑（`_lifecycle/`）+ 兼容说明（老项目继续工作 + `fcop migrate --to-v3` 升级路径）。
3. 工具数引用 `32 个` → `35 个` 全文替换（含 4 处或更多）。
4. 「四条必读规则」段补充提示 v3.0 的 Rule A / Rule E / Boundary Charter 三层规则集存在（不必铺开讲细节，给指针即可）。
5. 顶部 "协议规则文件升级 / 自动检查" 与底部 "快速命令清单" 二查关键命令是否仍正确（例如 `redeploy_rules` 仍存在）。

## 不在范围

- 不改 `fcop-rules.mdc` / `fcop-protocol.mdc`（那是 fcop 包本身的产物，规则文件只能由 `redeploy_rules` 升）。
- 不改本仓 `fcop/` 实际目录拓扑（升不升 v3 由 ADMIN 另决）。
- 不删除任何历史信息，所有改动按 Rule 5 "append where ambiguous" 做。

## 验收标准

- LETTER 顶部摘要标题 + 日期反映 v3.0.1。
- 全文 grep `32 个工具` / `32 tools` 命中数 = 0。
- 文档至少出现一次：`_lifecycle/`、`文件夹即状态`、`fcop migrate --to-v3`、`Boundary Charter`。
- 无任何关于本仓 `_lifecycle/` 已存在的虚假断言（0.c）。
