import pytest

from pathfinding.core import Vector2D, Cell, CellState
from pathfinding.exception import PathPointIsUnsafeException
from pathfinding.utils import check_points
from pathfinding.world import WorldElement


class TestWorldElement(WorldElement):
    def __init__(self, entity, state):
        super().__init__(entity)
        self.cell = Cell(Vector2D(0, 0), 10, 10, state)

    def get_cell(self) -> Cell | None:
        return self.cell


@pytest.fixture
def start_point():
    return Vector2D(0, 0)


@pytest.fixture
def end_point():
    return Vector2D(100, 100)


@pytest.fixture
def safe_element():
    return TestWorldElement(0, CellState.SAFE)


@pytest.fixture
def unsafe_element():
    return TestWorldElement(1, CellState.UNSAFE)


@pytest.fixture
def mixed_element():
    return TestWorldElement(2, CellState.MIXED)


def test_check_point_safe(start_point, end_point, safe_element):
    check_points(start_point, end_point, safe_element, safe_element)
    # No exception should be raised


def test_check_point_unsafe(start_point, end_point, unsafe_element):
    with pytest.raises(PathPointIsUnsafeException):
        check_points(start_point, end_point, unsafe_element, unsafe_element)


def test_check_point_mixed(start_point, end_point, mixed_element):
    with pytest.raises(PathPointIsUnsafeException):
        check_points(start_point, end_point, mixed_element, mixed_element)
