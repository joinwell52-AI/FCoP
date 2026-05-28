# Glama 目录收录与质量分（fcop-mcp）

> 对应 [awesome-mcp-servers PR #6301](https://github.com/punkpeye/awesome-mcp-servers/pull/6301) 维护者要求：**Claim** + **可见 Glama quality score**。  
> 服务器：<https://glama.ai/mcp/servers/joinwell52-AI/FCoP>  
> Score：<https://glama.ai/mcp/servers/joinwell52-AI/FCoP/score>

## 当前状态（2026-05-28）

| 项目 | 状态 |
|------|------|
| Glama Claim | ✅ 已完成（Author verified） |
| Glama Release | ✅ 已发布（v3.2.4） |
| Profile 完成度 | **92%**（可选：Related servers 未填） |
| Server Coherence | **B** |
| Tool Definition Quality | **B** |
| Maintenance / License | **A** |
| Score 徽章 | **A - A**（README 已嵌入） |
| awesome-mcp-servers PR | `joinwell52-AI/awesome-mcp-servers-1` → `add-fcop` |

## 仓库已准备的文件

| 文件 | 作用 |
|------|------|
| `glama.json` | 维护者元数据（`joinwell52-AI`） |
| `Dockerfile` | Glama / 本地构建（`python:3.12-slim` + `fcop` / `fcop-mcp`） |
| `.dockerignore` | 缩小构建上下文 |
| `README.md` / `README.zh.md` | Glama card / score 徽章 |

## Glama Dockerfile 向导（若需重 Deploy）

**不要**使用默认的 `uv sync` + `fcop`（那是 CLI，不是 MCP 服务）。

| 字段 | 推荐值 |
|------|--------|
| Python version | **3.12** |
| Node.js | **24**（`mcp-proxy`） |
| Build steps | `["pip install --no-cache-dir fcop==3.2.4 fcop-mcp==3.2.4"]` |
| CMD | `["mcp-proxy", "--", "fcop-mcp"]` |

或优先使用仓库根目录 **`Dockerfile`**（若 Admin 页提供 “Use repository Dockerfile”）。

## 徽章（已写入 README）

```markdown
[![FCoP MCP server](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/badges/card.svg)](https://glama.ai/mcp/servers/joinwell52-AI/FCoP)

[![FCoP MCP server](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/badges/score.svg)](https://glama.ai/mcp/servers/joinwell52-AI/FCoP/score)
```

## 本地验证 Docker 镜像

```bash
docker build -t fcop-mcp:glama-test .
docker run --rm fcop-mcp:glama-test python -c "import fcop_mcp, fcop; print('ok')"
```

## PR #6301 维护者回复要点

- Claim：<https://glama.ai/mcp/servers/joinwell52-AI/FCoP>
- Score：<https://glama.ai/mcp/servers/joinwell52-AI/FCoP/score>
- 列表条目：45 MCP tools，`v3.2.4`，含 Glama card + score 徽章
