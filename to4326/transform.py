import math
from functools import reduce
from typing import Sequence
from pyproj import CRS, Transformer
from .types import *
from .calc import *
from .lonlat import *
from . import validate

EPSG4326 = CRS.from_epsg(4326)


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


class FalidCuttingAntimeridian(Exception):
    def __str__(self):
        return "falid cutting antimeridian."


def _is_ccw(linear_ring: Points):
    area = 0.0
    if len(linear_ring) > 2:
        if (
            linear_ring[0][0] == linear_ring[-1][0]
            and linear_ring[0][1] == linear_ring[-1][1]
        ):
            length = len(linear_ring) - 1
        else:
            length = len(linear_ring)

        for i in range(length - 1):
            area = (
                area
                + linear_ring[i][0] * linear_ring[i + 1][1]
                - linear_ring[i][1] * linear_ring[i + 1][0]
            )

        area = (
            area
            + linear_ring[length - 1][0] * linear_ring[0][1]
            - linear_ring[length - 1][1] * linear_ring[0][0]
        )

    return area >= 0


def _within(point: Point, linear_ring: Points, on_edge: bool = False):
    """
    Winding Number Algorithm
    """
    theta: float = 0
    for i in range(len(linear_ring)):
        x1, y1 = linear_ring[i - 1]
        x2, y2 = linear_ring[i]
        x1 -= point[0]
        y1 -= point[1]
        x2 -= point[0]
        y2 -= point[1]

        cv = x1 * x2 + y1 * y2
        sv = x1 * y2 - x2 * y1
        if sv == 0 and cv <= 0:
            return on_edge

        theta += math.atan2(sv, cv)
    return abs(theta) > 1


def _transform(points: Points, src_crs: CRS, dst_crs: CRS):
    if src_crs == dst_crs:
        return points
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)

    return [list(transformer.transform(*p)) for p in points]


def transform_ring(linear_ring: Points, src_crs: CRS, partition: int = 0):
    """
    not support linear rings of including the pole.
    """
    validate.linear_ring(linear_ring)
    length = len(linear_ring) - 1

    north_pole = _transform([[0, 90]], EPSG4326, src_crs)[0]
    if _within(north_pole, linear_ring):
        raise IncludingPole
    south_pole = _transform([[0, -90]], EPSG4326, src_crs)[0]
    if _within(south_pole, linear_ring):
        raise IncludingPole

    interpolated_linear_ring = []
    for i in range(length - 1):
        interpolated_linear_ring.extend(
            linear_interpolate(linear_ring[i], linear_ring[i + 1], partition)[:-1]
        )
    interpolated_linear_ring.extend(
        linear_interpolate(linear_ring[length - 1], linear_ring[0], partition)
    )

    if src_crs == EPSG4326:
        return interpolated_linear_ring

    return _transform(interpolated_linear_ring, src_crs, EPSG4326)


def transform_bbox(
    src_bbox: Sequence[float], src_crs: CRS, partition: int = 9, expand: bool = False
):
    """
    input bbox is not allowed warp.
    """
    if not (len(src_bbox) == 4 or len(src_bbox) == 6):
        raise InvalidBounds

    has_height = len(src_bbox) == 6
    left = src_bbox[0]
    bottom = src_bbox[1]
    right = src_bbox[3] if has_height else src_bbox[2]
    top = src_bbox[4] if has_height else src_bbox[3]

    if right < left:
        raise NotAllowedWarpBounds

    points = transform_ring(
        [[left, bottom], [right, bottom], [right, top], [left, top], [left, bottom]],
        src_crs,
        partition=partition,
    )

    ys = [p[1] for p in points]
    if _is_ccw(points):
        xs = [p[0] for p in points]
        if len(src_bbox) == 6:
            return [min(xs), min(ys), src_bbox[2], max(xs), max(ys), src_bbox[5]]
        return [min(xs), min(ys), max(xs), max(ys)]

    try:
        bounds_ring = cut_ring_at_antimeridian(points)
        xs1 = [p[0] for p in reduce(lambda a, b: a + b, bounds_ring.within)]
        xs2 = [p[0] for p in reduce(lambda a, b: a + b, bounds_ring.overflow)]
        if len(src_bbox) == 6:
            return [
                min(xs1),
                min(ys),
                src_bbox[2],
                max(xs2) + 360 if expand else max(xs2),
                max(ys),
                src_bbox[5],
            ]
        return [min(xs1), min(ys), max(xs2) + 360 if expand else max(xs2), max(ys)]
    except:
        raise FalidCuttingAntimeridian


def geojson_from_linear_ring(linear_ring: Points, src_crs: CRS, partition: int = 9):
    if not _is_ccw(linear_ring):
        raise NotAllowedCwLinearRing
    points = transform_ring(linear_ring, src_crs, partition=partition)
    ys = [p[1] for p in points]

    if _is_ccw(points):
        xs = [p[0] for p in points]
        return {
            "type": "Feature",
            "bbox": [min(xs), min(ys), max(xs), max(ys)],
            "geometry": {"type": "Polygon", "coordinates": [points]},
        }

    try:
        ring = cut_ring_at_antimeridian(points)
        xs1 = [p[0] for p in reduce(lambda a, b: a + b, ring.within)]
        xs2 = [p[0] for p in reduce(lambda a, b: a + b, ring.overflow)]
        coordinates = []
        coordinates.extend([[r] for r in ring.within])
        coordinates.extend([[r] for r in ring.overflow])
        return {
            "type": "Feature",
            "bbox": [min(xs1), min(ys), max(xs2), max(ys)],
            "geometry": {"type": "MultiPolygon", "coordinates": coordinates},
        }

    except:
        raise FalidCuttingAntimeridian


def geojson_from_corner_coordinates(
    upper_left: Point,
    lower_left: Point,
    upper_right: Point,
    lower_right: Point,
    src_crs: CRS,
    partition: int = 9,
):
    return geojson_from_linear_ring(
        [upper_left, lower_left, lower_right, upper_right, upper_left],
        src_crs,
        partition=partition,
    )
