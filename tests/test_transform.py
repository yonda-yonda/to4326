import pytest
from to4326.exceptions import *
import to4326.transform as transform


def test_transform():
    assert transform._transform(
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]], 4326, 4326
    ) == [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]

    assert transform._transform(
        [
            [223069, -268407],
            [-275846, -495187],
        ],
        3411,
        4326,
    ) == [
        [-5.270541933285495, 86.77915026771586],
        [-74.12017710269978, 84.77098843082935],
    ]


def test_transform_ring():
    assert transform.transform_ring(
        [
            [382200.000, 2512500.000],
            [382200.000, 2279400.000],
            [610500.000, 2279400.000],
            [610500.000, 2512500.000],
            [382200.000, 2512500.000],
        ],
        32645,
    ) == [
        [85.85296718933647, 22.71566587084141],
        [85.8694977275825, 20.610041795245515],
        [88.06045501053292, 20.610485722030123],
        [88.07596179098907, 22.71615986368381],
        [85.85296718933647, 22.71566587084141],
    ]

    assert transform.transform_ring(
        [
            [508800.000, 7247400.000],
            [508800.000, 7001100.000],
            [753000.000, 7001100.000],
            [753000.000, 7247400.000],
            [508800.000, 7247400.000],
        ],
        32660,
    ) == [
        [177.18908505580515, 65.34932256544839],
        [177.17456390562774, 63.13910500179646],
        [-177.99275205341496, 63.05068519969726],
        [-177.57860702499983, 65.25180997065199],
        [177.18908505580515, 65.34932256544839],
    ]

    assert transform.transform_ring(
        [[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]], 4326
    ) == [[170, -10], [-170, -10], [-170, 10], [170, 10], [170, -10]]


def test_transform_bbox():
    assert transform.transform_bbox([382200, 2279400, 610500, 2512500], 32645) == [
        85.85296718933647,
        20.610041795245515,
        88.07596179098907,
        22.719775713801845,
    ]
    assert transform.transform_bbox([508800, 7001100, 753000, 7247400], 32660) == [
        177.17456390562774,
        63.05068519969726,
        -177.57860702499983,
        65.34932256544839,
    ]
    assert transform.transform_bbox(
        [508800, 7001100, 753000, 7247400], 32660, expand=True
    ) == [
        177.17456390562774,
        63.05068519969726,
        -177.57860702499983 + 360,
        65.34932256544839,
    ]
    assert transform.transform_bbox(
        [382200, 2279400, 10, 610500, 2512500, 50], 32645
    ) == [
        85.85296718933647,
        20.610041795245515,
        10,
        88.07596179098907,
        22.719775713801845,
        50,
    ]
    assert transform.transform_bbox(
        [508800, 7001100, 5, 753000, 7247400, 10], 32660
    ) == [
        177.17456390562774,
        63.05068519969726,
        5,
        -177.57860702499983,
        65.34932256544839,
        10,
    ]


def test_geojson_from_linear_ring():
    assert transform.geojson_from_linear_ring(
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]], 4326, partition=0
    ) == {
        "type": "Feature",
        "bbox": [-10, -10, 10, 10],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]]],
        },
    }
    assert transform.geojson_from_linear_ring(
        [[-10, -10], [10, -10], [10, 10], [-10, 10], [-10, -10]], 4326, partition=1
    ) == {
        "type": "Feature",
        "bbox": [-10.0, -10, 10, 10],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-10.0, -10],
                    [0.0, -10],
                    [10, -10.0],
                    [10, 0.0],
                    [10.0, 10],
                    [0.0, 10],
                    [-10, 10.0],
                    [-10, 0.0],
                    [-10, -10],
                ]
            ],
        },
    }

    assert transform.geojson_from_linear_ring(
        [
            [223069.075613658875227, -268407.860357680357993],
            [-275846.995845806901343, -495187.89283925422933],
            [-163320.733313913689926, -742745.670409420854412],
            [335595.338145552086644, -515965.637927847041283],
            [223069.075613658875227, -268407.860357680357993],
        ],
        3411,
    ) == {
        "type": "Feature",
        "bbox": [
            -74.12022112082042,
            82.98826228650147,
            -5.270622665103448,
            86.88878705473334,
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-5.270622665103448, 86.77914371855618],
                    [-14.250061369548213, 86.87412426312318],
                    [-23.548864966957215, 86.88878705473334],
                    [-32.693812151359616, 86.82201802001164],
                    [-41.25560995422688, 86.67873416307306],
                    [-48.9538596657912, 86.46825557920494],
                    [-55.68003779057252, 86.20176494269847],
                    [-61.45601993315672, 85.89017913245713],
                    [-66.37532859434766, 85.54298702755824],
                    [-70.55724119088521, 85.16790348854887],
                    [-74.12022112082042, 84.77097678044598],
                    [-71.97110864705208, 84.61841509935437],
                    [-69.94331397518876, 84.45873464719025],
                    [-68.0315123231705, 84.29253849885926],
                    [-66.22993488762883, 84.12038499165931],
                    [-64.5325844049517, 83.94278809292268],
                    [-62.93340319357807, 83.76021880654855],
                    [-61.42639995777989, 83.57310727610472],
                    [-60.00574206724918, 83.38184531482337],
                    [-58.665819773133734, 83.18678915779185],
                    [-57.40128818663171, 82.98826228650147],
                    [-53.951992624649165, 83.27843524136415],
                    [-50.20571088005186, 83.54224084412589],
                    [-46.15863801687481, 83.77628363534642],
                    [-41.818277399785174, 83.97705623949825],
                    [-37.20658593714978, 84.14110603045513],
                    [-32.36219263801153, 84.2652552572159],
                    [-27.340749255999818, 84.34685551746712],
                    [-22.212645835564576, 84.38403943161795],
                    [-17.05792785558349, 84.37592038404522],
                    [-11.959143304085023, 84.32269393312409],
                    [-11.56347384314647, 84.5702079431649],
                    [-11.129970887643898, 84.81748727101969],
                    [-10.652993182505446, 85.06448689529408],
                    [-10.12573285508205, 85.31115283779752],
                    [-9.53990164907278, 85.55741971247636],
                    [-8.885311834454305, 85.80320743194677],
                    [-8.149308950579606, 86.04841671801508],
                    [-7.315992915614546, 86.29292288494149],
                    [-6.365131918099119, 86.53656708154573],
                    [-5.270622665103448, 86.77914371855618],
                ]
            ],
        },
    }

    assert transform.geojson_from_linear_ring(
        [
            [508800.000, 7247400.000],
            [508800.000, 7001100.000],
            [753000.000, 7001100.000],
            [753000.000, 7247400.000],
            [508800.000, 7247400.000],
        ],
        32660,
        partition=1,
    ) == {
        "type": "Feature",
        "bbox": [
            177.17456390562774,
            63.05068519969726,
            -177.57860702499983,
            65.34932256544839,
        ],
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [180, 65.31807448056004],
                        [179.81058927281353, 65.323257946911],
                        [177.18908505580515, 65.34932256544839],
                        [177.18150083071316, 64.24429821916637],
                        [177.17456390562774, 63.13910500179646],
                        [179.59505058865193, 63.11547654369982],
                        [180, 63.104599649017885],
                        [180, 65.31807448056004],
                    ]
                ],
                [
                    [
                        [-180, 63.104599649017885],
                        [-177.99275205341496, 63.05068519969726],
                        [-177.79484203871405, 64.15151244109893],
                        [-177.57860702499983, 65.25180997065199],
                        [-180, 65.31807448056004],
                        [-180, 63.104599649017885],
                    ]
                ],
            ],
        },
    }


def test_geojson_from_corner_coordinates():
    assert transform.geojson_from_corner_coordinates(
        [223069.075613658875227, -268407.860357680357993],
        [-275846.995845806901343, -495187.89283925422933],
        [335595.338145552086644, -515965.637927847041283],
        [-163320.733313913689926, -742745.670409420854412],
        3411,
    ) == {
        "type": "Feature",
        "bbox": [
            -74.12022112082042,
            82.98826228650147,
            -5.270622665103448,
            86.88878705473334,
        ],
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-5.270622665103448, 86.77914371855618],
                    [-14.250061369548213, 86.87412426312318],
                    [-23.548864966957215, 86.88878705473334],
                    [-32.693812151359616, 86.82201802001164],
                    [-41.25560995422688, 86.67873416307306],
                    [-48.9538596657912, 86.46825557920494],
                    [-55.68003779057252, 86.20176494269847],
                    [-61.45601993315672, 85.89017913245713],
                    [-66.37532859434766, 85.54298702755824],
                    [-70.55724119088521, 85.16790348854887],
                    [-74.12022112082042, 84.77097678044598],
                    [-71.97110864705208, 84.61841509935437],
                    [-69.94331397518876, 84.45873464719025],
                    [-68.0315123231705, 84.29253849885926],
                    [-66.22993488762883, 84.12038499165931],
                    [-64.5325844049517, 83.94278809292268],
                    [-62.93340319357807, 83.76021880654855],
                    [-61.42639995777989, 83.57310727610472],
                    [-60.00574206724918, 83.38184531482337],
                    [-58.665819773133734, 83.18678915779185],
                    [-57.40128818663171, 82.98826228650147],
                    [-53.951992624649165, 83.27843524136415],
                    [-50.20571088005186, 83.54224084412589],
                    [-46.15863801687481, 83.77628363534642],
                    [-41.818277399785174, 83.97705623949825],
                    [-37.20658593714978, 84.14110603045513],
                    [-32.36219263801153, 84.2652552572159],
                    [-27.340749255999818, 84.34685551746712],
                    [-22.212645835564576, 84.38403943161795],
                    [-17.05792785558349, 84.37592038404522],
                    [-11.959143304085023, 84.32269393312409],
                    [-11.56347384314647, 84.5702079431649],
                    [-11.129970887643898, 84.81748727101969],
                    [-10.652993182505446, 85.06448689529408],
                    [-10.12573285508205, 85.31115283779752],
                    [-9.53990164907278, 85.55741971247636],
                    [-8.885311834454305, 85.80320743194677],
                    [-8.149308950579606, 86.04841671801508],
                    [-7.315992915614546, 86.29292288494149],
                    [-6.365131918099119, 86.53656708154573],
                    [-5.270622665103448, 86.77914371855618],
                ]
            ],
        },
    }

    assert transform.geojson_from_corner_coordinates(
        [508800.000, 7247400.000],
        [508800.000, 7001100.000],
        [753000.000, 7247400.000],
        [753000.000, 7001100.000],
        32660,
        partition=1,
    ) == {
        "type": "Feature",
        "bbox": [
            177.17456390562774,
            63.05068519969726,
            -177.57860702499983,
            65.34932256544839,
        ],
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [180, 65.31807448056004],
                        [179.81058927281353, 65.323257946911],
                        [177.18908505580515, 65.34932256544839],
                        [177.18150083071316, 64.24429821916637],
                        [177.17456390562774, 63.13910500179646],
                        [179.59505058865193, 63.11547654369982],
                        [180, 63.104599649017885],
                        [180, 65.31807448056004],
                    ]
                ],
                [
                    [
                        [-180, 63.104599649017885],
                        [-177.99275205341496, 63.05068519969726],
                        [-177.79484203871405, 64.15151244109893],
                        [-177.57860702499983, 65.25180997065199],
                        [-180, 65.31807448056004],
                        [-180, 63.104599649017885],
                    ]
                ],
            ],
        },
    }


def test_invalid_error():
    with pytest.raises(InvalidLinearRing):
        transform.transform_ring([[0, 0], [10, 10]], 4326)
    with pytest.raises(transform.IncludingPole):
        transform.transform_ring(
            [
                [-1096140.177763625513762, 633075.779011003673077],
                [-1156379.742859589401633, -520081.609968872275203],
                [919322.002944564330392, -628513.79071983625181],
                [979561.568040528334677, 524643.59826003969647],
                [-1096140.177763625513762, 633075.779011003673077],
            ],
            3411,
        )
    with pytest.raises(transform.InvalidBounds):
        transform.transform_bbox([508800, 7001100, 753000, 7247400, 1000], 32660)
    with pytest.raises(transform.NotAllowedWarpBounds):
        transform.transform_bbox([508800, 7001100, -753000, 7247400], 32660)
    with pytest.raises(transform.NotAllowedWarpBounds):
        transform.transform_bbox([508800, 7001100, 10, -753000, 7247400, 100], 32660)
    with pytest.raises(InvalidLinearRing):
        transform.geojson_from_linear_ring(
            [
                [508800.000, 7247400.000],
                [508800.000, 7001100.000],
                [753000.000, 7001100.000],
                [753000.000, 7247400.000],
            ],
            32660,
        )
    with pytest.raises(transform.IncludingPole):
        transform.geojson_from_linear_ring(
            [
                [-1096140.177763625513762, 633075.779011003673077],
                [-1156379.742859589401633, -520081.609968872275203],
                [919322.002944564330392, -628513.79071983625181],
                [979561.568040528334677, 524643.59826003969647],
                [-1096140.177763625513762, 633075.779011003673077],
            ],
            3411,
        )
    with pytest.raises(transform.NotAllowedCwLinearRing):
        transform.geojson_from_corner_coordinates(
            [508800.000, 7247400.000],
            [508800.000, 7001100.000],
            [-753000.000, 7247400.000],
            [-753000.000, 7001100.000],
            32660,
        )
    with pytest.raises(transform.IncludingPole):
        transform.geojson_from_corner_coordinates(
            [-1096140.177763625513762, 633075.779011003673077],
            [-1156379.742859589401633, -520081.609968872275203],
            [979561.568040528334677, 524643.59826003969647],
            [919322.002944564330392, -628513.79071983625181],
            3411,
        )