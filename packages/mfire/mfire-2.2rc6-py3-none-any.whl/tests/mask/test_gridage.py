import numpy as np
import pytest
import xarray as xr
from shapely.geometry import shape as SHAshape

import mfire.mask.gridage as gr
from mfire.mask.grids import get_info as GRIDget_info

xr.set_options(keep_attrs=True)
"""
al coordinates ofset for 0.5 to recenter the grid point
"""
ref_grid = {
    "conversion_slope": np.array([1 / 3.0, 1]),
    "conversion_offset": np.array([-0.5, -0.5]),
    "nb_c": 3,
    "nb_l": 2,
}


class TestGeoDraw:
    """
    other methods are tested by test_create_mask_PIL below
    """

    def test_lonlat2xy(self):
        geodraw = gr.GeoDraw(ref_grid)
        points = [[3, 1], [6, 2], [9, 1]]
        result = geodraw._lonlat2xy(points)
        # +0.5 to recentre grid
        ref_lonlat = [0.5, 0.5, 1.5, 1.5, 2.5, 0.5]
        assert result == ref_lonlat


class TestGridageFunctions:
    """
    gridinfo = get_gridinfo(grid_da)
    """

    def test_get_gridinfo(self):
        value_da = [[0, 0, 0], [0, 0, 0]]
        grid_da = xr.DataArray(
            data=value_da,
            coords={"latitude": [1, 2], "longitude": [3, 6, 9]},
            dims=["latitude", "longitude"],
            name="grille",
        )
        result = gr.get_gridinfo(grid_da)
        assert result.keys() == ref_grid.keys()
        for key in result.keys():
            if isinstance(result[key], np.ndarray):
                compare = result[key] == ref_grid[key]
                assert compare.all()
            else:
                assert (key == key) and (result[key] == ref_grid[key])

    def test_create_mask_PIL(self):
        # create a grid
        nlt = 10
        nlg = 20
        value_da = np.random.rand(nlt, nlg)
        grid_da = xr.DataArray(
            data=value_da,
            coords={"latitude": np.arange(nlt), "longitude": np.arange(nlg)},
            dims=["latitude", "longitude"],
            name="grille",
        )

        # a single polygon
        poly = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 4], [3, 4], [3, 1], [1, 1]]],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4]),
            "longitude": ("longitude", [1, 2, 3]),
        }
        value = np.ones(12).astype("bool")
        value = value.reshape((4, 3))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a multi polygon
        poly = SHAshape(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[1, 1], [1, 4], [3, 4], [3, 1], [1, 1]]],
                    [[[5, 6], [5, 9], [8, 9], [8, 6], [5, 6]]],
                ],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4, 6, 7, 8, 9]),
            "longitude": ("longitude", [1, 2, 3, 5, 6, 7, 8]),
        }
        value = np.zeros(56).astype("bool")
        value = value.reshape((8, 7))
        value[0:4, 0:3] = True
        value[4:8, 3:7] = True
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a polygon with a hole
        poly = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [
                    [[1, 1], [1, 9], [9, 9], [9, 1], [1, 1]],
                    [[4, 4], [4, 6], [6, 6], [6, 4], [4, 4]],
                ],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            "longitude": ("longitude", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        }
        value = np.ones(81).astype("bool")
        value = value.reshape((9, 9))
        value[3:6, 3:6] = False
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a polygon which becomes a line
        poly = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [
                    [[0.5, 0.9], [0.9, 4.1], [1.1, 4.1], [1.1, 0.9], [0.9, 0.9]]
                ],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4]),
            "longitude": ("longitude", [1]),
        }
        value = np.ones(4).astype("bool")
        value = value.reshape((4, 1))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a polygon which becomes a point
        poly = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [
                    [[0.9, 0.9], [0.9, 1.1], [1.1, 1.1], [1.1, 0.9], [0.9, 0.9]]
                ],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {"latitude": ("latitude", [1]), "longitude": ("longitude", [1])}
        value = np.ones(1).astype("bool")
        value = value.reshape((1, 1))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a single line vertical/horizontal
        poly = SHAshape(
            {"type": "LineString", "coordinates": [[1, 1], [1, 4], [3, 4], [3, 1]]}
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4]),
            "longitude": ("longitude", [1, 2, 3]),
        }
        value = np.zeros(12).astype("bool")
        value = value.reshape((4, 3))
        value[:, 0] = True
        value[:, 2] = True
        value[3, 1] = True
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a single line oblique
        poly = SHAshape({"type": "LineString", "coordinates": [[1, 1], [4, 8]]})
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4, 5, 6, 7, 8]),
            "longitude": ("longitude", [1, 2, 3, 4]),
        }
        value = np.zeros(32).astype("bool")
        value = value.reshape((8, 4))
        value[0:2, 0] = True
        value[2:4, 1] = True
        value[4:6, 2] = True
        value[6:8, 3] = True
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a multi line
        poly = SHAshape(
            {
                "type": "MultiLineString",
                "coordinates": [[[1, 1], [1, 4]], [[3, 4], [3, 1]]],
            }
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {
            "latitude": ("latitude", [1, 2, 3, 4]),
            "longitude": ("longitude", [1, 3]),
        }
        value = np.ones(8).astype("bool")
        value = value.reshape((4, 2))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a line which becomes a point
        poly = SHAshape(
            {"type": "LineString", "coordinates": [[0.9, 0.9], [0.9, 1.1], [1.1, 1.1]]}
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {"latitude": ("latitude", [1]), "longitude": ("longitude", [1])}
        value = np.ones(1).astype("bool")
        value = value.reshape((1, 1))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a single point
        poly = SHAshape({"type": "Point", "coordinates": [1.1, 1.1]})
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {"latitude": ("latitude", [1]), "longitude": ("longitude", [1])}
        value = np.ones(1).astype("bool")
        value = value.reshape((1, 1))
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)
        # a multi point
        poly = SHAshape(
            {"type": "MultiPoint", "coordinates": [[0.9, 0.9], [3.9, 1.1], [1.1, 2.1]]}
        )
        result = gr.create_mask_PIL(poly, GRIDget_info(grid_da))
        coords = {"latitude": ("latitude", [1, 2]), "longitude": ("longitude", [1, 4])}
        value = np.zeros(4).astype("bool")
        value = value.reshape((2, 2))
        value[0, 0] = True
        value[-1, 0] = True
        value[0, -1] = True
        data_vars = {"grille": (["latitude", "longitude"], value)}
        ref_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
        )
        xr.testing.assert_equal(result, ref_ds)

        # Linear ring without geoAction
        poly = SHAshape(
            {
                "type": "LinearRing",
                "coordinates": [(0, 0), (1, 1), (1, 0)],
            }
        )
        with pytest.raises(gr.GeoTypeException, match="LinearRing"):
            gr.create_mask_PIL(poly, GRIDget_info(grid_da))
