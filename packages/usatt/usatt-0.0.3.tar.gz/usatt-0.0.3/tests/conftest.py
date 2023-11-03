from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def usattid():
    """
    Default USATT id of Lily Zhang for testing purposes.
    """
    return 31126
