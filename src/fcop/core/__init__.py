"""Internal implementation package.

Modules under :mod:`fcop.core` are **not** part of the public API.
Their names, signatures, and behavior can change in any minor release
of fcop. Consumers should import from the top-level :mod:`fcop` package
instead.

The public facade is defined in ``src/fcop/__init__.py`` and in
adr/ADR-0001-library-api.md. Anything not re-exported there is private.
"""
