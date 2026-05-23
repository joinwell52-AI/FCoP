#!/usr/bin/env python3
"""
fcop-mcp 发版前一条龙检查脚本
用法: python scripts/prerelease_check.py [--expected-tools N]
所有检查通过才允许发版；任何一条 FAIL 即退出码非零。
"""
import re, sys, ast, zipfile, glob, json
from pathlib import Path

ROOT = Path(__file__).parent.parent          # mcp/
PROJECT_ROOT = ROOT.parent                   # FCoP/ 项目根
SERVER = ROOT / "src/fcop_mcp/server.py"
PYPROJECT = ROOT / "pyproject.toml"
VERSION_FILE = ROOT / "src/fcop_mcp/_version.py"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"   # 实际位于项目根，非 mcp/ 下
DOCS_MCP  = PROJECT_ROOT / "docs/mcp-tools.md"
RULES_DATA = PROJECT_ROOT / "src/fcop/rules/_data"
FCOP_VERSION_FILE = PROJECT_ROOT / "src/fcop/_version.py"

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m!\033[0m"

errors = []

def check(name, cond, msg_fail, msg_pass=""):
    if cond:
        print(f"  {PASS} {name}" + (f": {msg_pass}" if msg_pass else ""))
    else:
        print(f"  {FAIL} {name}: {msg_fail}")
        errors.append(f"{name}: {msg_fail}")

# ── 0. 获取版本 ────────────────────────────────────────────────
print("\n[0] 读取版本号")
ver_ns = {}
exec(VERSION_FILE.read_text(encoding="utf-8"), ver_ns)
version = ver_ns.get("__version__", "UNKNOWN")
print(f"  {PASS} _version.py __version__ = {version}")

# ── 1. 工具数量 ────────────────────────────────────────────────
print("\n[1] 工具数量检查")
content = SERVER.read_text(encoding="utf-8")
decorators = re.findall(r"@mcp\.tool\b", content)
tool_names = re.findall(r"@mcp\.tool.*?\ndef (\w+)\(", content, re.DOTALL)
tool_count = len(decorators)

expected_arg = next((int(sys.argv[i+1]) for i, a in enumerate(sys.argv) if a == "--expected-tools"), None)
expected = expected_arg or 45
check("工具数量", tool_count == expected,
      f"期望 {expected}，实际 {tool_count}",
      f"{tool_count} 个")

# 检查工具名无重复
dupes = [t for t in set(tool_names) if tool_names.count(t) > 1]
check("工具名无重复", not dupes, f"重复: {dupes}")

# ── 2. 文档覆盖率 ──────────────────────────────────────────────
print("\n[2] docs/mcp-tools.md 覆盖率")
if DOCS_MCP.exists():
    doc_content = DOCS_MCP.read_text(encoding="utf-8")
    # 检查文档中声明的工具数量
    count_match = re.search(r"工具.*?共\s*(\d+)\s*个|(\d+)\s*tools\b", doc_content, re.I)
    doc_declared = int(count_match.group(1) or count_match.group(2)) if count_match else 0
    check("文档声明工具数", doc_declared == tool_count,
          f"文档写 {doc_declared}，实际 {tool_count}")
    # 检查每个工具名在文档中是否出现
    missing_in_doc = [t for t in tool_names if f"`{t}`" not in doc_content]
    check("所有工具在文档中有反引号引用",
          not missing_in_doc,
          f"缺失: {missing_in_doc}")
else:
    check("docs/mcp-tools.md 存在", False, "文件不存在")

# ── 3. CHANGELOG ───────────────────────────────────────────────
print("\n[3] CHANGELOG 检查")
if CHANGELOG.exists():
    cl = CHANGELOG.read_text(encoding="utf-8")
    check(f"CHANGELOG 含版本 {version}", version in cl,
          f"CHANGELOG 中未找到 {version}")
else:
    print(f"  {WARN} CHANGELOG.md 不存在（非阻塞）")

# ── 4. wheel 工具数一致性 ─────────────────────────────────────
print("\n[4] 本地 wheel 工具数（如已构建）")
dist_dir = ROOT / "dist"
whl_files = sorted(dist_dir.glob(f"fcop_mcp-{version}-*.whl")) if dist_dir.exists() else []
if whl_files:
    whl = whl_files[-1]
    with zipfile.ZipFile(whl) as z:
        for name in z.namelist():
            if name.endswith("server.py"):
                whl_content = z.read(name).decode("utf-8")
                whl_count = len(re.findall(r"@mcp\.tool\b", whl_content))
                check(f"wheel ({whl.name}) 工具数",
                      whl_count == tool_count,
                      f"wheel={whl_count} vs src={tool_count}")
                break
else:
    print(f"  {WARN} 未找到 {version} 的 wheel（先 build 再重跑）")

# ── 5. 语法检查 ────────────────────────────────────────────────
print("\n[5] server.py 语法检查")
try:
    ast.parse(content)
    print(f"  {PASS} server.py 语法正确")
except SyntaxError as e:
    check("server.py 语法", False, str(e))

# ── 6. 每个工具必有 docstring ─────────────────────────────────
print("\n[6] 工具 docstring 检查")
no_doc = []
pattern = re.compile(
    r'@mcp\.tool.*?\ndef (\w+)\([^)]*\).*?:\s*\n\s*("""|\s*(?!""")\S)',
    re.DOTALL
)
for m in re.finditer(r'@mcp\.tool.*?\ndef (\w+)\(.*?\).*?:\s*\n(\s*"""|\s*[^\s"])',
                     content, re.DOTALL):
    fn_name = m.group(1)
    after = m.group(2).strip()
    if not after.startswith('"""') and not after.startswith("'''"):
        no_doc.append(fn_name)
check("所有工具有 docstring", not no_doc,
      f"缺 docstring: {no_doc}" if no_doc else "")

# ── 7. fcop 库版本与 fcop-mcp 版本一致性 ─────────────────────
print("\n[7] fcop 库版本一致性检查")
if FCOP_VERSION_FILE.exists():
    fcop_ver_ns = {}
    exec(FCOP_VERSION_FILE.read_text(encoding="utf-8"), fcop_ver_ns)
    fcop_version = fcop_ver_ns.get("__version__", "UNKNOWN")
    check("fcop 库版本 == fcop-mcp 版本",
          fcop_version == version,
          f"fcop={fcop_version}, fcop-mcp={version}（应保持同步）",
          f"fcop={fcop_version} == fcop-mcp={version}")
else:
    check("src/fcop/_version.py 存在", False,
          f"未找到 {FCOP_VERSION_FILE}")

# ── 8. 捆绑规则关键文件检查 ───────────────────────────────────
print("\n[8] 捆绑规则关键文件检查")
CRITICAL_RULE_FILES = [
    "fcop-rules.mdc",
    "fcop-protocol.mdc",
    "agent-bringup-prompt.zh.md",
    "agent-bringup-prompt.en.md",
    "letter-to-admin.zh.md",
    "letter-to-admin.en.md",
]
if RULES_DATA.exists():
    for fname in CRITICAL_RULE_FILES:
        fpath = RULES_DATA / fname
        exists = fpath.exists()
        non_empty = exists and fpath.stat().st_size > 100
        check(f"{fname} 存在且非空",
              non_empty,
              "文件不存在" if not exists else f"文件过小({fpath.stat().st_size if exists else 0} bytes)")
else:
    check("src/fcop/rules/_data/ 目录存在", False,
          f"未找到 {RULES_DATA}")

# ── 9. 规则文件版本与包版本对齐检查 ──────────────────────────
print("\n[9] 规则文件版本对齐检查")
rules_file = RULES_DATA / "fcop-rules.mdc"
if rules_file.exists():
    rules_text = rules_file.read_text(encoding="utf-8")
    # 从版本号提取 major.minor（如 3.2.2 → 3.2）
    major_minor = ".".join(version.split(".")[:2])
    major = version.split(".")[0]
    # 检查规则文件是否含有当前主版本号引用
    has_version_ref = (f"fcop@{major}." in rules_text or
                       f"fcop {major}." in rules_text or
                       f"version: {major}." in rules_text or
                       f"fcop_rules_version: {major}." in rules_text)
    check(f"fcop-rules.mdc 包含 v{major}.x 版本引用",
          has_version_ref,
          f"规则文件未引用 v{major}.x，可能与包版本严重脱节")

    # 检查规则文件是否包含 _lifecycle/ 目录结构（FCoP 3.0+ 核心变更）
    has_lifecycle = "_lifecycle/" in rules_text or "_lifecycle" in rules_text
    check("fcop-rules.mdc 包含 _lifecycle/ 目录结构",
          has_lifecycle,
          "规则文件未提及 _lifecycle/，未反映 FCoP 3.0 目录变更")
else:
    check("fcop-rules.mdc 可读", False, "文件不存在，跳过版本检查")

# ── 10. fcop-protocol.mdc v3 目录结构覆盖 ────────────────────
print("\n[10] fcop-protocol.mdc v3 目录结构覆盖")
protocol_file = RULES_DATA / "fcop-protocol.mdc"
if protocol_file.exists():
    proto_text = protocol_file.read_text(encoding="utf-8")
    has_lifecycle_proto = "_lifecycle/" in proto_text or "_lifecycle" in proto_text
    check("fcop-protocol.mdc 包含 _lifecycle/ 目录结构",
          has_lifecycle_proto,
          "协议解释文件未反映 FCoP 3.0 _lifecycle/ 结构")
    # 检查是否包含生命周期各阶段
    lifecycle_stages = ["inbox", "active", "review", "done", "archive"]
    missing_stages = [s for s in lifecycle_stages
                      if f"_lifecycle/{s}" not in proto_text and
                         f"{s}/" not in proto_text]
    check("fcop-protocol.mdc 覆盖生命周期各阶段",
          len(missing_stages) < 3,
          f"缺少阶段描述: {missing_stages}")
else:
    check("fcop-protocol.mdc 可读", False, "文件不存在，跳过结构检查")

# ── 结果汇总 ──────────────────────────────────────────────────
print(f"\n{'='*50}")
if errors:
    print(f"\033[91m发版阻塞！{len(errors)} 项未通过：\033[0m")
    for e in errors:
        print(f"  • {e}")
    sys.exit(1)
else:
    print(f"\033[92m全部通过 ✓  版本 {version} 可以发版\033[0m")
    sys.exit(0)
