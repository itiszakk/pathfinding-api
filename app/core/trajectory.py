"""
Trajectory module
"""

from enum import StrEnum


class Trajectory(StrEnum):
    """
    Enumerate types of trajectory
    """

    SHARP = 'sharp'
    SMOOTH = 'smooth'
