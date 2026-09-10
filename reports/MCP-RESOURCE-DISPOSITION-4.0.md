# FCoP 4.0 MCP 资源逐项处置

> Canonical source：`tests/test_fcop_mcp/snapshots/tool_surface.json`
> Registration source：`mcp/src/fcop_mcp/server.py:3738-3899`
> 基线：`origin/main@68dbeb15f4e7f84e1d03f907be9fa66c2265843e`

## 1. 审计口径

工具、静态资源和 URI template 分别计数。资源返回的是 snapshot/view/profile 文本，不得覆盖仓库 current Specification、磁盘事实或版本绑定。canonical snapshot 数量为静态资源 **11**、resource template **3**。

测试证据统一为 `tests/test_fcop_mcp` snapshot/resource tests（`80 passed`）和全量 suite（`1225 passed, 2 skipped`）。

## 2. 静态资源（11/11）

| # | 当前 URI | 内容来源 | 是否规范性 | 缓存/生成方式 | v4 Disposition | 版本风险 | 测试证据 |
|---:|---|---|---|---|---|---|---|
| 1 | `fcop://config` | 当前 Project `config_path` 原文；未初始化时生成 JSON 状态 | 否；是 workspace/Profile snapshot | 每次请求读磁盘或生成 | `PROFILE_RESOURCE` | 中：当前 docstring 仍称旧 `docs/agents/fcop.json`；不得把 config 当 C1 唯一身份 | snapshot + resource tests |
| 2 | `fcop://letter/en` | bundled `letter-to-admin.en.md` | 否 | wheel 资源读取 | `TOOLKIT_RESOURCE` | 中：随规则/工具演进可能漂移 | 同上 |
| 3 | `fcop://letter/zh` | bundled `letter-to-admin.zh.md` | 否 | wheel 资源读取 | `TOOLKIT_RESOURCE` | 中：同上 | 同上 |
| 4 | `fcop://prompt/install` | bundled `agent-install-prompt.zh.md` | 否 | wheel 资源读取 | `TOOLKIT_RESOURCE` | 中：安装命令/包版本会变；不得自动初始化 | 同上 |
| 5 | `fcop://prompt/install/en` | bundled `agent-install-prompt.en.md` | 否 | wheel 资源读取 | `TOOLKIT_RESOURCE` | 中：同上 | 同上 |
| 6 | `fcop://protocol` | `fcop.rules.get_protocol_commentary()` → bundled `fcop-protocol.mdc` 3.2.5 | 解释性/Profile 规则投影 | wheel 资源读取 | `PROFILE_RESOURCE` | 高：部署副本可滞后，不能替代 frozen Specification | 同上 |
| 7 | `fcop://rules` | `fcop.rules.get_rules()` → bundled `fcop-rules.mdc` 3.2.5 | 行为规则/Profile；不是 Base Schema | wheel 资源读取 | `PROFILE_RESOURCE` | 高：Host 部署副本与 wheel 可不同版本 | 同上 |
| 8 | `fcop://spec` | `fcop.rules.get_spec("zh")` → bundled v1.1 中文 spec | 仅 informative snapshot | wheel 资源读取 | `SPEC_SNAPSHOT` | **严重**：URI 名未表明 v1.1；并非 current v3/3.2.5，更不是 v4 | 同上 |
| 9 | `fcop://spec/en` | `fcop.rules.get_spec("en")` → bundled v1.1 English spec | 仅 informative snapshot | wheel 资源读取 | `SPEC_SNAPSHOT` | **严重**：同上 | 同上 |
| 10 | `fcop://status` | 调用 `get_team_status()` | 否；派生 view | 每次请求扫描/格式化 | `TOOLKIT_RESOURCE` | 中：可能受 Host binding、规则版本与读取失败影响 | 同上 |
| 11 | `fcop://teams` | `fcop.teams.get_available_teams()` 的 name/roles/leader JSON | 否；bundled Profile catalog | 每次请求枚举模板 | `PROFILE_RESOURCE` | 中：固定角色不得反向进入 Base Core | 同上 |

所有内容来源均已定位，`UNKNOWN_SOURCE=0`。

## 3. Resource templates（3/3）

| # | 当前 URI 模板 | 参数 | 内容来源 | v4 Disposition | 路径安全 | 测试证据 |
|---:|---|---|---|---|---|---|
| 1 | `fcop://teams/{team}` | `team` | `fcop.teams.get_template(team,"zh").readme` | `PROFILE_RESOURCE` | 不直接拼接任意磁盘路径；由已注册 team template 解析，未知 team 返回错误文本 | snapshot + resource tests |
| 2 | `fcop://teams/{team}/{role}` | `team`, `role` | 中文 template 的 `roles[role.upper()]` | `PROFILE_RESOURCE` | team 先经 registry；role 仅作 dict key，未知 role 返回已知列表 | 同上 |
| 3 | `fcop://teams/{team}/{role}/en` | `team`, `role` | English template 的 `roles[role.upper()]` | `PROFILE_RESOURCE` | 同上 | 同上 |

模板没有直接使用用户输入做 `Path` join，因此当前调用链没有目录穿越写入面；但返回内容是 Profile 文档，不是 authorization 的 Core 证明。

## 4. 规范性与版本绑定结论

1. `fcop://spec[/en]` 的实现 docstring 已明确它返回 wheel-bundled v1.1、current 3.0 spec 不在 wheel（`server.py:3769-3806`）。因此 URI 是历史 `SPEC_SNAPSHOT`，不可作为 3.2.5/4.0 authoritative spec。
2. `fcop://rules` 与 `fcop://protocol` 返回 packaged rule/profile snapshot；工作区部署副本可能落后。版本比较应显式呈现，而不是任选其一覆盖另一份。
3. `fcop://config` / `status` 是当前绑定项目的 snapshot/view；C1 workspace identity 必须来自 WP1 冻结的文件合同。
4. team/role 资源是 Profile。FCoP 4.0 Base Core 不内置 CodeFlowMu 或任何 preset team 角色表。
5. v4 若继续提供不带版本号的 `fcop://spec`，必须明确其绑定策略、内容摘要和不一致时的 fail-closed 行为；本轮不修改 URI 或内容。

## 5. 完成状态

```text
STATIC_RESOURCES_COMPLETED: 11/11
RESOURCE_TEMPLATES_COMPLETED: 3/3
UNKNOWN_SOURCE: 0
CANONICAL_STATIC_DUPLICATES: 0
CANONICAL_TEMPLATE_DUPLICATES: 0
```
