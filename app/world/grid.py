from __future__ import annotations

import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.timing import timing
from app.core.vector import Vector2D
from app.world.world import World, WorldElement


class GridElement(WorldElement):
    def __init__(self, index: Vector2D, cell: Cell):
        super().__init__(index)
        self.cell = cell

    def get_cell(self):
        return self.cell

    def __repr__(self):
        return f'IndexedCell(index={self.entity}, cell={self.cell})'

    def __hash__(self):
        return hash(self.entity)

    def __eq__(self, other):
        return self.entity == other.entity


class Grid(World):

    @timing('Grid')
    def __init__(self, pixels: numpy.ndarray, cell_size: int):
        super().__init__(pixels, cell_size)
        self.rows = pixels.shape[1] // cell_size
        self.columns = pixels.shape[0] // cell_size
        self.elements: list[list[GridElement]] = []
        self.build_elements()

    def build_elements(self):
        for i in range(self.columns):
            sub = []

            for j in range(self.rows):
                position = Vector2D(i * self.cell_size, j * self.cell_size)
                element = GridElement(index=Vector2D(i, j),
                                      cell=Cell(self.pixels, position, self.cell_size, self.cell_size))
                sub.append(element)

            self.elements.append(sub)

    def get_elements(self) -> list[GridElement]:
        return [j for sub in self.elements for j in sub]

    def get(self, point: Vector2D) -> GridElement:
        return self.elements[point.x // self.cell_size][point.y // self.cell_size]

    def neighbours(self, index: GridElement, direction: Direction) -> list[GridElement]:
        neighbour = self.neighbour(index.entity, direction)
        return [neighbour] if neighbour is not None else []

    def neighbour(self, index: Vector2D, direction: Direction) -> GridElement | None:
        i, j = index

        match direction:
            case Direction.N:
                if j > 0:
                    return self.elements[i][j - 1]
            case Direction.E:
                if i < self.columns - 1:
                    return self.elements[i + 1][j]
            case Direction.S:
                if j < self.rows - 1:
                    return self.elements[i][j + 1]
            case Direction.W:
                if i > 0:
                    return self.elements[i - 1][j]
            case Direction.NW:
                if i > 0 and j > 0:
                    return self.elements[i - 1][j - 1]
            case Direction.NE:
                if i < self.columns - 1 and j > 0:
                    return self.elements[i + 1][j - 1]
            case Direction.SW:
                if i > 0 and j < self.rows - 1:
                    return self.elements[i - 1][j + 1]
            case Direction.SE:
                if i < self.columns - 1 and j < self.rows - 1:
                    return self.elements[i + 1][j + 1]

        return None
