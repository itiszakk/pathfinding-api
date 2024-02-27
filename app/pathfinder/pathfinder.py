"""
Base pathfinder module
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.distance import Distance
from app.core.graph import Graph
from app.core.trajectory import Trajectory
from app.core.vector import Vector2D
from app.pathfinder.tracer import Tracer
from app.world.world_element import WorldElement


class Pathfinder(ABC):
    """
    Abstract base class for implementing pathfinding algorithms
    """

    def __init__(self,
                 graph: Graph,
                 distance: Distance,
                 start: WorldElement,
                 end: WorldElement,
                 start_point: Vector2D,
                 end_point: Vector2D,
                 trajectory: Trajectory):
        """
        Initializes the Pathfinder object with specified parameters
        :param graph: the graph structure for pathfinding
        :param distance: the distance calculation method used by the pathfinding algorith
        :param start: the starting world element
        :param end: the ending world element
        :param start_point: the starting element coordinates
        :param end_point: the ending element coordinates
        :param trajectory: the trajectory type for pathfinding visualization
        """

        super().__init__()
        self.graph: Graph = graph
        self.distance = distance
        self.start = start
        self.end = end
        self.start_point = start_point
        self.end_point = end_point
        self.trajectory = trajectory

    def search(self):
        """
        Performs the pathfinding algorithm and returns the traced path
        :return: the traced path from start to end
        """
        visited = self.method()
        tracer = Tracer(self.start, self.start_point, self.end, self.end_point, self.trajectory)
        return tracer.backtrace(visited)

    def cost(self, e0: WorldElement, e1: WorldElement):
        """
        Calculates the cost between two adjacent nodes
        :param e0: the first node
        :param e1: the second node
        :return: the cost between the two nodes
        """

        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

    def heuristics(self, e0: WorldElement, e1: WorldElement):
        """
        Calculates the heuristics between two adjacent nodes
        :param e0: the first node
        :param e1: the second node
        :return: the heuristics between the two nodes
        """

        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

    @abstractmethod
    def method(self) -> dict[WorldElement, WorldElement]:
        """
        Abstract method representing the pathfinding algorithm to be implemented by subclasses
        :return: a dictionary representing the path found by the algorithm
        """
