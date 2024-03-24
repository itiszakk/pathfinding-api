"""
World API module
"""

from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse

from pathfinding.api import WorldRequest, WorldContext, Context, utils
from pathfinding.world import WorldImage

router = APIRouter()


@router.post(path='/image',
             summary='Create world image',
             tags=['world'])
def get_image(file: UploadFile,
              world: WorldRequest,
              cell: int = 50,
              border: int = 1):
    """
    Endpoint to create a world image based on the provided parameters
    :param file: uploaded file containing the world map
    :param world: type of world representation
    :param cell: size of cells in the grid (default: 50)
    :param border: size of border between cells (default: 1)
    :return: StreamingResponse with the generated world image
    """

    world_context = WorldContext(file, world, cell, border)
    world = utils.build_world(world_context)
    image = WorldImage(world, Context(world_context))

    return StreamingResponse(image.stream(), media_type='image/png')
