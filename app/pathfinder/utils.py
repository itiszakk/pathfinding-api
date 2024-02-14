from app.context import PathfinderRequest, Context
from app.core.direction import Direction
from app.core.distance import Distance
from app.core.graph import Graph
from app.core.point import Point
from app.core.timing import timing
from app.exception import PathPointIsUnsafeException
from app.pathfinder.astar import AStar
from app.pathfinder.jps import JPS
from app.pathfinder.tracer import TracerInfo
from app.world.world import World, WorldElement

PATHFINDERS = {
    PathfinderRequest.AStar: AStar,
    PathfinderRequest.JPS: JPS
}


@timing("Graph")
def build_graph(world: World, distance: Distance) -> Graph:
    graph = Graph(distance)

    elements = world.get_elements()

    for element in elements:
        for direction in Direction:
            graph.create_edge(element, direction, world.neighbours(element, direction))

    return graph


def build_trace_info(world: World, context: Context) -> TracerInfo:
    start_point = Point(context.start[0], context.start[1])
    start = world.get(start_point)
    end_point = Point(context.end[0], context.end[1])
    end = world.get(end_point)

    check_points(start_point, end_point, start, end)

    graph = build_graph(world, context.distance)

    pathfinder = PATHFINDERS[context.pathfinder](graph, start, end, start_point, end_point, context.trajectory)
    return pathfinder.search()


def check_points(start_point: Point, end_point: Point, start: WorldElement, end: WorldElement):
    if start.unsafe():
        raise PathPointIsUnsafeException(start_point)

    if end.unsafe():
        raise PathPointIsUnsafeException(end_point)
