from __future__ import annotations

from typing import Optional

import numpy as np
import xarray as xr

from mfire.text.wind.reducers.wind_summary_builder.helpers import (
    BaseWindPeriodFinder,
    PandasWindSummary,
)
from mfire.utils.date import Datetime

from .wind_force import WindForce, WindForcePeriod


class WindForcePeriodFinder(BaseWindPeriodFinder[WindForce]):
    def _get_term_period(
        self,
        term_data: xr.DataArray,
        pd_summary: PandasWindSummary,
    ) -> Optional[WindForcePeriod]:
        """Compute the WindForcePeriod of the input term data."""

        wind_force: WindForce = WindForce.from_term_data_array(term_data)

        valid_time: np.datetime64 = term_data.valid_time.values

        return WindForcePeriod(
            pd_summary.get_term_previous_time(valid_time),
            Datetime(valid_time),
            wind_force,
        )

    def post_process_periods(
        self, periods_list: list[WindForcePeriod]
    ) -> list[WindForcePeriod]:
        """Post process found periods."""
        return periods_list

    def _update_period(
        self, period1: WindForcePeriod, period2: WindForcePeriod
    ) -> Optional[WindForcePeriod]:
        update_res: bool = period1.update(period2)
        if update_res:
            return period1
        return None
