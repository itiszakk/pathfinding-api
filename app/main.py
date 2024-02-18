import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import world, path

app = FastAPI()

app.include_router(world.router, prefix='/world')
app.include_router(path.router, prefix='/path')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
