"""
Pathfinder utilities module
"""

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
    """
    Builds TracerInfo object based on the given world and context.
    :param world: the world object representing the environment
    :param context: the context object containing pathfinding settings
    :return: TracerInfo object containing tracing information
    """

    start = world.get(context.start)
    end = world.get(context.end)
    pathfinder = context.pathfinder
    distance = context.distance
    trajectory = context.trajectory

    check_points(context.start, context.end, start, end)

    pathfinder = PATHFINDERS[pathfinder](world.graph(), distance, start, end, context.start, context.end, trajectory)
    return pathfinder.search()


def check_points(start_point: Vector2D, end_point: Vector2D, start: WorldElement, end: WorldElement):
    """
    Checks if start and end points are safe for pathfinding
    :param start_point: the starting point coordinates
    :param end_point: the ending point coordinates
    :param start: the starting world element
    :param end: the ending world element
    :raises PathPointIsUnsafeException: If start or end point is unsafe
    """

    if start.unsafe():
        raise PathPointIsUnsafeException(start_point)

    if end.unsafe():
        raise PathPointIsUnsafeException(end_point)
