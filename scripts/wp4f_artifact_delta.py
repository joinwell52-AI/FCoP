"""Compare Stable archives with published RC; allow only release metadata/docs."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from email.parser import BytesParser
from pathlib import Path

try:
    from wp4e_artifact_delta import members
except ModuleNotFoundError:
    from scripts.wp4e_artifact_delta import members

BASELINE = {
    "fcop-4.0.0rc1-py3-none-any.whl": "b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9",
    "fcop-4.0.0rc1.tar.gz": "1e1dc76f46f2e5b5875153f83552155784ac0fadab4cec37bdf43c1a7cc22a5e",
    "fcop_mcp-4.0.0rc1-py3-none-any.whl": "53ca18feee98f37992764748d4faa8ac1811330d7c3229ad3ed312ff3bb2736e",
    "fcop_mcp-4.0.0rc1.tar.gz": "a77729d8718909db47b8c08c310688a015d20f1e91a88051e88e4ae5c3c52de9",
}


def compare(old, new):
    old = {n.replace("4.0.0rc1.dist-info", "4.0.0.dist-info"): v for n, v in old.items()}
    assert old.keys() == new.keys(), "Archive member set changed"
    changed = [n for n in old if old[n] != new[n]]
    for name in changed:
        if name in {"README.md", "README.zh.md", "fcop-README.pypi.md", "CHANGELOG.md", "pyproject.toml"}:
            continue
        if name.endswith("/_version.py"):
            assert old[name].replace(b'"4.0.0rc1"', b'"4.0.0"') == new[name]
            continue
        if name in {"src/fcop_mcp/routing.py", "fcop_mcp/routing.py"}:
            trees = [ast.parse(raw) for raw in (old[name], new[name])]
            pairs = []
            for tree in trees:
                node = next(n for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "PACKAGE_COMPATIBILITY" for t in n.targets))
                pairs.append(ast.literal_eval(node.value.args[0]))
                tree.body.remove(node)
            assert pairs[1] == pairs[0] | {("4.0.0", "4.0.0")}
            assert ast.dump(trees[0]) == ast.dump(trees[1])
            continue
        if name.endswith(".dist-info/RECORD"):
            continue
        if name.endswith(".dist-info/METADATA") or name == "PKG-INFO":
            before, after = [BytesParser().parsebytes(raw) for raw in (old[name], new[name])]
            assert after["Version"] == "4.0.0"
            allowed = {"Version", "Requires-Dist", "Classifier"}
            assert [(k, v) for k, v in before.items() if k not in allowed] == [
                (k, v) for k, v in after.items() if k not in allowed]
            assert after.get_all("Classifier", []) == [v.replace("4 - Beta", "5 - Production/Stable")
                                                   for v in before.get_all("Classifier", [])]
            assert after.get_all("Requires-Dist", []) == [v.replace("4.0.0rc1", "4.0.0")
                                                          for v in before.get_all("Requires-Dist", [])]
            readme = "mcp/README.md" if after["Name"].replace("_", "-") == "fcop-mcp" else "fcop-README.pypi.md"
            expected = Path(readme).read_text(encoding="utf-8")
            assert after.get_payload(decode=True).decode("utf-8").strip() == expected.strip()
            continue
        raise AssertionError("Unapproved artifact member changed: " + name)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    rows = []
    for name, expected in BASELINE.items():
        old = args.baseline / name
        new = args.candidate / name.replace("4.0.0rc1", "4.0.0")
        assert hashlib.sha256(old.read_bytes()).hexdigest() == expected
        rows.append(dict(filename=new.name, sha256=hashlib.sha256(new.read_bytes()).hexdigest(),
                         changed_members=compare(members(old), members(new))))
    print(json.dumps(dict(status="PASS", version_metadata_and_docs_only=True, artifacts=rows), sort_keys=True))


if __name__ == "__main__":
    main()
