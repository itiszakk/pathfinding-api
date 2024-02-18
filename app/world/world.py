from __future__ import annotations

from abc import ABC, abstractmethod

import numpy

from app.core.direction import Direction
from app.core.point import Point
from app.world.world_element import WorldElement


class World(ABC):
    def __init__(self, pixels: numpy.ndarray, cell_size: int):
        super().__init__()
        self.pixels = pixels
        self.cell_size = cell_size

    @classmethod
    @abstractmethod
    def get_elements(cls) -> list[WorldElement]:
        ...

    @classmethod
    @abstractmethod
    def get(cls, point: Point) -> WorldElement:
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, element: WorldElement, direction: Direction) -> list[WorldElement]:
        ...
