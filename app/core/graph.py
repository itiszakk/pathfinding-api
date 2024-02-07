from typing import Any

from app.core.direction import Direction


class Graph:
    def __init__(self):
        self.graph: dict[Any, dict[Direction, list[Any]]] = {}

    def add_vertex(self, element: Any):
        self.graph[element] = {}

    def add_edge(self, origin: Any, direction: Direction, destinations: list[Any]):
        self.graph[origin][direction] = destinations

    def neighbours_by_direction(self, element: Any, direction: Direction):
        return self.graph[element][direction]

    def neighbours(self, element: Any):
        neighbours = []

        for direction in Direction:
            neighbours_by_direction = self.neighbours_by_direction(element, direction)
            neighbours.extend(neighbours_by_direction)

        return neighbours
