# WP4D 恢复与兼容性：守卫阻断，安装态验证未运行

修改前 1912 个现有节点完整通过，但未发布 RC 身份触发一个旧测试的提前 skip。不能把基线通过数移作候选恢复/兼容证据。

[固定未修改测试](https://github.com/joinwell52-AI/FCoP/blob/4160fc5d216f784bee6b35902b507fff8e0ba6f6/tests/test_fcop/test_audit.py#L242) 只读取版本第二段；`4.0.0rc1` 的 minor 为 0，因此在第 248 行 skip，未执行角色文档创建及最终 violations 断言。
[生产扫描逻辑](https://github.com/joinwell52-AI/FCoP/blob/4160fc5d216f784bee6b35902b507fff8e0ba6f6/src/fcop/project.py#L2422) 使用 major 与 minor 共同计算距离。源码阅读支持“旧测试前置条件忽略 major”的诊断，但没有执行被跳过的断言，故不据此宣称 RC 生产扫描已经通过。

没有修改旧测试、Core 扫描、Conformance、恢复或生命周期；需要 ADMIN 对该局部测试条件的明确裁定，不能在当前范围擅改。

| 安装态证明 | 状态 |
|---|---|
| response-loss 同身份重试与零重复效果 | NOT_RUN |
| 杀进程后磁盘恢复和锁定上下文 | NOT_RUN |
| 版本/缺失规则/digest/overflow 零副作用 | NOT_RUN |
| 固定 3.2.5 workspace 全树零漂移 | NOT_RUN |
| Host discover/select/deploy/rollback | NOT_RUN |
| CodeFlowMu 固定消费者 shadow 14/14 | NOT_RUN（0/14 已验证） |

这些项目无开始/结束、命令退出码或 Actions URL；均为 N/A，而非 PASS。没有运行 CodeFlowMu 或对其工作树写入，没有将旧 shadow 结果冒充本阶段。

## 冻结文件

17:24:29 +08:00，逐文件比较 `read_bytes()` 与 `git show 167c5fd4ca4c9603c392bae3a4a055963e7b7ed6:<path>`，21/21 字节不变，其中规则候选 19/19。Core Conformance tree 为 `24ab264c6bca9a3183ee270becb552f22a4c4f9e`；规则分发 Conformance tree 为 `4f99c7261b63b6db81c500604a231defaca9f14b`。

| 冻结文件 | SHA-256 |
|---|---|
| src/fcop/rules/_data/v4/authorization.en.md | 96c1c18bab3a879b51a1e2d0041f1f08eeae685185ad9489f13ed0a999f9a00b |
| src/fcop/rules/_data/v4/authorization.zh.md | 13b82fdeb7c577a68a70d94303bf090eac42ce44c137c1a166b23f7014c1b854 |
| src/fcop/rules/_data/v4/compatibility.en.md | a65385a3a2e68d043c65f9b8c34c6ac311bb7f9b2ea1e9f4c162886f858a64d8 |
| src/fcop/rules/_data/v4/compatibility.zh.md | d6ce267c8216a2d6df2e5e601f4d237d941778a36687eae1d310616f6170585e |
| src/fcop/rules/_data/v4/convergence.en.md | ec3cf38b6dba4d3eb8447cc7cd25e947c06abed228c37c9d651f873662edc70e |
| src/fcop/rules/_data/v4/convergence.zh.md | 2b5c2a52c33bc38e8c3c85fdd75d5de3c837cc483a29941ec02a61a059c1701a |
| src/fcop/rules/_data/v4/envelopes.en.md | 0405885cbe3fe791c0e1a6c76da004d093d58cd55159ffeb3ca8c89e4ec045a3 |
| src/fcop/rules/_data/v4/envelopes.zh.md | 0a69c9196e95185cf9e98b71af8c564be5797e26a71c5a9b7dc32d0735a08fef |
| src/fcop/rules/_data/v4/idempotency.en.md | 1b100010d36342e6d98e9031429b3e11aad5657dfa953031e43bc4c99772a16a |
| src/fcop/rules/_data/v4/idempotency.zh.md | 51c53931e02b1f39950f4a2f16b5e8e9a5f9d10b77f5ea1ad6b07c3e96385f08 |
| src/fcop/rules/_data/v4/lifecycle.en.md | b6356c078ab00b893379f0b4f558616444ef4a4aa0e17432460719a9be362b2b |
| src/fcop/rules/_data/v4/lifecycle.zh.md | 26b338914cffe2ea076f0e88133fc69617c91ecb149b3e40217baeef708cffef |
| src/fcop/rules/_data/v4/manifest.json | 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4 |
| src/fcop/rules/_data/v4/recovery.en.md | aad4861efa59df69742c4bf577d57a553cbb170f6f92d61f6df74ec3ec503908 |
| src/fcop/rules/_data/v4/recovery.zh.md | b19226071498f6414e11379b9d67cee36e4a79d65510fffefd14a021cd829000 |
| src/fcop/rules/_data/v4/relations.en.md | 1b706c4ff76efb6edad40ab7985a0693eb9466da483d7024eb1f29668e022789 |
| src/fcop/rules/_data/v4/relations.zh.md | fa51c77a568dae7f7cf41242b612ae2b2963075004aaebef533334a0466d3d42 |
| src/fcop/rules/_data/v4/workspace.en.md | 06d4a9604fbab50ade36369f8f1d2950f099a241d659613cc78f1dd7e93555b3 |
| src/fcop/rules/_data/v4/workspace.zh.md | 617009dc95cf4bedd252491334f45cf61fa1fe8ccf935f2127e2a1da9a49e30b |
| spec/fcop-4.0-spec.md | 0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9 |
| spec/fcop-4.0-spec.zh.md | 7302983e8a6e2225470d3da8f2e768abd4dfcc1c7adbe17116a64dda7e357c19 |

## 执行身份与证据口径

- 唯一任务书：`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9`，SHA-256 `bfc93f595800efe5185588ff92b612c9ca66e1622118e76c805d5fd908a1e290`，18471 bytes。
- 已验收实现基线：`167c5fd4ca4c9603c392bae3a4a055963e7b7ed6`；未发布候选内容提交：`4160fc5d216f784bee6b35902b507fff8e0ba6f6`。
- 环境：Windows 10 build 19045 / Python 3.12.9；时区 +08:00；独立工作树 `D:/FCoP-wp4d-rc-candidate`。
- Draft PR：[31](https://github.com/joinwell52-AI/FCoP/pull/31)，base 为 `task/fcop-4.0-wp4d-rc-candidate`，不指向 main。
- 本报告为 BLOCKED 证据，不是 RC 验收或发布证明。具体命令、起止时间、退出码、测试数、日志和哈希见 [RESULT](FCOP-4.0-WP4D-RESULT.md)。
- 尚未构建四个 RC 制品，故 artifact SHA-256 均为 NOT_GENERATED；安装态、12 组合和最终 HEAD CI 未验收，不能沿用父 Gate 的通过数。
