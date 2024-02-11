from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.distance import Distance
from app.core.movement import Movement
from app.core.point import Point
from app.core.timing import timing


class WorldGraph:
    def __init__(self):
        self.graph: dict[WorldElement, dict[Direction, list[WorldElement]]] = {}

    def add_vertex(self, element: WorldElement):
        self.graph[element] = {}

    def add_edge(self, origin: WorldElement, direction: Direction, destinations: list[WorldElement]):
        self.graph[origin][direction] = destinations

    def neighbours_by_direction(self, element: WorldElement, direction: Direction):
        return self.graph[element][direction]

    def neighbours(self, element: WorldElement):
        neighbours = []

        for direction in Direction:
            neighbours_by_direction = self.neighbours_by_direction(element, direction)
            neighbours.extend(neighbours_by_direction)

        return neighbours


class WorldElement(ABC):
    def __init__(self, entity: Any):
        self.entity = entity

    def unsafe(self) -> bool:
        return self.get_cell().state != Cell.State.SAFE

    @classmethod
    @abstractmethod
    def get_cell(cls) -> Cell:
        ...


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

    def allow_diagonal(self, direction: Direction):
        return self.movement == Movement.Diagonal and direction.is_diagonal()

    def cost(self, start: WorldElement, end: WorldElement):
        p0 = start.get_cell().center()
        p1 = end.get_cell().center()

        return self._DISTANCE_BY_MOVEMENT[self.movement](p0, p1)

    def heuristic(self, start: WorldElement, end: WorldElement):
        p0 = start.get_cell().center()
        p1 = end.get_cell().center()

        return self._DISTANCE_BY_MOVEMENT[self.movement](p0, p1)

    @timing("Graph")
    def graph(self) -> WorldGraph:
        graph = WorldGraph()

        for element in self.get_elements():
            graph.add_vertex(element)

            for direction in Direction:
                neighbours = self.neighbours(element, direction)
                graph.add_edge(element, direction, neighbours)

        return graph

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
