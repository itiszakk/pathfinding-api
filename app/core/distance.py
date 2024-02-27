"""
Distance module
"""

import math
from enum import StrEnum

from app.core.vector import Vector2D


def manhattan(p0: Vector2D, p1: Vector2D):
    """
    Calculates the Manhattan distance between two points
    :param p0: the first point
    :param p1: the second point
    :return: the Manhattan distance between two points
    """

    return abs(p0.x - p1.x) + abs(p0.y - p1.y)


def euclidian(p0: Vector2D, p1: Vector2D):
    """
    Calculates the Euclidian distance between two points
    :param p0: the first point
    :param p1: the second point
    :return: the Euclidian distance between two points
    """

    return math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)


class Distance(StrEnum):
    """
    Enumerates distance calculation methods
    """

    MANHATTAN = 'manhattan'
    EUCLIDIAN = 'euclidian'

    def calculate(self, p0: Vector2D, p1: Vector2D) -> float | None:
        """
        Calculates the distance between two points based on the selected method
        :param p0: the first point
        :param p1: the second point
        :return: the distance between the two points
        """
        if self is Distance.MANHATTAN:
            return manhattan(p0, p1)

        if self is Distance.EUCLIDIAN:
            return euclidian(p0, p1)

        return None
