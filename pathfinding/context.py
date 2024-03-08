"""
Context module
"""

from __future__ import annotations

from enum import StrEnum

from fastapi import UploadFile

from pathfinding.core.distance import Distance
from pathfinding.core.trajectory import Trajectory
from pathfinding.core.vector import Vector2D


class WorldRequest(StrEnum):
    """
    Enumeration for different world types
    """

    GRID = 'grid'
    QTREE = 'qtree'


class PathfinderRequest(StrEnum):
    """
    Enumeration for different pathfinder algorithms
    """

    ASTAR = 'astar'
    JPS = 'jps'


class WorldContext:
    """
    Class for encapsulating request context related to world visualization
    """

    def __init__(self,
                 file: UploadFile | None = None,
                 world: WorldRequest = WorldRequest.GRID,
                 cell_size: int = 50,
                 border_size: int = 1):
        """
        Initializes a WorldContext object with the provided parameters
        :param file: uploaded file containing the world map
        :param world: type of the world to be visualized. Defaults to WorldRequest.Grid
        :param cell_size: size of each cell in the world grid. Defaults to 50
        :param border_size: size of the border around each cell. Defaults to 1
        """

        self.file = file
        self.world = world
        self.cell_size = cell_size
        self.border_size = border_size


class PathfinderContext:
    """
    Class for encapsulating request context related to pathfinding visualization
    """

    def __init__(self,
                 distance: Distance | None = None,
                 pathfinder: PathfinderRequest | None = None,
                 trajectory: Trajectory | None = None,
                 trajectory_size: int = 5,
                 point_size: int = 10,
                 start: tuple[int, int] = (0, 0),
                 end: tuple[int, int] = (0, 0)):
        """
        Initializes a PathfindingContext object with the provided parameters
        :param distance: distance metric for pathfinding. Defaults to None
        :param pathfinder: pathfinder algorithm to be used for pathfinding. Defaults to None
        :param trajectory: type of trajectory to be visualized. Defaults to None
        :param trajectory_size: size of the trajectory line. Defaults to 5
        :param point_size: size of points in the trajectory. Defaults to 10
        :param start: starting point for pathfinding. Defaults to (0, 0)
        :param end: ending point for pathfinding. Defaults to (0, 0)
        """

        self.distance = distance
        self.pathfinder = pathfinder
        self.trajectory = trajectory
        self.trajectory_size = trajectory_size
        self.point_size = point_size
        self.start = Vector2D(*start)
        self.end = Vector2D(*end)


class Context:
    """
    Class for encapsulating request context related to world visualization and pathfinding
    """

    def __init__(self, world_context: WorldContext, pathfinder_context: PathfinderContext | None = None):
        """
        Initializes a Context object with the provided parameters
        :param world_context: WorldContext object
        :param pathfinder_context: optional PathfinderContext object
        """

        self.world_context = world_context
        self.pathfinder_context = pathfinder_context
