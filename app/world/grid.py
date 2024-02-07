import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.movement import Movement
from app.core.point import Point
from app.core.timing import timing
from app.world.world import World


class Grid(World):
    @timing('Grid build')
    def __init__(self, pixels: numpy.ndarray, cell_size: int, movement: Movement):
        super().__init__(pixels, cell_size, movement)
        self.rows = pixels.shape[1] // cell_size
        self.columns = pixels.shape[0] // cell_size
        self.build_elements()

    def build_elements(self):
        for row in range(self.rows):
            for col in range(self.columns):
                position = Point(col * self.cell_size, row * self.cell_size)
                cell = Cell(self.pixels, position, self.cell_size, self.cell_size)
                self.elements.append(cell)

    def get_elements(self) -> list[int]:
        return list(range(len(self.elements)))

    def get_cell(self, element) -> Cell:
        return self.elements[element]

    def get_cells(self) -> list[Cell]:
        return self.elements

    def select(self, targets: list[int]) -> list[Cell]:
        return [self.elements[target] for target in targets]

    def get(self, point: Point) -> int:
        return self.index(point.y // self.cell_size, point.x // self.cell_size)

    def index(self, row: int, column: int) -> int:
        return row * self.columns + column

    def neighbours(self, index: int, direction: Direction) -> list[int]:
        row = index // self.columns
        column = index - row * self.columns

        if self.allow_diagonal(direction):
            neighbour = self.diagonal_neighbour(row, column, direction)
        else:
            neighbour = self.cardinal_neighbour(row, column, direction)

        return [neighbour] if neighbour is not None else []

    def diagonal_neighbour(self, row, column, direction: Direction) -> int:
        match direction:
            case Direction.NW:
                index = self.index(row - 1, column - 1)
                if row > 0 and column > 0 and self.check(index):
                    return index
            case Direction.NE:
                index = self.index(row - 1, column + 1)
                if row > 0 and column < self.columns - 1 and self.check(index):
                    return index
            case Direction.SE:
                index = self.index(row + 1, column + 1)
                if row < self.rows - 1 and column < self.columns - 1 and self.check(index):
                    return index
            case Direction.SW:
                index = self.index(row + 1, column - 1)
                if row < self.rows - 1 and column > 0 and self.check(index):
                    return index

    def cardinal_neighbour(self, row, column, direction: Direction) -> int:
        match direction:
            case Direction.N:
                index = self.index(row - 1, column)
                if row > 0 and self.check(index):
                    return index
            case Direction.E:
                index = self.index(row, column + 1)
                if column < self.columns - 1 and self.check(index):
                    return index
            case Direction.S:
                index = self.index(row + 1, column)
                if row < self.rows - 1 and self.check(index):
                    return index
            case Direction.W:
                index = self.index(row, column - 1)
                if column > 0 and self.check(index):
                    return index

    def check(self, index: int) -> bool:
        return self.elements[index].check()
