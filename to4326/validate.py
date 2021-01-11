from .types import *


class InvalidPoint(Exception):
    def __str__(self):
        return "point's dimension must be 2."


class InvalidLinearRing(Exception):
    def __str__(self):
        return "invalid linear ring."


def points(points: Points):
    for p in points:
        if not len(p) == 2:
            raise InvalidPoint


def linear_ring(linear_ring: Points):
    points(linear_ring)
    if (
        len(linear_ring) <= 3
        or not linear_ring[0][0] == linear_ring[-1][0]
        or not linear_ring[0][1] == linear_ring[-1][1]
    ):
        raise InvalidLinearRing