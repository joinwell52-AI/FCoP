# CLI v1 参考 — FCoP 4.0.2

**CLI = Setup + Observe + Diagnose；MCP = Work。** 支持 Python 3.10–3.13。
`fcop` 包含 Core 和 CLI，不依赖 MCP；`fcop-mcp` 为可选安装。

```sh
pip install fcop
fcop version
fcop doctor
fcop init
fcop status
```

可选工具目录查询：

```sh
pip install fcop-mcp
fcop tools
fcop tools merge_branches --json
```

| 命令 | 参数 | 写入 |
| --- | --- | --- |
| init | --root PATH、--protocol VERSION | 显式调用 Core 创建工作区 |
| status | --root PATH | 无 |
| inspect | TASK-ID 或 --path ENVELOPE、--root PATH | 无 |
| validate | --root PATH、可选 --path ENVELOPE | 无 |
| tools | 可选 TOOL-NAME | 无 |
| doctor | --root PATH | 无 |
| version | 无 | 无 |
| spec | 无 | 无 |
| migrate | 保留 --to-v3、--project-root、--workspace、--apply | 默认预演，仅 --apply 写入 |

八个非迁移命令支持 `--json`。工作区根默认当前目录；相对信封路径相对
`--root` 解析，绝对信封路径也必须位于该工作区内。支持空格和中文路径。
CLI 不提供创建任务、批准、Branch、收敛或授权操作，这些仍由 MCP/Python 承担。

使用 `fcop --help` 查看命令；裸 `fcop` 保留历史迁移提示，写 stderr 并返回 1。
`migrate-workspace` 与 `migrate --to-v3` 的既有参数、输出和退出语义不变。

## 输出合同

JSON stdout 仅含一个文档，固定字段为 schema_version（1）、command、status、
data、errors、warnings。status 为 ok/error/invalid/unavailable；异常时 data
可为 null，errors 每项含 code 和 message。键排序、无 ANSI/banner、无新增时间戳。
人类输出是相同事实的标题加缩进文本。参数解析错误写 stderr，返回 2；结构化
业务结果写 stdout。迁移命令沿用旧输出。

退出码：0 成功/有效（可能有提示）；1 内部失败（裸调用历史行为也为 1）；
2 协议/数据/输入无效；3 工作区、依赖或环境不可用/不支持。

未初始化时 status 返回 initialized=false，inspect/validate 返回 3。
doctor 对缺少工作区或可选 MCP 给 WARN，不安装、不初始化。重复键、非法编码、
半初始化配置不会被猜测修复。重复 init 遵守 Core 的已存在错误，不覆盖。

doctor 检查 Python 声明、包版本与导入、CLI 入口、MCP 兼容与 Catalog、捆绑资料、
工作区配置和可读权限。每项含 check_id、PASS/WARN/FAIL、message、evidence；
不通过试写测试权限，不联网、不修改 Host，不提供 --fix/--repair/--recover。

## 事实边界

公共只读 `fcop.observation` 聚合现有 Core 能力，提供 workspace_status、
inspect_object、validate_workspace、bundled_inventory。不新增生命周期、授权
或恢复规则。inspect 保留 Core 返回的摘要 null、未就绪理由和错误；validate
只检查可观察的编码、Schema、权威路径、身份、状态目录与最后事件及引用，
弱引用不能解析仍是警告，不评价工作质量。多文件读取不是并发写入下的原子快照。

spec 分开报告安装包内的 v4 Schema/规则版本及旧规则版本；v4 规范为固定
路径、提交和哈希引用，不谎称 wheel 包含完整规范，也不从网络下载。

`fcop_mcp.catalog.get_tool_catalog(name=None)` 从唯一 MCP 声明表返回新建的、
排序后的 name/disposition 行；未知名称抛 KeyError。不启动服务，不复制参数
定义。CLI/Catalog/真实 stdio 工具集合相等，MCP 的 49/12/4 能力面不变。
