from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.direction import Direction
from app.core.distance import Distance
from app.core.graph import Graph
from app.core.vector import Vector2D
from app.core.trajectory import Trajectory
from app.pathfinder.tracer import Tracer
from app.world.world_element import WorldElement


class Pathfinder(ABC):
    def __init__(self,
                 graph: Graph,
                 distance: Distance,
                 start: WorldElement,
                 end: WorldElement,
                 start_point: Vector2D,
                 end_point: Vector2D,
                 trajectory: Trajectory):
        super().__init__()
        self.graph: Graph = graph
        self.distance = distance
        self.start = start
        self.end = end
        self.start_point = start_point
        self.end_point = end_point
        self.trajectory = trajectory

    def search(self):
        visited = self.method()
        tracer = Tracer(self.start, self.start_point, self.end, self.end_point, self.trajectory)
        return tracer.backtrace(visited)

    @staticmethod
    def direction(current: WorldElement, parent: WorldElement):
        cx, cy = current.get_cell().center()
        px, py = parent.get_cell().center()

        dx = cx - px
        dy = cy - py

        if dx != 0 and dy != 0:
            if dx > 0:
                return Direction.SE if dy > 0 else Direction.NE
            else:
                return Direction.SW if dy > 0 else Direction.NW
        else:
            if dx != 0:
                return Direction.E if dx > 0 else Direction.W
            elif dy != 0:
                return Direction.S if dy > 0 else Direction.N

    def cost(self, e0: WorldElement, e1: WorldElement):
        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

    def heuristics(self, e0: WorldElement, e1: WorldElement):
        p0 = e0.get_cell().center()
        p1 = e1.get_cell().center()

        return self.distance.calculate(p0, p1)

    @classmethod
    @abstractmethod
    def method(cls) -> dict[WorldElement, WorldElement]:
        ...
