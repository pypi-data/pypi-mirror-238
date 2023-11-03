from typing import List, Optional

import numpy as np
import pytest
import xarray as xr

from mfire.localisation.area_algebra import (
    GenericArea,
    compute_IoL,
    compute_IoU,
    generic_merge,
)


class TestAreaAlgebraFunctions:
    def setUp_domain_and_area(
        self, id0: Optional[List] = None, id1: Optional[List] = None
    ):
        self.lat = np.arange(10, 0, -1)
        self.lon = np.arange(-5, 5, 1)
        self.id0 = id0 if id0 is not None else ["a", "b"]
        self.id1 = id1 if id1 is not None else ["c", "d", "e"]
        self.domain_arr = np.array(
            [
                [[int(i > k) for i in self.lon] for j in self.lat]
                for k in range(len(self.id0))
            ]
        )
        self.areas_arr = np.array(
            [
                [[int(j > 5 + k) for i in self.lon] for j in self.lat]
                for k in range(len(self.id1))
            ]
        )
        self.domain_da = xr.DataArray(
            self.domain_arr,
            coords=(("id", self.id0), ("lat", self.lat), ("lon", self.lon)),
            name="toto",
        )
        self.areas_da = xr.DataArray(
            self.areas_arr,
            coords=(("id", self.id1), ("lat", self.lat), ("lon", self.lon)),
            name="toto",
        )

    def test_compute_IoU(self):
        """
        In this test, we created 2 binary dataarrays da0 and da1 containing
        respectively the zones ('a', 'b') and ('c', 'd', 'e'). The IoL returns us a
        table of the IoL of all the combinations of the 2 sets of zones.
        """
        self.setUp_domain_and_area()
        da0 = self.domain_da.rename({"id": "id0"})
        da1 = self.areas_da.rename({"id": "id1"})
        iou_da = xr.DataArray(
            [[0.28571429, 0.25, 0.20689655], [0.23076923, 0.20689655, 0.17647059]],
            coords=(("id0", self.id0), ("id1", self.id1)),
        )
        xr.testing.assert_equal(
            compute_IoU(da0, da1, dims=("lat", "lon")).round(8), iou_da
        )
        xr.testing.assert_equal(
            compute_IoU(da0, da1, dims=("lat", "lon")),
            compute_IoU(da1, da0, dims=("lat", "lon")).T,
        )

    def test_generic_merge(self):
        self.setUp_domain_and_area()
        xr.testing.assert_identical(generic_merge(self.domain_da, None), self.domain_da)
        xr.testing.assert_identical(generic_merge(None, self.domain_da), self.domain_da)
        merged_da = xr.DataArray(
            np.concatenate([self.domain_arr, self.areas_arr]),
            coords=(("id", self.id0 + self.id1), ("lat", self.lat), ("lon", self.lon)),
            name="toto",
        )
        xr.testing.assert_equal(generic_merge(self.domain_da, self.areas_da), merged_da)

    @pytest.mark.parametrize(
        "phenomenon_map,expected",
        [
            # a is excluded since IoL < 25%
            ([[0, 0, 0], [1, 0, 0], [0, 0, 0]], None),
            # a is included since IoL(=0.25) >= 25%
            ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], ["a"]),
            # check the exclusion with a and b
            ([[1, 1, 0], [0, 0, 0], [0, 0, 0]], ["b"]),
            ([[1, 1, 0], [1, 1, 0], [0, 0, 0]], ["a"]),
            ([[1, 0, 0], [0, 0, 0], [0, 0, 0]], ["b"]),
            # several locations (locations are stored according to proportion of
            # phenomenon)
            ([[0, 0, 1], [1, 1, 1], [0, 0, 0]], ["c", "a"]),
            ([[1, 0, 1], [0, 0, 1], [0, 0, 1]], ["c", "b"]),
        ],
    )
    def test_compute_IoL(self, phenomenon_map, expected):
        lat = [30, 31, 32]
        lon = [40, 41, 42]
        id = ["a", "b", "c"]

        geos_descriptive = xr.DataArray(
            np.array(
                [
                    [[1, 1, 0], [1, 1, 0], [1, 1, 0]],  # area "a"
                    [[1, 1, 0], [0, 0, 0], [0, 0, 0]],  # area "b"
                    [[0, 0, 1], [0, 0, 1], [0, 0, 1]],  # area "c"
                ]
            ),
            coords=(("id", id), ("lat", lat), ("lon", lon)),
        )
        phenomenon_map = xr.DataArray(
            phenomenon_map,
            coords=(("lat", lat), ("lon", lon)),
        )

        result = compute_IoL(geos_descriptive, phenomenon_map, dims=("lat", "lon"))
        if result is not None:
            result = list(result.id.data)

        assert result == expected


class TestGenericArea:

    generic_area: GenericArea = GenericArea(alt_min=500, alt_max=2000)

    def test_intersect(self):
        """TODO"""
        pass

    def test_filter_areas(self):
        """TODO"""
        pass

    def test_get_other_altitude_area(self):
        """TODO"""
        pass

    def test_rename_single_inter(self):
        assert (
            self.generic_area.rename_single_inter("en Isère", "à Grenoble")
            == "à Grenoble"
        )
        assert (
            self.generic_area.rename_single_inter("en Isère", "entre 1000 m et 1500 m")
            == "entre 1000 m et 1500 m"
        )
        assert (
            self.generic_area.rename_single_inter("en Isère", "entre 1000 m et 2000 m")
            == "au-dessus de 1000 m"
        )
        assert (
            self.generic_area.rename_single_inter(
                "au-dessus de 1500 m", "sur le massif de Belledonne"
            )
            == "sur le massif de Belledonne au-dessus de 1500 m"
        )
        assert (
            self.generic_area.rename_single_inter(
                "entre 1500 m et 2000 m",
                "sur le massif de Belledonne",
            )
            == "sur le massif de Belledonne au-dessus de 1500 m"
        )
        assert (
            self.generic_area.rename_single_inter(
                "entre 1000 m et 1800 m", "au-dessus de 1500 m"
            )
            == "entre 1500 m et 1800 m"
        )
        assert (
            self.generic_area.rename_single_inter(
                "entre 1000 m et 2000 m", "au-dessus de 1500 m"
            )
            == "au-dessus de 1500 m"
        )

    def test_rename_inter(self):
        """TODO"""
        pass

    def test_rename_single_difference(self):
        assert (
            self.generic_area.rename_single_difference("en Isère", "à Grenoble")
            == "comp_à Grenoble"
        )
        assert (
            self.generic_area.rename_single_difference(
                "en Isère", "entre 1000 m et 1500 m"
            )
            == "en dessous de 1000 m et au-dessus de 1500 m"
        )
        assert (
            self.generic_area.rename_single_difference(
                "en Isère", "entre 1000 m et 2000 m"
            )
            == "en dessous de 1000 m"
        )
        assert (
            self.generic_area.rename_single_difference(
                "au-dessus de 1500 m", "sur le massif de Belledonne"
            )
            == "au-dessus de 1500 m sauf sur le massif de Belledonne"
        )
        assert (
            self.generic_area.rename_single_difference(
                "entre 1500 m et 2000 m",
                "sur le massif de Belledonne",
            )
            == "au-dessus de 1500 m sauf sur le massif de Belledonne"
        )
        assert (
            self.generic_area.rename_single_difference(
                "entre 1000 m et 1800 m", "au-dessus de 1500 m"
            )
            == "entre 1000 m et 1500 m"
        )
        assert (
            self.generic_area.rename_single_difference(
                "entre 500 m et 1800 m", "au-dessus de 1500 m"
            )
            == "en dessous de 1500 m"
        )

    def test_rename_difference(self):
        """TODO"""
        pass

    def test_get_best_comp(self):
        """TODO"""
        pass

    def test_difference(self):
        """TODO"""
        pass


class TestAltArea:
    def test_restrict_to(self):
        """TODO"""
        pass

    def test_intersect(self):
        """TODO"""
        pass

    def test_difference(self):
        """TODO"""
        pass


class TestRiskArea:
    def test_separate_alt_other(self):
        """TODO"""
        pass

    def test_get_possibilities(self):
        """TODO"""
        pass

    def test_intersect(self):
        """TODO"""
        pass

    def test_difference(self):
        """TODO"""
        pass
