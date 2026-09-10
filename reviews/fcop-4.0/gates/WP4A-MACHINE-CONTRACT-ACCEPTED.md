---
document_role: ADMIN_GATE_RECEIPT
gate: WP4A_MACHINE_CONTRACT_ACCEPTED
decision: ACCEPTED
effective_input_head: d663e9dc05ca4f8db135b87f04f5dee4c3543e55
frozen_contract_commit: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
wp4a_3_content_commit: eb2c20a29b5d6d2d24f238ac2d266b671ab38fca
wp4a_3_manifest_commit: d663e9dc05ca4f8db135b87f04f5dee4c3543e55
accepted_at_utc: 2026-09-06
main_merge_authorized: false
release_authorized: false
wp4b_authorized: false
codeflowmu_change_authorized: false
---

# FCoP 4.0 WP4A Machine Contract 验收回执

## 1. ADMIN 决定

ADMIN 已对 GitHub 固定远端 HEAD `d663e9dc05ca4f8db135b87f04f5dee4c3543e55` 完成审核，正式签署：

```yaml
GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
DECISION: ACCEPTED
EFFECTIVE_INPUT_HEAD: d663e9dc05ca4f8db135b87f04f5dee4c3543e55
```

本 Gate 验收 WP4A、WP4A.1、WP4A.2 与 WP4A.3 累积形成的 FCoP 4.0 机器可读合同、最小 Python 使用面、Schema 打包和跨平台检出策略，关闭 WP4A 序列。

## 2. 固定审核依据

- 冻结合同：`aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`
- WP4A.3 任务书：`db4c99806e797a563541381e376c7c62e13f8da0`
- WP4A.3 Content：`eb2c20a29b5d6d2d24f238ac2d266b671ab38fca`
- WP4A.3 Manifest / 审核 HEAD：`d663e9dc05ca4f8db135b87f04f5dee4c3543e55`
- Draft PR：`https://github.com/joinwell52-AI/FCoP/pull/14`
- test-fcop run：`https://github.com/joinwell52-AI/FCoP/actions/runs/34019262674`
- test-fcop-mcp run：`https://github.com/joinwell52-AI/FCoP/actions/runs/34019262649`

审核以固定远端代码、Manifest、GitHub Job 和回读字节为准，不以本地路径或口头完成声明代替。

## 3. 交付完整性

ADMIN 重新读取审核 HEAD 中的四个 WP4A.3 交付文件并独立计算 SHA-256：

| 文件 | SHA-256 | 结果 |
|---|---|---|
| `.gitattributes` | `0c976f274663a6904cde1cbba7bfcd10c7238745bbe065f31b52b128297b3745` | MATCH |
| `reports/FCOP-4.0-WP4A.3-RESULT.md` | `a2aa4eefc48abb90e573af3757776c65384664d7012211a930db43686f1d0f9b` | MATCH |
| `reports/FCOP-4.0-WP4A.3-WINDOWS-SCHEMA-CHECKOUT-POLICY.md` | `ddc9b5670664812617aff015ed8e7e6a5bbe67f335b72c9c11e0032be32af3c9` | MATCH |
| `reviews/fcop-4.0/wp4a.3/MANIFEST.md` | `c9345a07363d9ad0c9236510469d3b9a02fdea427755e9a0d1d822ca6e7d8f9f` | MATCH |

```yaml
REMOTE_DELIVERY_SHA256: 4/4 MATCHED
V4_SCHEMA_FILES: 24
V4_SCHEMA_BLOB_DRIFT: 0
V4_SCHEMA_SHA256_DRIFT: 0
SCHEMA_SOURCE_PACKAGE_PARITY: 12/12
```

`.gitattributes` 只固定两处 v4 Schema 的 LF 检出，没有扩大到全仓文件，也没有放宽 `generate.py --check` 的原始字节合同。

## 4. GitHub CI 验收

固定审核 HEAD 对应两套 Workflow 共 29 个 Job：

```yaml
TEST_FCOP_JOBS: 15/15 SUCCESS
  WINDOWS_PYTHON_3_10_TO_3_13: 4/4
  UBUNTU_MACOS_PYTHON_3_10_TO_3_13: 8/8
  COVERAGE: PASS
  STABILITY_CHARTER: PASS
  BUILD_INSTALL_PIP_AUDIT: PASS

TEST_FCOP_MCP_JOBS: 14/14 SUCCESS
  OS_PYTHON_MATRIX: 12/12
  TOOL_CONTRACT: PASS
  BUILD_INSTALL_SMOKE: PASS

GITHUB_CI_TOTAL: 29/29 SUCCESS
```

fcop package Job 已从前轮的 skipped 恢复为真实执行成功。未使用取消、忽略、 `continue-on-error` 或平台排除冒充绿色。

## 5. WP4A 能力验收

接受以下结果：

```yaml
V4_SCHEMA_DOCUMENTS: 12
SCHEMA_BINDING: 10/10
V4_CONFORMANCE: 119/119
FROZEN_TEST_IDS: 60/60
TEST_FCOP: 1190/1190
MCP_REGRESSION: 80/80
PUBLIC_SURFACE_DRIFT: 0
MINIMAL_SEQUENTIAL_APP: PASS
MINIMAL_PARALLEL_FAMILY_APP: PASS
CLEAN_WHEEL_INSTALL: PASS
```

普通开发者已经能够仅通过 `fcop` Python 包创建显式 4.0 workspace、执行顺序任务或一层 Branch family，并用随 wheel 分发的机器合同验证真实产物；这一能力不依赖 CodeFlowMu、MCP、网络、数据库或后台服务。

## 6. 架构边界

WP4A 没有增加第二套协议、生命周期、授权系统或权威 Store。Schema、registry 和示例只表达或调用已接受 Core。

CodeFlowMu 未修改，继续固定使用 `fcop==3.2.5` 与 `fcop-mcp==3.2.5`；本 Gate 不代表 CodeFlowMu 已采用 FCoP 4.0。

## 7. 本 Gate 不授权

```yaml
WP4B_AUTHORIZED: false
WP4C_AUTHORIZED: false
WP4D_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
PYPI_PUBLISH_AUTHORIZED: false
GITHUB_RELEASE_AUTHORIZED: false
CODEFLOWMU_CHANGE_AUTHORIZED: false
WORKSPACE_MIGRATION_AUTHORIZED: false
```

本 Gate 不能被解释为允许修改 MCP、规则包、Host Adapter、CodeFlowMu，不能被解释为允许合并 PR #14、合并 main 或发布。

## 8. 下一步

下一步只能由 ADMIN 另行固定并授权 WP4B MCP 薄适配任务书。执行者必须从包含本 Gate 与该任务书的固定提交建立独立 worktree；没有任务书提交和 SHA-256，不得开始 WP4B。
