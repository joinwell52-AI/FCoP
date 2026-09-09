"""Generate under fixed 3.2.5; read the exact fixture under installed RC."""
from __future__ import annotations

import base64
import hashlib
import json
import socket
import sys
from pathlib import Path


def offline(event, args):
    if event.startswith("socket.") and event in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto"}:
        caller = sys._getframe(1).f_code
        if caller.co_filename != socket.__file__ or caller.co_name != "_fallback_socketpair":
            raise RuntimeError("No application networking")


def snapshot(root):
    return {p.relative_to(root).as_posix(): base64.b64encode(p.read_bytes()).decode()
            if p.is_file() else None for p in sorted(root.rglob("*"))}


def main():
    sys.addaudithook(offline)
    import fcop
    from fcop import Project
    assert Path(fcop.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    mode, directory, manifest = sys.argv[1:4]
    root, path = Path(directory), Path(manifest)
    root.mkdir(parents=True)
    if mode == "generate":
        assert fcop.__version__ == "3.2.5"
        p = Project(root)
        p.init_solo(role_code="ME", deploy_rules=False, deploy_role_templates=False)
        p.write_task(sender="ME", recipient="ME", priority="P2",
                     subject="Historical workspace", body="Fixed accepted 3.2.5 fixture.")
        before = snapshot(root)
        expected = {}
        for uri in ("fcop://rules", "fcop://protocol", "fcop://guidance/sequential/en"):
            value = p.rule_distribution(action="read_resource", request={"resource_uri": uri})
            assert isinstance(value["content"], str) and value["mime_type"] == "text/markdown"
            expected[uri] = hashlib.sha256(value["content"].encode()).hexdigest()
        assert snapshot(root) == before
        declaration = json.loads((root / "fcop/fcop.json").read_bytes())
        assert declaration["version"] == 1 and p.is_v3
        # Accepted 3.2.5 init uses v3 topology with historical config schema version 1.
        # Preserve its actual declaration; do not relabel it as protocol 4.0.
        path.write_text(json.dumps(dict(producer="3.2.5",
                        producer_commit="167c5fd4ca4c9603c392bae3a4a055963e7b7ed6",
                        tree=before, resource_sha256=expected), sort_keys=True) + "\n", encoding="utf-8")
    else:
        assert mode == "read" and fcop.__version__ == "4.0.0rc1"
        fixture = json.loads(path.read_bytes())
        for name, encoded in fixture["tree"].items():
            target = root / name
            assert target.resolve().is_relative_to(root.resolve())
            if encoded is None:
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(encoded))
        before = snapshot(root)
        assert before == fixture["tree"]
        p = Project(root)
        p.status()
        tasks = p.list_tasks(status="all")
        assert tasks
        for uri, digest in fixture["resource_sha256"].items():
            value = p.rule_distribution(action="read_resource", request={"resource_uri": uri})
            assert isinstance(value["content"], str) and value["mime_type"] == "text/markdown"
            assert hashlib.sha256(value["content"].encode()).hexdigest() == digest
        assert snapshot(root) == before
        print(json.dumps({"legacy_read_only": True, "fixture_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "files": len([v for v in before.values() if v is not None]),
                          "import_path": fcop.__file__}, sort_keys=True))


if __name__ == "__main__":
    main()
