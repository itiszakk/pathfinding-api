from app.context import PathfinderRequest, Context
from app.core.point import Point
from app.exception import PathPointIsUnsafeException
from app.pathfinder.astar import AStar
from app.pathfinder.jps import JPS
from app.pathfinder.tracer import Tracer
from app.world.world import World, WorldElement

PATHFINDERS = {
    PathfinderRequest.AStar: AStar,
    PathfinderRequest.JPS: JPS
}


def build_tracer(world: World, context: Context) -> Tracer:
    start_point = Point(context.start[0], context.start[1])
    end_point = Point(context.end[0], context.end[1])
    start = world.get(start_point)
    end = world.get(end_point)

    check_points(start_point, end_point, start, end)

    pathfinder = PATHFINDERS[context.pathfinder](world, start, end, start_point, end_point)
    visited = pathfinder.search()

    tracer = Tracer(world, start_point, end_point, context.trajectory)
    tracer.trace(end, visited)

    return tracer


def check_points(start_point: Point, end_point: Point, start: WorldElement, end: WorldElement):
    if start.unsafe():
        raise PathPointIsUnsafeException(start_point)

    if end.unsafe():
        raise PathPointIsUnsafeException(end_point)
