---
task_id: "20260418-143000-001"
sender: "PM"
recipient: "DEV"
status: "PENDING"
priority: "HIGH"
created_at: "2026-04-18T14:30:00Z"
required_tools: ["cursor_edit", "terminal"]
---

## 任务描述

实现用户登录接口，支持手机号 + 验证码登录方式。

### 具体要求

- `POST /api/auth/login` 接受 `phone` 和 `code` 字段
- 手机号格式校验（11位数字，1开头）
- 验证码 6 位数字，有效期 5 分钟
- 登录成功返回 JWT token
- 失败返回标准错误格式

### 预期输出格式

```json
{
  "files_modified": ["src/api/auth.py", "src/models/user.py"],
  "test_passed": true,
  "notes": "简短说明"
}
```

### 参考资料

- [现有认证模块](../src/api/auth.py)
- [用户模型](../src/models/user.py)
