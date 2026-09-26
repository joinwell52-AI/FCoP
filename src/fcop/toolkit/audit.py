"""Protocol audit reuses the sole workspace validator."""
from fcop.workspace import validate_workspace


def audit(root):
    return validate_workspace(root)
