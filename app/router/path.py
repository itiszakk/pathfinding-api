from fastapi import APIRouter, UploadFile, Query
from starlette.responses import StreamingResponse

from app.context import WorldRequest, PathfinderRequest, ContextBuilder, Context
from app.core.movement import Movement
from app.core.trajectory import Trajectory
from app.exception import PathfinderNotSupportedException
from app.pathfinder import utils as pathfinder_utils
from app.world import utils as world_utils
from app.world.world_image import WorldImage

router = APIRouter()

SUPPORTED_PATHFINDERS = {
    WorldRequest.Grid: [PathfinderRequest.AStar, PathfinderRequest.JPS],
    WorldRequest.QTree: [PathfinderRequest.AStar]
}


@router.post(path='/image',
             summary='Create path image',
             tags=['path'])
def get_path_image(file: UploadFile,
                   world: WorldRequest,
                   pathfinder: PathfinderRequest,
                   movement: Movement,
                   trajectory: Trajectory,
                   cell: int = 50,
                   border: int = 1,
                   trajectory_size: int = 5,
                   point: int = 10,
                   start: tuple[int, int] = Query((0, 0)),
                   end: tuple[int, int] = Query((0, 0))):
    context = (ContextBuilder()
               .file(file)
               .world(world)
               .pathfinder(pathfinder)
               .movement(movement)
               .trajectory(trajectory)
               .trajectory_size(trajectory_size)
               .cell_size(cell)
               .border_size(border)
               .point_size(point)
               .start(start)
               .end(end)
               .build())
    check_context(context)

    world = world_utils.build_world(context)

    tracer = pathfinder_utils.build_tracer(world, context)
    tracer.info()

    image = WorldImage(world, context, tracer)

    return StreamingResponse(image.stream(), media_type='image/png')


def check_context(context: Context):
    check_pathfinder(context)


def check_pathfinder(context: Context):
    if context.pathfinder not in SUPPORTED_PATHFINDERS[context.world]:
        raise PathfinderNotSupportedException(context.world, context.pathfinder)
