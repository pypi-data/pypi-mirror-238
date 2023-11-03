import pytest
import xarray as xr

from mfire.localisation.table import SummarizedTable
from mfire.utils.date import Period


class TestTable:
    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_summarized_table(self):

        full_period = Period("20190726T16", "20190727T15")
        request_time = "20190726T16"
        df = xr.Dataset()
        df.coords["period"] = [
            "20190727T06_to_20190727T09",
            "20190727T10_to_20190727T13",
            "20190727T14_to_20190727T17",
        ]
        df.coords["id"] = [f"zone{k+1}" for k in range(3)]
        df["elt"] = (("id", "period"), [[0, 1, 1], [0, 1, 1], [1, 0, 1]])

        table_handler = SummarizedTable(
            df["elt"], request_time=request_time, full_period=full_period
        )

        dout = xr.Dataset()
        dout.coords["period"] = [
            "20190727T06_to_20190727T09",
            "20190727T10_to_20190727T13",
            "20190727T14_to_20190727T17",
        ]
        dout.coords["id"] = ["zone1_+_zone2", "zone3"]
        dout["elt"] = (("id", "period"), [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0]])
        assert table_handler.get_unique_name() == "P3_3_5"
        xr.testing.assert_equal(table_handler.get_unique_table(), dout["elt"])

        df = xr.Dataset()
        df.coords["period"] = [
            "20190727T06_to_20190727T09",
            "20190727T10_to_20190727T13",
            "20190727T14_to_20190727T17",
        ]
        df.coords["id"] = [f"zone{k+1}" for k in range(3)]
        df["elt"] = (("id", "period"), [[1, 0, 0], [0, 1, 1], [1, 0, 0]])

        dout = xr.Dataset()
        dout.coords["id"] = ["zone2", "zone1_+_zone3"]
        dout.coords["period"] = [
            "20190727T06_to_20190727T09",
            "20190727T10_to_20190727T13_+_20190727T14_to_20190727T17",
        ]
        dout["elt"] = (("id", "period"), [[0.0, 1.0], [1.0, 0.0]])
        table_handler = SummarizedTable(
            df["elt"], request_time=request_time, full_period=full_period
        )
        assert table_handler.get_unique_name() == "P2_1_2"
        xr.testing.assert_equal(table_handler.get_unique_table(), dout["elt"])

    def test_merge_period_due_to_name(self):
        full_period = Period("20190726T16", "20190727T15")
        request_time = "20190726T16"
        df = xr.Dataset()
        df.coords["period"] = [
            "20190727T06_to_20190727T11",
            "20190727T14_to_20190727T15",
            "20190727T15_to_20190727T16",
        ]
        df.coords["id"] = [f"zone{k+1}" for k in range(3)]
        df["elt"] = (("id", "period"), [[0, 1, 1], [0, 1, 1], [1, 0, 1]])

        table_handler = SummarizedTable(
            df["elt"], request_time=request_time, full_period=full_period
        )

        dout = xr.Dataset()
        dout.coords["period"] = [
            "20190727T06_to_20190727T11",
            "20190727T14_to_20190727T16",
        ]
        dout.coords["id"] = ["zone1_+_zone2", "zone3"]
        dout["elt"] = (("id", "period"), [[0.0, 1.0], [1.0, 1.0]])

        xr.testing.assert_equal(table_handler.get_unique_table(), dout["elt"])
        assert table_handler.get_unique_name() == "P2_1_3"
