"""
Tracer module
"""

from itertools import pairwise

from shapely import geometry

from pathfinding.core.cell import Cell
from pathfinding.core.timing import timing
from pathfinding.core.trajectory import Trajectory
from pathfinding.core.vector import Vector2D
from pathfinding.world.world_element import WorldElement


def line_intersection(a, b) -> Vector2D | None:
    """
    Calculates the intersection point between two lines
    :param a: the first line
    :param b: the second line
    :return: Intersection point if exists, None otherwise
    """
    a = geometry.LineString(a)
    b = geometry.LineString(b)

    if not a.intersects(b):
        return None

    intersection = a.intersection(b)
    return Vector2D(round(intersection.x), round(intersection.y))


class TracerInfo:
    """
    Encapsulates tracer information
    """

    def __init__(self, visited: list[Cell], path: list[Cell], points: list[Vector2D]):
        """
        Initializes TracerInfo object
        :param visited: list of visited cells during tracing
        :param path: list of cells representing the path
        :param points: list of points representing the path
        """

        self.visited = visited
        self.path = path
        self.points = points

        print(f'Visited: {len(visited)}')
        print(f'Path: {len(path)}')


class Tracer:
    """
    Class to trace back the path from end to start.
    """

    def __init__(self, start: WorldElement, start_point: Vector2D, end: WorldElement, end_point: Vector2D,
                 trajectory: Trajectory):
        """
        Initializes Tracer object
        :param start: the starting world element
        :param start_point: the starting point coordinates
        :param end: the ending world element
        :param end_point: the ending point coordinates
        :param trajectory: the trajectory type for pathfinding visualization
        """

        self.start = start
        self.start_point = start_point
        self.end = end
        self.end_point = end_point
        self.trajectory = trajectory

    @timing('Tracing')
    def backtrace(self, visited: dict[WorldElement, WorldElement]) -> TracerInfo:
        """
        Traces back the path from end to start based on visited nodes
        :param visited: Dictionary representing visited nodes during pathfinding
        :return: TracerInfo object encapsulating tracing information
        """

        visited_cells = [v.get_cell() for v in visited.keys()]
        path_cells = []
        points = []

        current = self.end

        while current in visited:
            path_cells.append(current.get_cell())
            current = visited[current]

        points.append(self.end_point)

        for cell in path_cells[1:-1]:
            points.append(cell.center())

        points.append(self.start_point)

        if self.trajectory is Trajectory.SMOOTH:
            points = self.smooth_points(path_cells, points)

        return TracerInfo(visited_cells, path_cells, points)

    def smooth_points(self, path_cells: list[Cell], points: list[Vector2D]):
        """
        Smoothes the path by adjusting points to reduce sharp turns
        :param path_cells: list of cells representing the path
        :param points: list of points representing the path
        :return: smoothed list of points
        """

        smooth_points = [self.end_point]

        for index, trajectory in enumerate(pairwise(points)):
            cell = path_cells[index]
            position, w, h = cell.position, cell.w, cell.h

            trajectory = ((trajectory[0].x, trajectory[0].y), (trajectory[1].x, trajectory[1].y))

            n_line = ((position.x, position.y),
                      (position.x + w - 1, position.y))

            e_line = ((position.x + w - 1, position.y),
                      (position.x + w - 1, position.y + h - 1))

            s_line = ((position.x, position.y + h - 1),
                      (position.x + w - 1, position.y + h - 1))

            w_line = ((position.x, position.y),
                      (position.x, position.y + h - 1))

            cell_segments = [n_line, e_line, s_line, w_line]

            for cell_segment in cell_segments:
                intersection = line_intersection(trajectory, cell_segment)

                if intersection is not None:
                    smooth_points.append(intersection)
                    break

        smooth_points.append(self.start_point)

        return smooth_points
