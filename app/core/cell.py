from __future__ import annotations

from enum import Enum

import numpy

from app.core.color import Color
from app.core.point import Point


class Cell:
    class State(Enum):
        def __init__(self, index, color):
            super().__init__()
            self.index = index
            self.color = color

        SAFE = 0, Color.SAFE
        MIXED = 1, Color.MIXED
        UNSAFE = 2, Color.UNSAFE

        @staticmethod
        def of(slice: numpy.ndarray) -> Cell.State:
            any_safe = numpy.any(slice == Color.SAFE)
            any_unsafe = numpy.any(slice == Color.UNSAFE)

            if any_safe and not any_unsafe:
                return Cell.State.SAFE
            elif not any_safe and any_unsafe:
                return Cell.State.UNSAFE
            return Cell.State.MIXED

    def __init__(self, pixels: numpy.ndarray, position: Point, width, height):
        self.position = position
        self.w = width
        self.h = height
        self.state = None

        self.init_state(pixels)

    def init_state(self, pixels: numpy.ndarray):
        x0, y0 = self.position.x, self.position.y
        x1, y1 = self.position.x + self.w, self.position.y + self.h
        self.state = Cell.State.of(pixels[y0:y1, x0:x1])

    def contains(self, point: Point) -> bool:
        x_contains = self.position.x <= point.x < self.position.x + self.w
        y_contains = self.position.y <= point.y < self.position.y + self.h
        return x_contains and y_contains

    def center(self) -> Point:
        return Point(self.position.x + self.w // 2, self.position.y + self.h // 2)

    def __repr__(self) -> str:
        return f'Cell(state={self.state}, position=({self.position}), w={self.w}, h={self.h})'
