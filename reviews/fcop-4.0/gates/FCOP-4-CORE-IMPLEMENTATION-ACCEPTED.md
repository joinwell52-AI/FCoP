---
document_role: ADMIN_GATE_RECEIPT
gate: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
decision: ACCEPTED
effective_input_head: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp3e_0_content_commit: c5a6de102cd96e7291aa8b4572976571a6152268
wp3e_0_manifest_commit: a030eee3b20b7a0d1eef3535b7bf7554a622e1ce
wp3e_1_content_commit: 14c9030717b323cd0f4c7606a8da4e0f8b1a0e39
wp3e_1_manifest_commit: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
accepted_at_utc: 2026-09-06
main_merge_authorized: false
release_authorized: false
wp4_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 Core Implementation 验收回执

## 1. ADMIN 决定

ADMIN 对固定远端提交 `1d94b881e38cc0b98ca41c47d25c605431d5f9a7` 完成审核，正式签署：

```yaml
GATE: FCOP_4_CORE_IMPLEMENTATION_ACCEPTED
DECISION: ACCEPTED
EFFECTIVE_INPUT_HEAD: 1d94b881e38cc0b98ca41c47d25c605431d5f9a7
```

本回执验收截至 WP3E.1 的 FCoP 4.0 Core 实现，关闭 WP3A–WP3E Core 实现序列。

## 2. 验收依据

### 2.1 权威输入

- 冻结合同：`aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
- WP3E.0 Content：`c5a6de102cd96e7291aa8b4572976571a6152268`
- WP3E.0 Manifest：`a030eee3b20b7a0d1eef3535b7bf7554a622e1ce`
- WP3E.1 Content：`14c9030717b323cd0f4c7606a8da4e0f8b1a0e39`
- WP3E.1 Manifest / 审核 HEAD：`1d94b881e38cc0b98ca41c47d25c605431d5f9a7`

审核以 GitHub 固定提交中的代码、测试、报告和 Manifest 为准，不以本地路径或口头汇报代替远端事实。

### 2.2 WP3E.1 实际差异

从任务书提交 `a2b32633708c22196a32f064d9850755634c25e7` 到 Content 提交：

- `src/fcop/v4/creation.py`：删除 2 行；
- `tests/test_fcop/test_v4_creation.py`：新增 42 行；
- 新增 `reports/FCOP-4.0-WP3E.1-CREATE-DIGEST-CLOSEOUT.md`。

从 Content 提交到 Manifest 提交只新增：

- `reviews/fcop-4.0/wp3e.1/MANIFEST.md`。

未发现冻结规范、冻结 Conformance、Schema、MCP、规则包或 CodeFlowMu 文件改动。

### 2.3 合同缺陷已收口

WP3E.1 已从正式 `normalized_request_digest` 中移除临时 Toolkit Gate 上下文字段 `references_required_by_gate`。

保留的行为为：

- Gate 参数仍做布尔类型校验；
- Gate 开启且引用无法解析时仍拒绝创建；
- 同一正式请求，无论先携带或后携带该临时 Gate 上下文，均得到相同摘要；
- 同一 `operation_id` 的精确重试返回既有结果；
- TASK、operation fact 与 receipt 不持久化该临时字段；
- 非布尔 Gate 值继续 Fail Closed。

该结果符合冻结合同 F4.8.4：创建摘要仅由正式请求字段决定，Toolkit 调用上下文不得进入协议身份。

## 3. 远端完整性核验

ADMIN 从固定审核 HEAD 回读交付文件并独立计算 SHA-256：

| 文件 | 字节数 | SHA-256 | 结果 |
|---|---:|---|---|
| `src/fcop/v4/creation.py` | 42112 | `c3dc49f4f87c59741ed7b37fa73f3dada61ebfb6c3d61a8c594b40f329c0c0a1` | MATCH |
| `tests/test_fcop/test_v4_creation.py` | 39696 | `2faf6bbb509c021dad9e27a7527ebd267efb932a4f6f8667af96406c1a2bef61` | MATCH |
| `reports/FCOP-4.0-WP3E.1-CREATE-DIGEST-CLOSEOUT.md` | 5074 | `d8487eb0dfd0fe096f316f86dc808ad9707b0ad7ebdc7a05c280a5f5f47702e6` | MATCH |

```yaml
REMOTE_DELIVERY_SHA256: 3/3 MATCHED
CONTENT_TO_MANIFEST_CHANGE: MANIFEST_ONLY
FROZEN_SCOPE_DRIFT: 0
PUBLIC_SURFACE_DRIFT: 0
```

## 4. 测试证据判定

接受以下固定交付证据：

```yaml
WP3E_TARGET_NODES: 23/23
WP3E_V4_UNIT_TESTS: 235/235
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 92/92
V4_TOTAL: 119/119
TEST_FCOP: 1143/1143
V3_REGRESSION: 908 passed / 235 deselected
MCP_REGRESSION: 80/80
UNEXPECTED_FAILURES: 0
```

GitHub 对审核 HEAD 没有报告 status contexts。因此上述结果被认定为固定交付中的 Windows 本地测试证据，不被表述为云端 CI 通过；Linux/macOS 原生验证也仍未据此宣称完成。

## 5. 架构边界复核

本轮未新增：

- 公共 API；
- 生产模块；
- Runtime 依赖；
- 后台组件；
- 权威 Store；
- 状态机；
- 锁系统；
- Base Error Code。

本轮没有修改 CodeFlowMu。CodeFlowMu 继续固定使用 `fcop==3.2.5` 与 `fcop-mcp==3.2.5`，不因本 Gate 自动升级。

## 6. 本 Gate 明确不授权

```yaml
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
WP4_AUTHORIZED: false
MCP_IMPLEMENTATION_CHANGE_AUTHORIZED: false
SCHEMA_CHANGE_AUTHORIZED: false
RULE_PACKAGE_CHANGE_AUTHORIZED: false
HOST_ADAPTER_CHANGE_AUTHORIZED: false
CODEFLOWMU_CHANGE_AUTHORIZED: false
```

本 Gate 不能被解释为：

- 允许合并到 `main`；
- 允许发布 FCoP 4.0；
- 允许发布 PyPI 或 GitHub Release；
- 允许开始 WP4；
- 允许修改 MCP、Schema、规则包、Host Adapter 或 CodeFlowMu；
- 允许绕过后续固定任务书与阶段验收。

## 7. 下一步

下一步只能由 ADMIN 另行固定并授权 WP4 任务书。该任务书应从本回执所验收的固定输入 HEAD 顺序接出，并继续采用 GitHub 固定提交、两提交交付、远端回读及独立 Gate 的审核规则。

在新的固定任务书和明确授权出现前，执行方必须停止。
