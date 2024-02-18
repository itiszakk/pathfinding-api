from __future__ import annotations

from abc import ABC, abstractmethod

import numpy

from app.core.direction import Direction
from app.core.graph import Graph
from app.core.vector import Vector2D
from app.core.timing import timing
from app.world.world_element import WorldElement


class World(ABC):
    def __init__(self, pixels: numpy.ndarray, cell_size: int):
        super().__init__()
        self.pixels = pixels
        self.cell_size = cell_size

    @timing('Graph')
    def graph(self) -> Graph:
        graph = Graph()

        elements = self.get_elements()

        for element in elements:
            for direction in Direction:
                graph.create_edge(element, direction, self.neighbours(element, direction))

        return graph

    @classmethod
    @abstractmethod
    def get_elements(cls) -> list[WorldElement]:
        ...

    @classmethod
    @abstractmethod
    def get(cls, point: Vector2D) -> WorldElement:
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, element: WorldElement, direction: Direction) -> list[WorldElement]:
        ...
