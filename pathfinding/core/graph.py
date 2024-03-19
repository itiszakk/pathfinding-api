"""
Graph module
"""

from pathfinding.core import Direction


class Vertex:
    def __init__(self, entity, obstacle: bool = False):
        self.entity = entity
        self.obstacle = obstacle

    def __hash__(self):
        return hash(self.entity)

    def __eq__(self, other):
        return self.entity == other.entity

    def __repr__(self):
        return f'Vertex(#{self.__hash__()})'


class Graph:
    """
    Represents a graph structure for navigating through world elements
    """

    def __init__(self):
        """
        Initializes the Graph object with an empty graph
        """

        self.graph: dict[Vertex, dict[Direction, list[Vertex]]] = {}

    def add_edge(self, origin: Vertex, direction: Direction, destinations: list[Vertex]):
        """
        Creates an edge between the origin element and its destinations in the specified direction
        :param origin: origin vertex
        :param direction: edge direction
        :param destinations: destinations connected by the edge
        """

        if origin not in self.graph:
            self.graph[origin] = {}

        self.graph[origin][direction] = destinations

    def neighbour(self, element: Vertex, direction: Direction) -> Vertex | None:
        """
        Returns the neighbour of the given vertex in the specified direction
        :param element: the vertex for which to find a neighbour
        :param direction: specified direction
        :return: neighbour vertex if exists, None otherwise
        """

        neighbours = self.graph.get(element, {}).get(direction, [])
        return neighbours[0] if neighbours else None

    def neighbours(self, element: Vertex) -> list[Vertex]:
        """
        Returns the neighbours of the given vertex
        :param element: the vertex for which to find neighbours
        :return: a list of neighbours
        """

        neighbours = []

        for direction in self.graph.get(element, []):
            neighbours.extend(self.graph[element][direction])

        return neighbours
