from pqdict import pqdict

from app.core.timing import timing
from app.pathfinder.pathfinder import Pathfinder
from app.world.world import WorldElement


class JPS(Pathfinder):
    def __init__(self, world, start, end, start_point, end_point):
        super().__init__(world, start, end, start_point, end_point)

    @timing('JPS')
    def search(self):
        queue = pqdict({self.start: 0})
        cost_so_far = {self.start: 0}
        visited = {self.start: None}

        while queue:
            current = queue.popitem()[0]

            if current == self.end:
                break

            neighbours = self.prune(current)

            for neighbour in neighbours:

                if neighbour.unsafe():
                    continue

                cost = cost_so_far[current] + self.world.cost(current, neighbour)

                if neighbour not in visited or cost < cost_so_far[neighbour]:
                    queue[neighbour] = cost + self.world.heuristic(neighbour, self.end)
                    cost_so_far[neighbour] = cost
                    visited[neighbour] = current

        return visited

    # TODO method
    def prune(self, element: WorldElement) -> list[WorldElement]:
        neighbours = []

        return neighbours
