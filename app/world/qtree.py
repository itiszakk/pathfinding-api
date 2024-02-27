"""
Quadtree module
"""

from __future__ import annotations

from collections import deque
from enum import IntEnum

import numpy

from app.core.cell import Cell, CellState
from app.core.direction import Direction
from app.core.timing import timing
from app.core.vector import Vector2D
from app.world.world import World, WorldElement


class Position(IntEnum):
    """
    Enumeration representing positions in the quadrants
    """
    NW = 0
    NE = 1
    SW = 2
    SE = 3


class QNode(WorldElement):
    """
    Represents a node in the Quadtree
    """

    def __init__(self, pixels: numpy.ndarray, position: Vector2D, width, height):
        """
        Initializes a QNode with the specified parameters
        :param pixels: the pixel array representing the node
        :param position: the position vector of the node
        :param width: the width of the node
        :param height: the height of the node
        """

        super().__init__(self)
        self.cell = Cell(pixels, position, width, height)
        self.depth = 0
        self.parent: QNode | None = None
        self.children = {}

    def get_cell(self) -> Cell:
        """
        Retrieves the cell associated with the node
        :return: the cell associated with the node
        """

        return self.cell

    def is_leaf(self) -> bool:
        """
        Checks if the node is a leaf node
        :return: True if leaf node, False otherwise
        """

        return not self.children

    def get(self, point: Vector2D) -> QNode | None:
        """
        Retrieves the node containing the specified point
        :param point: the point to retrieve the node for
        :return: the node containing the point if found, None otherwise
        """

        if point is None:
            return None

        if self.is_leaf():
            return self

        for node in self.children.values():
            if node.cell.contains(point):
                return node.get(point)

        return None

    def add_child(self, node: QNode, position: Position):
        """
        Adds a child node to the current node
        :param node: The child node to add
        :param position: the position of the child node
        """

        node.depth = self.depth + 1
        node.parent = self
        self.children[position] = node

    def divide(self, pixels: numpy.ndarray, min_size: int):
        """
        Divides the node into quadrants recursively
        :param pixels: the pixel array
        :param min_size: the minimum size for division
        """

        x0, y0 = self.cell.position.x, self.cell.position.y
        w, h = self.cell.w, self.cell.h

        if self.cell.state != CellState.MIXED:
            return

        new_w, new_h = w // 2, h // 2

        if new_w < min_size or new_h < min_size:
            return

        self.add_child(QNode(pixels, Vector2D(x0, y0), new_w, new_h), Position.NW)
        self.add_child(QNode(pixels, Vector2D(x0 + new_w, y0), new_w + w % 2, new_h), Position.NE)
        self.add_child(QNode(pixels, Vector2D(x0, y0 + new_h), new_w, new_h + h % 2), Position.SW)
        self.add_child(QNode(pixels, Vector2D(x0 + new_w, y0 + new_h), new_w + w % 2, new_h + h % 2), Position.SE)

        for child in self.children.values():
            child.divide(pixels, min_size)

    def search(self) -> list[QNode]:
        """
        Performs a depth-first search to retrieve all leaf nodes
        :return: list of all leaf nodes
        """

        if self.is_leaf():
            return [self]

        nodes = []
        for node in self.children.values():
            nodes.extend(node.search())

        return nodes

    def __hash__(self):
        """
        Hashing method for the QNode
        :return: hash value
        """

        return hash(id(self))

    def __repr__(self) -> str:
        """
        String representation of the QNode
        :return: String representation
        """

        return f'QNode(depth={self.depth}, cell={self.cell})'


class QTree(World):
    """
    Represents a Quadtree
    """

    @timing('QTree')
    def __init__(self, pixels, cell_size):
        """
        Initializes a Quadtree with the specified parameters
        :param pixels: the pixel array
        :param cell_size: the minimum size of each cell
        """

        super().__init__(pixels, cell_size)
        self.root = QNode(pixels, Vector2D(0, 0), pixels.shape[1], pixels.shape[0])
        self.build_elements()

    def build_elements(self):
        """
        Builds elements for the Quadtree
        """

        self.root.divide(self.pixels, self.cell_size)

    def get_elements(self) -> list[QNode]:
        """
        Retrieves all leaf nodes in the Quadtree
        :return: list of all leaf nodes
        """

        return self.root.search()

    def get_cells(self) -> list[Cell]:
        """
        Retrieves cells in the Quadtree
        :return: list of all cells
        """

        cells = []
        nodes = self.get_elements()

        for node in nodes:
            cells.append(node.cell)

        return cells

    def get(self, point: Vector2D) -> QNode:
        """
        Retrieves the node containing the specified point
        :param point: the point to retrieve the node for
        :return: the node containing the point
        """

        return self.root.get(point)

    def neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        """
        Retrieves neighboring nodes of the specified node in the given direction
        :param element: the node to find neighbors for
        :param direction: the direction to search for neighbors
        :return: list of neighboring nodes
        """

        if direction.is_diagonal():
            diagonal_neighbour = self.diagonal_neighbour(element, direction)
            return [diagonal_neighbour] if diagonal_neighbour is not None else []

        return self.cardinal_neighbours(element, direction)

    def cardinal_neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        """
        Retrieves cardinal neighbors of the specified node in the given direction
        :param element: the node to find neighbors for
        :param direction: the direction to search for neighbors
        :return: list of cardinal neighbors
        """

        equal_or_greater = self.get_equal_or_greater_neighbour(element, direction)
        candidates = self.get_smaller_neighbours(equal_or_greater, direction)

        neighbours = []

        for candidate in candidates:

            if candidate is not None:
                neighbours.append(candidate)

        return neighbours

    def diagonal_neighbour(self, element: QNode, direction: Direction) -> QNode:
        """
        Retrieves the diagonal neighbor of the specified node in the given direction
        :param element: the node to find the diagonal neighbor for
        :param direction: the direction to search for the diagonal neighbor
        :return: the diagonal neighbor
        """

        point = None

        match direction:
            case Direction.NW:
                point = Vector2D(element.cell.position.x - 1, element.cell.position.y - 1)
            case Direction.NE:
                point = Vector2D(element.cell.position.x + element.cell.w, element.cell.position.y - 1)
            case Direction.SE:
                point = Vector2D(element.cell.position.x + element.cell.w, element.cell.position.y + element.cell.h)
            case Direction.SW:
                point = Vector2D(element.cell.position.x - 1, element.cell.position.y + element.cell.h)

        return self.get(point)

    def get_equal_or_greater_neighbour(self, element: QNode, direction: Direction) -> QNode | None:
        """
        Retrieves the equal or greater neighbor of the specified node in the given direction
        :param element: the node to find the equal or greater neighbor for
        :param direction: the direction to search for the equal or greater neighbor
        :return: the equal or greater neighbor
        """

        if element.parent is None:
            return None

        match direction:
            case Direction.N:
                if element == element.parent.children[Position.SW]:
                    return element.parent.children[Position.NW]

                if element == element.parent.children[Position.SE]:
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

                if element == element.parent.children[Position.SW]:
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

                if element == element.parent.children[Position.NE]:
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

                if element == element.parent.children[Position.SE]:
                    return element.parent.children[Position.SW]

                next_element = self.get_equal_or_greater_neighbour(element.parent, direction)

                if next_element is None or next_element.is_leaf():
                    return next_element

                if element == element.parent.children[Position.NW]:
                    return next_element.children[Position.NE]

                return next_element.children[Position.SE]

    def get_smaller_neighbours(self, element: QNode, direction: Direction) -> list[QNode]:
        """
        Retrieves smaller neighbors of the specified node in the given direction
        :param element: the node to find neighbors for
        :param direction: the direction to search for neighbors
        :return: list of smaller neighbors
        """

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
