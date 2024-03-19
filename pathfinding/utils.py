"""
Utilities module
"""

import numpy
from PIL import Image
from fastapi import UploadFile

from pathfinding.context import WorldRequest, PathfinderRequest, WorldContext, PathfinderContext
from pathfinding.core import Vertex, Vector2D
from pathfinding.exception import PathPointIsUnsafeException
from pathfinding.pathfinder import AStar, JPS, Pathfinder
from pathfinding.world import Grid, QTree, World, WorldElement

IMAGE_MODE = 'RGB'

WORLDS = {
    WorldRequest.GRID: Grid,
    WorldRequest.QTREE: QTree
}

PATHFINDERS = {
    PathfinderRequest.ASTAR: AStar,
    PathfinderRequest.JPS: JPS
}

GRAPH_ONLY_SAFE = {
    PathfinderRequest.ASTAR: True,
    PathfinderRequest.JPS: False
}


def upload_image_to_array(upload: UploadFile) -> numpy.ndarray:
    """
    Converts an uploaded image file to a numpy array
    :param upload: the uploaded image file
    :return: numpy array representing the image
    """

    image = Image.open(upload.file).convert(IMAGE_MODE)
    return numpy.array(image)


def build_world(context: WorldContext) -> World:
    """
    Builds a world instance based on the provided context
    :param context: the context containing information about the world
    :return: an instance of the appropriate World subclass
    """

    return WORLDS[context.world](upload_image_to_array(context.file), context.cell_size)


def build_pathfinder(world: World, context: PathfinderContext) -> Pathfinder:
    """
    Builds Pathfinder object based on the given world and context.
    :param world: the world object representing the environment
    :param context: the context object containing pathfinding settings
    :return: TracerInfo object containing tracing information
    """

    start_point = context.start
    start_element = world.get(start_point)
    end_point = context.end
    end_element = world.get(end_point)
    pathfinder = context.pathfinder
    distance = context.distance
    trajectory = context.trajectory

    check_points(start_point, end_point, start_element, end_element)

    return PATHFINDERS[pathfinder](world.graph(GRAPH_ONLY_SAFE[pathfinder]),
                                   distance,
                                   Vertex(start_element),
                                   Vertex(end_element),
                                   start_point,
                                   end_point,
                                   trajectory)


def check_points(start_point: Vector2D, end_point: Vector2D, start: WorldElement, end: WorldElement):
    """
    Checks if start and end points are safe for pathfinding
    :param start_point: the starting point coordinates
    :param end_point: the ending point coordinates
    :param start: the starting world element
    :param end: the ending world element
    :raises PathPointIsUnsafeException: If start or end point is unsafe
    """

    if start.obstacle():
        raise PathPointIsUnsafeException(start_point)

    if end.obstacle():
        raise PathPointIsUnsafeException(end_point)
