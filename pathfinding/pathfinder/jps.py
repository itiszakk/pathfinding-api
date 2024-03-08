"""
Jump Point Search (JPS) module
"""

from collections import namedtuple

from pqdict import pqdict

from pathfinding.core.direction import Direction
from pathfinding.core.timing import timing
from pathfinding.pathfinder.pathfinder import Pathfinder
from pathfinding.world.world import WorldElement


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

    def successors(self, current: WorldElement, parent: WorldElement) -> list[WorldElement]:
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

    def prune(self, current: WorldElement, parent: WorldElement):
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
            vertical_safe = vertical is not None and vertical.safe()

            horizontal = self.graph.neighbour(current, cardinal.h)
            horizontal_safe = horizontal is not None and horizontal.safe()

            if vertical_safe:
                neighbours.append(vertical)

            if horizontal_safe:
                neighbours.append(horizontal)

            if vertical_safe and horizontal_safe:
                neighbours.append(self.graph.neighbour(current, direction))
        else:
            if direction.is_horizontal():
                new = self.graph.neighbour(current, direction)
                top = self.graph.neighbour(current, Direction.N)
                bottom = self.graph.neighbour(current, Direction.S)

                if new is not None and new.safe():
                    neighbours.append(new)

                    if top is not None and top.safe():
                        neighbours.append(self.graph.neighbour(top, direction))

                    if bottom is not None and bottom.safe():
                        neighbours.append(self.graph.neighbour(bottom, direction))

                if top is not None and top.safe():
                    neighbours.append(top)

                if bottom is not None and bottom.safe():
                    neighbours.append(bottom)
            elif direction.is_vertical():
                new = self.graph.neighbour(current, direction)
                left = self.graph.neighbour(current, Direction.W)
                right = self.graph.neighbour(current, Direction.E)

                if new is not None and new.safe():
                    neighbours.append(new)

                    if left is not None and left.safe():
                        neighbours.append(self.graph.neighbour(left, direction))

                    if right is not None and right.safe():
                        neighbours.append((self.graph.neighbour(right, direction)))

                if left is not None and left.safe():
                    neighbours.append(left)

                if right is not None and right.safe():
                    neighbours.append(right)

        return neighbours

    def jump(self, current: WorldElement, parent: WorldElement):
        """
        Jumps to a new node, stopping at jump points
        :param current: the current node being expanded
        :param parent: the parent node of the current node
        :return: the next jump point
        """
        if current is None or current.unsafe():
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
                top_forced = top is not None and top.safe() and prev_top is not None and prev_top.unsafe()

                bottom = self.graph.neighbour(current, Direction.S)
                prev_bottom = self.graph.neighbour(top, JPS.OPPOSITE[direction])
                bottom_forced = (bottom is not None and bottom.safe()
                                 and prev_bottom is not None and prev_bottom.unsafe())

                if top_forced or bottom_forced:
                    return current

            elif direction.is_vertical():
                left = self.graph.neighbour(current, Direction.E)
                prev_left = self.graph.neighbour(left, JPS.OPPOSITE[direction])
                left_forced = left is not None and left.safe() and prev_left is not None and prev_left.unsafe()

                right = self.graph.neighbour(current, Direction.W)
                prev_right = self.graph.neighbour(right, JPS.OPPOSITE[direction])
                right_forced = right is not None and right.safe() and prev_right is not None and prev_right.unsafe()

                if left_forced or right_forced:
                    return current

        return self.jump(self.graph.neighbour(current, direction), current)

    @staticmethod
    def direction(current: WorldElement, parent: WorldElement):
        """
        Determines the direction from current node to its parent node
        :param current: the current node
        :param parent: the parent node
        :return: the direction from current node to its parent node
        """

        cx, cy = current.get_cell().center()
        px, py = parent.get_cell().center()

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
