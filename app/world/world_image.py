from __future__ import annotations

from io import BytesIO
from itertools import pairwise

from PIL import Image, ImageDraw

from app.context import Context
from app.core.cell import Cell
from app.core.color import Color
from app.core.vector import Vector2D
from app.core.timing import timing
from app.pathfinder.tracer import TracerInfo
from app.world.world import World


class WorldImage:
    MODE = 'RGB'
    FORMAT = 'png'

    def __init__(self, world: World, context: Context, tracer_info: TracerInfo | None = None):
        super().__init__()
        self.world = world
        self.context = context
        self.tracer_info = tracer_info

    def stream(self):
        image = self.image()

        stream = BytesIO()
        image.save(stream, WorldImage.FORMAT)
        stream.seek(0)

        return stream

    @timing('Image')
    def image(self) -> Image.Image:
        shape = self.world.pixels.shape
        image = Image.new(WorldImage.MODE, (shape[1], shape[0]))
        draw = ImageDraw.Draw(image)

        self.draw_cells(draw)

        if self.tracer_info is not None:
            self.draw_trajectory(draw)
            self.draw_points(draw)

        return image

    def draw_cells(self, draw: ImageDraw.ImageDraw):
        elements = self.world.get_elements()

        for element in elements:
            cell = element.get_cell()
            x0, y0 = cell.position.x, cell.position.y
            x1, y1 = cell.position.x + cell.w - 1, cell.position.y + cell.h - 1
            color = self.get_color(cell)

            draw.rectangle((x0, y0, x1, y1), fill=color, outline=Color.BORDER, width=self.context.border_size)

    def get_color(self, cell: Cell):
        if self.tracer_info is None:
            return cell.state.color

        if cell in self.tracer_info.path:
            return Color.PATH

        if cell in self.tracer_info.visited:
            return Color.VISITED

        return cell.state.color

    def draw_trajectory(self, draw: ImageDraw.ImageDraw):
        for current_point, next_point in pairwise(self.tracer_info.points):
            self.draw_line(draw, current_point, next_point)

    def draw_points(self, draw: ImageDraw.ImageDraw):
        for point in self.tracer_info.points:
            self.draw_point(draw, point)

    def draw_point(self, draw: ImageDraw.ImageDraw, p: Vector2D):
        point_size = self.context.point_size

        x0, y0 = p.x - point_size, p.y - point_size
        x1, y1 = p.x + point_size, p.y + point_size

        draw.ellipse((x0, y0, x1, y1), fill=Color.POINT)

    def draw_line(self, draw: ImageDraw.ImageDraw, p0: Vector2D, p1: Vector2D):
        draw.line((p0.x, p0.y, p1.x, p1.y), fill=Color.TRAJECTORY, width=self.context.trajectory_size)
