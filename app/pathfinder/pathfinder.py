from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.graph import Graph
from app.core.point import Point
from app.core.trajectory import Trajectory
from app.pathfinder.tracer import Tracer
from app.world.world_element import WorldElement


class Pathfinder(ABC):
    def __init__(self,
                 graph: Graph,
                 start: WorldElement,
                 end: WorldElement,
                 start_point: Point,
                 end_point: Point,
                 trajectory: Trajectory):
        super().__init__()
        self.graph: Graph = graph
        self.start = start
        self.end = end
        self.start_point = start_point
        self.end_point = end_point
        self.trajectory = trajectory

    def search(self):
        visited = self.method()
        tracer = Tracer(self.start, self.start_point, self.end, self.end_point, self.trajectory)
        return tracer.backtrace(visited)

    @classmethod
    @abstractmethod
    def method(cls) -> dict[WorldElement, WorldElement]:
        ...
