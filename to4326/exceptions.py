class InvalidPoint(Exception):
    def __str__(self):
        return "point's dimension must be 2."


class InvalidLinearRing(Exception):
    """invalid linear ring."""


class IncludingPole(Exception):
    """not support points around the poles."""


class InvalidBounds(Exception):
    """invalid bounds."""


class NotAllowedWarpBounds(Exception):
    """not support warpping bounds."""


class NotAllowedCwLinearRing(Exception):
    """not support cw linear ring."""


class InvalidSelfintersection(Exception):
    """invalid Selfintersection."""


class FalidCuttingAntimeridian(Exception):
    """falid cutting antimeridian."""