from fastapi import HTTPException

from app.context import WorldRequest, PathfinderRequest


class PathfinderNotSupportedException(HTTPException):
    def __init__(self, world: WorldRequest, pathfinder: PathfinderRequest):
        super().__init__(status_code=500, detail=f'Pathfinder \'{pathfinder}\' does not support world \'{world}\'')
