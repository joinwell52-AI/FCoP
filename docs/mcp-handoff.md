# A session ends. The task and its report remain.

[简体中文](mcp-handoff.zh.md) · [FCoP](../README.md) · [Example source](../examples/mcp_handoff.py)

Try one concrete handoff: a first MCP session creates a task, computes a SHA-256 digest and submits a report. That session exits. A fresh session retrieves the same task, attempt and report from local files.

## Copy this to your coding AI

```text
Run the FCoP handoff example for me:
https://github.com/joinwell52-AI/FCoP/blob/main/docs/mcp-handoff.md
Inspect the example, prepare its dependencies in isolation, and run it in a fresh demo directory. Show me the actual result, the saved task/report and whether review is still pending. Handle the commands yourself and preserve my current project and client settings.
```

The AI needs terminal and file access. This demo runs its own MCP sessions and does not require an API key or change your IDE configuration. To connect FCoP to your actual client afterward, use the [AI installation request](ai-install.md).

## What you should see

```text
1/4 Discover the published MCP adapter (no workspace writes).
2/4 Create, claim, compute SHA-256 and submit a report for review.
3/4 First session exited. Open a new session on the same files.
4/4 PASS: same task, attempt and report; 7 files unchanged; review pending.
```

This is the expected output shape. Your run must actually finish before reporting success; run paths and identifiers vary. The task remains in **review**, even though its report says `result=done`. Reading a delivery claim does not approve it.

## Execution guide for the AI

1. Check Python 3.10+ and `uvx`. If needed, prepare uv following its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/) within the host's permissions. Use a compatible Python environment without changing another project's dependencies.
2. Read and obtain [examples/mcp_handoff.py](../examples/mcp_handoff.py) from this repository into a new demo directory, or use a local FCoP checkout. The script uses only Python's standard library; uv resolves `fcop==4.0.2` and `fcop-mcp==4.0.2` together in an isolated environment.
3. Run the script with that Python executable. From the repository root:

   ```sh
   python examples/mcp_handoff.py --output <new-demo-parent>
   ```

   Replace `<new-demo-parent>` with an actual path. Omit `--output` to use the system temporary directory. Every run creates a new directory and preserves its files. Initial package downloads may take longer than later runs.

4. Check the exit code and read the generated `result.json`. Require `status=pass`, `stage=review`, matching task/attempt/report identities, the actual report digest and unchanged workspace file hashes. Discovery should report 49 tools, 12 resources and 4 templates for this pinned pair. The transcript and two stderr logs sit alongside the workspace.
5. Show the user where the task and report are, explain what survived the session change, and say that acceptance remains pending. A failed dependency download, timeout or tool call is a failure to investigate, not a successful trial.

The computation uses Python `hashlib`, with input `FCoP handoff example`. Its SHA-256 is:

```text
cceecdb3da6e529e216fa6c65dcbf764aa74a65d52c32c798ca4af4d68e8f489
```

## What this demonstrates

Two independent stdio connections exercise the published MCP adapter. The second reads the same persisted work after the first exits. The client script performs the computation and tool calls; this is not an LLM benchmark, a Cursor-to-Codex test or evidence of external adoption. It does not exercise approval or archival.

If it fails, [open an issue](https://github.com/joinwell52-AI/FCoP/issues/new) with your OS, Python/uv versions, failing step and a redacted error excerpt. If it works, a short report of the task you want to hand off next is useful feedback. Star [FCoP](https://github.com/joinwell52-AI/FCoP) if you want to keep the protocol and examples handy.
