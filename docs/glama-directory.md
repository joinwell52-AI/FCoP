# Glama 目录收录与质量分（fcop-mcp）

> 对应 [awesome-mcp-servers PR #6301](https://github.com/punkpeye/awesome-mcp-servers/pull/6301) 维护者要求：须 **Claim** + **Glama Release** 后才有 quality score。  
> Score 页：<https://glama.ai/mcp/servers/joinwell52-AI/FCoP/score>

## 仓库已准备的文件

| 文件 | 作用 |
|------|------|
| `glama.json` | 维护者元数据（`joinwell52-AI`） |
| `Dockerfile` | Glama 构建镜像（`pip install fcop fcop-mcp` + `ENTRYPOINT fcop-mcp`） |
| `.dockerignore` | 缩小构建上下文 |
| `README.md` / `README.zh.md` | Glama card / score 徽章 |

## 你必须在浏览器完成的步骤（无法由 Agent 代登）

### 1. Claim

1. 打开 <https://glama.ai/mcp/servers/joinwell52-AI/FCoP>
2. 点击 **Claim**
3. 用 **joinwell52-AI** 组织下有权限的 GitHub 账号登录并授权

### 2. 同步仓库

Claim 后进入 Admin → **Sync Server**（或等待每日自动同步）。  
确保 `main` 已包含本仓库的 `glama.json` 与根目录 `Dockerfile`。

### 3. Glama Release（不是 GitHub Release）

1. Admin → **Dockerfile** 页
2. Dockerfile path：`Dockerfile`（仓库根目录）
3. 点击 **Deploy**，等待构建成功
4. 点击 **Make Release**，版本填 `3.2.4`（与 PyPI / `fcop-mcp` 一致）

完成后 Score 页应出现 **Tool Definition Quality** 与 **Server Coherence**，总分会高于当前的 **17%**。

### 4. 可选：种子用量

在服务器页使用 **Try in Browser** 跑几次工具调用，缓解 “No recent usage” 提示。

### 5. 回复 PR #6301

在 PR 留言并 @punkpeye，附上更新后的 Score 链接。

## 本地验证 Docker 镜像

```bash
docker build -t fcop-mcp:glama-test .
docker run --rm fcop-mcp:glama-test
```

stdio 模式下进程会等待 stdin；看到无报错退出即说明依赖安装正常。可用：

```bash
docker run --rm fcop-mcp:glama-test python -c "import fcop_mcp, fcop; print('ok')"
```

## 徽章（已写入 README）

```markdown
[![FCoP MCP server](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/badges/card.svg)](https://glama.ai/mcp/servers/joinwell52-AI/FCoP)
[![FCoP MCP server](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/badges/score.svg)](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/score)
```
