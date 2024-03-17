import pytest

from pathfinding.core.direction import Direction
from pathfinding.core.graph import Graph, Vertex


@pytest.fixture
def graph():
    return Graph()


@pytest.fixture
def origin():
    return Vertex(1)


@pytest.fixture
def destinations():
    return [Vertex(2), Vertex(3)]


def test_add_edge(graph, origin, destinations):
    graph.add_edge(origin, Direction.N, [destinations[0]])
    assert graph.graph[origin][Direction.N] == [destinations[0]]


def test_neighbour(graph, origin, destinations):
    graph.add_edge(origin, Direction.N, [destinations[0]])
    assert graph.neighbour(origin, Direction.N) == destinations[0]


def test_neighbour_nonexistent(graph, origin):
    assert graph.neighbour(origin, Direction.N) is None


def test_neighbours(graph, origin, destinations):
    graph.add_edge(origin, Direction.N, [destinations[0]])
    graph.add_edge(origin, Direction.E, [destinations[1]])
    neighbours = graph.neighbours(origin)
    assert len(neighbours) == 2
    assert destinations[0] in neighbours
    assert destinations[1] in neighbours


def test_neighbours_nonexistent(graph, origin):
    assert graph.neighbours(origin) == []
