# to4326
to4326 convert bounds of satellite data such as GeoTIFF to Polygon of EPSG:4326.
Depends: pyproj

## Example

```Python
import to4326

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

## Docs
* [Methods](./docs/METHODS.md)
* [Examples](./docs/EXAMPLES.md)