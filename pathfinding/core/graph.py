"""
Graph module
"""

from pathfinding.core.direction import Direction
from pathfinding.world.world_element import WorldElement


class Graph:
    """
    Represents a graph structure for navigating through world elements
    """

    def __init__(self):
        """
        Initializes the Graph object with an empty graph
        """

        self.graph: dict[WorldElement, dict[Direction, list[WorldElement]]] = {}

    def create_edge(self, origin: WorldElement, direction: Direction, destinations: list[WorldElement]):
        """
        Creates an edge between the origin element and its destinations in the specified direction
        :param origin: origin world element
        :param direction: edge direction
        :param destinations: destinations connected by the edge
        """

        if origin not in self.graph:
            self.graph[origin] = {}

        self.graph[origin][direction] = destinations

    def neighbour(self, element: WorldElement, direction: Direction) -> WorldElement | None:
        """
        Returns the neighbour of the given element in the specified direction
        :param element: the element for which to find a neighbour
        :param direction: specified direction
        :return: neighbour element if exists, None otherwise
        """

        if element is None:
            return None

        neighbours = self.graph[element][direction]
        return neighbours[0] if neighbours else None

    def neighbours(self, element: WorldElement, safe=True) -> list[WorldElement]:
        """
        Returns the neighbours of the given element, optionally filtering out unsafe neighbours
        :param element: the element for which to find neighbours
        :param safe: filter out unsafe neighbours. Defaults to True
        :return: a list of neighbours
        """

        if element is None:
            return []

        neighbours = []

        for candidates in self.graph[element].values():
            for candidate in candidates:
                if safe and candidate.unsafe():
                    continue

                neighbours.append(candidate)

        return neighbours
