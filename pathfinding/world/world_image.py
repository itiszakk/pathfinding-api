"""
World visualisation module
"""

from __future__ import annotations

from io import BytesIO
from itertools import pairwise

from PIL import Image, ImageDraw

from pathfinding.context import Context
from pathfinding.core.cell import Cell
from pathfinding.core.color import Color
from pathfinding.core.timing import timing
from pathfinding.core.vector import Vector2D
from pathfinding.pathfinder.tracer import TracerInfo
from pathfinding.world.world import World


class WorldImage:
    """
    A class for generating images representing worlds with optional trajectory visualization
    """

    MODE = 'RGB'
    FORMAT = 'png'

    def __init__(self, world: World, context: Context, tracer_info: TracerInfo | None = None):
        """
        Initializes a WorldImage object with the provided world, context, and optional tracer information
        :param world: the world to be visualized
        :param context: the context providing information about the visualization
        :param tracer_info: information about the traced path. Defaults to None
        """

        super().__init__()
        self.world = world
        self.context = context
        self.tracer_info = tracer_info

    def stream(self):
        """
        Generates the image stream of the world
        :return: image stream
        """

        image = self.image()

        stream = BytesIO()
        image.save(stream, WorldImage.FORMAT)
        stream.seek(0)

        return stream

    @timing('Image')
    def image(self) -> Image.Image:
        """
        Generates the image of the world
        :return: generated image
        """
        shape = self.world.pixels.shape
        image = Image.new(WorldImage.MODE, (shape[1], shape[0]))
        draw = ImageDraw.Draw(image)

        self.draw_cells(draw)

        if self.tracer_info is not None:
            self.draw_trajectory(draw)
            self.draw_points(draw)

        return image

    def draw_cells(self, draw: ImageDraw.ImageDraw):
        """
        Draws cells representing the world
        :param draw: drawing context
        """

        border_size = self.context.world_context.border_size

        elements = self.world.get_elements()

        for element in elements:
            cell = element.get_cell()
            x0, y0 = cell.position.x, cell.position.y
            x1, y1 = cell.position.x + cell.w - 1, cell.position.y + cell.h - 1
            color = self.get_color(cell)

            draw.rectangle((x0, y0, x1, y1), fill=color, outline=Color.BORDER, width=border_size)

    def get_color(self, cell: Cell):
        """
        Determines the color of a cell based on its state and tracer information
        :param cell: the cell whose color needs to be determined
        :return: RGB color tuple
        """

        if self.tracer_info is None:
            return cell.state.color

        if cell in self.tracer_info.path:
            return Color.PATH

        if cell in self.tracer_info.visited:
            return Color.VISITED

        return cell.state.color

    def draw_trajectory(self, draw: ImageDraw.ImageDraw):
        """
        Draws trajectory on the image
        :param draw: drawing context
        """

        for current_point, next_point in pairwise(self.tracer_info.points):
            self.draw_line(draw, current_point, next_point)

    def draw_points(self, draw: ImageDraw.ImageDraw):
        """
        Draws points on the image
        :param draw: drawing context
        """

        for point in self.tracer_info.points:
            self.draw_point(draw, point)

    def draw_point(self, draw: ImageDraw.ImageDraw, p: Vector2D):
        """
        Draws a single point on the image
        :param draw: drawing context
        :param p: the point to be drawn
        """

        point_size = self.context.pathfinder_context.point_size

        x0, y0 = p.x - point_size, p.y - point_size
        x1, y1 = p.x + point_size, p.y + point_size

        draw.ellipse((x0, y0, x1, y1), fill=Color.POINT)

    def draw_line(self, draw: ImageDraw.ImageDraw, p0: Vector2D, p1: Vector2D):
        """
        Draws a line between two points on the image
        :param draw: drawing context
        :param p0: starting point of the line
        :param p1: ending point of the line
        """

        trajectory_size = self.context.pathfinder_context.trajectory_size
        draw.line((p0.x, p0.y, p1.x, p1.y), fill=Color.TRAJECTORY, width=trajectory_size)
