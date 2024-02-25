from app.context import PathfinderRequest, Context
from app.core.vector import Vector2D
from app.exception import PathPointIsUnsafeException
from app.pathfinder.astar import AStar
from app.pathfinder.jps import JPS
from app.pathfinder.tracer import TracerInfo
from app.world.world import World, WorldElement

PATHFINDERS = {
    PathfinderRequest.AStar: AStar,
    PathfinderRequest.JPS: JPS
}


def build_trace_info(world: World, context: Context) -> TracerInfo:
    start = world.get(context.start)
    end = world.get(context.end)
    pathfinder = context.pathfinder
    distance = context.distance
    trajectory = context.trajectory

    check_points(context.start, context.end, start, end)

    pathfinder = PATHFINDERS[pathfinder](world.graph(), distance, start, end, context.start, context.end, trajectory)
    return pathfinder.search()


def check_points(start_point: Vector2D, end_point: Vector2D, start: WorldElement, end: WorldElement):
    if start.unsafe():
        raise PathPointIsUnsafeException(start_point)

    if end.unsafe():
        raise PathPointIsUnsafeException(end_point)
