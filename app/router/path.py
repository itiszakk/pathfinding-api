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
    check_points(context)
    check_pathfinder(context)


def check_pathfinder(context: Context):
    if context.pathfinder not in SUPPORTED_PATHFINDERS[context.world]:
        raise PathfinderNotSupportWorldException(context.world, context.pathfinder)


def check_points(context: Context):
    if context.start == context.end:
        raise PathPointsAreEqualException()
