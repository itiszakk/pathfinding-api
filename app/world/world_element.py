from abc import ABC, abstractmethod
from typing import Any

from app.core.cell import Cell


class WorldElement(ABC):
    def __init__(self, entity: Any):
        self.entity = entity

    def safe(self) -> bool:
        return self.get_cell().safe()

    def unsafe(self) -> bool:
        return self.get_cell().unsafe()

    @classmethod
    @abstractmethod
    def get_cell(cls) -> Cell:
        ...
