"""
This module defines custom HTTP exceptions
"""

from fastapi import HTTPException

from app.context import WorldRequest, PathfinderRequest
from app.core.vector import Vector2D


class PathfinderNotSupportWorldException(HTTPException):
    """
    Exception raised when a pathfinder does not support a particular world type
    """

    def __init__(self, world: WorldRequest, pathfinder: PathfinderRequest):
        """
        Initializes a PathfinderNotSupportWorldException with the given world and pathfinder
        :param world: the unsupported world type
        :param pathfinder: tThe pathfinder algorithm that does not support the world type
        """

        super().__init__(status_code=500, detail=f'Pathfinder \'{pathfinder}\' does not support world \'{world}\'')


class PathPointIsUnsafeException(HTTPException):
    """
    Exception raised when a path point is considered unsafe
    """

    def __init__(self, point: Vector2D):
        """
        Initializes a PathPointIsUnsafeException with the given point
        :param point: the unsafe path point
        """

        super().__init__(status_code=500, detail=f'{point} is unsafe')


class PathPointsAreEqualException(HTTPException):
    """
    Exception raised when the start and end points for pathfinding are equal
    """

    def __init__(self):
        """
        Initializes a PathPointsAreEqualException
        """

        super().__init__(status_code=500, detail='Start and end points are equal')
