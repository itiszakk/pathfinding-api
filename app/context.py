from __future__ import annotations

from enum import StrEnum

from fastapi import UploadFile

from app.core.distance import Distance
from app.core.trajectory import Trajectory
from app.core.vector import Vector2D


class WorldRequest(StrEnum):
    Grid = 'grid'
    QTree = 'qtree'


class PathfinderRequest(StrEnum):
    AStar = 'astar'
    JPS = 'jps'


class Context:
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
