import math
from enum import StrEnum

from app.core.point import Point


def manhattan(p0: Point, p1: Point):
    return abs(p0.x - p1.x) + abs(p0.y - p1.y)


def euclidian(p0: Point, p1: Point):
    return math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)


class Distance(StrEnum):
    Euclidian = 'euclidian'
    Manhattan = 'manhattan'

    def calculate(self, p0: Point, p1: Point):
        if self is Distance.Manhattan:
            return manhattan(p0, p1)
        elif self is Distance.Euclidian:
            return euclidian(p0, p1)
