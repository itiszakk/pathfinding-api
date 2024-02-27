"""
World utilities module
"""

import numpy
from PIL import Image
from fastapi import UploadFile

from app.context import Context, WorldRequest
from app.world.grid import Grid
from app.world.qtree import QTree
from app.world.world import World

IMAGE_MODE = 'RGB'

WORLDS = {
    WorldRequest.Grid: Grid,
    WorldRequest.QTree: QTree
}


def upload_image_to_array(upload: UploadFile) -> numpy.ndarray:
    """
    Converts an uploaded image file to a numpy array
    :param upload: the uploaded image file
    :return: numpy array representing the image
    """

    image = Image.open(upload.file).convert(IMAGE_MODE)  # Open and convert the image
    return numpy.array(image)  # Convert the image to a numpy array


def build_world(context: Context) -> World:
    """
    Builds a world instance based on the provided context
    :param context: the context containing information about the world
    :return: an instance of the appropriate World subclass
    """

    return WORLDS[context.world](upload_image_to_array(context.file), context.cell_size)
