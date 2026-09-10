# FCoP 4.0 Schema 与 Python 快速开始

本文对应 WP4A.1 审核分支，不代表发布或工作区迁移授权。请使用本轮本地构建的 wheel，不要假定已有正式 FCoP 4.0 发布。包版本没有修改；v3 工作区及旧八份 Schema 保持不动。

## 运行真实示例

在安装审核 wheel 及既有依赖的环境中运行：

```sh
python /path/to/examples/v4/application.py sequential
python /path/to/examples/v4/application.py family
```

两个示例自行创建临时工作区，完成后清理该临时目录；输出归档 TASK、事件数量及文件 SHA-256，并通过新解释器从磁盘重新读取最终状态。示例不依赖 CodeFlowMu、MCP、网络、数据库或后台 Runtime。family 示例在 Root active 时创建两个普通 Branch TASK，各自产生 REPORT，再计算 family digest、追加 convergence，并使用独立授权完成 Root T7；不使用 Git branch/merge。

可信 evaluator 必须在 `Project(root, trusted_profiles={profile_id: evaluator})` 初始化边界注册，再通过 `create_workspace(protocol_version='4.0', encoding='fcop-filesystem/4.0', profiles=[profile_id])` 显式采用。业务请求只传引用，不携带裁判逻辑。示例采用固定演示 proof，**不是生产身份认证方案**，不能据此信任调用者声明。

## 离线发现 Schema

通过 `importlib.resources.files('fcop').joinpath('_data/schemas/v4')` 读取包内 JSON；建立 `$id` 到文档的离线映射，用 Draft 2020-12 validator 和 FormatChecker 验证。完整代码见英文并行文档。URL 是标识符，不要求联网访问 fcop.dev。内部 loader 不增加 Project 公共方法，也不是新的 Profile 注册协议。

实现复用既有 `jsonschema>=4,<5`，为兼容该范围使用 RefResolver；较新版本会给出弃用警告，没有因此新增运行依赖。所有引用来自包内固定文档，拒绝网络下载。

实际读写请使用 Project。独立消费者处理不可信原始字节时，必须先拒绝非法 UTF-8、BOM、CRLF 和 JSON/YAML 重复键，再将**完整对象**交给 Schema。普通 json.loads/yaml.safe_load 的最后键覆盖语义不符合该前置要求；Schema 无法发现已被解析器丢掉的重复键。

仅 workspace 与四类 frontmatter 根允许不透明 Profile 字段；encoding、transition binding、事件、固定 receipt 和 family 结构保持封闭。Profile 可以收紧自己的字段，但不能放宽 Base。历史事件的字符串字段不证明迁移合法，不能推导 NOW。Schema 通过更不代表授权、唯一 REPORT head、family 覆盖、幂等竞态或恢复成立，这些继续由真实 Core 和符合性测试检查。

canonical create request 不吸收 Profile 上下文；完整文件 evidence digest 仍覆盖扩展字段字节。生命周期保留未知字段语义值，不承诺原 YAML 排版字节不变。

运行 `python spec/schemas/v4/generate.py --check` 验证源码/包副本。精确验证结果、制品哈希及 CI 限制见 WP4A 报告。示例成功不等于 ADMIN 已签署 Gate。
