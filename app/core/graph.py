from app.core.direction import Direction
from app.world.world_element import WorldElement


class Graph:
    def __init__(self):
        self.graph: dict[WorldElement, dict[Direction, list[WorldElement]]] = {}

    def create_edge(self, origin: WorldElement, direction: Direction, destinations: list[WorldElement]):
        if origin not in self.graph:
            self.graph[origin] = {}

        self.graph[origin][direction] = destinations

    def neighbour(self, element: WorldElement, direction: Direction) -> WorldElement | None:
        if element is None:
            return None

        neighbours = self.graph[element][direction]
        return neighbours[0] if neighbours else None

    def neighbours(self, element: WorldElement, safe=True) -> list[WorldElement]:
        if element is None:
            return []

        neighbours = []

        for candidates in self.graph[element].values():
            for candidate in candidates:
                if safe and candidate.unsafe():
                    continue

                neighbours.append(candidate)

        return neighbours
