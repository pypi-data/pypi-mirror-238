import datetime as dt

import numpy.random as npr
import pytest
import xarray as xr

from mfire.localisation.temporal_localisation import TemporalLocalisation


class TestTemporalLocalisation:
    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_temporal(self):
        # On fixe la seed afin d'avoir une reproductibilité des résultats.
        npr.seed(0)
        # Test fait sur 4 zones et 40 pas de temps
        din = xr.Dataset()
        din.coords["valid_time"] = [
            dt.datetime(2019, 1, 1) + dt.timedelta(hours=i) for i in range(40)
        ]
        din.coords["id"] = ["A" + str(i) for i in range(4)]
        din["elt"] = (("valid_time", "id"), npr.binomial(1, 0.1, (40, 4)))
        temp_loc = TemporalLocalisation(din["elt"])
        dout = temp_loc.new_division()

        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T02_to_20190101T06",
            "20190101T07_to_20190101T21",
            "20190101T22_to_20190102T13",
        ]
        expected_result["id"] = ["A0", "A1", "A2", "A3"]
        expected_result["elt"] = (
            ("period", "id"),
            [[1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0]],
        )
        xr.testing.assert_equal(expected_result["elt"], dout)

        # On teste le fait de ne pas trimmer les périodes
        temp_loc.update(trim_period=False)
        dout = temp_loc.new_division()
        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T00_to_20190101T06",
            "20190101T07_to_20190101T21",
            "20190101T22_to_20190102T15",
        ]
        expected_result["id"] = ["A0", "A1", "A2", "A3"]
        expected_result["elt"] = (
            ("period", "id"),
            [[1.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0]],
        )
        xr.testing.assert_equal(expected_result["elt"], dout)

        # Test avec des données sur une période plus courte
        din = xr.Dataset()
        din.coords["valid_time"] = [
            dt.datetime(2019, 1, 1) + dt.timedelta(hours=i) for i in range(4)
        ]
        din.coords["id"] = ["A" + str(i) for i in range(2)]
        din["elt"] = (
            ("valid_time", "id"),
            [[True, True], [False, True], [True, True], [False, True]],
        )

        temp_loc = TemporalLocalisation(din["elt"])
        dout = temp_loc.new_division()
        expected_result = xr.Dataset()
        expected_result["period"] = ["20190101T00_to_20190101T03"]
        expected_result["id"] = ["A0", "A1"]
        expected_result["elt"] = (("period", "id"), [[1.0, 1]])

        xr.testing.assert_equal(expected_result["elt"], dout)

    def test_different_tempo(self):
        din = xr.Dataset()
        din.coords["valid_time"] = [
            dt.datetime(2019, 1, 1) + dt.timedelta(hours=i) for i in range(7)
        ]
        din.coords["id"] = ["A" + str(i) for i in range(2)]
        din["elt"] = (
            ("valid_time", "id"),
            [
                [False, True],
                [False, True],
                [False, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True],
            ],
        )
        temp_loc = TemporalLocalisation(din["elt"])
        dout = temp_loc.new_division()

        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T00_to_20190101T02",
            "20190101T03_to_20190101T06",
        ]
        expected_result["id"] = ["A0", "A1"]
        expected_result["elt"] = (("period", "id"), [[0.0, 1], [1.0, 1.0]])
        xr.testing.assert_equal(expected_result["elt"], dout)
        dout = temp_loc.new_division(delta_h=2)
        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T00_to_20190101T02",
            "20190101T03_to_20190101T04",
            "20190101T05_to_20190101T06",
        ]
        expected_result["id"] = ["A0", "A1"]
        expected_result["elt"] = (("period", "id"), [[0.0, 1], [1.0, 1.0], [1.0, 1.0]])

        xr.testing.assert_equal(expected_result["elt"], dout)

    def test_large_tempo(self):
        din = xr.Dataset()
        din.coords["valid_time"] = [
            dt.datetime(2019, 1, 1) + dt.timedelta(hours=i) for i in range(12)
        ]
        din.coords["id"] = ["A" + str(i) for i in range(2)]
        din["elt"] = (
            ("valid_time", "id"),
            [
                [False, True],
                [False, True],
                [False, True],
                [False, True],
                [False, True],
                [True, True],
                [True, True],
                [True, True],
                [True, True],
                [False, True],
                [False, True],
                [False, True],
            ],
        )
        temp_loc = TemporalLocalisation(din["elt"])
        dout = temp_loc.new_division(delta_h=3)
        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T00_to_20190101T04",
            "20190101T05_to_20190101T08",
            "20190101T09_to_20190101T11",
        ]
        expected_result["id"] = ["A0", "A1"]
        expected_result["elt"] = (("period", "id"), [[0.0, 1], [1.0, 1.0], [0.0, 1.0]])
        xr.testing.assert_equal(expected_result["elt"], dout)

        dout = temp_loc.new_division(delta_h=5)
        expected_result = xr.Dataset()
        expected_result["period"] = [
            "20190101T00_to_20190101T04",
            "20190101T05_to_20190101T11",
        ]
        expected_result["id"] = ["A0", "A1"]
        expected_result["elt"] = (("period", "id"), [[0.0, 1], [1.0, 1.0]])
        xr.testing.assert_equal(expected_result["elt"], dout)

        # On teste le fait de ne pas trimmer les périodes
        temp_loc.update(trim_period=False)
        dout = temp_loc.new_division(delta_h=5)
        xr.testing.assert_equal(expected_result["elt"], dout)
