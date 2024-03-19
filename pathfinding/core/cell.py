"""
Cell module
"""

from __future__ import annotations

from enum import Enum

import numpy

from pathfinding.core import Color, Vector2D


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
    def of(pixels: numpy.ndarray, position: Vector2D, size: Vector2D) -> CellState:
        """
        Determines cell state by parameters
        :param pixels: image pixels
        :param position: start position
        :param size: cell size
        :return: cell state
        """

        pixels_slice = pixels[position.y:position.y + size.y, position.x:position.x + size.x]
        unsafe_pixels = numpy.count_nonzero(numpy.all(pixels_slice == Color.UNSAFE, axis=2))

        if unsafe_pixels == pixels_slice.shape[0] * pixels_slice.shape[1]:
            return CellState.UNSAFE
        elif unsafe_pixels == 0:
            return CellState.SAFE

        return CellState.MIXED


class Cell:
    """
    Represents a single cell.
    """

    def __init__(self, position: Vector2D, width: int, height: int, state: CellState = CellState.SAFE):
        """
        Initializes a cell with given parameters
        :param position: cell position
        :param width: cell width
        :param height: cell height
        :param state: cell state
        """

        self.position = position
        self.w = width
        self.h = height
        self.state = state

    def contains(self, point: Vector2D) -> bool:
        """
        Check if a point is contained within the cell
        :param point: the point to check
        :return: True if contained, False otherwise
        """

        x_contains = self.position.x <= point.x <= self.position.x + self.w
        y_contains = self.position.y <= point.y <= self.position.y + self.h
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

        return self.state == CellState.UNSAFE

    def mixed(self) -> bool:
        """
        Checks if the cell is mixed
        :return: True if mixed, False otherwise
        """

        return self.state == CellState.MIXED

    def __repr__(self) -> str:
        """
        Returns a string representation of the cell
        :return: string representation of the cell
        """

        return f'Cell(state={self.state}, position={self.position}, w={self.w}, h={self.h})'
