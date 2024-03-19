import pytest

from pathfinding.core import Vector2D
from pathfinding.core.distance import manhattan, euclidian


@pytest.fixture
def p0():
    return Vector2D(0, 0)


@pytest.fixture
def p1():
    return Vector2D(3, 4)


def test_manhattan(p0, p1):
    assert manhattan(p0, p1) == 7


def test_euclidian(p0, p1):
    assert pytest.approx(euclidian(p0, p1), 5.0) == 5.0
