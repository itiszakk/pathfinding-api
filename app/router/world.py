from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse

from app.context import WorldRequest, Context
from app.world import utils as world_utils
from app.world.world_image import WorldImage

router = APIRouter()


@router.post(path='/image',
             summary='Create world image',
             tags=['world'])
def get_image(file: UploadFile,
              world: WorldRequest,
              cell: int = 50,
              border: int = 1):
    context = Context(file=file, world=world, cell_size=cell, border_size=border)

    world = world_utils.build_world(context)
    image = WorldImage(world, context)

    return StreamingResponse(image.stream(), media_type='image/png')
