"""
Context module
"""

from __future__ import annotations

from enum import StrEnum

from fastapi import UploadFile

from app.core.distance import Distance
from app.core.trajectory import Trajectory
from app.core.vector import Vector2D


class WorldRequest(StrEnum):
    """
    Enumeration for different world types
    """

    Grid = 'grid'
    QTree = 'qtree'


class PathfinderRequest(StrEnum):
    """
    Enumeration for different pathfinder algorithms
    """

    AStar = 'astar'
    JPS = 'jps'


class Context:
    """
    Class for encapsulating request context related to world visualization and pathfinding
    """

    def __init__(self,
                 file: UploadFile | None = None,
                 world: WorldRequest = WorldRequest.Grid,
                 distance: Distance | None = None,
                 cell_size: int = 50,
                 border_size: int = 1,
                 pathfinder: PathfinderRequest | None = None,
                 trajectory: Trajectory | None = None,
                 trajectory_size: int = 5,
                 point_size: int = 10,
                 start: tuple[int, int] = (0, 0),
                 end: tuple[int, int] = (0, 0)):
        """
        Initializes a Context object with the provided parameters
        :param file: uploaded file containing the world map
        :param world: type of the world to be visualized. Defaults to WorldRequest.Grid
        :param distance: distance metric for pathfinding. Defaults to None
        :param cell_size: size of each cell in the world grid. Defaults to 50
        :param border_size: size of the border around each cell. Defaults to 1
        :param pathfinder: pathfinder algorithm to be used for pathfinding. Defaults to None
        :param trajectory: type of trajectory to be visualized. Defaults to None
        :param trajectory_size: size of the trajectory line. Defaults to 5
        :param point_size: size of points in the trajectory. Defaults to 10
        :param start: starting point for pathfinding. Defaults to (0, 0)
        :param end: ending point for pathfinding. Defaults to (0, 0)
        """
        
        self.file = file
        self.world = world
        self.distance = distance
        self.cell_size = cell_size
        self.border_size = border_size
        self.pathfinder = pathfinder
        self.trajectory = trajectory
        self.trajectory_size = trajectory_size
        self.point_size = point_size
        self.start = Vector2D(*start)
        self.end = Vector2D(*end)
