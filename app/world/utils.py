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
    image = Image.open(upload.file).convert(IMAGE_MODE)
    return numpy.array(image)


def build_world(context: Context) -> World:
    pixels = upload_image_to_array(context.file)
    return WORLDS[context.world](pixels, context.cell_size, context.movement)
