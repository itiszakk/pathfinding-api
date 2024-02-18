from app.core.direction import Direction
from app.world.world_element import WorldElement


def direction(current: WorldElement, parent: WorldElement):
    cx, cy = current.get_cell().center()
    px, py = parent.get_cell().center()

    dx = cx - px
    dy = cy - py

    if dx != 0 and dy != 0:
        if dx > 0:
            return Direction.SE if dy > 0 else Direction.NE
        else:
            return Direction.SW if dy > 0 else Direction.NW
    else:
        if dx != 0:
            return Direction.E if dx > 0 else Direction.W
        elif dy != 0:
            return Direction.S if dy > 0 else Direction.N
