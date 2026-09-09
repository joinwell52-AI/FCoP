# FCoP 4.0 WP4D：Windows socketpair 离线守卫定点勘误与恢复授权 v1.0

```yaml
document_role: EXECUTION_ERRATUM
execution_authorized: true
authorized_scope: WP4D_MCP_SAMPLE_SOCKETPAIR_GUARD_ONLY_AND_WP4D_RESUME
parent_taskbook_commit: cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9
audit_erratum_commit: 22db1377163bb0b1e74c4b94fa1f594b3e762a9d
toolchain_erratum_commit: 086c358f4c96e21aa31890d147eacae4a359a11a
blocked_implementation_head: 737d3d3482f371616863a018f04ab1a756259723
draft_pr: https://github.com/joinwell52-AI/FCoP/pull/31
blocker: WINDOWS_310_311_STDLIB_SOCKETPAIR_BLOCKED_BY_SAMPLE_OFFLINE_GUARD
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

确认授权定点修正 MCP-only 第三方样例的离线审计守卫，并在验证通过后恢复原 WP4D。

固定日志证明：Windows Python 3.10/3.11 上，asyncio Proactor 初始化 self-pipe 时调用标准库 `socket.socketpair()`；该版本的标准库实现函数名为 `socketpair`，内部通过 loopback `bind/connect` 构造 IPC 对。现有样例只识别较新版本路径 `_fallback_socketpair`，因此在 MCP stdio server 启动前误拦截 `socket.bind`。

这不是 FCoP Core、MCP server、FastMCP、协议或制品缺陷。正确修复边界是：只按 CPython 标准库 `socketpair` / `_fallback_socketpair` 的 code object 身份放行其内部审计事件；不得按 loopback 地址、端口、事件名或调用栈字符串泛化豁免网络访问。

CPython 固定参考：

- Python 3.10.11：`https://github.com/python/cpython/blob/v3.10.11/Lib/socket.py`
- Python 3.11.9：`https://github.com/python/cpython/blob/v3.11.9/Lib/socket.py`
- Python 3.12.14：`https://github.com/python/cpython/blob/v3.12.14/Lib/socket.py`

此前 `10/12` 与 BLOCKED 回执保持为历史事实，不得改写为当时通过。

## 2. 唯一允许的样例修改

只允许修改：

```text
examples/v4/third-party/mcp-only/server.py
```

### 2.1 精确允许集合

必须在安装 audit hook 前，从当前解释器的标准库 `socket` 模块收集下列真实函数对象中存在且具有 `__code__` 的 code object：

```text
socket.socketpair
socket._fallback_socketpair
```

形成不可变的精确允许集合。`offline(event, args)` 仅在下列条件全部成立时允许受控事件继续：

1. 当前事件仍属于既有受控集合：`socket.connect`、`socket.bind`、`socket.getaddrinfo`、`socket.sendto`；
2. `sys._getframe(1).f_code` 与上述标准库函数对象之一的 `__code__` **对象身份相同**；
3. 该 code object 是在安装 audit hook 前直接从已导入的标准库 `socket` 模块获取。

推荐等价结构：

```python
_SOCKETPAIR_CODES = frozenset(
    fn.__code__
    for name in ("socketpair", "_fallback_socketpair")
    if (fn := getattr(socket, name, None)) is not None
    and hasattr(fn, "__code__")
)


def offline(event, args):
    if event not in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto"}:
        return
    if sys._getframe(1).f_code in _SOCKETPAIR_CODES:
        return
    raise RuntimeError("WP4D server network access forbidden: " + event)
```

可以作 Ruff/兼容性所需的等价格式调整，但语义必须同等或更窄。

### 2.2 必须保持不变

样例的以下内容冻结：

- `PROFILE`、evaluator 与授权判定；
- audit hook 的安装位置：必须在导入 `fcop_mcp.server` 之前生效；
- 被守卫的四个 socket 事件；
- 拒绝异常类型和消息前缀；
- `create_server` 参数；
- `transport="stdio"` 与 `show_banner=False`；
- 客户端 JSON-RPC、46/12/4、流程、重开、幂等、冲突零副作用等全部逻辑。

不得改动 `examples/v4/third-party/mcp-only/client.py` 来隐藏 server 启动失败。

## 3. 定点守卫测试授权

允许新增且仅允许新增：

```text
tests/test_fcop_mcp/test_wp4d_rc_offline_guard.py
```

该测试必须在独立子进程中加载样例守卫，避免 audit hook 污染 pytest 主进程，并覆盖：

1. 当前平台的 `socket.socketpair()` 可成功创建并关闭双方端点；
2. 样例代码直接执行 AF_INET loopback `bind` 仍抛出既有 `RuntimeError`；
3. 直接 `connect`、`getaddrinfo`、`sendto` 各自仍被拒绝；
4. 用户定义的同名 `socketpair` 函数不得进入允许集合；
5. 允许集合不得依据 filename、函数名称字符串、host、port 或 loopback 地址作运行时放行。

禁止 monkeypatch 守卫结果、删除 audit event、仅静态搜索源码或将失败断言改为 skip/xfail。

## 4. 禁止的替代修法

不得：

- 泛化允许 `127.0.0.1`、`::1`、`localhost`、任意 loopback 或临时端口；
- 对 Windows、Python 3.10/3.11 或 Proactor 整体关闭 audit hook；
- 允许所有来自 `socket.py` 的调用；
- 只按 `co_filename` 或 `co_name` 字符串放行；
- 改为网络 MCP transport；
- 修改 FastMCP、AnyIO、asyncio、CPython 或已安装依赖；
- 修改 `scripts/wp4d_consume.py`、RC workflow 或矩阵以绕过两个失败单元；
- 修改 FCoP/MCP 生产代码、规范、Schema、Conformance、规则、候选版本或依赖 pin；
- 复用失败矩阵结果并宣称 `12/12`。

## 5. 恢复基线与提交纪律

必须继续使用现有实现分支与 Draft PR #31：

```text
feat/fcop-4.0-wp4d-rc-candidate
```

从远端固定阻断 HEAD：

```text
737d3d3482f371616863a018f04ab1a756259723
```

验证父链和干净工作树。定点修正形成一个独立提交，且只包含：

```text
examples/v4/third-party/mcp-only/server.py
tests/test_fcop_mcp/test_wp4d_rc_offline_guard.py
```

不得改写、压缩或删除既有三次阻断记录与证据；不得 force-push。

## 6. 恢复验证顺序

### 6.1 定点验证

先执行新增守卫测试，在 Windows Python 3.10、3.11、3.12、3.13 以及至少一个非 Windows 平台上全部通过，零 skip。

随后用固定候选制品重跑 MCP-only 安装态样例：

- Windows Python 3.10 wheel + sdist 均通过；
- Windows Python 3.11 wheel + sdist 均通过；
- server 必须实际完成 initialize；
- transport 保持 stdio；
- server 日志不得出现网络守卫 RuntimeError 或隐藏异常。

### 6.2 全矩阵与制品身份

修正发生在四制品之外的第三方样例，已核验候选制品内容不应改变。但最终执行仍必须：

- 重新核验四个候选制品与 `candidate-manifest.json` 的固定哈希；
- 证明候选提交/manifest 身份仍与 RC workflow 绑定；
- 完整重跑全部 `12/12` consumer，而不是只补两个失败单元；
- 每个 cell 的 wheel 与 sdist 两条安装来源均完成，因此最终 installed origin paths 必须 `24/24`；
- 保持 Twine `2/2` 与制品可复现 `4/4` 的远端证据可追溯。

如果现有候选 manifest 将提交 SHA 绑定到修改前 HEAD，必须按原 WP4D 规则重新构建四制品并产生新哈希；不得篡改 manifest 或只替换 commit 字段。后续所有 consumer 必须使用同一组新制品。

### 6.3 最终全量验收

最终 Manifest HEAD 必须重新完成：

- Windows 与 Ubuntu 全量回归，均不低于 `1925/1925`（原 `1924` 加新增守卫测试，实际收集数如因参数化增加应如实报告）；
- 既有全部适用 CI，Windows 项全部通过；
- RC consumer `12/12`、skip `0`、installed origin paths `24/24`；
- Python-only 与 MCP-only 第三方项目；
- response-loss retry、crash recovery、3.2.5 workspace 零迁移/零漂移；
- Host 规则分发矩阵；
- CodeFlowMu 固定 3.2.5 只读 shadow `14/14`；
- MCP 公开面 `46 tools / 12 static resources / 4 templates`；
- 权威候选文件 `19/19` 与冻结字节 `21/21`；
- 最终 Manifest HEAD 的全部适用 CI。

不得继承阻断 HEAD 的 Ubuntu `1924/1924`、既有 CI `27/27` 或 consumer `10/12` 作为最终 HEAD 通过证据。NOT_RUN、skip、queued、in progress、cancelled 和 allowed failure 都不是 PASS。

## 7. 报告与 Manifest 追加字段

六份报告、JUnit 和 Manifest 必须保留三次历史 BLOCKED 事实，并新增：

```yaml
socketpair_guard_erratum_commit: <this-taskbook-commit>
socketpair_guard_resume_base: 737d3d3482f371616863a018f04ab1a756259723
socketpair_guard_fix_commit: <two-file-commit>
socketpair_allowance: STDLIB_CODE_OBJECT_IDENTITY_ONLY
generic_loopback_allowed: false
direct_network_negative_tests: <passed>/<total>
windows_guard_matrix: 4/4
rc_consumer_matrix: 12/12
installed_origin_paths: 24/24
```

最终全部交付文件必须从远端 Manifest HEAD 逐项回读并核验 SHA-256，只记录远端值。

## 8. 权限边界

本勘误不授权：

- 修改 `main` 或合并 Draft PR；
- 创建或推送 tag；
- 上传 PyPI；
- 创建 GitHub Release；
- 更新 MCP Registry、Zenodo、DOI、`CITATION.cff` 或 `mcp/server.json`；
- 修改 `.github/workflows/release.yml`；
- 修改 CodeFlowMu；
- 签署 `FCOP_4_RC_ACCEPTED`。

## 9. 停止条件

若 code-object 身份放行仍不能使 Windows 3.10/3.11 的 stdio MCP 启动，或任一直接网络负向测试被放行，或需要超出第 2–3 节的文件范围，立即停止：

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
