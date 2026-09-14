# 会话结束后，任务和交付还在。

[English](mcp-handoff.md) · [FCoP](../README.zh.md) · [示例源码](../examples/mcp_handoff.py)

先试一个具体交接：第一个 MCP 会话创建任务，计算 SHA-256，并提交报告。会话退出后，第二个全新会话从本地文件中读回同一任务、同一次尝试和同一份报告。

## 复制这段话给你的编程 AI

```text
请帮我运行 FCoP 跨会话交接示例：
https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-handoff.zh.md
先检查示例，在隔离环境准备依赖，再用全新演示目录实际运行。告诉我真实结果，打开保存的任务和报告，并说明是否仍待验收。命令由你执行，保留我现有项目和客户端设置。
```

AI 需要能运行命令和读写文件。本例自行建立 MCP 会话，无需模型 API Key，也无需修改 IDE 配置。体验后要接入正在使用的客户端，可以继续用 [AI 安装指令](ai-install.md)。

## 你会看到什么

| 步骤 | 实际操作 | 核对什么 |
|---|---|---|
| 1 | 发现已发布 MCP 服务的工具与资源 | 发现过程没有写入演示工作区 |
| 2 | 创建、领取任务，计算摘要，提交报告 | 任务进入 `review`，交付内容保存为文件 |
| 3 | 关闭第一个会话，启动全新会话 | 从同一工作区读回任务和报告 |
| 4 | 比较任务、尝试、报告身份和文件摘要 | 内容仍在，第二个会话读取后文件未改变 |

成功运行末尾会显示 `PASS`；固定 4.0.2 示例预期核对 7 个文件。路径和任务编号每次不同。必须实际运行成功才能说通过。

**报告写着 `result=done`，任务仍是 `review`。** 交付主张已保存，不等于已经有人验收。

## 给 AI 的执行说明

1. 检查 Python 3.10+ 和 `uvx`。缺少 uv 时，按 [uv 官方安装说明](https://docs.astral.sh/uv/getting-started/installation/) 在宿主权限允许范围内准备。使用合适的 Python 环境，保留其他项目的依赖。
2. 阅读本仓库的 [examples/mcp_handoff.py](../examples/mcp_handoff.py)，放进新演示目录，或使用已有 FCoP 源码副本。脚本本身只用 Python 标准库；uv 在隔离环境中准备固定的 `fcop==4.0.2` 和 `fcop-mcp==4.0.2`。
3. 由你运行脚本。在仓库根目录下，命令如下：

   ```sh
   python examples/mcp_handoff.py --output <新演示目录的父目录>
   ```

   把占位符换成真实路径。省略 `--output` 时使用系统临时目录。每次都新建独立目录并保留结果；首次下载依赖可能较慢。

4. 检查退出码，读取生成的 `result.json`：应为 `status=pass`、`stage=review`；任务、尝试与报告的身份对应；报告包含实际摘要；第二个会话读取前后工作区文件哈希一致。固定双包应发现 49 个工具、12 个资源、4 个资源模板。工作区旁保留 MCP 调用记录和两个 stderr 日志。
5. 打开任务和报告，告诉用户保存在哪里、跨会话保留了什么，以及验收仍未完成。依赖下载失败、超时或工具报错时，按真实失败排查，不能写“试用成功”。

计算由 Python `hashlib` 完成，输入为 `FCoP handoff example`，SHA-256 应为：

```text
cceecdb3da6e529e216fa6c65dcbf764aa74a65d52c32c798ca4af4d68e8f489
```

## 这个示例证明到哪里

两个独立 stdio 连接调用真实发布的 MCP 适配器；第一个会话退出后，第二个读回持久化工作。计算与调用由脚本完成，未调用大模型，未测试 Cursor 到 Codex 的具体界面，也不代表外部用户采用。审批与归档不在本例范围内。

运行失败时，可以在 [Issues](https://github.com/joinwell52-AI/FCoP/issues/new) 提供系统、Python/uv 版本、失败步骤和去除私人路径后的报错片段。成功后，欢迎告诉我们你下一步希望交接的真实任务。如果这套协议和示例对你有用，可以给 [FCoP](https://github.com/joinwell52-AI/FCoP) 加星收藏。
