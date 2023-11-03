from __future__ import annotations

from usatt._data import get_ratings, get_summary


def test_get_ratings(usattid):
    ratings = get_ratings(usattid)
    assert ratings["USATT#"] == usattid
    assert ratings["Name"] == "Lily Zhang"


def test_get_summary():
    data = get_summary(query="Ong", filter={"minAge": 8})
    assert len(data) >= 2
