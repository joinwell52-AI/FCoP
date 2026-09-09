# WP4D 制品可复现性：NOT_RUN

阶段在源码回归守卫处阻断；没有生成、上传或混用候选制品。

| 必需制品 | 构建/两次比对/twine | SHA-256 |
|---|---|---|
| fcop-4.0.0rc1-py3-none-any.whl | NOT_RUN | NOT_GENERATED |
| fcop-4.0.0rc1.tar.gz | NOT_RUN | NOT_GENERATED |
| fcop_mcp-4.0.0rc1-py3-none-any.whl | NOT_RUN | NOT_GENERATED |
| fcop_mcp-4.0.0rc1.tar.gz | NOT_RUN | NOT_GENERATED |

预定命令类别为 Ubuntu/Python 3.12 下两次全新目录 `python -m build` 与两组 `python -m twine check`；均未执行，开始/结束、退出码、测试数和 Actions artifact URL 均 N/A（不是通过）。SOURCE_DATE_EPOCH 未进入实际构建记录。0/4 已验证，不得记成 4/4。

内存中曾拟定构建/consumer 脚本草案，但没有落入交付内容，也未作为已实现、已运行或可用制品报告。后续续作必须在明确解除阻断后按任务书重新建立完整证据。

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
