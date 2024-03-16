"""
Vector module
"""

from collections import namedtuple

BaseVector2D = namedtuple('Vector2D', ['x', 'y'])


class Vector2D(BaseVector2D):
    def __repr__(self):
        return f'(x={self.x}, y={self.y})'
