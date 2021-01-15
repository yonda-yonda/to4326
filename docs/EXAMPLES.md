# Example
## simple
createt GeoJSON of `Polygon`.

```Python
from to4326 import transform

upper_left = [382200.000, 2512500.000]
lower_left = [382200.000, 2279400.000]
upper_right = [610500.000, 2512500.000]
lower_right = [610500.000, 2279400.000]
src_crs = 32645

transform.geojson_from_corner_coordinates(upper_left, lower_left, upper_right, lower_right, src_crs)
```
**result**
```JSON
{
  "type":"Feature",
  "bbox":[
    85.85296718933647,
    20.610041795245515,
    88.07596179098907,
    22.719775713801845
   ],
  "properties": {},
  "geometry":{
    "type":"Polygon",
    "coordinates":[
      [
        [85.85296718933647, 22.71566587084141],
        [85.85471144948144, 22.505128271679137],
        // ...
        [85.85296718933647,22.71566587084141]
      ]
    ]
  }
}
```

## crossing antimeridian
createt GeoJSON of `MultiPolygon`.

```Python
from to4326 import transform

upper_left = [508800.000, 7247400.000]
lower_left = [508800.000, 7001100.000]
upper_right = [753000.000, 7247400.000]
lower_right = [753000.000, 7001100.000]
src_crs = 32660

transform.geojson_from_linear_ring(
  [upper_left, lower_left, lower_right, upper_right, upper_left], src_crs
)
```
**result**
```JSON
{
  "type":"Feature",
  "bbox":[
    85.85296718933647,
    20.610041795245515,
    88.07596179098907,
    22.719775713801845
  ],
  "properties": {},
  "geometry":{
  "type":"MultiPolygon",
  "coordinates": [
      [
        [
          [180, 65.31939602795103],
          [179.81058927281353, 65.323257946911],
          // ...
          [180, 65.31939602795103]
        ]
      ],
      [
        [
          [-180, 63.107371495051154],
          [-179.92160135394897, 63.105802348825904],
          // ...
          [-180, 63.107371495051154]
        ]
      ]
    ]
   }
}
```


## with rasterio
```Python
import rasterio
from to4326 import transform

dataset = rasterio.open('geotiff path')
bounds = ds_raster.bounds
src_crs = dataset.crs
upper_left = dataset.transform * (0, 0)
lower_left = dataset.transform * (0, dataset.height)
upper_right = dataset.transform * (dataset.width, 0) 
lower_right = dataset.transform * (dataset.width, dataset.height)

transform.geojson_from_corner_coordinates(upper_left, lower_left, upper_right, lower_right, src_crs)
```