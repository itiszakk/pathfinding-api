"""
Direction module
"""

from __future__ import annotations

from enum import Enum, auto


class DirectionType(Enum):
    """
    Enumerates types of directions
    """
    Vertical = auto()
    Horizontal = auto()
    Diagonal = auto()


class Direction(Enum):
    """
    Enumerates specific directions
    """

    N = auto()
    E = auto()
    S = auto()
    W = auto()
    NW = auto()
    NE = auto()
    SW = auto()
    SE = auto()

    def opposite(self):
        """
        Returns the opposite direction
        :return: the opposite direction
        """
        if self is Direction.N:
            return Direction.S
        elif self is Direction.S:
            return Direction.N
        elif self is Direction.W:
            return Direction.E
        elif self is Direction.E:
            return Direction.W
        elif self is Direction.NW:
            return Direction.SE
        elif self is Direction.SE:
            return Direction.NW
        elif self is Direction.NE:
            return Direction.SW
        elif self is Direction.SW:
            return Direction.NE

    def get_type(self) -> DirectionType:
        """
        Returns the type of direction
        :return: the type of direction
        """
        if self is Direction.N or self is Direction.S:
            return DirectionType.Vertical
        elif self is Direction.W or self is Direction.E:
            return DirectionType.Horizontal

        return DirectionType.Diagonal

    def is_diagonal(self):
        """
        Checks if the direction is diagonal
        :return: True if diagonal, False otherwise
        """
        return self.get_type() is DirectionType.Diagonal

    def is_vertical(self):
        """
        Checks if the direction is vertical
        :return: True if vertical, False otherwise
        """
        return self.get_type() is DirectionType.Vertical

    def is_horizontal(self):
        """
        Checks if the direction is horizontal
        :return: True if horizontal, False otherwise
        """
        return self.get_type() is DirectionType.Horizontal
