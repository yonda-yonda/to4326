class InvalidPoint(Exception):
    def __str__(self):
        return "point's dimension must be 2."


class InvalidLinearRing(Exception):
    def __str__(self):
        return "invalid linear ring."


class IncludingPole(Exception):
    def __str__(self):
        return "not support points around the poles."


class InvalidBounds(Exception):
    def __str__(self):
        return "invalid bounds."


class NotAllowedWarpBounds(Exception):
    def __str__(self):
        return "not support warpping bounds."


class NotAllowedCwLinearRing(Exception):
    def __str__(self):
        return "not support cw linear ring."


class InvalidSelfintersection(Exception):
    def __str__(self):
        return "invalid Selfintersection."


class FalidCuttingAntimeridian(Exception):
    def __str__(self):
        return "falid cutting antimeridian."