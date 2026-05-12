---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-002
task_id: TASK-20260512-002
sender: ME
recipient: ADMIN
status: done
thread_key: fcop-mcp-binding-guard-20260512
session_id: sess-20260512-me-01
created_at: 2026-05-12T16:28:00+08:00
---

# TASK-002 完成报告 · 三步守门细化（S1 / S2 / S3）

## 结论

**S1 / S2 / S3 全部交付，测试从 34 增至 70 通过（2 跳过）。**

TASK-001（D1-D6）+ TASK-002（S1-S3）合并后：

| 验收标准 | 状态 |
|---|---|
| D1 · write-side 显式绑定守门 | ✅ |
| D2 · protected path deny-list | ✅ |
| D3 · fcop_report() 顶部告警 | ✅ |
| D4 · binding_required schema tag | ✅ |
| D5 · 测试套件全绿 | ✅ 70 passed |
| D6 · release notes + CHANGELOG | ✅ |
| S1 · fcop.json 存在性检查 | ✅ |
| S2 · HOME 子目录放行 + casefold | ✅ |
| S3 · _assert_writable_project() 公共助手 + parametrize | ✅ |
| PM #50 复现测试 | ✅ TC-06 通过 |

---

## 实现要点

### S1 — `_has_fcop_json(path)` + 三步守门第 2 步

```python
def _has_fcop_json(path: Path) -> bool:
    return (path / "fcop" / "fcop.json").is_file() or \
           (path / "docs" / "agents" / "fcop.json").is_file()
```

三步守门顺序（`_assert_writable_project()`）：
1. D1 — cwd fallback 拒绝
2. **S1** — fcop.json 存在性（init 工具豁免）
3. D2/S2 — deny-list 拒绝

**init 工具豁免集**：`{"init_project", "init_solo", "create_custom_team"}`

### S2 — HOME 子目录精确语义

`_is_protected_path(path)` 改用 `Path.home().resolve()` 获取 HOME，
Windows 下用 `casefold()` 进行路径比较：

```python
home = Path.home().resolve()
if sys.platform == "win32":
    if path.as_posix().casefold() == home.as_posix().casefold():
        return True
```

- `C:\Users\Administrator` → 拒绝 ✅
- `C:\Users\Administrator\my-project` → 放行 ✅
- `C:\Users\ADMINISTRATOR`（大写变体）→ 拒绝（casefold 捕获）✅

### S3 — `_assert_writable_project()` 公共助手

- `_assert_write_allowed` 重命名为 `_assert_writable_project`
- 旧名保留为向后兼容别名
- 所有 write-side 工具入口调用 `_get_project_write()` → 内部调 `_assert_writable_project()`
- `fcop_create_alert` 直接调 `_assert_writable_project("fcop_create_alert")`

### Parametrize 测试（TC-12）

```
TC-12 test_tc12_s3_all_tools_refuse_cwd_fallback    — 15 × 工具
TC-12 test_tc12_s3_all_tools_refuse_home_binding    — 15 × 工具
```

共 30 个参数化用例，证明所有工具行为一致。

---

## 测试结果

```
tests/test_write_guard.py  47 passed, 2 skipped
tests/test_governance.py   23 passed
Total: 70 passed, 2 skipped, 0 failures

ruff: All checks passed
mypy: no issues found in 1 source file
```

---

— ME, 2026-05-12 16:28 (UTC+8)
