from itertools import pairwise
from typing import Any

from shapely import geometry

from app.core.cell import Cell
from app.core.distance import Distance
from app.core.point import Point
from app.core.timing import timing
from app.core.trajectory import Trajectory
from app.world.world import World, WorldElement


def line_intersection(a, b) -> Point | None:
    a = geometry.LineString(a)
    b = geometry.LineString(b)

    if not a.intersects(b):
        return None

    intersection = a.intersection(b)
    return Point(round(intersection.x), round(intersection.y))


class Tracer:
    def __init__(self, world: World, start_point: Point, end_point: Point, trajectory: Trajectory):
        self.world = world
        self.start_point = start_point
        self.end_point = end_point
        self.trajectory = trajectory
        self.visited: list[Cell] = []
        self.path: list[Cell] = []
        self.points: list[Point] = []

    @timing('Tracing')
    def trace(self, current: Any, visited: dict[WorldElement, WorldElement]):
        self.build_visited(visited)

        if current not in visited:
            return

        self.build_path(current, visited)
        self.build_points()

    def build_visited(self, visited: dict[WorldElement, WorldElement]):
        for target in visited.keys():
            self.visited.append(target.get_cell())

    def build_path(self, current: WorldElement, visited: dict[WorldElement, WorldElement]):
        while current in visited:
            self.path.append(current.get_cell())
            current = visited[current]

    def build_points(self):
        self.points.append(self.end_point)

        for cell in self.path[1:-1]:
            self.points.append(cell.center())

        self.points.append(self.start_point)

        if self.trajectory == Trajectory.Smooth:
            self.smooth_points()

    def smooth_points(self):
        smooth_points = [self.points[0]]

        for index, trajectory in enumerate(pairwise(self.points)):
            cell = self.path[index]
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

        smooth_points.append(self.points[-1])

        self.points = smooth_points

    def info(self):
        print(f'Path: {len(self.path)}')
        print(f'Visited: {len(self.visited)}')
        print(f'Length: {self.get_path_length()}')

    def get_path_length(self):
        length = 0

        for p0, p1 in pairwise(self.points):
            length += Distance.euclidian(p0, p1)

        return length
