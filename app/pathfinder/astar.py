from pqdict import pqdict

from app.core.timing import timing
from app.pathfinder.pathfinder import Pathfinder


class AStar(Pathfinder):
    def __init__(self, graph, distance, start, end, start_point, end_point, trajectory):
        super().__init__(graph, distance, start, end, start_point, end_point, trajectory)

    @timing('AStar')
    def method(self):
        queue = pqdict({self.start: 0})
        cost_so_far = {self.start: 0}
        visited = {self.start: None}

        while queue:
            current = queue.popitem()[0]

            if current == self.end:
                break

            neighbours = self.graph.neighbours(current)

            for neighbour in neighbours:

                if neighbour in queue:
                    continue

                cost = cost_so_far[current] + self.cost(current, neighbour)

                if neighbour not in visited or cost < cost_so_far[neighbour]:
                    queue[neighbour] = cost + self.heuristics(neighbour, self.end)
                    cost_so_far[neighbour] = cost
                    visited[neighbour] = current

        return visited
