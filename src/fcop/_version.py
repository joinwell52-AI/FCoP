"""Single source of truth for the fcop package version.

`pyproject.toml` reads `__version__` from this file via hatchling's dynamic
version mechanism. `fcop/__init__.py` re-exports it. Never edit the version
number in multiple places — change it here and here only.

Versioning policy (see adr/ADR-0001-library-api.md, "semver 承诺"):

- 0.x.x  pre-1.0, minor bumps may break public API
- 1.x.x  stable, breaking changes require major bump

The ``dev0`` / ``rc1`` / ``a1`` / ``b1`` suffixes are allowed during
development per PEP 440.
"""

__version__ = "0.6.0.dev0"
