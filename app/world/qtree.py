from __future__ import annotations

from collections import deque
from enum import IntEnum

import numpy

from app.core.cell import Cell
from app.core.direction import Direction
from app.core.point import Point
from app.core.timing import timing
from app.world.world import World, WorldElement


class Position(IntEnum):
    NW = 0
    NE = 1
    SW = 2
    SE = 3


class QNode(WorldElement):
    def __init__(self, pixels: numpy.ndarray, position: Point, width, height):
        super().__init__(self)
        self.cell = Cell(pixels, position, width, height)
        self.depth = 0
        self.parent: QNode | None = None
        self.children = {}

    def get_cell(self) -> Cell:
        return self.cell

    def is_leaf(self) -> bool:
        return not self.children

    def get(self, point: Point) -> QNode | None:
        if point is None:
            return None

        if self.is_leaf():
            return self

        for node in self.children.values():
            if node.cell.contains(point):
                return node.get(point)

    def add_child(self, node: QNode, position: Position):
        node.depth = self.depth + 1
        node.parent = self
        self.children[position] = node

    def divide(self, pixels: numpy.ndarray, min_size: int):
        x0, y0 = self.cell.position.x, self.cell.position.y
        w, h = self.cell.w, self.cell.h

        if self.cell.state != Cell.State.MIXED:
            return

        new_w, new_h = w // 2, h // 2

        if new_w < min_size or new_h < min_size:
            return

        self.add_child(QNode(pixels, Point(x0, y0), new_w, new_h), Position.NW)
        self.add_child(QNode(pixels, Point(x0 + new_w, y0), new_w + w % 2, new_h), Position.NE)
        self.add_child(QNode(pixels, Point(x0, y0 + new_h), new_w, new_h + h % 2), Position.SW)
        self.add_child(QNode(pixels, Point(x0 + new_w, y0 + new_h), new_w + w % 2, new_h + h % 2), Position.SE)

        for child in self.children.values():
            child.divide(pixels, min_size)

    def search(self) -> list[QNode]:
        if self.is_leaf():
            return [self]

        nodes = []
        for node in self.children.values():
            nodes.extend(node.search())

        return nodes

    def __repr__(self) -> str:
        return f'QNode(depth={self.depth}, cell={self.cell})'


class QTree(World):

    @timing('QTree')
    def __init__(self, pixels, cell_size, movement):
        super().__init__(pixels, cell_size, movement)
        self.root = QNode(pixels, Point(0, 0), pixels.shape[1], pixels.shape[0])
        self.build_elements()

    def build_elements(self):
        self.root.divide(self.pixels, self.cell_size)
        self.elements = self.get_elements()

    def get_elements(self) -> list[QNode]:
        return self.root.search()

    def get_cells(self) -> list[Cell]:
        cells = []
        nodes = self.get_elements()

        for node in nodes:
            cells.append(node.cell)

        return cells

    def get(self, point: Point) -> QNode:
        return self.root.get(point)

    def neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        if self.allow_diagonal(direction):
            diagonal_neighbour = self.diagonal_neighbour(element, direction)
            return [diagonal_neighbour] if diagonal_neighbour is not None else []

        return self.cardinal_neighbours(element, direction)

    def cardinal_neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        equal_or_greater = self.get_equal_or_greater_neighbour(element, direction)
        candidates = self.get_smaller_neighbours(equal_or_greater, direction)

        neighbours = []

        for candidate in candidates:

            if candidate is not None:
                neighbours.append(candidate)

        return neighbours

    def diagonal_neighbour(self, element: QNode, direction: Direction) -> QNode:
        point = None

        match direction:
            case Direction.NW:
                point = Point(element.cell.position.x - 1, element.cell.position.y - 1)
            case Direction.NE:
                point = Point(element.cell.position.x + element.cell.w, element.cell.position.y - 1)
            case Direction.SE:
                point = Point(element.cell.position.x + element.cell.w, element.cell.position.y + element.cell.h)
            case Direction.SW:
                point = Point(element.cell.position.x - 1, element.cell.position.y + element.cell.h)

        return self.get(point)

    def get_equal_or_greater_neighbour(self, element: QNode, direction: Direction) -> QNode | None:
        if element.parent is None:
            return None

        match direction:
            case Direction.N:
                if element == element.parent.children[Position.SW]:
                    return element.parent.children[Position.NW]
                elif element == element.parent.children[Position.SE]:
                    return element.parent.children[Position.NE]

                next_element = self.get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[Position.NW]:
                    return next_element.children[Position.SW]

                return next_element.children[Position.SE]

            case Direction.E:
                if element == element.parent.children[Position.NW]:
                    return element.parent.children[Position.NE]
                elif element == element.parent.children[Position.SW]:
                    return element.parent.children[Position.SE]

                next_element = self.get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[Position.NE]:
                    return next_element.children[Position.NW]

                return next_element.children[Position.SW]

            case Direction.S:
                if element == element.parent.children[Position.NW]:
                    return element.parent.children[Position.SW]
                elif element == element.parent.children[Position.NE]:
                    return element.parent.children[Position.SE]

                next_element = self.get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[Position.SW]:
                    return next_element.children[Position.NW]

                return next_element.children[Position.NE]

            case Direction.W:
                if element == element.parent.children[Position.NE]:
                    return element.parent.children[Position.NW]
                elif element == element.parent.children[Position.SE]:
                    return element.parent.children[Position.SW]

                next_element = self.get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[Position.NW]:
                    return next_element.children[Position.NE]

                return next_element.children[Position.SE]

    def get_smaller_neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        neighbours = []
        candidates = deque()

        if element is not None:
            candidates.append(element)

        while candidates:
            candidate = candidates.popleft()

            if candidate.is_leaf():
                neighbours.append(candidate)
                continue

            match direction:
                case Direction.N:
                    candidates.append(candidate.children[Position.SW])
                    candidates.append(candidate.children[Position.SE])
                case Direction.E:
                    candidates.append(candidate.children[Position.NW])
                    candidates.append(candidate.children[Position.SW])
                case Direction.S:
                    candidates.append(candidate.children[Position.NW])
                    candidates.append(candidate.children[Position.NE])
                case Direction.W:
                    candidates.append(candidate.children[Position.NE])
                    candidates.append(candidate.children[Position.SE])

        return neighbours
