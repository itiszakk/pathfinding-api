from __future__ import annotations

from enum import StrEnum

from fastapi import UploadFile

from app.core.distance import Distance
from app.core.trajectory import Trajectory


class WorldRequest(StrEnum):
    Grid = 'grid'
    QTree = 'qtree'


class PathfinderRequest(StrEnum):
    AStar = 'astar'
    JPS = 'jps'


class Context:
    def __init__(self):
        self.file: UploadFile | None = None
        self.world: WorldRequest = WorldRequest.Grid
        self.distance: Distance | None = None
        self.cell_size: int = 50
        self.border_size: int = 1
        self.pathfinder: PathfinderRequest | None = None
        self.trajectory: Trajectory | None = None
        self.trajectory_size: int = 5
        self.point_size: int = 10
        self.start: tuple[int, int] = (0, 0)
        self.end: tuple[int, int] = (0, 0)


class ContextBuilder:
    def __init__(self):
        self.context = Context()

    def file(self, file: UploadFile) -> ContextBuilder:
        self.context.file = file
        return self

    def world(self, world: WorldRequest) -> ContextBuilder:
        self.context.world = world
        return self

    def cell_size(self, cell_size: int) -> ContextBuilder:
        self.context.cell_size = cell_size
        return self

    def border_size(self, border_size: int) -> ContextBuilder:
        self.context.border_size = border_size
        return self

    def pathfinder(self, pathfinder: PathfinderRequest) -> ContextBuilder:
        self.context.pathfinder = pathfinder
        return self

    def distance(self, distance: Distance) -> ContextBuilder:
        self.context.distance = distance
        return self

    def trajectory(self, trajectory: Trajectory) -> ContextBuilder:
        self.context.trajectory = trajectory
        return self

    def trajectory_size(self, trajectory_size: int) -> ContextBuilder:
        self.context.trajectory_size = trajectory_size
        return self

    def point_size(self, point_size: int) -> ContextBuilder:
        self.context.point_size = point_size
        return self

    def start(self, start: tuple[int, int]) -> ContextBuilder:
        self.context.start = start
        return self

    def end(self, end: tuple[int, int]) -> ContextBuilder:
        self.context.end = end
        return self

    def build(self) -> Context:
        return self.context
