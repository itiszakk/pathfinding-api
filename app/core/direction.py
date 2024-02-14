from __future__ import annotations

from enum import Enum, auto


class DirectionType(Enum):
    Vertical = auto()
    Horizontal = auto()
    Diagonal = auto()


class Direction(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()
    NW = auto()
    NE = auto()
    SW = auto()
    SE = auto()

    def opposite(self):
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
        if self is Direction.N or self is Direction.S:
            return DirectionType.Vertical
        elif self is Direction.W or self is Direction.E:
            return DirectionType.Horizontal

        return DirectionType.Diagonal

    def is_diagonal(self):
        return self.get_type() is DirectionType.Diagonal

    def is_vertical(self):
        return self.get_type() is DirectionType.Vertical

    def is_horizontal(self):
        return self.get_type() is DirectionType.Horizontal
