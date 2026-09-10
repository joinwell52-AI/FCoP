"""Run from outside the checkout in a clean, wheel-installed interpreter."""

import hashlib
import json
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

import fcop
from fcop.v4.schema import _validators

assert "site-packages" in str(fcop.__file__), fcop.__file__
validators = _validators()
assert len(validators) == 12
directory = files("fcop").joinpath("_data/schemas/v4")
schemas = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
           for path in directory.iterdir() if path.name.endswith(".schema.json")}
results = {}
for mode in ("sequential", "family"):
    output = subprocess.check_output([sys.executable, str(Path(__file__).with_name("application.py")),
                                       mode], text=True)
    results[mode] = json.loads(output)
    assert results[mode]["state"] == "archive"
print(json.dumps({"fcop_import": str(fcop.__file__), "schemas": schemas, "applications": results},
                 indent=2))
