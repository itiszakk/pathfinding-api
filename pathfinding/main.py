"""
This module configures and runs the FastAPI application
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pathfinding.router import world, path

APPLICATION_HOST = "localhost"
APPLICATION_PORT = 8080

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


def main():
    """
    Entry point for running the FastAPI application
    """
    uvicorn.run(app, host=APPLICATION_HOST, port=APPLICATION_PORT)


if __name__ == "__main__":
    main()
