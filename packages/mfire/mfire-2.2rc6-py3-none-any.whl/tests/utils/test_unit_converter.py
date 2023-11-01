import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.utils.unit_converter import fromW1ToWWMF
from tests.functions_test import assert_identically_close


class TestUnitConverterFunctions:
    @pytest.mark.parametrize(
        "w1,expected",
        [
            (8, 59),
            (100, -1),
            ([16, 24], [62, 91]),
            ([2, 32, np.nan], [32, 92, np.nan]),
            (
                xr.DataArray([2, 32, np.nan]),
                xr.DataArray([32, 92, np.nan], attrs={"units": "wwmf"}),
            ),
            (xr.DataArray([4, 22]), xr.DataArray([38, 80], attrs={"units": "wwmf"})),
        ],
    )
    def test_from_w1_to_wwmf(self, w1, expected):
        result = fromW1ToWWMF(w1)
        assert_identically_close(result, expected)
