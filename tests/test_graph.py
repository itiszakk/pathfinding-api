import pytest

from pathfinding.core.cell import Cell, CellState
from pathfinding.core.direction import Direction
from pathfinding.core.graph import Graph
from pathfinding.core.vector import Vector2D
from pathfinding.world.world_element import WorldElement


class TestElement(WorldElement):
    def __init__(self, entity, cell):
        super().__init__(entity)
        self.cell = cell

    def get_cell(self) -> Cell | None:
        return self.cell


def cell(state: CellState):
    return Cell(Vector2D(0, 0), 10, 10, state)


@pytest.fixture
def graph():
    return Graph()


@pytest.fixture
def origin():
    return TestElement(1, cell(CellState.SAFE))


def test_create_edge_with_present_safe_destination(graph, origin):
    destination = TestElement(2, cell(CellState.SAFE))
    graph.create_edge(origin, Direction.N, [destination])
    assert graph.graph[origin][Direction.N] == [destination]


def test_create_edge_with_present_mixed_destination(graph, origin):
    destination = TestElement(2, cell(CellState.MIXED))
    graph.create_edge(origin, Direction.N, [destination])
    assert graph.graph[origin][Direction.N] == []


def test_create_edge_with_present_unsafe_destination(graph, origin):
    destination = TestElement(2, cell(CellState.UNSAFE))
    graph.create_edge(origin, Direction.N, [destination])
    assert graph.graph[origin][Direction.N] == []


def test_create_edge_with_missing_destination(graph, origin):
    graph.create_edge(origin, Direction.N, [])
    assert not graph.graph[origin][Direction.N]


def test_neighbour_if_missing(graph, origin):
    assert graph.neighbour(origin, Direction.N) is None


def test_neighbour_if_exists(graph, origin):
    destination = TestElement(2, cell(CellState.SAFE))
    graph.create_edge(origin, Direction.N, [destination])
    assert graph.neighbour(origin, Direction.N) == destination


def test_neighbours_if_missing(graph, origin):
    assert graph.neighbours(origin) == []


def test_neighbours_if_exists(graph, origin):
    destination_1 = TestElement(2, cell(CellState.SAFE))
    destination_2 = TestElement(3, cell(CellState.SAFE))
    graph.create_edge(origin, Direction.N, [destination_1])
    graph.create_edge(origin, Direction.E, [destination_2])
    neighbours = graph.neighbours(origin)
    assert len(neighbours) == 2
    assert destination_1 in neighbours
    assert destination_2 in neighbours
