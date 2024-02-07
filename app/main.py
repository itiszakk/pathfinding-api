import numpy
import uvicorn
from PIL import Image
from fastapi import FastAPI, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from context import Context, ContextBuilder, WorldRequest, PathfinderRequest
from app.core.movement import Movement
from app.core.point import Point
from app.core.trajectory import Trajectory
from app.pathfinder.astar import AStar
from app.pathfinder.jps import JPS
from app.pathfinder.tracer import Tracer
from app.world.grid import Grid
from app.world.qtree import QTree
from app.world.world import World
from app.world.world_image import WorldImage

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

WORLDS = {
    WorldRequest.Grid: Grid,
    WorldRequest.QTree: QTree
}

PATHFINDERS = {
    PathfinderRequest.AStar: AStar,
    PathfinderRequest.JPS: JPS
}


def upload_image_to_array(upload: UploadFile) -> numpy.ndarray:
    image = Image.open(upload.file).convert('RGB')
    return numpy.array(image)


def build_world(context: Context) -> World:
    pixels = upload_image_to_array(context.file)
    return WORLDS[context.world](pixels, context.cell_size, context.movement)


def build_tracer(world: World, context: Context) -> Tracer:
    start_point = Point(context.start[0], context.start[1])
    end_point = Point(context.end[0], context.end[1])
    start = world.get(start_point)
    end = world.get(end_point)

    pathfinder = PATHFINDERS[context.pathfinder](world, start, end, start_point, end_point)
    visited = pathfinder.search()

    tracer = Tracer(world, start_point, end_point, context.trajectory)
    tracer.trace(end, visited)

    return tracer


@app.post('/preview', summary='Map preview')
def preview(file: UploadFile,
            world: WorldRequest,
            cell_size: int = 50,
            border_size: int = 1):
    context = (ContextBuilder()
               .file(file)
               .world(world)
               .cell_size(cell_size)
               .border_size(border_size)
               .build())
    context.info()

    world = build_world(context)
    image = WorldImage(world, context)

    return StreamingResponse(image.stream(), media_type='image/png')


@app.post('/path', summary='Path')
def path(file: UploadFile,
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
    context.info()

    world = build_world(context)

    tracer = build_tracer(world, context)
    tracer.info()

    image = WorldImage(world, context, tracer)

    return StreamingResponse(image.stream(), media_type='image/png')


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
