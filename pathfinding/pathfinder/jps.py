"""
Jump Point Search (JPS) module
"""

from collections import namedtuple

from pqdict import pqdict

from pathfinding.core import Direction, timing, Vertex
from pathfinding.pathfinder import Pathfinder


class JPS(Pathfinder):
    """
    A subclass of Pathfinder implementing the Jump Point Search (JPS) pathfinding algorithm
    """

    Cardinal = namedtuple('Cardinal', ['v', 'h'])

    CARDINAL = {
        Direction.NW: Cardinal(Direction.N, Direction.W),
        Direction.NE: Cardinal(Direction.N, Direction.E),
        Direction.SW: Cardinal(Direction.S, Direction.W),
        Direction.SE: Cardinal(Direction.S, Direction.E)
    }

    OPPOSITE = {
        Direction.N: Direction.S,
        Direction.S: Direction.N,
        Direction.W: Direction.E,
        Direction.E: Direction.W,
        Direction.NW: Direction.SE,
        Direction.SE: Direction.NW,
        Direction.NE: Direction.SW,
        Direction.SW: Direction.NE
    }

    @timing('JPS')
    def method(self):
        """
        Implements the Jump Point Search (JPS) pathfinding algorithm and returns the visited nodes
        :return: A dictionary representing the visited nodes during pathfinding
        """

        queue = pqdict({self.start: 0})
        cost_so_far = {self.start: 0}
        visited = {self.start: None}

        while queue:
            current = queue.popitem()[0]

            if current == self.end:
                break

            successors = self.successors(current, visited[current])

            for successor in successors:

                if successor in queue:
                    continue

                cost = cost_so_far[current] + self.cost(current, successor)

                if successor not in visited or cost < cost_so_far[successor]:
                    queue[successor] = cost + self.heuristics(successor, self.end)
                    cost_so_far[successor] = cost
                    visited[successor] = current

        return visited

    def successors(self, current: Vertex, parent: Vertex) -> list[Vertex]:
        """
        Determines the successors of a given node in the search space
        :param current: the current node being expanded
        :param parent: the parent node of the current node
        :return: a list of successor nodes
        """

        successors = []

        neighbours = self.prune(current, parent)

        for neighbour in neighbours:
            jump_point = self.jump(neighbour, current)

            if jump_point is not None:
                successors.append(jump_point)

        return successors

    def prune(self, current: Vertex, parent: Vertex):
        """
        Prunes the search space by removing unnecessary successors
        :param current: the current node being expanded
        :param parent: the parent node of the current node
        :return: a list of pruned neighbours
        """

        if parent is None:
            return self.graph.neighbours(current)

        neighbours = []
        direction = self.direction(current, parent)

        if direction.is_diagonal():
            cardinal = JPS.CARDINAL[direction]
            vertical = self.graph.neighbour(current, cardinal.v)
            horizontal = self.graph.neighbour(current, cardinal.h)

            if self.safe(vertical):
                neighbours.append(vertical)

            if self.safe(horizontal):
                neighbours.append(horizontal)

            if self.safe(vertical) and self.safe(horizontal):
                neighbours.append(self.graph.neighbour(current, direction))
        else:
            if direction.is_horizontal():
                new = self.graph.neighbour(current, direction)
                top = self.graph.neighbour(current, Direction.N)
                bottom = self.graph.neighbour(current, Direction.S)

                if self.safe(new):
                    neighbours.append(new)

                    if self.safe(top):
                        neighbours.append(self.graph.neighbour(top, direction))

                    if self.safe(bottom):
                        neighbours.append(self.graph.neighbour(bottom, direction))

                if self.safe(top):
                    neighbours.append(top)

                if self.safe(bottom):
                    neighbours.append(bottom)
            elif direction.is_vertical():
                new = self.graph.neighbour(current, direction)
                left = self.graph.neighbour(current, Direction.W)
                right = self.graph.neighbour(current, Direction.E)

                if self.safe(new):
                    neighbours.append(new)

                    if self.safe(left):
                        neighbours.append(self.graph.neighbour(left, direction))

                    if self.safe(right):
                        neighbours.append((self.graph.neighbour(right, direction)))

                if self.safe(left):
                    neighbours.append(left)

                if self.safe(right):
                    neighbours.append(right)

        return neighbours

    def jump(self, current: Vertex, parent: Vertex):
        """
        Jumps to a new node, stopping at jump points
        :param current: the current node being expanded
        :param parent: the parent node of the current node
        :return: the next jump point
        """
        if not self.safe(current):
            return None

        if current is self.end:
            return current

        direction = self.direction(current, parent)

        if direction.is_diagonal():
            cardinal = JPS.CARDINAL[direction]
            vertical = self.graph.neighbour(current, cardinal.v)
            horizontal = self.graph.neighbour(current, cardinal.h)

            if self.jump(vertical, current) is not None or self.jump(horizontal, current) is not None:
                return current
        else:
            if direction.is_horizontal():
                top = self.graph.neighbour(current, Direction.N)
                prev_top = self.graph.neighbour(top, JPS.OPPOSITE[direction])

                bottom = self.graph.neighbour(current, Direction.S)
                prev_bottom = self.graph.neighbour(top, JPS.OPPOSITE[direction])

                if self.forced(top, prev_top) or self.forced(bottom, prev_bottom):
                    return current

            elif direction.is_vertical():
                left = self.graph.neighbour(current, Direction.W)
                prev_left = self.graph.neighbour(left, JPS.OPPOSITE[direction])

                right = self.graph.neighbour(current, Direction.E)
                prev_right = self.graph.neighbour(right, JPS.OPPOSITE[direction])

                if self.forced(left, prev_left) or self.forced(right, prev_right):
                    return current

        return self.jump(self.graph.neighbour(current, direction), current)

    @staticmethod
    def safe(vertex: Vertex):
        return vertex is not None and not vertex.obstacle

    @staticmethod
    def forced(curr: Vertex, prev: Vertex):
        return curr is not None and not curr.obstacle and prev is not None and prev.obstacle

    @staticmethod
    def direction(current: Vertex, parent: Vertex):
        """
        Determines the direction from current node to its parent node
        :param current: the current node
        :param parent: the parent node
        :return: the direction from current node to its parent node
        """

        cx, cy = current.entity.get_cell().center()
        px, py = parent.entity.get_cell().center()

        dx = cx - px
        dy = cy - py

        if dx != 0 and dy != 0:
            if dx > 0:
                return Direction.SE if dy > 0 else Direction.NE

            return Direction.SW if dy > 0 else Direction.NW

        if dx != 0:
            return Direction.E if dx > 0 else Direction.W

        if dy != 0:
            return Direction.S if dy > 0 else Direction.N

        return None
