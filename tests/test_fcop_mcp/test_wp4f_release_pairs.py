"""Stable package-pair checks belong to the independently installed MCP suite."""
import pytest


@pytest.mark.parametrize("pair", [("4.0.0", "4.0.0rc1"), ("4.0.0rc1", "4.0.0"),
                                 ("4.0.0", "3.2.5"), ("3.2.5", "4.0.0")])
def test_wp4f_mixed_release_pairs_still_fail_closed(
    monkeypatch: pytest.MonkeyPatch, pair: tuple[str, str],
) -> None:
    from fcop_mcp import routing

    monkeypatch.setattr(routing, "version", lambda name: pair[0 if name == "fcop" else 1])
    with pytest.raises(RuntimeError, match="toolkit:MCP_PACKAGE_INCOMPATIBLE"):
        routing.check_package_compatibility()


def test_wp4f_stable_pair_is_registered_without_losing_history(monkeypatch: pytest.MonkeyPatch) -> None:
    from fcop_mcp import routing

    assert frozenset({
        ("3.2.5", "3.2.5"), ("4.0.0rc1", "4.0.0rc1"), ("4.0.0", "4.0.0"), ("4.0.1", "4.0.1"), ("4.0.2", "4.0.2")}) == routing.PACKAGE_COMPATIBILITY
    monkeypatch.setattr(routing, "version", lambda name: "4.0.0")
    routing.check_package_compatibility()
