"""Quick check of fcop / fcop-mcp runtime deps for release audit."""
from importlib.metadata import requires

for pkg in ("fcop", "fcop-mcp"):
    print(f"=== {pkg} ===")
    deps = requires(pkg) or []
    for d in deps:
        print(f"  {d}")
    print()
