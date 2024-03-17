"""
Grid module
"""

from __future__ import annotations

import numpy

from pathfinding.core.cell import Cell, CellState
from pathfinding.core.direction import Direction
from pathfinding.core.timing import timing
from pathfinding.core.vector import Vector2D
from pathfinding.world.world import World, WorldElement


class GridElement(WorldElement):
    """
    Represents an element in a grid
    """

    def __init__(self, index: Vector2D, cell: Cell):
        """
        Initializes a GridElement with the specified index and cell.
        :param index: the index vector of the element
        :param cell: the cell associated with the element
        """

        super().__init__(index)
        self.cell = cell

    def get_cell(self):
        """
        Retrieves the cell associated with the element
        :return: the cell associated with the element
        """

        return self.cell

    def __repr__(self):
        """
        String representation of the GridElement
        :return: string representation
        """

        return f'GridElement(entity={self.entity}, cell={self.cell})'

    def __hash__(self):
        """
        Hashing method for the GridElement
        :return: hash value
        """

        return hash(self.entity)

    def __eq__(self, other):
        """
        Equality comparison method for the GridElement
        :param other: other object to compare
        :return: True if equal, False otherwise
        """

        return self.entity == other.entity


class Grid(World):
    """
    Represents a grid world
    """

    @timing('Grid')
    def __init__(self, pixels: numpy.ndarray, cell_size: int):
        """
        Initializes a Grid with the specified pixels and cell size
        :param pixels: the pixel array representing the grid
        :param cell_size: the size of each cell in pixels
        """

        super().__init__(pixels, cell_size)
        self.rows = pixels.shape[1] // cell_size
        self.columns = pixels.shape[0] // cell_size
        self.elements: list[list[GridElement]] = []
        self.build_elements()

    def build_elements(self):
        """
        Builds elements for the grid based on the pixel array and cell size
        """

        for i in range(self.columns):
            sub = []

            for j in range(self.rows):
                index = Vector2D(i, j)
                position = Vector2D(i * self.cell_size, j * self.cell_size)
                state = CellState.of(self.pixels, position, Vector2D(self.cell_size, self.cell_size))
                sub.append(GridElement(index, Cell(position, self.cell_size, self.cell_size, state)))

            self.elements.append(sub)

    def get_elements(self) -> list[GridElement]:
        """
        Retrieves all elements in the grid
        :return: list of all elements
        """

        return [j for sub in self.elements for j in sub]

    def get(self, point: Vector2D) -> GridElement:
        """
        Retrieves the grid element at the specified point
        :param point: the point to retrieve the element from
        :return: the grid element at the specified point
        """

        return self.elements[point.x // self.cell_size][point.y // self.cell_size]

    def neighbours(self, element: GridElement, direction: Direction) -> list[GridElement]:
        """
        Retrieves neighbouring elements of the specified element in the given direction
        :param element: the specified element
        :param direction: the direction to search for neighbors
        :return: list of neighbouring elements
        """

        neighbour = self.neighbour(element.entity, direction)
        return [neighbour] if neighbour is not None else []

    def neighbour(self, index: Vector2D, direction: Direction) -> GridElement | None:
        """
        Retrieves the neighbour of the specified index in the given direction
        :param index: the index of the element
        :param direction: the direction to search for the neighbour
        :return: the neighbouring element if found, None otherwise
        """

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
