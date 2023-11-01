from __future__ import annotations

import copy
from typing import Optional

import numpy as np
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers import (
    BaseWindPeriod,
    BaseWindPeriodFinder,
    PandasWindSummary,
)
from mfire.utils.date import Datetime, Timedelta

from .wind_direction import WindDirection, WindDirectionPeriod

# Logging
LOGGER = get_logger(name="wind_summary_builder.mod", bind="wind_summary_builder")


class WindDirectionPeriodFinder(BaseWindPeriodFinder[WindDirection]):

    DEGREES_SECTOR_SIZE: float = 22.5
    TERM_DIRECTION_SIZE_MAX: float = 4 * DEGREES_SECTOR_SIZE
    MULTIPLE_TERMS_DIRECTION_SIZE_MAX: float = 6 * DEGREES_SECTOR_SIZE
    PERIOD_DURATION_MIN: Timedelta = Timedelta(hours=3)
    PERCENT_MIN: float = 100.0

    def check_terms(self) -> bool:
        """Check all data terms."""
        return False if not self._term_periods else True

    @staticmethod
    def _get_unique_values_of_wd_array(wd_array: np.ndarray) -> list:
        """Get all unique values of a wind direction array."""
        unique, count = np.unique(wd_array, return_counts=True)
        unique_counts = list(zip(unique, count))
        unique_counts.sort(key=lambda e: e[1], reverse=True)
        return unique_counts

    def _get_most_populated_wind_directions_of_wd_ndarray(
        self, wd_array: np.ndarray
    ) -> Optional[WindDirection]:
        """Get the most populated wind direction of an array."""
        not_nan_count: int = np.count_nonzero(~np.isnan(wd_array))
        unique_counts: list = self._get_unique_values_of_wd_array(wd_array)

        met_values: list = []
        met_points_counter: int = 0

        for value, count in unique_counts:

            if np.isnan(value):
                continue

            met_points_counter += count
            met_values.append(value)
            percent = met_points_counter * 100.0 / not_nan_count

            if percent >= self.PERCENT_MIN:
                return WindDirection(met_values)

        return None

    def _create_wind_direction_instance(
        self, degrees: list[float]
    ) -> Optional[WindDirection]:
        """Create a WindDirection from a degrees list."""
        wind_direction = WindDirection(copy.deepcopy(degrees))
        check: bool = wind_direction.check_size(self.TERM_DIRECTION_SIZE_MAX)
        return wind_direction if check else None

    def _get_term_period(
        self,
        term_data: xr.DataArray,
        pd_summary: PandasWindSummary,
    ) -> Optional[WindDirectionPeriod]:
        """Compute the WindDirectionPeriod of the input term data."""

        wd = self._get_most_populated_wind_directions_of_wd_ndarray(term_data.values)

        if wd is None:
            return None

        valid_time: np.datetime64 = term_data.valid_time.values

        # Keep wind direction if its check is OK
        if wd.check_size(self.TERM_DIRECTION_SIZE_MAX):
            return WindDirectionPeriod(
                pd_summary.get_term_previous_time(valid_time), Datetime(valid_time), wd
            )

        return None

    def _update_period(
        self, period1: WindDirectionPeriod, period2: WindDirectionPeriod
    ) -> Optional[WindDirectionPeriod]:
        update_res: bool = period1.update(
            period2, size_max=self.MULTIPLE_TERMS_DIRECTION_SIZE_MAX
        )
        if update_res:
            return period1
        return None

    def _check_description_period_coverage(self, periods_list) -> bool:
        """Check if the beginning and the end of the description period are covered.

        It checks if:
        - the first period start at the beginning of the descriptive period
        - the last period ends et the end of the descriptive period.
        """
        if not periods_list:
            return False

        if (
            periods_list[0].begin_time == self._time_bounds[0]
            and periods_list[-1].end_time == self._time_bounds[1]
        ):
            return True
        return False

    def _find_periods(self) -> list[BaseWindPeriod[WindDirection]]:
        """Find all wind direction periods as a list.

        If a term has no wind direction, then the result is an empty list.
        """
        periods: list[BaseWindPeriod[WindDirection]]

        if self.check_terms() is False:
            periods = []
        else:
            periods = super()._find_periods()

        return periods

    def post_process_periods(
        self, periods: list[WindDirectionPeriod]
    ) -> list[WindDirectionPeriod]:
        """Post process found periods."""

        # Keep only periods with at have at least a 3 hours duration
        filtered_periods: list[WindDirectionPeriod] = []

        for period in periods:
            if period.duration >= self.PERIOD_DURATION_MIN:
                filtered_periods.append(period)

        if self._check_description_period_coverage(filtered_periods):

            # If a WindDirectionPeriod found: just keep this period
            if len(filtered_periods) == 1:
                pass

            # Else keep the first and the last periods
            else:
                filtered_periods = [filtered_periods[0], filtered_periods[-1]]
        else:
            filtered_periods = []

        return filtered_periods
