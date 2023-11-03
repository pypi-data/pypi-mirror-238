from mfire.text.wind.reducers.wind_summary_builder.case3.wind_block import WindBlock
from mfire.text.wind.reducers.wind_summary_builder.helpers import WindType
from mfire.text.wind.reducers.wind_summary_builder.wind_direction import (
    WindDirection,
    WindDirectionPeriod,
)
from mfire.utils.date import Datetime, Timedelta


class TestWindBlock:

    BEGIN_TIME: Datetime = Datetime(2023, 1, 1, 0, 0, 0)
    END_TIME: Datetime = Datetime(2023, 1, 1, 9, 0, 0)
    WIND_BLOCK: WindBlock = WindBlock(BEGIN_TIME, END_TIME, WindType.TYPE_3)

    def test_creation(self):

        assert self.WIND_BLOCK.begin_time == self.BEGIN_TIME
        assert self.WIND_BLOCK.end_time == self.END_TIME
        assert self.WIND_BLOCK.duration == Timedelta(self.END_TIME - self.BEGIN_TIME)

    def test_wd_period(self):
        wd_period = WindDirectionPeriod(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 4, 0, 0),
            WindDirection([10.0, 10.0]),
        )
        wd_periods = [wd_period]
        self.WIND_BLOCK.wd_periods = wd_periods
        assert self.WIND_BLOCK.wd_periods == wd_periods

        self.WIND_BLOCK.wd_periods = []
        assert self.WIND_BLOCK.wd_periods == []

        self.WIND_BLOCK.wd_periods = None
        assert self.WIND_BLOCK.wd_periods == []

        wd_period = WindDirectionPeriod(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 22, 0, 0),
            WindDirection([10.0, 10.0]),
        )
        wd_periods = [wd_period]
        self.WIND_BLOCK.wd_periods = wd_periods
        assert self.WIND_BLOCK.wd_periods == []

    def test_wf_period(self):
        wf_period = WindDirectionPeriod(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 4, 0, 0),
            WindDirection([10.0, 10.0]),
        )
        wf_periods = [wf_period]
        self.WIND_BLOCK.wf_periods = wf_periods
        assert self.WIND_BLOCK.wf_periods == wf_periods

        self.WIND_BLOCK.wf_periods = []
        assert self.WIND_BLOCK.wf_periods == []

        self.WIND_BLOCK.wf_periods = None
        assert self.WIND_BLOCK.wf_periods == []

        wf_period = WindDirectionPeriod(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 22, 0, 0),
            WindDirection([10.0, 10.0]),
        )
        wf_periods = [wf_period]
        self.WIND_BLOCK.wf_periods = wf_periods
        assert self.WIND_BLOCK.wf_periods == []
