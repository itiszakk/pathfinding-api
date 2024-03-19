import pytest

from pathfinding.core import Direction
from pathfinding.core.direction import DirectionType


@pytest.mark.parametrize("direction, expected_opposite", [
    (Direction.N, Direction.S),
    (Direction.S, Direction.N),
    (Direction.W, Direction.E),
    (Direction.E, Direction.W),
    (Direction.NW, Direction.SE),
    (Direction.SE, Direction.NW),
    (Direction.NE, Direction.SW),
    (Direction.SW, Direction.NE)
])
def test_opposite_direction(direction, expected_opposite):
    assert direction.opposite() == expected_opposite


@pytest.mark.parametrize("direction, expected_type", [
    (Direction.N, DirectionType.VERTICAL),
    (Direction.S, DirectionType.VERTICAL),
    (Direction.W, DirectionType.HORIZONTAL),
    (Direction.E, DirectionType.HORIZONTAL),
    (Direction.NW, DirectionType.DIAGONAL),
    (Direction.SE, DirectionType.DIAGONAL),
    (Direction.NE, DirectionType.DIAGONAL),
    (Direction.SW, DirectionType.DIAGONAL)
])
def test_get_type(direction, expected_type):
    assert direction.get_type() == expected_type


@pytest.mark.parametrize("direction, expected_diagonal", [
    (Direction.N, False),
    (Direction.S, False),
    (Direction.W, False),
    (Direction.E, False),
    (Direction.NW, True),
    (Direction.SE, True),
    (Direction.NE, True),
    (Direction.SW, True)
])
def test_is_diagonal(direction, expected_diagonal):
    assert direction.is_diagonal() == expected_diagonal


@pytest.mark.parametrize("direction, expected_vertical", [
    (Direction.N, True),
    (Direction.S, True),
    (Direction.W, False),
    (Direction.E, False),
    (Direction.NW, False),
    (Direction.SE, False),
    (Direction.NE, False),
    (Direction.SW, False)
])
def test_is_vertical(direction, expected_vertical):
    assert direction.is_vertical() == expected_vertical


@pytest.mark.parametrize("direction, expected_horizontal", [
    (Direction.N, False),
    (Direction.S, False),
    (Direction.W, True),
    (Direction.E, True),
    (Direction.NW, False),
    (Direction.SE, False),
    (Direction.NE, False),
    (Direction.SW, False)
])
def test_is_horizontal(direction, expected_horizontal):
    assert direction.is_horizontal() == expected_horizontal
