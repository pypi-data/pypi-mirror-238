import numpy as np
import pytest
from numpy import isclose

from mfire.utils.calc import (
    round_to_closest_multiple,
    round_to_next_multiple,
    round_to_previous_multiple,
)


class TestCalcFunctions:
    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1.5),
            (1.6, 0.5, 1.5),
            (22, 10, 20),
            (27, 10, 30),
            (np.array([1.3, 1.6]), 0.5, np.array([1.5, 1.5])),
            (np.array([22, 27]), 10, np.array([20, 30])),
        ],
    )
    def test_round_to_closest_multiple(self, x, m, expected):
        assert np.all(isclose(round_to_closest_multiple(x, m), expected, rtol=1e-5))

    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1.5),
            (1.6, 0.5, 2),
            (22, 10, 30),
            (27, 10, 30),
            (np.array([1.3, 1.6]), 0.5, np.array([1.5, 2])),
            (np.array([22, 27]), 10, np.array([30, 30])),
        ],
    )
    def test_round_to_next_multiple(self, x, m, expected):
        assert np.all(isclose(round_to_next_multiple(x, m), expected, rtol=1e-5))

    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1),
            (1.6, 0.5, 1.5),
            (22, 10, 20),
            (27, 10, 20),
            (np.array([1.3, 1.6]), 0.5, np.array([1, 1.5])),
            (np.array([22, 27]), 10, np.array([20, 20])),
        ],
    )
    def test_round_to_previous_multiple(self, x, m, expected):
        assert np.all(isclose(round_to_previous_multiple(x, m), expected, rtol=1e-5))
