"""Publish a Dev.to markdown draft using DEVTO_API_KEY.

The script intentionally reads the API key only from the environment so
the key does not appear in command-line arguments or repository files.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEVTO_API_URL = "https://dev.to/api/articles"
USER_AGENT = "FCoP-Devto-Publisher/1.0 (+https://github.com/joinwell52-AI/FCoP)"


def _load_dotenv(start: Path) -> None:
    env_path = start.resolve() / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def _parse_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Markdown file must start with YAML frontmatter.")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        raise ValueError("YAML frontmatter is missing a closing --- line.")

    frontmatter: dict[str, object] = {}
    for line in lines[1:end_index]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line!r}")
        key, raw_value = line.split(":", 1)
        frontmatter[key.strip()] = _parse_scalar(raw_value)

    body = "\n".join(lines[end_index + 1 :]).lstrip()
    return frontmatter, body


def _tags(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _build_payload(frontmatter: dict[str, object], body: str) -> dict[str, object]:
    title = frontmatter.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Frontmatter must include a non-empty title.")

    article: dict[str, object] = {
        "title": title,
        "published": bool(frontmatter.get("published", False)),
        "body_markdown": body,
    }

    if frontmatter.get("description"):
        article["description"] = str(frontmatter["description"])
    if frontmatter.get("canonical_url"):
        article["canonical_url"] = str(frontmatter["canonical_url"])
    if frontmatter.get("cover_image"):
        article["main_image"] = str(frontmatter["cover_image"])

    tags = _tags(frontmatter.get("tags"))
    if tags:
        article["tags"] = tags

    return {"article": article}


def publish(markdown_path: Path) -> dict[str, object]:
    _load_dotenv(Path.cwd())
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        raise RuntimeError("DEVTO_API_KEY is not set.")

    frontmatter, body = _parse_frontmatter(markdown_path.read_text(encoding="utf-8"))
    payload = _build_payload(frontmatter, body)
    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        DEVTO_API_URL,
        data=data,
        method="POST",
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Dev.to API returned HTTP {exc.code}: {detail}") from exc


def check_auth() -> dict[str, object]:
    _load_dotenv(Path.cwd())
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        raise RuntimeError("DEVTO_API_KEY is not set.")

    request = urllib.request.Request(
        "https://dev.to/api/users/me",
        method="GET",
        headers={
            "api-key": api_key,
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {
                "id": result.get("id"),
                "username": result.get("username"),
                "name": result.get("name"),
            }
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Dev.to auth check returned HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-key",
        action="store_true",
        help="Only check whether DEVTO_API_KEY can be loaded; never prints the key.",
    )
    parser.add_argument(
        "--check-auth",
        action="store_true",
        help="Check Dev.to authentication without publishing.",
    )
    parser.add_argument(
        "markdown",
        nargs="?",
        default="essays/ai-must-write-it-down.devto.md",
        help="Path to the Dev.to markdown file.",
    )
    args = parser.parse_args()

    if args.check_key:
        _load_dotenv(Path.cwd())
        api_key = os.environ.get("DEVTO_API_KEY", "")
        if not api_key:
            print("DEVTO_API_KEY=missing")
            return 1
        print(json.dumps({"DEVTO_API_KEY": "present", "length": len(api_key)}))
        return 0

    if args.check_auth:
        try:
            result = check_auth()
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, ensure_ascii=False))
        return 0

    try:
        result = publish(Path(args.markdown))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"id": result.get("id"), "url": result.get("url")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
