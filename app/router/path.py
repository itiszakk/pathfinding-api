"""
Path API module
"""

from fastapi import APIRouter, UploadFile, Query
from starlette.responses import StreamingResponse

from app.context import WorldRequest, PathfinderRequest, Context, PathfinderContext, WorldContext
from app.core.distance import Distance
from app.core.trajectory import Trajectory
from app.exception import PathfinderNotSupportWorldException, PathPointsAreEqualException
from app.pathfinder import utils as pathfinder_utils
from app.world import utils as world_utils
from app.world.world_image import WorldImage

router = APIRouter()

SUPPORTED_PATHFINDERS = {
    WorldRequest.GRID: [PathfinderRequest.ASTAR, PathfinderRequest.JPS],
    WorldRequest.QTREE: [PathfinderRequest.ASTAR]
}

DEFAULT_START = Query((0, 0))
DEFAULT_END = Query((0, 0))


@router.post(path='/image',
             summary='Create path image',
             tags=['path'])
def get_path_image(file: UploadFile,
                   world: WorldRequest,
                   pathfinder: PathfinderRequest,
                   distance: Distance,
                   trajectory: Trajectory,
                   cell: int = 50,
                   border: int = 1,
                   trajectory_size: int = 5,
                   point: int = 10,
                   start: tuple[int, int] = DEFAULT_START,
                   end: tuple[int, int] = DEFAULT_END):
    """
    Endpoint to create a path image based on the provided parameters
    :param file: uploaded file containing the world map
    :param world: type of world representation
    :param pathfinder: type of pathfinding algorithm
    :param distance: distance calculation method
    :param trajectory: trajectory type for path visualization
    :param cell: size of cells in the grid (default: 50)
    :param border: size of border between cells (default: 1)
    :param trajectory_size: size of trajectory (default: 5)
    :param point: size of path points (default: 10)
    :param start: starting point coordinates (default: (0, 0))
    :param end: ending point coordinates (default: (0, 0))
    :return: StreamingResponse with the generated path image
    """

    world_context = WorldContext(file, world, cell, border)
    pathfinder_context = PathfinderContext(distance, pathfinder, trajectory, trajectory_size, point, start, end)
    context = Context(world_context, pathfinder_context)
    check_context(context)

    world = world_utils.build_world(context.world_context)
    tracer_info = pathfinder_utils.build_trace_info(world, context.pathfinder_context)

    image = WorldImage(world, context, tracer_info)

    return StreamingResponse(image.stream(), media_type='image/png')


def check_context(context: Context):
    """
    Checks if the provided context is valid
    :param context: the context object containing pathfinding settings
    """

    check_points(context)
    check_pathfinder(context)


def check_pathfinder(context: Context):
    """
    Checks if the selected pathfinder is supported for the given world type
    :param context: the context object containing pathfinding settings
    :raises PathfinderNotSupportWorldException: if selected pathfinder is not supported for the world type
    """

    world = context.world_context.world
    pathfinder = context.pathfinder_context.pathfinder

    if pathfinder not in SUPPORTED_PATHFINDERS[world]:
        raise PathfinderNotSupportWorldException(world, pathfinder)


def check_points(context: Context):
    """
    Checks if start and end points are equal
    :param context: the context object containing pathfinding settings
    :raises PathPointsAreEqualException: if start and end points are equal
    """

    start = context.pathfinder_context.start
    end = context.pathfinder_context.end

    if start == end:
        raise PathPointsAreEqualException()
