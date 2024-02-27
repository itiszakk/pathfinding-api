"""
Base world module
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy

from app.core.direction import Direction
from app.core.graph import Graph
from app.core.timing import timing
from app.core.vector import Vector2D
from app.world.world_element import WorldElement


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
    def graph(self) -> Graph:
        """
        Generates the graph representation of the world
        :return: Graph object
        """
        graph = Graph()

        elements = self.get_elements()

        for element in elements:
            for direction in Direction:
                graph.create_edge(element, direction, self.neighbours(element, direction))

        return graph

    @classmethod
    @abstractmethod
    def get_elements(cls) -> list[WorldElement]:
        """
        Abstract method to get all elements in the world
        :return: list of WorldElement objects representing all elements in the world
        """
        ...

    @classmethod
    @abstractmethod
    def get(cls, point: Vector2D) -> WorldElement:
        """
        Abstract method to get a specific element in the world based on coordinates
        :param point: Vector2D representing the coordinates of the element
        :return: WorldElement object representing the element at the specified coordinates
        """
        ...

    @classmethod
    @abstractmethod
    def neighbours(cls, element: WorldElement, direction: Direction) -> list[WorldElement]:
        """
        Abstract method to get the neighbors of a specific element in the world.
        :param element: WorldElement object for which neighbors are to be determined
        :param direction: direction of the neighbors to be determined
        :return: list of WorldElement objects
        representing the neighbors of the specified element in the specified direction
        """
        ...
