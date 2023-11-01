from __future__ import annotations

from typing import Optional

import numpy as np

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.wind_direction import (
    WindDirection,
    WindDirectionPeriodFinder,
)
from mfire.utils.date import Timedelta

# Logging
LOGGER = get_logger(name="wind_summary_builder.mod", bind="wind_summary_builder")


class HighWindDirectionPeriodFinder(WindDirectionPeriodFinder):
    """HighWindDirectionPeriodFinder class."""

    PERIOD_DURATION_MIN: Timedelta = Timedelta(hours=2)

    def _get_most_populated_wind_directions_of_wd_ndarray(
        self, wd_array: np.ndarray
    ) -> Optional[WindDirection]:
        """Get the most populated wind direction of an array."""
        not_nan_count: int = np.count_nonzero(~np.isnan(wd_array))
        unique_counts: list = self._get_unique_values_of_wd_array(wd_array)

        met_values: list = []
        met_points_counter: int = 0
        last_wind_direction_ok: Optional[WindDirection] = None

        for value, count in unique_counts:

            if np.isnan(value):
                continue

            met_points_counter += count
            met_values.append(value)
            met_values = [min(met_values), max(met_values)]
            percent = met_points_counter * 100.0 / not_nan_count

            # Check direction
            wind_direction: WindDirection = self._create_wind_direction_instance(
                met_values
            )

            if wind_direction is None:
                break
            else:
                last_wind_direction_ok = wind_direction

                if percent >= self.PERCENT_MIN:
                    break

        return last_wind_direction_ok
