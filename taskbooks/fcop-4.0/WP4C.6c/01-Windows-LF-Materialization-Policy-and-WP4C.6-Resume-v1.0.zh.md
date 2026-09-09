# WP4C.6c：Windows LF 物化策略定点修正与 WP4C.6 恢复任务书 v1.0

## 1. ADMIN 裁定

WP4C.6b 在固定最终头 `34841330604e32c473a538afb634a81334eca8ad`
上的本地合并回归为 1736/1736，交付文件远端哈希为 17/17；GitHub Actions
中 Linux 与 macOS 均通过，而两个工作流的 Windows Python 3.10、3.11、3.12、
3.13 共八个矩阵项一致失败。失败集中为：

- `toolkit:RULE_MANIFEST_INVALID: Invalid raw Encoding`；
- `toolkit:RULE_ARTIFACT_MISMATCH: Frozen specification source drift`。

仓库当前 `.gitattributes` 仅对 v4 Schema 路径声明 `text eol=lf`。受冻结哈希、
字节长度及 UTF-8/LF 合同约束的规则 Manifest、十八份规则 Markdown 与冻结规范
未声明 checkout EOL；Windows checkout 因此可能把 Git blob 的 LF 字节物化为
CRLF。严格加载器拒绝 `\r`、逐字节验证 Manifest 和冻结规范是预期安全行为，
不得放宽。

据此裁定：这是仓库跨平台物化策略缺口，不是规范源、规则制品或 WP4C.6
生产实现漂移。允许一次仅限 `.gitattributes` 的定点修正，并恢复 WP4C.6 最终
验收。

```yaml
WP4C_6C_WINDOWS_LF_POLICY_CORRECTION_AUTHORIZED: true
AUTHORIZED_SCOPE: WP4C_6C_GITATTRIBUTES_ONLY_AND_WP4C_6_RESUME
BLOCKED_FINAL_HEAD: 34841330604e32c473a538afb634a81334eca8ad
CANONICAL_BLOB_BYTES_REMAIN_AUTHORITATIVE: true
STRICT_RAW_ENCODING_CHECK_REMAINS_REQUIRED: true
PRODUCTION_CODE_CHANGE_AUTHORIZED: false
TEST_CHANGE_AUTHORIZED: false
WORKFLOW_CHANGE_AUTHORIZED: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
CODEFLOWMU_WRITE_AUTHORIZED: false
```

## 2. 唯一授权修改

只允许修改仓库根目录 `.gitattributes`，保留已有两行，并追加以下四行，内容与
拼写必须完全一致：

```gitattributes
spec/fcop-4.0-spec.md text eol=lf
spec/fcop-4.0-spec.zh.md text eol=lf
src/fcop/rules/_data/v4/manifest.json text eol=lf
src/fcop/rules/_data/v4/*.md text eol=lf
```

不得以全局 `*.md`、`*.json`、`* text=auto` 或 workflow 中的 checkout/config
覆盖替代上述精确路径策略。不得运行会把无关路径纳入提交的全仓
`git add --renormalize .`。

该策略只规定 worktree 物化；不得修改以下权威文件本身的 Git blob 字节：

- `spec/fcop-4.0-spec.md`；
- `spec/fcop-4.0-spec.zh.md`；
- `src/fcop/rules/_data/v4/manifest.json`；
- `src/fcop/rules/_data/v4/*.md` 十八份规则文件。

## 3. 提交与证据链

允许在现有分支 `feat/fcop-4.0-wp4c.6a-distribution-resume` 和 Draft PR #30
继续，不得改写或压缩已有提交。固定顺序为：

1. 本任务书的 ADMIN 勘误提交；
2. 一个 Policy-only commit，除 `.gitattributes` 外不得包含任何文件；
3. 如需更新最终证据，只能追加一个 reports-only Content commit；
4. 最后追加一个 Manifest-only commit。

Policy-only commit 必须证明，相对阻断头 `3484133…`，二十一份权威输入的 Git
blob SHA-256 与字节长度全部不变；不得通过重写文件再恢复相同可见文本的方式
制造策略提交。

## 4. 必须完成的跨平台验证

在 Policy-only commit 后，至少完成并记录：

1. 对上述二十一份文件执行 `git check-attr text eol -- <paths>`，每一项均为
   `text: set`、`eol: lf`；
2. 在原生 Windows 的全新 checkout 中，不设置 `core.autocrlf=false` 等旁路，
   证明二十一份 worktree 文件不含 BOM 或 `\r`，并与对应 Git blob 逐字节相同；
3. 规则 Manifest 自校验和冻结英文规范 SHA-256 继续通过，现有 canonical data
   继续 19/19；
4. 现有 Alignment 2/2、DIST-27/28 20/20、Rule Distribution 176/176、Core
   119/119、FCoP、MCP、组合回归、clean-install/制品、真实 stdio 46/12/4、
   资源零副作用和 CodeFlowMu 固定 ref 只读 Shadow 均不得退化；
5. 在最终 Manifest HEAD 上，两个工作流的 Windows Python 3.10–3.13 八个矩阵
   项全部通过；对应 Linux、macOS 矩阵及下游 package job 也必须实际运行并通过，
   不得把 skipped、cancelled 或未触发记为通过。

CI 重跑必须来自包含 Policy-only commit 的新最终头；不得把
`34841330604e32c473a538afb634a81334eca8ad` 的失败运行重标为成功，也不得仅
rerun 旧 SHA 后作为新策略证据。

## 5. 禁止项与停止条件

本勘误不允许修改：

- `_loader.py`、`_read.py` 或任何生产代码；
- Manifest 中的 SHA-256/字节长度、冻结规范哈希或任何规范/规则正文；
- 测试、fixture、断言、skip、xfail、测试选择或阈值；
- GitHub Actions workflow、runner 矩阵或 checkout 参数；
- 已授权并通过的 `FcopError` 捕获定点修正；
- main、CodeFlowMu、版本号、PyPI、Release、发布状态或 WP4D。

若四行精确属性仍不能使 Windows 八个矩阵项全部通过，或需要第二处非报告修改，
立即停止并设置：

```yaml
WP4C_6_STATUS: BLOCKED
REQUESTED_GATE: NONE
```

全部验证完成后停止，只请求：

```yaml
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
REQUESTED_GATE: WP4C_RULE_DISTRIBUTION_ACCEPTED
```

不得自行签署 Gate、合并 main、发布或开始 WP4D。
