import pytest

from pathfinding.core.direction import Direction
from pathfinding.core.graph import Graph
from pathfinding.world.world_element import WorldElement


@pytest.fixture
def graph():
    return Graph()


@pytest.fixture
def origin():
    return WorldElement(1)


@pytest.fixture
def first_destination():
    return WorldElement(2)


@pytest.fixture
def second_destination():
    return WorldElement(3)


def test_create_edge_with_present_destination(graph, origin, first_destination):
    graph.create_edge(origin, Direction.N, [first_destination])
    assert graph.graph[origin][Direction.N] == [first_destination]


def test_create_edge_with_missing_destination(graph, origin):
    graph.create_edge(origin, Direction.N, [])
    assert not graph.graph[origin][Direction.N]


def test_neighbour_if_missing(graph, origin):
    assert graph.neighbour(origin, Direction.N) is None


def test_neighbour_if_exists(graph, origin, first_destination):
    graph.create_edge(origin, Direction.N, [first_destination])
    assert graph.neighbour(origin, Direction.N) == first_destination


def test_neighbours_if_missing(graph, origin):
    assert graph.neighbours(origin) == []


def test_neighbours_if_exists(graph, origin, first_destination, second_destination):
    graph.create_edge(origin, Direction.N, [first_destination])
    graph.create_edge(origin, Direction.E, [second_destination])
    neighbours = graph.neighbours(origin)
    assert len(neighbours) == 2
    assert first_destination in neighbours
    assert second_destination in neighbours
