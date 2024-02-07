from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.distance import Distance
from app.core.graph import Graph
from app.core.movement import Movement
from app.core.point import Point
from app.core.timing import timing


class World(ABC):
    _DISTANCE_BY_MOVEMENT = {
        Movement.Cardinal: Distance.manhattan,
        Movement.Diagonal: Distance.euclidian
    }

    def __init__(self, pixels: numpy.ndarray, cell_size: int, movement: Movement):
        super().__init__()
        self.pixels = pixels
        self.cell_size = cell_size
        self.movement = movement
        self.elements: list[Any] = []

    def allow_diagonal(self, direction: Direction):
        return self.movement == Movement.Diagonal and direction.is_diagonal()

    def cost(self, start, end):
        p0 = self.get_cell(start).center()
        p1 = self.get_cell(end).center()

        return self._DISTANCE_BY_MOVEMENT[self.movement](p0, p1)

    def heuristic(self, start, end):
        p0 = self.get_cell(start).center()
        p1 = self.get_cell(end).center()

        return self._DISTANCE_BY_MOVEMENT[self.movement](p0, p1)

    @timing("Graph build")
    def graph(self) -> Graph:
        graph = Graph()

        for element in self.get_elements():
            graph.add_vertex(element)

            for direction in Direction:
                neighbours = self.neighbours(element, direction)
                graph.add_edge(element, direction, neighbours)

        return graph

    @classmethod
    @abstractmethod
    def get_elements(cls) -> list[Any]:
        ...

    @classmethod
    @abstractmethod
    def get_cell(cls, element: Any) -> Cell:
        ...

    @classmethod
    @abstractmethod
    def get_cells(cls) -> list[Cell]:
        ...

    @classmethod
    @abstractmethod
    def select(cls, targets: list[Any]) -> list[Cell]:
        ...

    @classmethod
    @abstractmethod
    def get(cls, point: Point) -> Any:
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, element: Any, direction: Direction) -> list[Any]:
        ...
