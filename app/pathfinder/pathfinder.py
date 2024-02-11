from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.point import Point
from app.world.world import World, WorldElement, WorldGraph


class Pathfinder(ABC):
    def __init__(self,
                 world: World,
                 start: WorldElement,
                 end: WorldElement,
                 start_point: Point,
                 end_point: Point):
        super().__init__()
        self.world = world
        self.graph: WorldGraph = world.graph()
        self.start = start
        self.end = end
        self.start_point = start_point
        self.end_point = end_point

    @classmethod
    @abstractmethod
    def search(cls) -> dict[WorldElement, WorldElement]:
        ...
