# FCoP 4.0 WP4D：Twine Metadata 2.5 工具链定点勘误与恢复授权 v1.0

```yaml
document_role: EXECUTION_ERRATUM
execution_authorized: true
authorized_scope: WP4D_TWINE_METADATA_2_5_TOOLCHAIN_ONLY_AND_WP4D_RESUME
parent_taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
prior_erratum_commit: 22db1377163bb0b1e74c4b94fa1f594b3e762a9d
blocked_implementation_head: 700e9e1ecb3eb02e5860094175ba7f8099141695
draft_pr: https://github.com/joinwell52-AI/FCoP/pull/31
blocker: TWINE_6_2_REJECTS_CORE_METADATA_2_5
authorized_twine: 7.0.0
authorized_packaging: 26.3
completion_gate: FCOP_4_RC_ACCEPTED
main_merge_authorized: false
rc_publish_authorized: false
stable_release_authorized: false
pypi_publish_authorized: false
github_release_authorized: false
mcp_registry_publish_authorized: false
zenodo_publish_authorized: false
codeflowmu_write_authorized: false
```

## 1. ADMIN 裁定

确认授权定点修正 WP4D 候选构建校验工具链，并在修正通过后恢复原 WP4D：

```text
twine==6.2.0  -> twine==7.0.0
packaging     -> packaging==26.3
```

固定阻断证据表明：Hatchling 成功构建四个 `4.0.0rc1` 文件；失败发生在 `twine check`，Twine 6.2.0 将 `Metadata-Version: 2.5` 判为非法。Core Metadata 2.5 已是 PyPA 正式规范；Twine 7.0.0 官方变更说明明确修复 Metadata 2.5 支持，其依赖要求为 `packaging>=26.1`。本任务固定 `packaging==26.3`，避免校验器的传递依赖在重跑间漂移。

权威参考：

- PyPA Core Metadata：`https://packaging.python.org/specifications/core-metadata/`
- Twine 7.0.0 release notes：`https://github.com/pypa/twine/blob/7.0.0/docs/changelog.rst`
- Twine 7.0.0 dependency declaration：`https://github.com/pypa/twine/blob/7.0.0/pyproject.toml`
- PyPI Twine 7.0.0：`https://pypi.org/project/twine/7.0.0/`

这是候选验证工具兼容性修正，不是 FCoP Core、MCP、Schema、规则或制品元数据缺陷。此前 BLOCKED 回执保持为历史事实。

## 2. 唯一允许的工具链修改

### 2.1 RC workflow

只允许在：

```text
.github/workflows/rc-candidate.yml
```

将 build job 的固定工具安装行改为包含：

```text
build==1.4.2
hatchling==1.32.0
setuptools==82.0.1
wheel==0.45.1
twine==7.0.0
packaging==26.3
```

除 `twine` 替换和 `packaging` 精确 pin 外，不得改变 job 权限、触发器、构建命令、artifact 传递、矩阵、发布隔离或其他工具版本。

### 2.2 候选 manifest 工具身份

只允许在：

```text
scripts/wp4d_build.py
```

把 `packaging` 加入现有 `tools` 版本记录，使最终 `candidate-manifest.json` 同时记录：

```text
build, hatchling, setuptools, wheel, twine, packaging
```

不得改变构建、导出、两次重建、哈希、archive 检查、Metadata 检查、同制品约束或上传逻辑。

## 3. 禁止的替代修法

不得：

- 降级或伪造 `Metadata-Version`；
- 降级 Hatchling、setuptools、build 或 wheel 来规避合法 Metadata 2.5；
- 解包后修改 wheel、sdist、METADATA 或 PKG-INFO；
- patch Twine/packaging 源码或忽略 `twine check` 返回码；
- 删除、跳过、xfail 或弱化任何构建/元数据检查；
- 使用 `twine>=7`、未 pin 的 `packaging`、`latest` 或其他浮动范围；
- 把阻断运行生成但未上传核验的四个文件提升为候选制品；
- 修改 FCoP 或 MCP 的版本、依赖 pin、生产逻辑、规范、Schema、Conformance 或规则内容。

## 4. 恢复基线与提交纪律

执行人必须继续使用现有实现分支和 Draft PR #31：

```text
feat/fcop-4.0-wp4d-rc-candidate
```

从远端固定阻断 HEAD：

```text
700e9e1ecb3eb02e5860094175ba7f8099141695
```

验证父链与干净工作树。定点工具链修正必须形成一个独立提交，该提交只能包含：

```text
.github/workflows/rc-candidate.yml
scripts/wp4d_build.py
```

不得改写、压缩或删除既有阻断提交与证据。不得 force-push。

## 5. 恢复验证顺序

### 5.1 工具身份预检

在实际 build job 中记录并断言：

```text
twine==7.0.0
packaging==26.3
```

记录 Python 与其余五个固定构建工具版本。安装或身份不匹配即失败。

### 5.2 重新构建，不复用失败产物

必须从新的定点修正提交重新生成全部四个候选文件。阻断运行中生成的未核验文件不得复用、上传或继承哈希。

同一 build job 中：

1. 两个全新 source 目录分别构建四制品；
2. 两组各执行 `twine check`，均必须成功；
3. 比较两组对应文件的原始字节与 SHA-256，必须 `4/4` 相同；
4. 只上传第一组与新的机器可读 manifest；
5. manifest 必须记录 `twine: 7.0.0`、`packaging: 26.3`、固定 `SOURCE_DATE_EPOCH`、提交 SHA 与四制品哈希。

### 5.3 全量恢复

构建通过后必须继续完成原 WP4D 的全部未完成项：

- 最终 HEAD 源码全量回归；Windows、Ubuntu 均不得沿用阻断 HEAD 的 `1924/1924`；
- 既有适用 CI 与 Windows 矩阵；
- 12 个 OS/Python clean-room consumer；
- wheel 与 sdist 安装态验证；
- Python-only 与 MCP-only 第三方项目；
- response-loss retry 与 crash recovery；
- 3.2.5 workspace 零迁移、零漂移；
- Host 规则发现、拒绝、deploy、rollback 与零副作用；
- CodeFlowMu `14/14` 固定 3.2.5 只读 shadow；
- `46 tools / 12 static resources / 4 templates`；
- `19/19` 权威候选文件与 `21/21` 冻结字节；
- 最终 Manifest HEAD 的全部适用 CI。

任何 NOT_RUN、skip、queued、in progress、cancelled 或 allowed failure 都不得记为通过。

## 6. 报告与 Manifest 追加字段

六份报告、JUnit 和 Manifest 必须保留两次历史 BLOCKED 事实，并新增本次恢复证据。最终 Manifest 至少增加：

```yaml
toolchain_erratum_commit: <this-taskbook-commit>
toolchain_resume_base: 700e9e1ecb3eb02e5860094175ba7f8099141695
toolchain_fix_commit: <two-file-commit>
twine_version: 7.0.0
packaging_version: 26.3
metadata_version_observed: "2.5"
twine_checks: 2/2
artifact_reproducibility: 4/4
failed_run_artifacts_reused: false
```

最终全部交付文件必须从远端 Manifest HEAD 逐项回读并核验 SHA-256；只记录远端值。

## 7. 继续冻结的权限边界

本勘误不授权：

- 修改 `main` 或合并 Draft PR；
- 创建或推送 tag；
- 上传 PyPI；
- 创建 GitHub Release；
- 更新 MCP Registry、Zenodo、DOI、`CITATION.cff` 或 `mcp/server.json`；
- 修改 `.github/workflows/release.yml`；
- 修改 CodeFlowMu；
- 签署 `FCOP_4_RC_ACCEPTED`。

新增 RC workflow 仍必须保持 `permissions: contents: read`，不得读取发布 secrets、配置发布 environment 或调用上传 registry 的命令。

## 8. 停止条件

若 Twine 7.0.0 + packaging 26.3 仍不能对两组四制品完成 `twine check`，或需要超出第 2 节的工具链修改，立即停止：

```text
WP4D_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

只有原 WP4D 全部验收项在新的最终固定 HEAD 上通过，才可停止并请求：

```text
WP4D_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_ACCEPTED
RC_PUBLISH_AUTHORIZED: FALSE
MAIN_MERGE_AUTHORIZED: FALSE
```

执行人不得自行签署 Gate，不得在 Gate 后自动合并或发布。
