"""
Path API module
"""

from fastapi import APIRouter, UploadFile, Query
from starlette.responses import StreamingResponse

from app.context import WorldRequest, PathfinderRequest, Context
from app.core.distance import Distance
from app.core.trajectory import Trajectory
from app.exception import PathfinderNotSupportWorldException, PathPointsAreEqualException
from app.pathfinder import utils as pathfinder_utils
from app.world import utils as world_utils
from app.world.world_image import WorldImage

router = APIRouter()

SUPPORTED_PATHFINDERS = {
    WorldRequest.Grid: [PathfinderRequest.AStar, PathfinderRequest.JPS],
    WorldRequest.QTree: [PathfinderRequest.AStar]
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

    context = Context(file=file,
                      world=world,
                      pathfinder=pathfinder,
                      distance=distance,
                      trajectory=trajectory,
                      cell_size=cell,
                      border_size=border,
                      trajectory_size=trajectory_size,
                      point_size=point,
                      start=start,
                      end=end)
    check_context(context)

    world = world_utils.build_world(context)

    tracer_info = pathfinder_utils.build_trace_info(world, context)

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

    if context.pathfinder not in SUPPORTED_PATHFINDERS[context.world]:
        raise PathfinderNotSupportWorldException(context.world, context.pathfinder)


def check_points(context: Context):
    """
    Checks if start and end points are equal
    :param context: the context object containing pathfinding settings
    :raises PathPointsAreEqualException: if start and end points are equal
    """

    if context.start == context.end:
        raise PathPointsAreEqualException()
