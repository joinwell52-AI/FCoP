"""Render the static Pages site from maintained Markdown and a homepage template.

No writes by default: --json PATH emits one artifact for patch-based editors;
--check detects stale output; --write is available for normal maintenance.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit
from xml.etree import ElementTree

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
SERIES = ROOT / "docs/fcop-architecture-series"
PUBLIC = "https://joinwell52-ai.github.io/FCoP/"
GITHUB = "https://github.com/joinwell52-AI/FCoP/"
VERSION = "4.0.0"
ESC = html.escape
MD = MarkdownIt("commonmark", {"html": True}).enable("table")
ASSETS = [f"fcop-{name}{lang}.svg" for name in
          ("work-records", "lifecycle", "parallel-work") for lang in ("", ".zh")]
ARGS = ["--from", f"fcop-mcp=={VERSION}", "--with", f"fcop=={VERSION}", "fcop-mcp"]
CURSOR = {"mcpServers": {"fcop": {"type": "stdio", "command": "uvx", "args": ARGS,
          "env": {"FCOP_PROJECT_DIR": "D:/your-project"}}}}
CODEX_COMMAND = (f'codex mcp add fcop --env "FCOP_PROJECT_DIR=D:/your-project" -- '
                 + "uvx " + " ".join(ARGS))
CODEX_CONFIG = ('[mcp_servers.fcop]\ncommand = "uvx"\n'
                + "args = " + json.dumps(ARGS) + '\nstartup_timeout_sec = 60\n\n'
                + '[mcp_servers.fcop.env]\nFCOP_PROJECT_DIR = "D:/your-project"')
EN_ARTICLES = [
    ("Why work must outlive context", "Persist tasks, deliveries and decisions outside the model."),
    ("What belongs in the minimal Core", "Eight contracts that independent implementations must preserve."),
    ("Core, tools, policy and Runtime", "Keep semantics, implementation and execution responsibilities clear."),
    ("Parallel work, explicit convergence", "Let independent work proceed; converge on current evidence."),
    ("FCoP, MCP, A2A and CodeFlowMu", "Connect tools and systems without confusing their responsibilities."),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def page_path(source: Path) -> Path:
    return source.with_name("index.html") if source.name == "README.md" else source.with_suffix(".html")


def rewrite_url(value: str, source: Path) -> str:
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        return value
    target = (source.parent / unquote(url.path)).resolve()
    fragment = url.fragment
    if target in (ROOT / "README.md", ROOT / "README.zh.md"):
        path = "../index.html"
        fragment = {"try-it": "start"}.get(fragment, fragment)
    elif target.parent == SERIES and target.suffix == ".md":
        path = page_path(target).name
    elif target == SERIES:
        path = "index.html"
    elif target.parent == SERIES and target.suffix == ".json":
        path = target.name
    elif target.parent == ROOT / "assets" and target.name in ASSETS:
        path = "../site-assets/" + target.name
    else:
        relative = target.relative_to(ROOT).as_posix()
        path = GITHUB + ("tree/main/" if target.is_dir() else "blob/main/") + quote(relative)
    return urlunsplit(("", "", path, url.query, fragment))


def article(source: Path) -> str:
    tokens = MD.parse(read(source))
    headings = []
    seen: dict[str, int] = {}
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            title = tokens[i + 1].content
            base = re.sub(r"[^\w\-\s]", "", title.lower()).strip().replace(" ", "-") or "section"
            count = seen.get(base, 0)
            seen[base] = count + 1
            anchor = base + (f"-{count}" if count else "")
            token.attrSet("id", anchor)
            headings.append((int(token.tag[1]), title, anchor))
        for child in token.children or []:
            for attr in ("href", "src"):
                value = child.attrGet(attr)
                if value:
                    child.attrSet(attr, rewrite_url(value, source))
    body = MD.renderer.render(tokens, MD.options, {})
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    title = headings[0][1]
    toc = "".join(f'<li><a href="#{ESC(anchor)}">{ESC(text)}</a></li>'
                  for level, text, anchor in headings if level == 2)
    index = source.name == "README.md"
    canonical = PUBLIC + "fcop-architecture-series/" + page_path(source).name
    source_url = GITHUB + "blob/main/" + source.relative_to(ROOT).as_posix()
    return f'''<!doctype html>
<html lang="zh-CN" data-lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ESC(title)} · FCoP</title>
<meta name="description" content="{ESC(title)}。FCoP 架构原理系列全文，按 4.0 契约修订。">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{ESC(title)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="../site-assets/fcop-logo-256.png">
<link rel="stylesheet" href="../site-assets/site.css">
</head>
<body class="reading-page{' reading-index' if index else ''}">
<a class="skip-link" href="#main">跳转正文</a>
<header class="topbar"><div class="wrap nav-row">
<a class="brand" href="../?lang=zh"><img src="../site-assets/fcop-logo-256.png" width="34" height="34" alt=""><span>FCoP<span class="brand-version">4.0</span></span></a>
<nav aria-label="阅读导航"><a href="../?lang=zh">首页</a><a href="index.html">架构五篇</a><a href="{source_url}">GitHub ↗</a></nav>
</div></header>
<div class="reading-layout">
{'' if index else '<aside class="reading-toc" aria-label="文章目录"><h2>本文目录</h2><ol>' + toc + '</ol></aside>'}
<main class="article-content" id="main">
{body}
<p class="source-link">正文与仓库版本保持同步 · <a href="{source_url}">查看 Markdown 源文件 ↗</a></p>
</main></div>
<footer class="site-footer"><div class="wrap footer-row"><span>© 2026 Wei Zhu · FCoP · MIT</span><a href="{GITHUB}">☆ Star FCoP</a></div></footer>
</body>
</html>
'''


def artifacts() -> dict[Path, str]:
    manifest = json.loads(read(SERIES / "manifest.json"))
    readme = read(ROOT / "README.zh.md")
    python = re.search(r"```python\n(.*?)\n```", readme, re.S)
    assert python is not None
    rows = []
    for item, (title, summary) in zip(manifest["articles"], EN_ARTICLES, strict=True):
        rows.append(f'''<a class="series-row" href="fcop-architecture-series/{Path(item['file']).with_suffix('.html')}"><span class="series-number">{item['order']:02d}</span><div><h3><span class="en-only">{ESC(title)} <small>中文</small></span><span class="zh-only">{ESC(item['title'])}</span></h3><p><span class="en-only">{ESC(summary)}</span><span class="zh-only">{ESC(item['summary'])}</span></p></div><span class="series-arrow" aria-hidden="true">→</span></a>''')
    replacements = {
        "VERSION": VERSION, "PYTHON": ESC(python[1]), "SERIES_ROWS": "\n".join(rows),
        "CURSOR": ESC(json.dumps(CURSOR, indent=2)), "CODEX_COMMAND": ESC(CODEX_COMMAND),
        "CODEX_CONFIG": ESC(CODEX_CONFIG),
    }
    home = read(ROOT / "scripts/pages/index.template.html")
    for key, value in replacements.items():
        home = home.replace("@@" + key + "@@", value)
    assert "@@" not in home, "Unresolved template placeholder"
    for name in ASSETS:
        svg = ElementTree.fromstring(read(ROOT / "assets" / name))
        # Set the intrinsic ratio correctly before images finish loading.
        home = re.sub(r'(<img[^>]*src="site-assets/' + re.escape(name) + r'"[^>]*width=")\d+(" height=")\d+',
                      lambda m: m[1] + svg.attrib["width"] + m[2] + svg.attrib["height"], home)
    output = {ROOT / "docs/index.html": home}
    for filename in [manifest["index"], *(item["file"] for item in manifest["articles"]), manifest["collection"]]:
        source = SERIES / filename
        output[page_path(source)] = article(source)
    output.update({ROOT / "docs/site-assets" / name: read(ROOT / "assets" / name) for name in ASSETS})
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--json", metavar="PATH")
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    output = artifacts()
    if args.list:
        print(json.dumps([path.relative_to(ROOT).as_posix() for path in output]))
    elif args.json:
        path = ROOT / args.json
        print(json.dumps({"path": path.as_posix(), "content": output[path]}, ensure_ascii=False))
    elif args.check:
        stale = [path.relative_to(ROOT).as_posix() for path, content in output.items()
                 if not path.is_file() or read(path) != content]
        if stale:
            raise SystemExit("Stale generated pages: " + ", ".join(stale))
        if (ROOT / "assets/fcop-logo-256.png").read_bytes() != (ROOT / "docs/site-assets/fcop-logo-256.png").read_bytes():
            raise SystemExit("Logo copy differs from repository source")
        print(f"PASS: {len(output)} generated text files and local logo match sources")
    elif args.write:
        for path, content in output.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        (ROOT / "docs/site-assets/fcop-logo-256.png").write_bytes((ROOT / "assets/fcop-logo-256.png").read_bytes())


if __name__ == "__main__":
    main()
