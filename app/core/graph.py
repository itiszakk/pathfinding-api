from app.core.direction import Direction
from app.core.distance import Distance
from app.world.world_element import WorldElement


class Graph:
    def __init__(self, distance: Distance):
        self.graph: dict[WorldElement, dict[Direction, list[WorldElement]]] = {}
        self.distance = distance

    def create_edge(self, origin: WorldElement, direction: Direction, destinations: list[WorldElement]):
        if origin not in self.graph:
            self.graph[origin] = {}

        self.graph[origin][direction] = destinations

    def cost(self, e0: WorldElement, e1: WorldElement):
        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

    def heuristics(self, e0: WorldElement, e1: WorldElement):
        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

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
