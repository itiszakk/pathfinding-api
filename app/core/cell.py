"""
Cell module
"""

from __future__ import annotations

from enum import Enum

import numpy

from app.core.color import Color
from app.core.vector import Vector2D


class CellState(Enum):
    """
    Enumerates the possible states of a cell
    """

    def __init__(self, index, color):
        super().__init__()
        self.index = index
        self.color = color

    SAFE = 0, Color.SAFE
    MIXED = 1, Color.MIXED
    UNSAFE = 2, Color.UNSAFE

    @staticmethod
    def of(pixels: numpy.ndarray) -> CellState:
        """
        Determines cell state by pixels slice
        :param pixels: pixels slice
        :return: cell state
        """

        any_safe = numpy.any(pixels == Color.SAFE)
        any_unsafe = numpy.any(pixels == Color.UNSAFE)

        if any_safe and not any_unsafe:
            return CellState.SAFE
        elif not any_safe and any_unsafe:
            return CellState.UNSAFE
        return CellState.MIXED


class Cell:
    """
    Represents a single cell.
    """

    def __init__(self, pixels: numpy.ndarray, position: Vector2D, width, height):
        """
        Initializes a cell with given parameters
        :param pixels: image pixels
        :param position: cell position
        :param width: cell width
        :param height: cell height
        """

        self.position = position
        self.w = width
        self.h = height
        self.state = CellState.of(
            pixels[self.position.y:self.position.y + self.h, self.position.x:self.position.x + self.w])

    def contains(self, point: Vector2D) -> bool:
        """
        Check if a point is contained within the cell
        :param point: the point to check
        :return: True if contained, False otherwise
        """

        x_contains = self.position.x <= point.x < self.position.x + self.w
        y_contains = self.position.y <= point.y < self.position.y + self.h
        return x_contains and y_contains

    def center(self) -> Vector2D:
        """
        Calculates the center point of the cell
        :return: the center point of the cell
        """

        return Vector2D(self.position.x + self.w // 2, self.position.y + self.h // 2)

    def safe(self) -> bool:
        """
        Checks if the cell is safe
        :return: True if safe, False otherwise
        """

        return self.state == CellState.SAFE

    def unsafe(self) -> bool:
        """
        Checks if the cell is unsafe
        :return: True if unsafe, False otherwise
        """

        return not self.safe()

    def __repr__(self) -> str:
        """
        Returns a string representation of the cell
        :return: string representation of the cell
        """

        return f'Cell(state={self.state}, position=({self.position}), w={self.w}, h={self.h})'
