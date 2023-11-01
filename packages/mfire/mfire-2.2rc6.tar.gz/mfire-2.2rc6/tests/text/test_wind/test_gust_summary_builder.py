from typing import Optional

import numpy as np
import pytest
import xarray as xr

from mfire.text.wind.base import BaseParamBuilder
from mfire.text.wind.reducers.gust_summary_builder import GustSummaryBuilder
from mfire.text.wind.reducers.gust_summary_builder.gust_enum import GustCase
from mfire.text.wind.reducers.gust_summary_builder.gust_summary_builder import GustForce
from tests.text.utils import generate_valid_times

from .factories import CompositeFactory1x100, WindWeatherCompositeFactory


class TestGustForce:
    @pytest.mark.parametrize(
        "force, repr_value_exp, interval_exp",
        [
            (50.0, 50, (50, 60)),
            (59.9, 50, (50, 60)),
            (60.0, 60, (60, 70)),
        ],
    )
    def test_creation(self, force, repr_value_exp, interval_exp):
        wf = GustForce(force)
        assert wf.repr_value == repr_value_exp
        assert wf.interval == interval_exp

    @pytest.mark.parametrize(
        "valid_times, data_gust, gust_force_exp",
        [
            (
                generate_valid_times(periods=1),
                np.arange(1.0, 101.0, 1, dtype=np.float64),
                GustForce(95.0),
            ),
        ],
    )
    def test_creation_from_term(self, valid_times, data_gust, gust_force_exp):
        composite = CompositeFactory1x100().get(
            valid_times=valid_times,
            data_gust=data_gust,
        )
        dataset = composite.compute()
        data_array: xr.DataArray = dataset["gust"].sel(valid_time=valid_times[0])
        gust_force: GustForce = GustForce.from_term_data_array(data_array)
        assert gust_force == gust_force_exp

    def test_comparison(self):
        assert GustForce(50) == GustForce(50)
        assert GustForce(50) <= GustForce(50)
        assert GustForce(50) >= GustForce(50)

        assert GustForce(50) == GustForce(59)

        assert GustForce(50) < GustForce(60)
        assert GustForce(60) > GustForce(50)


class TestGustSummaryBuilder:
    @pytest.mark.parametrize(
        "valid_times, data, units_compo, units_data, data_exp, unit_exp",
        [
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"gust": "km/h"},
                {"gust": "km/h"},
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                "km/h",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"gust": "km/h"},
                {"gust": "m s**-1"},
                3.6
                * np.array(
                    [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]]
                ),
                "km/h",
            ),
        ],
    )
    def test_units_conversion(
        self,
        valid_times,
        data,
        units_compo,
        units_data,
        data_exp,
        unit_exp,
    ):
        """Test the conversion of the gust unit which has to be km/h."""
        composite = WindWeatherCompositeFactory().get(
            valid_times=valid_times,
            data_gust=data,
            units_compo=units_compo,
            units_data=units_data,
        )
        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)

        assert summary_builder.data.units == unit_exp

        values = summary_builder.data.sel(valid_time=valid_times).values
        # assert np.array_equal(values, gust_data_exp, equal_nan=True)
        np.testing.assert_allclose(values, data_exp)

    @pytest.mark.parametrize(
        "valid_times, data, case_exp, gust_force_exp, gust_interval_exp",
        [
            # Gusts are nan or <= 50.
            (
                generate_valid_times(periods=1),
                [[1.0, 5.0], [np.nan, 49.9]],
                GustCase.CASE_1,
                None,
                None,
            ),
            # Gusts are <= 50.
            (
                generate_valid_times(periods=1),
                [[1.0, 5.0], [0.0, 49.9]],
                GustCase.CASE_1,
                None,
                None,
            ),
            # All gust are <= 50.
            (
                generate_valid_times(periods=2),
                [[[1.0, 5.0], [np.nan, 49.9]], [[3.0, 25.0], [41.0, np.nan]]],
                GustCase.CASE_1,
                None,
                None,
            ),
            # All gusts are nan.
            (
                generate_valid_times(periods=1),
                np.array([[np.nan, np.nan], [np.nan, np.nan]]),
                GustCase.CASE_1,
                None,
                None,
            ),
            # All gusts are nan or 50.
            (
                generate_valid_times(periods=1),
                [[50.0, 50.0], [50.0, np.nan]],
                GustCase.CASE_1,
                None,
                None,
            ),
            # Some gusts are > 50.
            (
                generate_valid_times(periods=1),
                [[50.0, 50.0], [50.1, np.nan]],  # > 50 -> [nan, nan], [50.1, nan]
                GustCase.CASE_2,
                50.1,  # Q95 of [50.1] is 50.1
                (50, 60),
            ),
            # Some gusts are > 50.
            (
                generate_valid_times(periods=1),
                [[50.0, 50.0], [50.1, 0.0]],  # > 50 -> [nan, nan], [50.1, nan]
                GustCase.CASE_2,
                50.1,  # Q95 of [50.1] is 50.1
                (50, 60),
            ),
            # Some gusts are > 50.
            (
                generate_valid_times(periods=1),
                [[50.0, 50.1], [50.2, 50.3]],  # > 50 -> [50., 50.1], [50.2, 50.3]
                GustCase.CASE_2,
                50.29,  # Q95 of [50., 50.1, 50.2, 50.3] is 50.29
                (50, 60),
            ),
            # Some gusts are > 50.
            (
                generate_valid_times(periods=2),
                # > 50 -> [nan, nan], [nan, nan], [70., 71.], [30., 36.]
                [[[1.2, 5.3], [20.2, 20.4]], [[70.0, 71.0], [30.0, 36.0]]],
                GustCase.CASE_2,
                70.95,  # Q95 of [70., 71.] is 70.95
                (70, 80),
            ),
        ],
    )
    def test_summary(
        self,
        valid_times,
        data: np.ndarray,
        case_exp: GustCase,
        gust_force_exp: Optional[float],
        gust_interval_exp: Optional[tuple],
    ):
        """Test the gust summary."""
        composite = WindWeatherCompositeFactory().get(
            valid_times=valid_times, data_gust=data
        )
        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)
        summary = summary_builder.compute()

        # Test the case og summary
        selector = BaseParamBuilder.SELECTOR_KEY
        assert summary[GustSummaryBuilder.GUST][selector] == case_exp.value

        if gust_force_exp is not None:
            data_filtered: xr.DataArray = summary_builder.data.where(
                summary_builder.data > summary_builder.FORCE_MIN
            )
            gust_force = GustForce.from_term_data_array(data_filtered)
            assert gust_force.force == gust_force_exp

        if gust_interval_exp is not None:
            assert summary["gust"]["units"] == "km/h"
            assert summary["gust"]["gust_interval"] == gust_interval_exp
        else:
            with pytest.raises(KeyError):
                _ = summary["gust"]["gust_interval"]
