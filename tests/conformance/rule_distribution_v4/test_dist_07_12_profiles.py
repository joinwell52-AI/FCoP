"""Selection, adoption, receipt provenance and independent Host evidence."""


import pytest

from .conftest import SEQUENTIAL, field


@pytest.mark.parametrize("variant", ["permutation", "cycle", "missing-dependency", "conflict"])
def test_dist_07(case, variant):
    """DIST-07; RD-08; Owner: WP4C.3. Arrange graph/order; Act select; Assert deterministic closed selection."""
    if variant == "permutation":
        first = case.invoke("select", readonly=True)
        case.manifest["artifacts"].reverse()
        case.flush()
        second = case.invoke("select", readonly=True)
        assert field(first, "selected_modules") == field(second, "selected_modules") == SEQUENTIAL
        assert field(first, "artifacts") == field(second, "artifacts")
    elif variant == "missing-dependency":
        case.reject(
            "select", "RULE_SELECTION_INVALID", case.request(selected_modules=SEQUENTIAL[1:])
        )
    else:
        for artifact in case.manifest["artifacts"]:
            if artifact["module_id"] == "workspace":
                artifact["depends_on" if variant == "cycle" else "conflicts_with"] = ["envelopes"]
        case.flush()
        case.reject("select", "RULE_MANIFEST_INVALID")
