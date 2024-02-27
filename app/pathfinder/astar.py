"""
A* module
"""

from pqdict import pqdict

from app.core.timing import timing
from app.pathfinder.pathfinder import Pathfinder


class AStar(Pathfinder):
    """
    A subclass of Pathfinder implementing the A* pathfinding algorithm
    """

    def __init__(self, graph, distance, start, end, start_point, end_point, trajectory):
        """
        Initializes the AStar object with specified parameters
        :param graph: the graph structure for pathfinding
        :param distance: the distance calculation method used by the pathfinding algorith
        :param start: the starting world element
        :param end: the ending world element
        :param start_point: the starting element coordinates
        :param end_point: the ending element coordinates
        :param trajectory: the trajectory type for pathfinding visualization
        """
        super().__init__(graph, distance, start, end, start_point, end_point, trajectory)

    @timing('AStar')
    def method(self):
        """
        Implements the A* pathfinding algorithm and returns the visited nodes
        :return: A dictionary representing the visited nodes during pathfinding
        """

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
