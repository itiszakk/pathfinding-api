import pytest

from pathfinding.core import Vector2D, Cell, CellState


@pytest.fixture
def cell_safe():
    return Cell(Vector2D(0, 0), 10, 10, CellState.SAFE)


@pytest.fixture
def cell_unsafe():
    return Cell(Vector2D(0, 0), 10, 10, CellState.UNSAFE)


@pytest.mark.parametrize("point, expected_contains", [
    (Vector2D(5, 5), True),
    (Vector2D(0, 5), True),
    (Vector2D(10, 5), True),
    (Vector2D(5, 0), True),
    (Vector2D(5, 10), True),
    (Vector2D(11, 11), False),
    (Vector2D(-1, -1), False)
])
def test_contains(cell_safe, point, expected_contains):
    assert cell_safe.contains(point) == expected_contains


def test_center():
    cell = Cell(Vector2D(0, 0), 10, 10)
    assert cell.center() == Vector2D(5, 5)


@pytest.mark.parametrize("cell_state, expected_safe", [
    (CellState.SAFE, True),
    (CellState.UNSAFE, False),
    (CellState.MIXED, False)
])
def test_safe(cell_state, expected_safe):
    cell = Cell(Vector2D(0, 0), 10, 10, cell_state)
    assert cell.safe() == expected_safe


@pytest.mark.parametrize("cell_state, expected_unsafe", [
    (CellState.SAFE, False),
    (CellState.UNSAFE, True),
    (CellState.MIXED, False)
])
def test_unsafe(cell_state, expected_unsafe):
    cell = Cell(Vector2D(0, 0), 10, 10, cell_state)
    assert cell.unsafe() == expected_unsafe


@pytest.mark.parametrize("cell_state, expected_mixed", [
    (CellState.SAFE, False),
    (CellState.UNSAFE, False),
    (CellState.MIXED, True)
])
def test_mixed(cell_state, expected_mixed):
    cell = Cell(Vector2D(0, 0), 10, 10, cell_state)
    assert cell.mixed() == expected_mixed
