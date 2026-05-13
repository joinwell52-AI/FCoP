---
protocol: fcop
version: 1
kind: rules
title: "MCP Registry Release · 三步升级路径(per ADMIN 2026-05-13)"
applies_to: ["fcop-mcp PyPI release + modelcontextprotocol.io registry publish"]
sender: SYSTEM
recipient: TEAM
authority: ADMIN red-line · "一条龙发版+备份" (2026-05-13 22:28 +08:00)
source_chat: TASK-20260513-014 / 同日 ADMIN 23:00 "未来升级路径"指导
session_id: sess-20260513-ME-014
---

# RULES · MCP Registry Release(`fcop-mcp` → `registry.modelcontextprotocol.io`)

> **目的 / Purpose**
>
> 把 ADMIN 在 2026-05-13 23:00 +08:00 给出的"未来升级路径"从聊天窗口
> **落进文件**(Rule 0.a),让未来任何一次 `fcop-mcp` 升级都能复用同一
> 套三步流程,不依赖某个会话的口头传授。
>
> Land ADMIN's "future upgrade path"(given in chat at 2026-05-13 23:00
> +08:00) into a file (Rule 0.a), so every future `fcop-mcp` bump can
> reuse the same three-step procedure without depending on any one
> session's verbal memory.

## 适用范围 / Scope

本文件**只**适用以下场景:

- 升级 `fcop-mcp` 到新版本(`2.0.2` / `2.1.0` / `3.0.0` …)
- 升级后需要让 `registry.modelcontextprotocol.io` 上的
  `io.github.joinwell52-AI/fcop` 记录跟着 bump

**不**适用:
- `fcop` 库独立发版(不进 MCP registry,只走 PyPI)
- MCP registry 名称变更(`io.github.…` namespace 一旦认领固定;
  改名需要重新走 Anthropic OAuth 验证流程)
- 撤回某个版本(MCP registry 没有撤回机制;同 PyPI 不可补发)

完整 12 类清单参见 `RULES-release-file-inventory.md`(本文件覆盖其中 H / M / N 三类)。

## 前提 / Prerequisites(只做一次,以后复用)

| # | 项 | 状态 |
|---|---|---|
| 1 | `mcp/README.md` 顶部第二行有 `mcp-name: io.github.joinwell52-AI/fcop` | ✅ 自 v2.0.1 起 |
| 2 | `mcp/server.json` 存在,符合 modelcontextprotocol.io schema | ✅ 自 v2.0.1 起 |
| 3 | 项目根有 `mcp-publisher.exe`(Windows)或 `mcp-publisher`(Unix) | ✅ ADMIN 已下载 |
| 4 | ADMIN 在 mcp-publisher 上已通过 GitHub OAuth 认领 `io.github.joinwell52-AI/*` namespace | ✅ token 有效期长 |

任一不满足 → **不要**走本流程,先按 `mcp/README.md` v2.0.2 章节 + modelcontextprotocol.io 文档把前提补齐。

## 三步升级 / Three-step upgrade

### Step ① · 改三处版本号(`agent` 可做)

```powershell
# 1. fcop-mcp 包版本(单一真相源)
# 编辑 mcp/src/fcop_mcp/_version.py
__version__ = "X.Y.Z"   # ← 改这一行

# 2. mcp/server.json 两处 version(顶层 + packages[0].version)
# 编辑 mcp/server.json
{
  "version": "X.Y.Z",                  # ← 顶层
  "packages": [
    {
      "version": "X.Y.Z",              # ← packages[0]
      ...
    }
  ]
}
```

> **lockstep 决策**:`fcop` 主库要不要同步 bump?
> - **要**(推荐,per ADR-0002 + v2.0.2 决策 1 · A):同时改 `src/fcop/_version.py`,
>   并在 CHANGELOG 写"双包 lockstep"注脚。
> - **不要**:在 CHANGELOG 显式声明"`fcop-mcp` 单独 bump,`fcop` 保持 X.Y.Z"。
>
> 决策本身需要落 FCoP 账本(`TASK-*` 文件),不在本 RULES 里钦定。

### Step ② · 构建 + PyPI 上传(`ADMIN` 手工,需 PyPI token)

```powershell
# 在项目根
cd mcp
python -m build
python -m twine upload --disable-progress-bar dist/fcop_mcp-X.Y.Z*

# 如果双包 lockstep,在另一终端
cd <项目根>
python -m build
python -m twine upload --disable-progress-bar dist/fcop-X.Y.Z*
```

**红线**(本步骤受 `RULES-release-sync-checklist.md` 硬约束 1 ·"PyPI 不可补发"):
- 上传前**最后一次**核对 `mcp/README.md`(PyPI long_description)写对了
- 上传成功后 X.Y.Z 永久存在,**不能撤回 / 不能补传**
- 旧的 X.Y.Z-1 仍在 PyPI,客户端可显式 pin

### Step ③ · 注册表 publish(`ADMIN` 手工,需 GitHub OAuth)

```powershell
# 在项目根
.\mcp-publisher.exe publish

# 期望输出:
# ✓ Server io.github.joinwell52-AI/fcop version X.Y.Z
#   registry.modelcontextprotocol.io
```

注册成功后,下游聚合器(PulseMCP 等)会**自动**抓取,不需要再做任何事。

**红线 token 维护**:
- GitHub OAuth token 有效期较长(月级),正常不会过期
- 提示"token expired" → `.\mcp-publisher.exe login` 重新走一次 OAuth
- 不要把 token 写进任何文件 / commit / chat 记录(SOP 隐式约束)

## 不要忘的"一条龙最后一里" / Don't skip the backup leg

按 `RULES-release-sync-checklist.md` 硬约束 4 ·"一条龙发版+备份",
Step ③ 完成后**必须**:

```powershell
# 让 backup 镜像跟上 origin(append-only)
git push backup main
git push backup --tags

# 三方 SHA 一致性核验
$tag = "vX.Y.Z"
$originSha = (gh api "repos/joinwell52-AI/FCoP/git/refs/tags/$tag" | ConvertFrom-Json).object.sha
$backupSha = (gh api "repos/joinwell52-AI/FCoP-backup/git/refs/tags/$tag" | ConvertFrom-Json).object.sha
if ($originSha -eq $backupSha) { Write-Host "[OK] backup tag $tag aligned" }
```

完整细节见 `docs/release-process.md §阶段 4.5`。

## 失败回退 / Failure recovery

| 失败点 | 现象 | 回退动作 |
|---|---|---|
| Step ② PyPI 上传 | `twine upload` 报 403 / 网络 / 版本号冲突 | 同 `RULES-release-sync-checklist.md`;PyPI 不可补发,所以**改版本号**重来(`X.Y.Z` → `X.Y.Z+1`)|
| Step ② 上传一半中断 | 一个包成,另一个没成 | 已成的不可撤;另一个改下一个版本号重传 |
| Step ③ publish 失败 | `mcp-publisher` 报错 | PyPI 版本仍可用(用户能 `pip install fcop-mcp==X.Y.Z`),只是 registry 停留在旧版本;另起 hotfix 任务专门补 registry,不需要再上 PyPI |
| Step ③ token 过期 | `unauthorized` | `.\mcp-publisher.exe login` → 重新 `publish` |
| 一条龙最后一里漏做 | `backup` 落后 `origin` | 立即 `git push backup main && git push backup --tags`,验证三方 SHA 一致 |

## 变更日志 / Change log

- **2026-05-13** · v1.0 落档(本文件首版)。来源:ADMIN 在 TASK-014 上下文
  给出的"三步升级路径";同期把 `mcp-publisher.exe publish` 第一次实战
  (`fcop-mcp@2.0.1` → `2.0.2`)的过程吸收为规则。Witness:
  `fcop/log/tasks/TASK-20260513-014-*.md`、`registry.modelcontextprotocol.io`
  公开 listing。

## See also

- `RULES-release-file-inventory.md` § H / M / N(MCP registry 路径相关 3 类)
- `RULES-release-sync-checklist.md` § 4(一条龙发版+备份硬约束)
- `docs/release-process.md` § 阶段 4.5(备份镜像同步)
- `mcp/README.md`(PyPI long_description,v2.0.2 章节是本文件的对外说明)
- `mcp/server.json`(MCP registry schema 实例)
