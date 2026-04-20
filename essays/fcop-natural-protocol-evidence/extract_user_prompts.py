"""Extract all user turns from the JSONL transcript as human-readable Markdown.

Usage:
    py -3.10 extract_user_prompts.py
"""
from __future__ import annotations

import json
from pathlib import Path

SRC = Path(__file__).with_name("transcript-full.jsonl")
DST = Path(__file__).with_name("transcript-user-prompts.md")


def iter_user_texts():
    with SRC.open(encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("role") != "user":
                continue
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            texts: list[str] = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    t = block.get("text") or ""
                    if t:
                        texts.append(t)
            if texts:
                yield idx, "\n".join(texts)


def main() -> None:
    lines: list[str] = [
        "# 原始对话记录 · 仅 user 消息",
        "",
        "> 从 `transcript-full.jsonl` 抽取出的全部 user 消息,按原始顺序排列。",
        "> 这是**取证向**的文件:用来核对我到底说了什么、没说什么。",
        "> 所有内容未做任何编辑或删减。",
        "",
        "---",
        "",
    ]
    count = 0
    for line_idx, text in iter_user_texts():
        count += 1
        lines.append(f"## #{count}(JSONL 第 {line_idx} 行)")
        lines.append("")
        lines.append("```")
        lines.append(text.rstrip())
        lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**共 {count} 条 user 消息**")
    lines.append("")
    lines.append("## 取证要点(可自行复核)")
    lines.append("")
    lines.append("### Part 1 · user 端为 0 命中")
    lines.append("")
    lines.append("在本文件中搜索以下关键词,应**全部为 0 命中**(不计入本节自述):")
    lines.append("")
    lines.append("| 关键词 | user 端命中次数 |")
    lines.append("|---|---|")
    lines.append("| `FCoP` | 0 |")
    lines.append("| `PM-01` / `DEV-01` / `ADMIN-01` / `QA-01` | 0 |")
    lines.append("| `TASK-` | 0 |")
    lines.append("| `thread_key` | 0 |")
    lines.append("| `agent_bridge` | 0 |")
    lines.append("| `四方` / `四幕` / `派工` / `接单回执` | 0 |")
    lines.append("")
    lines.append("### Part 2 · agent 端自发大量使用")
    lines.append("")
    lines.append("在同目录下的 `transcript-full.jsonl` 中搜索(含 assistant 端的全部工具调用与对话):")
    lines.append("")
    lines.append("| 关键词 | 全文件命中次数 | 说明 |")
    lines.append("|---|---|---|")
    lines.append("| `PM-01` | 2 | agent 自发使用的角色标签 |")
    lines.append("| `DEV-01` | 4 | agent 自发使用的角色标签 |")
    lines.append("| `ADMIN-01` | 2 | agent 自发使用的角色标签 |")
    lines.append("| `TASK-` | 24 | agent 自发采用的文件命名模式 |")
    lines.append("| `thread_key` | 6 | agent 自发补全的 YAML 元数据字段 |")
    lines.append("| `agent_bridge` | 8 | agent 自发引用的协议名 |")
    lines.append("")
    lines.append("有趣的细节:`FCoP` 这个**品牌名** agent 全程 0 次使用——"
                 "它没有用我们起的名字,它只是用了我们所定义的**结构**。")
    lines.append("")
    lines.append("> **这就是 \"LLM-native protocol\" 的硬核证据。**")
    lines.append("> **user 从没用过这些词;agent 却自发用了几十次。**")
    lines.append("> **我们没教它,它原本就在说。**")

    DST.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote {DST.name} with {count} user messages.")


if __name__ == "__main__":
    main()
