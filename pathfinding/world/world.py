"""
Base world module
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy

from pathfinding.core import Cell, Graph, Direction, Vertex, Vector2D, timing


class WorldElement(ABC):
    """
    Abstract base class for representing elements in a world
    """

    def __init__(self, entity):
        """
        Initializes a world element with the specified entity.
        :param entity: Any object representing the entity associated with the element
        """

        self.entity = entity

    def obstacle(self):
        """
        Checks if element is obstacle
        :return: True if obstacle, else otherwise
        """
        return self.get_cell().unsafe() or self.get_cell().mixed()

    def get_cell(self) -> Cell | None:
        """
        Abstract method to get the cell associated with the element
        :return: Cell object representing the cell associated with the element
        """
        return None

    def __hash__(self):
        return hash(self.entity)

    def __repr__(self):
        return f'WorldElement(entity={self.entity})'


class World(ABC):
    """
    Abstract base class representing a world
    """

    def __init__(self, pixels: numpy.ndarray, cell_size: int):
        """
        Initializes the world with pixels and cell size
        :param pixels: numpy.ndarray representing the world map
        :param cell_size: size of each cell in the world
        """

        super().__init__()
        self.pixels = pixels
        self.cell_size = cell_size

    @timing('Graph')
    def graph(self, only_safe: bool) -> Graph:
        """
        Generates the graph representation of the world
        :param only_safe: include only safe elements
        :return: Graph object
        """
        graph = Graph()

        elements = self.get_elements()

        for element in elements:
            for direction in Direction:
                destinations = []

                for neighbour in self.neighbours(element, direction):
                    if only_safe and neighbour.obstacle():
                        continue

                    destinations.append(Vertex(neighbour, neighbour.obstacle()))

                graph.add_edge(origin=Vertex(element, element.obstacle()),
                               direction=direction,
                               destinations=destinations)

        return graph

    @abstractmethod
    def get_elements(self) -> list[WorldElement]:
        """
        Abstract method to get all elements in the world
        :return: list of WorldElement objects representing all elements in the world
        """

    @abstractmethod
    def get(self, point: Vector2D) -> WorldElement:
        """
        Abstract method to get a specific element in the world based on coordinates
        :param point: Vector2D representing the coordinates of the element
        :return: WorldElement object representing the element at the specified coordinates
        """

    @abstractmethod
    def neighbours(self, element: WorldElement, direction: Direction) -> list[WorldElement]:
        """
        Abstract method to get the neighbors of a specific element in the world.
        :param element: WorldElement object for which neighbors are to be determined
        :param direction: direction of the neighbors to be determined
        :return: list of WorldElement objects
        representing the neighbors of the specified element in the specified direction
        """
