from itertools import pairwise

from shapely import geometry

from app.core.cell import Cell
from app.core.point import Point
from app.core.timing import timing
from app.core.trajectory import Trajectory
from app.world.world_element import WorldElement


def line_intersection(a, b) -> Point | None:
    a = geometry.LineString(a)
    b = geometry.LineString(b)

    if not a.intersects(b):
        return None

    intersection = a.intersection(b)
    return Point(round(intersection.x), round(intersection.y))


class TracerInfo:
    def __init__(self, visited: list[Cell], path: list[Cell], points: list[Point]):
        self.visited = visited
        self.path = path
        self.points = points


class Tracer:
    def __init__(self, start: WorldElement, start_point: Point, end: WorldElement, end_point: Point,
                 trajectory: Trajectory):
        self.start = start
        self.start_point = start_point
        self.end = end
        self.end_point = end_point
        self.trajectory = trajectory

    @timing('Tracing')
    def backtrace(self, visited: dict[WorldElement, WorldElement]) -> TracerInfo:
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

        if self.trajectory is Trajectory.Smooth:
            points = self.smooth_points(path_cells, points)

        return TracerInfo(visited_cells, path_cells, points)

    def smooth_points(self, path_cells, points):
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
