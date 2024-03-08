"""
Pathfinder utilities module
"""

from pathfinding.context import PathfinderRequest, PathfinderContext
from pathfinding.core.vector import Vector2D
from pathfinding.exception import PathPointIsUnsafeException
from pathfinding.pathfinder.astar import AStar
from pathfinding.pathfinder.jps import JPS
from pathfinding.pathfinder.tracer import TracerInfo
from pathfinding.world.world import World, WorldElement

PATHFINDERS = {
    PathfinderRequest.ASTAR: AStar,
    PathfinderRequest.JPS: JPS
}


def build_trace_info(world: World, context: PathfinderContext) -> TracerInfo:
    """
    Builds TracerInfo object based on the given world and context.
    :param world: the world object representing the environment
    :param context: the context object containing pathfinding settings
    :return: TracerInfo object containing tracing information
    """

    start_point = context.start
    start = world.get(start_point)
    end_point = context.end
    end = world.get(end_point)
    pathfinder = context.pathfinder
    distance = context.distance
    trajectory = context.trajectory

    check_points(start_point, end_point, start, end)

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
