import math

from app.core.point import Point


class Distance:

    @staticmethod
    def euclidian(p0: Point, p1: Point):
        return math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)

    @staticmethod
    def manhattan(p0: Point, p1: Point):
        return abs(p0.x - p1.x) + abs(p0.y - p1.y)
