from __future__ import annotations

from enum import Enum


class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    NW = 4
    NE = 5
    SW = 6
    SE = 7

    def is_diagonal(self) -> bool:
        return self in [Direction.NW, Direction.NE, Direction.SW, Direction.SE]

    def opposite(self):
        if self is Direction.N:
            return Direction.S

        if self is Direction.E:
            return Direction.W

        if self is Direction.S:
            return Direction.N

        if self is Direction.W:
            return Direction.E

        if self is Direction.NW:
            return Direction.SE

        if self is Direction.NE:
            return Direction.SW

        if self is Direction.SW:
            return Direction.NE

        if self is Direction.SE:
            return Direction.NW
