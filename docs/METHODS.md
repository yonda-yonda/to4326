# Methods
## transform

### geojson_from_corner_coordinates

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| upper_left | [Point](#point) | **REQUIRED.** Source upper left corner. |
| lower_left | [Point](#point) | **REQUIRED.** Source lower left corner. |
| upper_right | [Point](#point) | **REQUIRED.** Source upper right corner. |
| lower_right | [Point](#point) | **REQUIRED.** Source lower right corner. |
| src_crs | string, int, pyproj.CRS | **REQUIRED.** Source CRS. ex: 'EPSG:3097' or 3097 |
| partition | int | Number of cutting each edge. Recommends more than 9. (DEFAULT=9) |

#### return
geojson.

### geojson_from_linear_ring

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| linear_ring | [Points](#points) | **REQUIRED.** Source linear ring. |
| src_crs | string, int, pyproj.CRS | **REQUIRED.** Source CRS. ex: 'EPSG:3097' or 3097 |
| partition | int | Number of cutting each edge. Recommends more than 9. (DEFAULT=9) |

#### return
geojson.


### transform_bbox
#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| src_bbox | list[float] | **REQUIRED.** Source bbox. This list length must be 4 or 6. |
| src_crs | string, int, pyproj.CRS | **REQUIRED.** Source CRS. ex: 'EPSG:3097' or 3097 |
| partition | int | Number of cutting each edge. Recommends more than 9. (DEFAULT=9) |
| expand | bool | If True, return non warped bbox (for example [170, 0, 190, 10]). (DEFAULT=False) |

#### return
transformed bbox.

### transform_ring
#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| linear_ring | [Points](#points) | **REQUIRED.** Source linear ring. |
| src_crs | string, int, pyproj.CRS | **REQUIRED.** Source CRS. ex: 'EPSG:3097' or 3097 |
| partition | int | Number of cutting each edge. (DEFAULT=0) |

#### return
transformed linear ring.

## lonlat

### cut_ring_at_antimeridian
#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| linear_ring | [Points](#points) | **REQUIRED.** Source linear ring. The distance in the longitude between the points must be less than 180deg. |
| overflowing | bool | If True, linear_ring is right side of the antimeridian. (DEFAULT=False) |
| allow_selfintersection | bool | If True, allow self-intersection of linear_ring. (DEFAULT=False) |

#### return
dataclass

| Name | Type | Description |
| ---------- | ---------- | ----------- |
| within | [[Points](#points)] | list of linear ring at left side of the antimeridian. |
| overflow | [[Points](#points)] | list of linear ring at right side of the antimeridian. |


## utils

### is_ccw
judge whether linear ring is counter clock wise.

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| linear_ring | [Points](#points) | **REQUIRED.** linear ring. |

#### return
bool

### within
judge whether point within linear ring.

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| point | [Point](#point) | **REQUIRED.** point. |
| linear_ring | [Points](#points) | **REQUIRED.** linear ring. |
| include_border | bool | If True, judge point on edge of linear_ring as "within". (DEFAULT=False) |

#### return
bool

### intersection
judge whether p1 to p2 intersect with p3 to p4, or points more than 3 are on a line.

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| p1 | [Point](#point) | **REQUIRED.** |
| p2 | [Point](#point) | **REQUIRED.** |
| p3 | [Point](#point) | **REQUIRED.** |
| p4 | [Point](#point) | **REQUIRED.** |

#### return
bool

### selfintersection
judge whether linear ring is self-intersection.

#### props
| Name | Type | Description |
| ---------- | ---------- | ----------- |
| linear_ring | [Points](#points) | **REQUIRED.** linear ring (non warped). |

#### return
bool

# schema
## Point
Coordinate value, list of number(int or float). ex: [x, y]

## Points
list of Point.