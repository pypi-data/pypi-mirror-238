import pytest
import xarray as xr

from mfire.mask.fusion import (
    CheckZone,
    CoverZone,
    FusionZone,
    extract_areaName,
    finest_grid_name,
    perform_zone_fusion,
)

# from shapely.geometry import shape as SHAshape


class TestCheckZone:
    def test_compute(self):
        # dmask : dataset of all zones
        coords = {
            "id": ("id", ["zone1", "zone2", "zone3", "zone4"]),
            "latitude": (
                "latitude",
                [
                    1,
                    2,
                ],
            ),
            "longitude": (
                "longitude",
                [
                    5,
                    6,
                    7,
                ],
            ),
        }
        value = [
            [[1, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1]],
            [[0, 1, 1], [0, 1, 1]],
        ]
        data_vars = {
            "grille": (["id", "latitude", "longitude"], value),
            "is_polygon": (["id"], [True, True, True, True]),
            "areaName": (["id"], ["nom1", "nom2", "nom3", "nom4"]),
        }
        dmask = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        # gmask : dataarray of possible zones
        coords = {
            "id": ["zone1", "zone2", "zone4"],
            "latitude": [
                1,
                2,
            ],
            "longitude": [
                5,
                6,
                7,
            ],
        }
        # fusion novatrice
        dims = ["id", "latitude", "longitude"]
        value = [
            [[True, False, False], [True, False, False]],
            [[False, True, False], [False, True, False]],
            [[False, True, True], [False, True, True]],
        ]
        gmask = xr.DataArray(data=value, coords=coords, dims=dims, name="grille")
        list_poss = ["zone1", "zone2", "zone4"]
        dims = ("latitude", "longitude")
        cz = CheckZone(dmask, gmask, list_poss, dims)
        rslt = cz.compute("zone1", "zone2")
        assert rslt
        # fusion déjà existante z2+z3 = z4
        coords = {
            "id": ["zone2", "zone3", "zone4"],
            "latitude": [
                1,
                2,
            ],
            "longitude": [
                5,
                6,
                7,
            ],
        }
        dims = ["id", "latitude", "longitude"]
        value = [
            [[False, True, False], [False, True, False]],
            [[False, False, True], [False, False, True]],
            [[False, True, True], [False, True, True]],
        ]
        gmask = xr.DataArray(data=value, coords=coords, dims=dims, name="grille")
        list_poss = ["zone2", "zone3", "zone4"]
        dims = ("latitude", "longitude")
        cz = CheckZone(dmask, gmask, list_poss, dims)
        rslt = cz.compute("zone2", "zone3")
        assert not rslt
        # xr.testing.assert_equal(rslt, ref_ds)


class TestCoverZone:
    def test_compute(self):
        # zones differ
        dims = ["id", "latitude", "longitude"]
        value = [
            [[True, False, False], [True, False, False]],
            [[False, True, False], [False, True, False]],
        ]
        coords = {
            "id": ["zone2", "zone3"],
            "latitude": [
                1,
                2,
            ],
            "longitude": [
                5,
                6,
                7,
            ],
        }
        gmask = xr.DataArray(data=value, coords=coords, dims=dims, name="grille")
        dims = ("latitude", "longitude")
        cz = CoverZone(gmask, dims)
        rslt = cz.compute("zone2", "zone3")
        assert rslt
        # zones do not differ enough
        dims = ["id", "latitude", "longitude"]
        value = [
            [
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
            ],
            [
                [False, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
            ],
        ]
        coords = {
            "id": ["zone2", "zone3"],
            "latitude": [1, 2, 3],
            "longitude": [5, 6, 7, 8],
        }
        gmask = xr.DataArray(data=value, coords=coords, dims=dims, name="grille")
        dims = ("latitude", "longitude")
        cz = CoverZone(gmask, dims)
        rslt = cz.compute("zone2", "zone3")
        assert not rslt


class TestFusionZone:
    def test_compute(self):
        # dmask : dataset of all zones
        coords = {
            "id": ("id", ["zone1", "zone2", "zone3", "zone4"]),
            "latitude": (
                "latitude",
                [
                    1,
                    2,
                ],
            ),
            "longitude": (
                "longitude",
                [
                    5,
                    6,
                    7,
                ],
            ),
        }
        value = [
            [[1, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1]],
            [[0, 1, 1], [0, 1, 1]],
        ]
        data_vars = {
            "grille": (["id", "latitude", "longitude"], value),
            "is_polygon": (["id"], [True, True, True, True]),
            "areaName": (["id"], ["nom1", "nom2", "nom3", "nom4"]),
        }
        dmask = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        fz = FusionZone(dmask, "parent")
        ref_rslt = {
            "name": "nom2 et nom3",
            "base": ["zone2", "zone3"],
            "id": "parent__zone2__zone3",
            "areaType": "fusion2",
        }
        rslt = fz.compute("zone2", "zone3")
        assert rslt == ref_rslt


class TestModule:
    def test_extract_areaName(self):
        properties = {"name": "nom"}
        rslt = extract_areaName(properties)
        assert rslt == "nom"
        properties = {"label": "nom"}
        rslt = extract_areaName(properties)
        assert rslt == "nom"
        properties = {"alt_label": "nom"}
        rslt = extract_areaName(properties)
        assert rslt == "nom"
        properties = {"areaName": "nom"}
        rslt = extract_areaName(properties)
        assert rslt == "nom"
        properties = {"area_name": "nom"}
        rslt = extract_areaName(properties)
        assert rslt == "nom"
        properties = {"notknownkey": "nom"}
        with pytest.raises(ValueError):
            _ = extract_areaName(properties)

    def test_finest_grid_name(self):
        # dmask : dataset of all zones
        coords = {
            "id": ("id", ["zone1", "zone2", "zone3", "axe"]),
            "latitude_eurw1s100": (
                "latitude_eurw1s100",
                [
                    1,
                    2,
                ],
            ),
            "longitude_eurw1s100": (
                "longitude_eurw1s100",
                [
                    5,
                    6,
                    7,
                ],
            ),
            "latitude_best": ("latitude_best", [1, 2, 3]),
            "longitude_best": ("longitude_best", [5, 6, 7, 4]),
        }
        value = [
            [[1, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1]],
            [[1, 1, 1], [1, 1, 1]],
        ]
        value_best = [
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
            [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
            [[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0]],
        ]
        data_vars = {
            "eurw1s100": (
                [
                    "id",
                    "latitude_eurw1s100",
                    "longitude_eurw1s100",
                ],
                value,
            ),
            "best": (["id", "latitude_best", "longitude_best"], value_best),
            "is_polygon": (["id"], [True, True, True, True]),
            "areaName": (["id"], ["nom1", "nom2", "nom3", "nom4"]),
        }
        dmask = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        rslt = finest_grid_name(dmask)
        assert rslt == "best"

    def test_perform_zone_fusion(self):
        # dmask : dataset of all zones
        coords = {
            "id": ("id", ["zone1", "zone2", "zone3", "axe"]),
            "latitude_eurw1s100": (
                "latitude_eurw1s100",
                [
                    1,
                    2,
                ],
            ),
            "longitude_eurw1s100": (
                "longitude_eurw1s100",
                [
                    5,
                    6,
                    7,
                ],
            ),
        }
        value = [
            [[1, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1]],
            [[1, 1, 1], [1, 1, 1]],
        ]
        data_vars = {
            "eurw1s100": (["id", "latitude_eurw1s100", "longitude_eurw1s100"], value),
            "is_polygon": (["id"], [True, True, True, True]),
            "areaName": (["id"], ["nom1", "nom2", "nom3", "nom4"]),
        }
        dmask = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        rslt = perform_zone_fusion(dmask, "axe")
        # generate 3 pairs (z1,z2) (z1,z3) z2,z3)
        ref_rslt = [
            {
                "areaType": "fusion2",
                "base": ["zone1", "zone2"],
                "id": "axe__zone1__zone2",
                "name": "nom1 et nom2",
            },
            {
                "areaType": "fusion2",
                "base": ["zone1", "zone3"],
                "id": "axe__zone1__zone3",
                "name": "nom1 et nom3",
            },
            {
                "areaType": "fusion2",
                "base": ["zone2", "zone3"],
                "id": "axe__zone2__zone3",
                "name": "nom2 et nom3",
            },
        ]
        assert rslt == ref_rslt
