from fastapi import HTTPException

from app.context import WorldRequest, PathfinderRequest
from app.core.vector import Vector2D


class PathfinderNotSupportWorldException(HTTPException):
    def __init__(self, world: WorldRequest, pathfinder: PathfinderRequest):
        super().__init__(status_code=500, detail=f'Pathfinder \'{pathfinder}\' does not support world \'{world}\'')


class PathPointIsUnsafeException(HTTPException):
    def __init__(self, point: Vector2D):
        super().__init__(status_code=500, detail=f'{point} is unsafe')


class PathPointsAreEqualException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail='Start and end points are equal')
