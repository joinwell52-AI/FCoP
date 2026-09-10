"""Read every delivered GitHub blob and compare SHA-256 with local Git objects."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

BASE = "64a24295d6c1fa53a182a819d39b295c2ba8d2d0"
REPO = "joinwell52-AI/FCoP"


def git(*args):
    return subprocess.check_output(["git", *args])


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", "repos/" + REPO + "/" + path]))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("head")
    a = p.parse_args()
    head = git("rev-parse", a.head + "^{commit}").decode().strip()
    branch = "codex/fcop-4.0-wp4e-release-readiness"
    assert api("git/ref/heads/" + branch)["object"]["sha"] == head
    tree = api("git/trees/" + head + "?recursive=1")
    assert not tree["truncated"]
    entries = {r["path"]: r for r in tree["tree"] if r["type"] == "blob"}
    names = git("diff", "--name-only", BASE, head).decode().splitlines()

    def verify(name):
        doc = api("git/blobs/" + entries[name]["sha"])
        assert doc["encoding"] == "base64"
        remote = base64.b64decode(doc["content"])
        local = git("show", head + ":" + name)
        assert local == remote
        return dict(path=name, bytes=len(remote), sha256=hashlib.sha256(remote).hexdigest(),
                    git_blob=entries[name]["sha"])

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(verify, names))
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head], check=True)
    print(json.dumps(dict(head=head, base=BASE, branch=branch, remote_readback="PASS",
                          verified=len(rows), files=rows), sort_keys=True))


if __name__ == "__main__":
    main()
