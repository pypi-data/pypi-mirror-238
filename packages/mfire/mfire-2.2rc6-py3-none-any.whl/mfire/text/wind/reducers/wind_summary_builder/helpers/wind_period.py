from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

import numpy as np
import pandas as pd
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers import (
    PandasWindSummary,
    SummaryKeysMixin,
)
from mfire.utils.date import Datetime, Period, Timedelta

# Logging
LOGGER = get_logger(name="wind_period.mod", bind="wind_period")

WindElement = TypeVar("WindElement")


class WindPeriodMixin:
    def __init__(
        self,
        begin_time: Datetime,
        end_time: Datetime,
    ):
        if begin_time > end_time:
            raise ValueError(f"begin_time '{begin_time}' > end_time '{end_time}'")
        self._period: Period = Period(begin_time, end_time)

    @property
    def begin_time(self) -> Datetime:
        """begin_time

        Returns:
            Datetime: Beginning of the period
        """
        return self._period.begin_time

    @property
    def end_time(self) -> Datetime:
        """end_time

        Returns:
            Datetime: End of the period
        """
        return self._period.end_time

    @property
    def period(self) -> Period:
        return self._period

    @property
    def duration(self) -> Timedelta:
        return self._period.duration


class BaseWindPeriod(SummaryKeysMixin, WindPeriodMixin, ABC, Generic[WindElement]):
    """BaseWindPeriod abstract class."""

    def __init__(
        self,
        begin_time: Datetime,
        end_time: Datetime,
        wind_element: WindElement,
    ):
        if begin_time > end_time:
            raise ValueError(f"begin_time '{begin_time}' > end_time '{end_time}'")
        self._period: Period = Period(begin_time, end_time)
        super().__init__(begin_time, end_time)
        self._wind_element: WindElement = wind_element

    @property
    def wind_element(self) -> WindElement:
        return self._wind_element

    @wind_element.setter
    def wind_element(self, wind_element: WindElement) -> None:
        self._wind_element = wind_element

    def __eq__(self, other: Optional[BaseWindPeriod]) -> bool:
        if other is None:
            return False
        return self.period == other.period and self.wind_element == other.wind_element

    def __add__(self, other: BaseWindPeriod) -> BaseWindPeriod:
        """Add 2 WindPeriod instances."""
        # Get the WindPeriod with the maximum end_time
        p_max: BaseWindPeriod = max(self, other, key=lambda b: b.end_time)

        return self.__class__(
            min(self.begin_time, other.begin_time),
            p_max.end_time,
            self.wind_element + other.wind_element,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.period,
                self.wind_element,
            )
        )

    def update(self, other: BaseWindPeriod, **kwargs):
        """Update the period with a Datetime and a WindForce."""
        if self.end_time > other.begin_time:
            LOGGER.warning(
                f"Try to update a {self.__class__.__name__} with another which has a "
                f"too early begin_time !"
            )
            return False
        return True

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the WindPeriod instance."""
        return {
            self.BEGIN_TIME_MARKER: self.begin_time.describe_as_period(
                reference_datetime
            ),
            self.END_TIME_MARKER: self.end_time.describe_as_period(reference_datetime),
            self.TIME_DESC: self.period.describe(reference_datetime),
        }


class BaseWindPeriodFinder(ABC, Generic[WindElement]):
    """BaseWindPeriodFinder class."""

    def __init__(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray | pd.Index,
    ):
        self._term_periods: list[Optional[BaseWindPeriod]] = []
        self._time_bounds: list[np.ndarray] = []

        self._get_term_periods(data_array, pd_summary, valid_times)
        self._ind_max: int = len(self._term_periods) - 1
        self._ind: int = 0

    @property
    def term_periods(self) -> list[Optional[WindElement]]:
        """Get the term periods list."""
        return self._term_periods

    def _prepare_pd_summary(self, pd_summary: PandasWindSummary) -> None:
        """Prepare the PandasWindSummary before getting terms data.

        It is called in the _get_term_periods() method.
        """
        pass

    def _get_term_periods(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray,
    ) -> None:
        """Compute the period of all terms contained in the input data_array.

        Notes
        -----
        This method fills term_periods attribute.
        """

        for valid_time in valid_times:

            term_data: xr.DataArray = data_array.sel(valid_time=valid_time)

            # Get term data
            self._term_periods.append(self._get_term_period(term_data, pd_summary))

        self._time_bounds = [
            pd_summary.get_term_previous_time(valid_times[0]),
            Datetime(valid_times[-1]),
        ]

    @abstractmethod
    def _get_term_period(
        self,
        term_data: xr.DataArray,
        pd_summary: PandasWindSummary,
    ) -> Optional[BaseWindPeriod[WindElement]]:
        """Compute the period of the given term."""
        pass

    @staticmethod
    def _add_periods_to_pd_summary(
        periods_list: list[BaseWindPeriod],
        pd_summary: PandasWindSummary,
        col_name: str,
    ):
        """Add the periods of a list in a PandasWindSummary."""
        pd_summary.create_column(col_name)

        cnt = 0

        for period in periods_list:
            loc: slice = slice(
                period.begin_time.as_np_datetime64(),
                period.end_time.as_np_datetime64(),
            )
            pd_summary.data.loc[loc, col_name] = cnt
            cnt += 1

    @abstractmethod
    def _update_period(
        self, period1: BaseWindPeriod, period2: BaseWindPeriod
    ) -> Optional[BaseWindPeriod]:
        pass

    def _find_periods(self) -> list[BaseWindPeriod]:
        """Find all wind periods as a list."""

        # Initialize the index
        self._ind = 0

        period_prev: Optional[BaseWindPeriod] = None
        periods = []

        while self._ind <= self._ind_max:

            period_cur: Optional[BaseWindPeriod] = self._term_periods[self._ind]

            if period_prev is None:
                period_prev = period_cur
            elif period_cur is None:
                periods.append(period_prev)
                period_prev = None
            else:
                period_updated: Optional[BaseWindPeriod] = self._update_period(
                    period_prev, period_cur
                )

                # If the update succeeded, then continue
                if period_updated is None:
                    periods.append(period_prev)
                    period_prev = period_cur

            self._ind += 1

        if period_prev is not None:
            periods.append(period_prev)

        return periods

    @abstractmethod
    def post_process_periods(
        self, periods_list: list[BaseWindPeriod]
    ) -> list[BaseWindPeriod]:
        """Post process found periods."""
        pass

    def run(self) -> list[BaseWindPeriod]:
        """Run the period finder."""
        periods: list[BaseWindPeriod] = self._find_periods()

        if periods:
            periods = self.post_process_periods(periods)

        return periods
