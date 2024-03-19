import numpy
import pytest

from pathfinding.core.cell import CellState, Color, Vector2D


@pytest.fixture
def safe_pixels():
    return numpy.full((10, 10, 3), Color.SAFE, dtype=numpy.uint8)


@pytest.fixture
def unsafe_pixels():
    return numpy.full((10, 10, 3), Color.UNSAFE, dtype=numpy.uint8)


@pytest.fixture
def mixed_pixels():
    pixels = numpy.full((10, 10, 3), Color.SAFE, dtype=numpy.uint8)
    pixels[0:5, 0:5] = Color.UNSAFE
    return pixels


def test_of_with_all_safe(safe_pixels):
    assert CellState.of(safe_pixels, Vector2D(0, 0), Vector2D(10, 10)) == CellState.SAFE


def test_of_with_all_unsafe(unsafe_pixels):
    assert CellState.of(unsafe_pixels, Vector2D(0, 0), Vector2D(10, 10)) == CellState.UNSAFE


def test_of_with_mixed(mixed_pixels):
    assert CellState.of(mixed_pixels, Vector2D(0, 0), Vector2D(10, 10)) == CellState.MIXED
