from pqdict import pqdict

from app.core.timing import timing
from app.core.direction import Direction
from app.pathfinder.pathfinder import Pathfinder


class JPS(Pathfinder):
    def __init__(self, world, start, end, start_point, end_point):
        super().__init__(world, start, end, start_point, end_point)

    @timing('JPS search')
    def search(self):
        queue = pqdict({self.start: 0})
        cost_so_far = {self.start: 0}
        visited = {self.start: None}

        while queue:
            current = queue.popitem()[0]

            if current == self.end:
                break

            successors = self.successors(current)

            for successor in successors:
                cost = cost_so_far[current] + self.world.cost(current, successor)

                if successor not in visited or cost < cost_so_far[successor]:
                    queue[successor] = cost + self.world.heuristic(successor, self.end)
                    cost_so_far[successor] = cost
                    visited[successor] = current

        return visited

    def successors(self, element):
        successors = []

        for direction in Direction:
            neighbours = self.graph.neighbours_by_direction(element, direction)

            for neighbour in neighbours:
                jump_point = self.jump(neighbour, direction)

                if jump_point is not None:
                    successors.append(jump_point)

        return successors

    # TODO jump
    def jump(self, element, direction):
        return element
