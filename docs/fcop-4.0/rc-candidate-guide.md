# FCoP 4.0.0rc1 candidate guide / 候选指南

Latest stable: 3.2.5. Release candidate: 4.0.0rc1 (unpublished).
最新稳定版为 3.2.5；4.0.0rc1 为尚未公开发布的候选。

Use the WP4E Manifest-accepted artifact set in a fresh environment outside
the repository and all existing workspaces. Verify all four SHA-256 hashes
before installing either package. Do not use public PyPI to obtain this
unpublished candidate; do not silently substitute WP4D artifacts.
在仓库与现有工作区之外建立新环境；先核验四制品 SHA-256，再安装双包。
不要从公开 PyPI 获取未发布 RC，也不要用 WP4D 旧制品冒充 WP4E。

```bash
python -m venv .venv
# Activate the new venv using your shell.
python -m pip install ./candidate/fcop-4.0.0rc1-py3-none-any.whl ./candidate/fcop_mcp-4.0.0rc1-py3-none-any.whl
python -c "from importlib.metadata import version; assert version('fcop') == version('fcop-mcp') == '4.0.0rc1'"
```

The adapter dependency is `fcop>=4.0.0rc1,<4.1.0`; mixed pairs are rejected.
sdist installation is separately tested for both distributions.
Both packages must come from the same accepted set.
适配器依赖如上，混装拒绝；两个包的 sdist 来源均须独立测试。

- [English minimal Python and MCP entries](../../README.md)
- [中文最小 Python 与 MCP 入口](../../README.zh.md)
- [MCP capability mapping](../mcp-tools.md)
- [Python full sample](../../examples/v4/third-party/python-only/app.py)
- [MCP-only full sample](../../examples/v4/third-party/mcp-only/client.py)
- [Trusted sample startup](../../examples/v4/third-party/mcp-only/server.py)

Copy the examples to a new external directory. Run the stdio client with
`python -I -B client.py /absolute/path/to/new-demo-directory`.
Its directory must not already exist; the demo creates only its own files.
The server's fixed educational evaluator must be replaced by an independently
designed trusted policy before production use. Caller-provided logic is never
a trusted evaluator.
样例必须复制到新的外部目录；新建演示目录，不碰已有工作区。
教学 evaluator 不是生产授权方案，调用者提供的逻辑不构成授权。

Installing 4.0 does not migrate any 3.x workspace or redeploy its Host rules.
No downstream application needs to pause for this candidate verification.
安装 4.0 不自动迁移 3.x 工作区，不重新部署 Host 规则；候选验证不要求下游停机。

Public publication, main merge, tag, Registry and Zenodo updates are not
authorized in WP4E Phase A. The future release must use the WP4E Gate-accepted
hashes without rebuilding at upload time.
WP4E Phase A 不授权发布、合并、tag、Registry 或 Zenodo 更新。
未来发布只能使用 WP4E Gate 接受的原制品，上传时不重新构建。

