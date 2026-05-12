---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260512-001
sender: ADMIN
recipient: ME
priority: P0
risk_level: high
status: done
thread_key: fcop-mcp-binding-guard-20260512
session_id: sess-20260512-me-01
---

# fcop-mcp 1.4 · Write-side 工具 binding 守门 + USER HOME deny-list (P0 fix)

## 背景 / Motivation

2026-05-12 15:35:06,Bridgeflow PM 在 `redeploy_rules()` 操作前未调
`set_project_dir()`,触发 fcop-mcp 当前默认行为 ——**用 MCP 进程的
cwd 兜底**。该进程 cwd = `C:\Users\Administrator\`(USER HOME),
导致 4 件协议文件(`.cursor/rules/fcop-rules.mdc` /
`fcop-protocol.mdc` / `AGENTS.md` / `CLAUDE.md`)**全局落到 USER
HOME**,污染该机器上**所有 cursor 项目**。

PM 自检发现 + 备份 + 删除 + 重绑定 + 重跑,ADMIN 独立验证 USER HOME
0 残留 + 4 件备份 sha256 齐 = 事件**已完整闭环**,污染**已 0 残留**。

完整时间线 + 证据链见 PM-01 汇报(2026-05-12 15:38 + 15:42 UTC+8),
归档路径 `D:\Bridgeflow\.scratch\pm50-user-home-pollution-20260512-1535\`。

PM 提了 9.2 v2.5 v1.6 自约束(MCP-server-cwd-awareness),归类为
"PM 操作纪律新维度"。**但归因偏轻** —— 真正的根因是 fcop-mcp 的
**P0 设计缺陷**:write-side 高破坏力工具在没有显式 binding 时**默认
用 cwd 兜底**,等价于让 `rm -rf` 在没指定路径时默认在 `/` 上跑。

`set_project_dir` 的 schema 里**有警告**:

> "typical symptom: unbound_report shows a project path like
> C:\\Users\\<you>"

但只是 schema 注释,**没有硬守门**。协议方默认 agent 会主动读 schema
警告 = 又一次"协议 = 环境"失守(schema 在协议定义里有警告,但 PM 操
作前没接触到)。

## 任务 / Deliverables

修 fcop-mcp,让以下行为成为**协议层硬约束**:

### D1 · Write-side 工具 explicit binding 守门

**所有 write-side MCP 工具**(下面 ≥ 8 个)在未 explicit bind 项目根时
**直接 ConfigError,不允许默认 cwd 兜底**:

候选清单(待 OPS 在实现时枚举确认):

- `redeploy_rules()`
- `deploy_role_templates()`
- `init_project()` / `init_solo()` / `create_custom_team()`
- `new_workspace()`
- `write_task()` / `write_report()` / `write_issue()` /
  `write_review()`
- `archive_task()`
- `mark_human_approved()`
- `report_failure()`
- `drop_suggestion()`

ConfigError 错误文案模板:

```
WriteRefused: <tool_name> requires an explicitly bound project
root, but no binding is active. Call set_project_dir(path=...)
first, or restart the MCP server with cwd set to the project root.
This guard exists to prevent USER HOME pollution
(see fcop-mcp v1.4 release notes).
```

### D2 · USER HOME / system root deny-list

即使绑定了,如果 `project_dir` 解析到以下路径之一,**直接拒绝**:

- `%USERPROFILE%`(Windows)
- `~`(展开后的 home,跨平台)
- `/`(Unix root)
- 任一 drive letter root(`C:\` / `D:\` / …,Windows)
- `%PROGRAMDATA%` / `%APPDATA%` / `%LOCALAPPDATA%`
- `/etc` / `/usr` / `/opt`(Unix system roots)

ConfigError 错误文案模板:

```
WriteRefused: project_dir resolved to a protected system path
(<path>). FCoP write-side tools refuse to operate at this scope
to prevent global pollution. Bind to a project subdirectory
instead.
```

### D3 · `fcop_report()` 顶部 project_path 红字告警

`fcop_report()` 输出的报告首段加一段:

```
当前 project_path: <abs_path>
```

如果 `<abs_path>` 落在 D2 deny-list 内,加红字告警:

```
⚠️  WARNING: project_path is set to a protected system path.
    Any write operation will be refused. Run set_project_dir(...)
    to bind to a real project root.
```

### D4 · 现有 schema 警告升级为机器可读 `binding_required: true`

`set_project_dir` 的 schema 文档警告**保留**,但**所有 write-side 工具
的 schema** 加机器可读字段:

```yaml
binding_required: true
allowed_project_dir_class: "real_project_root"  # not system root
```

这给上层 orchestrator(Cursor / Claude Code / Devin)一个机器可读的
hook,知道"这个工具不能在 unbound 状态下调"。

### D5 · 测试用例(必须覆盖)

- 单测:每个 write-side 工具在 unbound 状态下调用 → ConfigError(D1)
- 单测:绑定到 USER HOME → ConfigError(D2)
- 单测:绑定到 drive root → ConfigError(D2)
- 单测:绑定到合法 project dir → 正常工作
- 集成测:模拟 PM #50 路径(MCP cwd = USER HOME,直接调 `redeploy_rules`)
  → ConfigError 不写盘(D1 兜底 D2 deny-list)
- 回归:已有 fcop-mcp 测试套件全部仍 GREEN

### D6 · Release notes + 升级提示

- `docs/releases/1.4.0.md` 加 "Breaking-ish behavior change"
  小节,说明 unbound 调用从"静默成功"变成"ConfigError",老脚本
  可能需要先调 `set_project_dir`
- `fcop_report()` 检测到 fcop-mcp 版本 < 1.4 时,底部加升级提醒

## 验收标准 / Acceptance Criteria

1. **D1 实施**:write-side 工具清单确定 + 全部加 binding 守门 + 错误
   文案落实
2. **D2 实施**:deny-list 跨 Windows / Unix 覆盖 + 测试通过
3. **D3 实施**:`fcop_report()` 顶部告警可视化
4. **D4 实施**:schema `binding_required: true` 字段落实
5. **D5 实施**:测试套件 6 类用例全 GREEN
6. **D6 实施**:release notes 写完 + 升级提醒接通
7. **PM #50 复现测试**:在干净环境模拟 PM 当时的 cwd / 调用序列 →
   工具拒绝写盘,USER HOME 仍然 0 文件

## 风险 / 回滚

- **风险 R1**:Breaking-ish 行为变化可能打到老脚本(已有用户脚本可能
  靠 cwd 兜底跑)。**缓解**:release notes 显式标 breaking,提供
  迁移指南
- **风险 R2**:D2 deny-list 在 macOS / Linux 上的 home 路径检测可能
  误伤(用户把项目放在 home 下子目录是合法的)。**缓解**:只拒绝
  **精确等于** home 的情况,子目录放行
- **回滚**:本次 fix 是新增守门,如果发现严重副作用,降级回
  v1.3.x 即可,无数据损失

## 与其他协议工作的关系

- **不阻塞** Bridgeflow §5 A 路径(PM 那边 commit 30 件 + QA verdict
  互不冲突)
- **与 ADR-0033(Rule 2 升级场景操作化)是同源洞察** —— "操作姿势
  规约"那一节会引用本次 fix 作为 motivation
- **与 ADR-0034(Task Naming Topic Slug)互不相关**

## 状态机

- `proposed`(本文件落盘时)→ 等 ADMIN GREEN
- `accepted` → ME 开工实施
- `done` → 写 REPORT-001-ME-to-ADMIN.md + archive

---

**请 ADMIN 决**:

- (A) **批准推进**,ME 立即开工(预计 2~3 小时完成 D1~D5,D6 同步)
- (B) **调整范围** —— 比如 D2 deny-list 想加 / 减项,或 D6 升级提醒
  想另起 TASK
- (C) **拒绝/延后** —— 等 v1.4 整体节奏一起,或者拆成多个 TASK 逐
  步上(PM #50 已止血,理论上可以慢慢做)

我推荐 (A) —— 这是 P0 安全 bug,污染过一次说明触发条件不罕见;在
fcop-mcp 1.4 之前每一天 unbound write 都是潜在事故。

— ME, 2026-05-12 15:46 (UTC+8)
