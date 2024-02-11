from __future__ import annotations

import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.movement import Movement
from app.core.point import Point
from app.core.timing import timing
from app.world.world import World, WorldElement


class IndexedCell(WorldElement):
    def __init__(self, index: int, cell: Cell):
        super().__init__(index)
        self.cell = cell

    def get_cell(self):
        return self.cell

    def __hash__(self):
        return self.entity

    def __eq__(self, other: IndexedCell):
        return self.entity == other.entity and self.cell == other.cell


class Grid(World):

    @timing('Grid')
    def __init__(self, pixels: numpy.ndarray, cell_size: int, movement: Movement):
        super().__init__(pixels, cell_size, movement)
        self.rows = pixels.shape[1] // cell_size
        self.columns = pixels.shape[0] // cell_size
        self.elements: dict[int, IndexedCell] = {}
        self.build_elements()

    def build_elements(self):
        for row in range(self.rows):
            for col in range(self.columns):
                position = Point(col * self.cell_size, row * self.cell_size)
                cell = Cell(self.pixels, position, self.cell_size, self.cell_size)
                index = self.index(row, col)
                self.elements[index] = IndexedCell(index, cell)

    def get_elements(self) -> list[IndexedCell]:
        return list(self.elements.values())

    def get(self, point: Point) -> IndexedCell:
        index = self.index(point.y // self.cell_size, point.x // self.cell_size)
        return self.elements[index]

    def index(self, row: int, column: int) -> int:
        return row * self.columns + column

    def neighbours(self, index: IndexedCell, direction: Direction) -> list[IndexedCell]:
        row = index.entity // self.columns
        column = index.entity - row * self.columns

        if self.allow_diagonal(direction):
            neighbour = self.diagonal_neighbour(row, column, direction)
        else:
            neighbour = self.cardinal_neighbour(row, column, direction)

        return [neighbour] if neighbour is not None else []

    def diagonal_neighbour(self, row, column, direction: Direction) -> IndexedCell:
        index = None

        match direction:
            case Direction.NW:
                index = self.index(row - 1, column - 1) if row > 0 and column > 0 else None
            case Direction.NE:
                index = self.index(row - 1, column + 1) if row > 0 and column < self.columns - 1 else None
            case Direction.SW:
                index = self.index(row + 1, column - 1) if row < self.rows - 1 and column > 0 else None
            case Direction.SE:
                index = self.index(row + 1, column + 1) if row < self.rows - 1 and column < self.columns - 1 else None

        return self.elements[index] if index is not None else None

    def cardinal_neighbour(self, row, column, direction: Direction) -> IndexedCell:
        index = None

        match direction:
            case Direction.N:
                index = self.index(row - 1, column) if row > 0 else None
            case Direction.E:
                index = self.index(row, column + 1) if column < self.columns - 1 else None
            case Direction.S:
                index = self.index(row + 1, column) if row < self.rows - 1 else None
            case Direction.W:
                index = self.index(row, column - 1) if column > 0 else None

        return self.elements[index] if index is not None else None
