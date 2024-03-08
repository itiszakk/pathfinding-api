"""
Direction module
"""

from __future__ import annotations

from enum import Enum, auto


class DirectionType(Enum):
    """
    Enumerates types of directions
    """
    VERTICAL = auto()
    HORIZONTAL = auto()
    DIAGONAL = auto()


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

        if self is Direction.S:
            return Direction.N

        if self is Direction.W:
            return Direction.E

        if self is Direction.E:
            return Direction.W

        if self is Direction.NW:
            return Direction.SE

        if self is Direction.SE:
            return Direction.NW

        if self is Direction.NE:
            return Direction.SW

        if self is Direction.SW:
            return Direction.NE

        return None

    def get_type(self) -> DirectionType:
        """
        Returns the type of direction
        :return: the type of direction
        """
        if self is Direction.N or self is Direction.S:
            return DirectionType.VERTICAL

        if self is Direction.W or self is Direction.E:
            return DirectionType.HORIZONTAL

        return DirectionType.DIAGONAL

    def is_diagonal(self):
        """
        Checks if the direction is diagonal
        :return: True if diagonal, False otherwise
        """
        return self.get_type() is DirectionType.DIAGONAL

    def is_vertical(self):
        """
        Checks if the direction is vertical
        :return: True if vertical, False otherwise
        """
        return self.get_type() is DirectionType.VERTICAL

    def is_horizontal(self):
        """
        Checks if the direction is horizontal
        :return: True if horizontal, False otherwise
        """
        return self.get_type() is DirectionType.HORIZONTAL
