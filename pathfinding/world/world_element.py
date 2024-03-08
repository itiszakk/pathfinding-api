"""
World element module
"""

from abc import ABC, abstractmethod
from typing import Any

from pathfinding.core.cell import Cell


class WorldElement(ABC):
    """
    Abstract base class for representing elements in a world
    """

    def __init__(self, entity: Any):
        """
        Initializes a world element with the specified entity.
        :param entity: Any object representing the entity associated with the element
        """

        self.entity = entity

    def safe(self) -> bool:
        """
        Checks if the element is safe
        :return: True if safe, False otherwise
        """
        return self.get_cell().safe()

    def unsafe(self) -> bool:
        """
        Checks if the element is unsafe
        :return: True if unsafe, False otherwise
        """
        return self.get_cell().unsafe()

    @abstractmethod
    def get_cell(self) -> Cell:
        """
        Abstract method to get the cell associated with the element
        :return: Cell object representing the cell associated with the element
        """
