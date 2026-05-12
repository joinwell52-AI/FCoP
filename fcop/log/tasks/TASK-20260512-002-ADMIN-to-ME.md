---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260512-002
sender: ADMIN
recipient: ME
priority: P0
risk_level: high
status: done
parent: TASK-20260512-001
thread_key: fcop-mcp-binding-guard-20260512
session_id: sess-20260512-me-01
---

# 追加 TASK-001 范围 · 三项细化

## 关系 / Relation

**修正自 / Refines** `TASK-20260512-001-ADMIN-to-ME.md`(fcop-mcp 1.4
write-side 守门 P0 fix)。

不是 supersede,是 **append**:TASK-001 主体范围仍然有效,本 TASK 在
其基础上**追加 3 项细化**。两份 TASK 一起读 = 最终范围。

ADMIN 输入时间:2026-05-12 15:58 (UTC+8)。

## 新增 / 细化项

### S1 · 写入前 project_dir 验证(P0,细化 D1)

**TASK-001 D1 的扩展**:不仅要求 `set_project_dir()` 已调用,还要求
**resolved project_dir 内确实存在 `fcop.json`**(或 `fcop/fcop.json`,
按协议默认布局),否则 reject。

行为:

```
write-side 工具被调用
    ↓
检查 1: project_dir 已 bind? → 否 → ConfigError (TASK-001 D1)
    ↓ 是
检查 2: resolved project_dir 下能找到 fcop.json? → 否 → ConfigError
    ↓ 是
检查 3: project_dir 不在 deny-list? → 否 → SafetyError (S2 / TASK-001 D2)
    ↓ 是
正常执行
```

错误文案:

```
WriteRefused: <tool_name> requires a valid FCoP project root,
but no fcop.json was found at <resolved_path> (or
<resolved_path>/fcop/fcop.json). Run init_solo() / init_project() /
create_custom_team() first if this is a new project, or call
set_project_dir(path=<correct_root>) to point to an existing one.
```

### S2 · USER HOME 子目录放行例外(P0,细化 D2)

**TASK-001 D2 的精确语义补丁**:`%USERPROFILE%` 进 deny-list,但
**子目录放行**。

精确判定规则:

| project_dir | 拒绝? | 理由 |
|---|---|---|
| `C:\Users\Administrator\` | ✅ 拒 | 严格等于 HOME |
| `C:\Users\Administrator` (无尾斜杠) | ✅ 拒 | 规范化后等于 HOME |
| `C:\Users\Administrator\codeflow\` | ❌ 放 | HOME 的子目录是合法项目位置 |
| `C:\Users\Administrator\some-real-project\` | ❌ 放 | 同上 |
| `C:\` / `D:\` / drive root | ✅ 拒 | drive root 不能做项目根 |
| `/` / `/etc` / `/usr` / `/opt` | ✅ 拒 | Unix system roots |
| `~` 展开后严格等于 HOME | ✅ 拒 | 跨平台 home |

实现要点:

- 用 `pathlib.Path.resolve()` 后比较(规范化路径 + 解析 symlink)
- Windows 上要 `casefold()`(Windows 路径大小写不敏感)
- 跨平台 home 用 `pathlib.Path.home()`

### S3 · 二工具 guard 行为对齐(P1,新增 D7)

PM #50 现场观测:

- `deploy_role_templates()` 调用时**已经**有 fcop.json 存在检查
  (实证:`ConfigError: fcop.json not found at C:\Users\Administrator\docs\agents\fcop.json`)
- `redeploy_rules()` 调用时**没有**这个检查 → 直接默默写到 cwd

**两个工具的 guard 行为不一致**,这是当前 fcop-mcp 的一处遗留 bug。
本 TASK 借此机会**全面对齐** —— 不只 `redeploy_rules` 补,而是
**TASK-001 D1 候选清单里所有 write-side 工具**都走同一个守门函数(S1
的三步检查)。

实现建议:

- 抽 `_assert_writable_project(tool_name: str) -> Path` 公共助手
- 所有 write-side 工具的入口第一行调它
- 测试用例(D5)加 "所有工具守门行为一致"的 fixture(用 parametrize
  对每个工具跑同一组场景)

## 验收补丁 / Acceptance Patch

在 TASK-001 § 验收标准 7 条之上,**追加 3 条**:

8. **S1 实施**:fcop.json 存在性检查在三步守门的第 2 步落实,所有
   write-side 工具走同一路径
9. **S2 实施**:deny-list 用 `Path.resolve()` + `casefold()`(Windows)
   规范化,通过"严格等于 HOME 拒、子目录放行"的 parametrize 测试
10. **S3 实施**:`_assert_writable_project()` 公共助手存在,所有
    write-side 工具入口调用,parametrize 测试证明行为一致

## 风险 / 回滚

- **风险 R3**:S2 子目录放行规则对 macOS / Linux 上的 `~/Desktop`
  / `~/Documents` 这类系统目录可能放行(用户在那里建项目是合法但
  不推荐的)。**缓解**:本 TASK 范围内**不**扩展这条 deny-list;留
  作 v1.5 提案(可在 release notes 提一句 "可选 strict mode")
- **风险 R4**:S3 抽公共助手可能影响现有测试套件的 mock 路径。
  **缓解**:测试时用 `monkeypatch` 替换助手而非内部函数

回滚同 TASK-001 R-rollback:降级回 v1.3.x 即可。

## 状态机

- `proposed`(本文件落盘时)
- `accepted` ← 与 TASK-001 一起 GREEN
- `done` → 与 TASK-001 共用 `REPORT-20260512-001-ME-to-ADMIN.md`
  或单独写 `REPORT-002`

---

**请 ADMIN 决**:

- (A) **批准** TASK-001 + TASK-002 合并范围,ME 开工
- (B) **再调** —— 比如 S2 想加严(`~/Desktop` 也拒),或 S3 想缓
- (C) **拒延** —— 跟 TASK-001 一起延后

我推荐 (A)。

— ME, 2026-05-12 16:03 (UTC+8)
