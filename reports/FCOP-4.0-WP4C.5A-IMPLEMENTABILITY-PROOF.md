# WP4C.5a 开工核验：v3 protocol 返回形态冲突

```yaml
STATUS: FROZEN_COMPATIBILITY_CONTRACT_CONFLICT
AUTHORIZED_SCOPE: WP4C_5A_ONLY
RESUMED_SCOPE: FULL_WP4C_5
TASKBOOK_COMMIT: c7986fb618b2f66c4ad2b157917f64a00bccf1c3
TASKBOOK_SHA256: cbc7a3be0f641bc782715d13bb6b774dfad002d8a1002896e629404e3e40ae47
TASKBOOK_BYTES: 10686
TASKBOOK_PARENT: df395c7e221f850352d907933ccaab0937706c8f
INPUT_INTEGRITY: PASS
ORIGIN_CONFORMANCE_REF: 1f4df9cc650f63b9e842d806340eb31b768f708e
AUTHORIZED_CONFORMANCE_CORRECTIONS: 2/2
EFFECTIVE_CONFORMANCE_REF: d29e4d41ad4e1fc74e6d3513faa6b95d97ba0dfb
EFFECTIVE_CONFORMANCE_TREE: 1134d730e4c5ab23aa7b3ec91138da6981c2f009
EFFECTIVE_CONFORMANCE_FILES: 9/9
PRODUCTION_IMPLEMENTATION_STARTED: false
IMPLEMENTABILITY_PROOF: BLOCKED_BEFORE_COMPLETION
REQUESTED_GATE: NONE
```

ME / solo 执行 ADMIN 固定任务书。此文件记录真实开工核验和合同冲突，**不是**已完成全部设计证明、实施或验收的声明。固定任务书是决策输入；本报告是执行证据。没有初始化、部署或迁移原 dogfood 工作区。

## 1. 上一项输入阻断已经解除

[WP4C.5a 唯一续作任务书](https://github.com/joinwell52-AI/FCoP/blob/c7986fb618b2f66c4ad2b157917f64a00bccf1c3/taskbooks/fcop-4.0/WP4C.5a/01-Effective-Conformance-Baseline-Correction-and-WP4C.5-Resume-Taskbook-v1.0.zh.md)已从固定 GitHub Contents Blob 解码核验：10686 字节、上述 SHA-256、严格 UTF-8、无 BOM、LF；本地 Git Blob 与远端相等。Commit API 确认直接父提交 df395c7e221f850352d907933ccaab0937706c8f，且仅新增该任务书。

完整读取原任务书、新任务书以及 PR #26 两份报告和 Manifest。原 WP4C.5 任务书固定 SHA-256 为 6ebf0db70dcfe3d55ecbc0cfbe4b33d4d739057dac93a5f66801440fb2c144b4，22456 字节。本次不再要求有效测试树等于原始冻结树。

新工作树为 `D:/FCoP-wp4c5a-compatibility-resume`，分支为 `review/fcop-4.0-wp4c.5a-compatibility-resume`，从 c7986fb 固定提交建立，开工时 CLEAN。相对 d29e4d4 只存在规定的六份文档：WP4C.4 Gate、原任务书、PR #26 三份阻断证据、新任务书。Core 两份规范对 aec4c2b、RD 双语合同/决策/矩阵对 f6831de 均无 Git 差异。

有效目录九个 Blob/大小与新任务书表格逐项相同，checkout 字节与其 Git Blob 相同；四项修正摘要均相同：

| 文件（tests/conformance/rule_distribution_v4/） | SHA-256 |
| --- | --- |
| conftest.py | e9571f4d0051e04cbc0e63ef9a8e2cdc9d5facd427afafb6c4934c305d835a67 |
| test_dist_00_meta.py | 816d739dd4eed73c545ee75947c893eba44f5a9f944dbc37ef978b582746c9d6 |
| test_dist_01_06_manifest.py | dafac52d52a9c8568dd9d360b58cbba6676446cf62b3a498701a19cbb0697d78 |
| test_dist_25_30_failures_artifacts_context_gates.py | be6a3fe99b19da82f1c14b964c96d02160812b169d5ad10b4d5cd5203a64839c |

`git log 1f4df9c..HEAD -- tests/conformance/rule_distribution_v4` 仅列出 e1ed85e4ba5aba212ddf3cc4f880c0abecc2bfab、115751b4c24a1924062a81a21e0d655e8cb5fedc。两次修正保留，不回退、不重做。

## 2. 新工作树实测 13 节点基线

命令：

```text
python -X utf8 -m pytest
 tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py::test_dist_23
 tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py::test_dist_24
 tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_26
 tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py::test_dist_29
 -q --tb=line -p no:cacheprovider
 --basetemp=D:/fcop-wp4c5a-target-baseline
 --junitxml=C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5a-target-baseline.xml
```

Windows / Python 3.12.9；PYTHONDONTWRITEBYTECODE=1，PYTHONPATH 只指新工作树 src、mcp/src、根目录。全新临时沙箱，未删除旧测试现场。结果 **1 passed / 12 failed / 3 warnings，32.98 秒，exit 1**；无 skip/xfail。JUnit：13919 字节，SHA-256 `40254c6f2ad35d713319addd28db6b683b3c4122c7dbd57e41aea2937375cf02`。

| 实际节点 | 结果 | 唯一 owner |
| --- | --- | --- |
| test_dist_23[unversioned-v3] | FAIL | WP4C.5 |
| test_dist_23[explicit-v4-on-v3] | FAIL | WP4C.5 |
| test_dist_23[v4-no-adoption] | PASS | WP4C.5 |
| test_dist_24[3.0-fcop://rules] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://protocol] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://guidance/sequential/en] | FAIL | WP4C.5 |
| test_dist_24[3.0-fcop://team] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://rules] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://protocol] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://guidance/sequential/en] | FAIL | WP4C.5 |
| test_dist_24[4.0-fcop://team] | FAIL | WP4C.5 |
| test_dist_26 | FAIL | WP4C.5 |
| test_dist_29 | FAIL | WP4C.5 |

这些当前失败来自未实现 action 或尚未接通的 legacy 分派，不把运行栈本身说成合同冲突。下节冲突是独立核对 oracle 与资源合同得出的结论。

## 3. 新冲突：DIST-24 把 v4 protocol 内容形态施加到 v3

三个必须同时遵守的输入：

1. 冻结 RD-21（`docs/fcop-4.0/rule-distribution-contract.md:204`；中文同条）要求 legacy 资源保留版本合同。WP0 资源处置表 `reports/MCP-RESOURCE-DISPOSITION-4.0.md:22` 固定 `fcop://protocol` 的来源为 `fcop.rules.get_protocol_commentary()`，是 packaged legacy commentary，不是规范身份 JSON。
2. 原任务书 §7.2 的版本表（第 177 行）明确 v3 保持 legacy protocol 资源合同，v4 才返回冻结规范 path/revision/sha256。第 181 行要求 Project typed object 与 MCP 文本语义等价，JSON 对象必须使用确定性 JSON；§7.3 第 198 行和 §11.2 第 314 行再次要求旧 v3 语义/内容不漂移。
3. 有效冻结测试 `tests/conformance/rule_distribution_v4/test_dist_21_24_assembly_compat_mcp.py:108,127` 参数化 3.0/4.0，却仅按 URI 判断 protocol 分支，没有限定 version=4.0：

```python
elif resource == "fcop://protocol":
    assert {"path", "revision", "sha256"} <= field(direct, "content").keys()
    assert "entry_generated" not in field(direct, "content")
```

因此 `test_dist_24[3.0-fcop://protocol]` 也要求 `content` 是带规范身份键的对象。Driver 原样转发 Project 公共返回值，不存在获准的版本化解包层。该测试文件 Git Blob 为 ad7781c0a9fe417b3f750f2e3044891ca5f98fdb、6175 字节、SHA-256 `8eed3f3a2d901a759cc608f8cc88b67dcba7b8a2ea023f40751a5803d8d85193`；固定 GitHub 回读与本地相等。这不是新 checkout 或两次历史修正引入的差异。

### 真实 MCP 内容核验

在刚完成的 `test_dist_24[3.0-fcop://protocol]` 临时 fixture 工作区内，调用现有 `server.create_server(root)` 和 `asyncio.run(mcp.read_resource('fcop://protocol'))`；没有替换生产返回值、没有 mock 成功结果。对比现有 `fcop.rules.get_protocol_commentary()`：

```yaml
DECLARED_PROTOCOL_VERSION: '3.0'
MCP_CONTENT_TYPE: str
MIME_TYPE: text/markdown
EQUALS_LEGACY_GETTER: true
UTF8_BYTES: 117608
SHA256: 8ac413b1c39238df82a175d108c166c58c27fbe833b202470e140755780250d3
HAS_KEYS_METHOD: false
SANDBOX_FILES_BEFORE_AFTER_EQUAL: true
```

现有实现路径为 `mcp/src/fcop_mcp/resources.py` 的 v3 `original()` 分支 → `mcp/src/fcop_mcp/server.py:3784` → legacy getter；该来源未修改。实测 FastMCP 注册表为 **46 tools / 11 static / 3 templates**，不是只抄 disposition 数量。

### 为什么不能自行绕过

- 保留 legacy 字符串作为 `content`：不满足冻结 `.keys()` 断言。
- 改成规范身份对象，并按任务书把对象序列化为 MCP JSON：改变现有 v3 Markdown 内容合同。
- Project 返回身份对象，MCP 再只提取另加的 text 字段：需要定义目前未固定的 v3 特殊解包/元数据舍弃合同；不能把它自行称为任务书要求的 JSON 对象表示与语义等价。
- 给字符串伪装 `.keys()`、根据 transport 返回不同内容、只为测试分支造成功结果：不是合规的类型化资源实现。
- 修改冻结条件为仅 v4 或放宽断言：超出本轮允许写集。

这里不声称所有未来设计都不可能；阻断的是**当前固定验收 oracle 与保留 legacy 内容/序列化要求没有一致的明确解释**。需 ADMIN 固定 v3 的正式返回形态，不能由实现暗中选择。

最小建议（未执行）：保留 v3 protocol 的 legacy 文本，规范身份对象断言只适用于 v4；如 ADMIN 希望采用 v3 内容对象与旧 MCP 文本之间的特殊投影，请先明确其字段、表示和等价规则及相应验收。不请求扩大业务功能或修改其他 Test ID。

## 4. 辅助验证与停止边界

现有 MCP snapshot 四项测试，加 `test_all_static_resources_and_disposition[v3]`，共 **5 passed / 1 warning，2.84 秒，exit 0**。运行于新沙箱 `D:/fcop-wp4c5a-resource-proof`，命令为 `python -X utf8 -m pytest tests/test_fcop_mcp/test_tool_surface.py tests/test_fcop_mcp/test_wp4b_delivery.py::test_all_static_resources_and_disposition[v3] -q --tb=short -p no:cacheprovider`，另指定上述 basetemp 与 JUnit。JUnit `C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c5a-resource-proof.xml`：860 字节、SHA-256 `8265361578ed229d5353ede90496a075780669137674752af18a8c422a0b1e71`。

原任务书 §3 第 88 行要求发现冻结合同/测试无法同时满足时停止；§15 同样规定只交付阻断报告。WP4C.5a §6 第 151 行明确阻断时只提交新事实报告、REQUESTED_GATE=NONE。遵照这些条款，未进入生产编码；不把此 preflight 充作完整 Implementability Proof，未完成五层设计、安全测试、全部回归或真实授权 Shadow。

CodeFlowMu 仅作 Git 身份和固定版本隔离证据的只读初查：当前本地 HEAD 仍为 b961b16dd0c8863ead6995d963fe0ca576a8abaa；历史证据提交是 789cb3fa8a007f050248784f7daf689808a549a2。读取其固定版本隔离结论不等于已完成本轮真实 Shadow；不引用历史产品测试数作为本轮验收。未修改、安装、启动、checkout 或清理该产品。

原 D:/FCoP 保持 dirty main da79dfefd99f597c9e422ce9edec22157f915a21；WP4C.4/PR #26 工作树和所有历史未跟踪材料保留。远端 main 核验基线为 68dbeb15f4e7f84e1d03f907be9fa66c2265843e。只交付本新报告、RESULT 和新 Manifest；不覆盖 PR #26 三文件，不改其 PR、不合并、不发布、不进入 WP4C.6。
