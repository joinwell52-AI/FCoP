# WP4D RC 身份与版本：局部通过，阶段阻断

双包源码身份为未发布 `4.0.0rc1`，两处 classifier 为 Beta。
MCP 下界精确为 `fcop>=4.0.0rc1,<4.1.0`；兼容集合仅增加同版本 RC 对，保留历史 3.2.5 对，不加入稳定 4.0.0。
根包依赖描述已纠正；PyYAML/jsonschema、FastMCP、Relay 的原依赖行为未改变。

任务书 §3.1 明确允许修正原有两个 pin 测试：保留 Test ID，强制相同 MAJOR.MINOR 和精确 prerelease 下界。新增测试 12 个，含 8 种错误 pin 拒绝；合计 14/14 通过、0 失败、0 skip。

这仅证明源码声明和静态依赖契约，不证明安装态元数据或真实错配组合。源 import 实测路径为 `D:/FCoP-wp4d-rc-candidate/src/fcop/__init__.py`，不冒充 site-packages。

## 固定远端内容回读

2026-09-09 17:24:29 +08:00，从 GitHub Contents API 按候选提交逐项读取原始 Blob，9/9 与本地文件及 Git Blob 相同：

| 文件 | bytes | GitHub SHA-256 |
|---|---:|---|
| docs/fcop-4.0/rc-candidate-boundary.md | 1469 | 8cf4906f96fc7b74096a77bba6b2bd4355e8ae72eb4d7fa64747ce514d3e06bb |
| mcp/pyproject.toml | 4861 | 86628c2f21270758a51abac4fc375673d2c6a0c4c4806cf141fa270babff85c8 |
| mcp/src/fcop_mcp/_version.py | 610 | 310a8df396e097eeb5d3d8a0c83e3e2bc8803539ea94f7ecad7efad070a68339 |
| mcp/src/fcop_mcp/routing.py | 3760 | 6f054a99e2b2807b813d0e43e644e8b950a2f63c2d0159d519c6c89bb35fcb8b |
| pyproject.toml | 6077 | c9faa4f794b30ed52fdfc7093e0f0b30f7d8965ec8c8139c94f04eb732c346dc |
| scripts/fcop_rc_candidate_check.py | 3243 | 0a284ca78f5e36d46bbd73ef2113186d90194917a31c33a12a29818b4c8b144c |
| src/fcop/_version.py | 564 | 14ffc70e19c78e318a2b65b2331dd21ccd3e84913493b1dca5a64079a6b0f3b9 |
| tests/test_fcop/test_pyproject_pins.py | 1283 | 45cafdb7f125355d66cb503a3248c0b255e8826343e44894f98d4d1c3462cfc3 |
| tests/test_fcop/test_wp4d_rc_identity.py | 1586 | a5876542335a04a05d7ed315cfd239e14bf58986e90bf5bca479cc2b0a7473f8 |

命令：`python -B scripts/fcop_rc_candidate_check.py`；17:23:07–17:23:08 +08:00，退出 0，输出双包候选身份、精确 pin、stable_pair=false、published=false。
候选身份测试命令、JUnit 及 14/14 明细见 RESULT。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
