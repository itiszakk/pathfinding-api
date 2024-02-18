import math
from enum import StrEnum

from app.core.vector import Vector2D


def manhattan(p0: Vector2D, p1: Vector2D):
    return abs(p0.x - p1.x) + abs(p0.y - p1.y)


def euclidian(p0: Vector2D, p1: Vector2D):
    return math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)


class Distance(StrEnum):
    Euclidian = 'euclidian'
    Manhattan = 'manhattan'

    def calculate(self, p0: Vector2D, p1: Vector2D):
        if self is Distance.Manhattan:
            return manhattan(p0, p1)
        elif self is Distance.Euclidian:
            return euclidian(p0, p1)
