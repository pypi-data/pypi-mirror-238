from copy import deepcopy
import pytest
import xarray as xr

from mfire.text.temperature.builders import TemperatureBuilder
from mfire.text.temperature.reducers import TemperatureSummary

from tests.text.utils import generate_valid_times

# ==============================
# Testing a Text SYNTHESIS
# ==============================


class TestTemperatureSummary:

    temperature_one_date = [[[[5, 6]]]]
    one_mask = [[[1, 1]]]
    one_time = generate_valid_times(periods=1)

    # First test case : only one date and one descriptive zone
    one_bracket_summary = {
        "high": {"location": "Zd1", "location_type": "", "min": 5, "max": 6}
    }
    test_1 = (
        [[[[5, 6]]]],
        [[[1, 1]]],
        ["Zd1"],
        generate_valid_times(periods=1),
        one_bracket_summary,
    )

    two_brackets_summary = {
        "high": {"location": "Zd1", "location_type": "", "min": 5, "max": 6},
        "low": {"location": "Zd2", "location_type": "", "min": 1, "max": 2},
    }
    test_two_brackets = (
        [[[[5, 6, 5], [1, 2, 1]]]],
        [[[1, 1, 1], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]],
        ["Zd1", "Zd2"],
        generate_valid_times(periods=1),
        two_brackets_summary,
    )

    three_brackets_summary = {
        "high": {"location": "Nord", "location_type": "", "min": 4, "max": 6},
        "low": {"location": "Sud", "location_type": "", "min": -2, "max": 0},
        "mid": {"location": "Milieu", "location_type": "", "min": 1, "max": 3},
    }
    test_three_brackets = (
        [[[[4, 5, 6], [1, 2, 3], [0, -1, -2]]]],
        [
            [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
        ],
        ["Nord", "Milieu", "Sud"],
        generate_valid_times(periods=1),
        three_brackets_summary,
    )

    # Testing that extreme values are correctly ignored (38, in this case)
    # we assume a valid threshold at 5% of the points as
    # defined by TemperatureSummary.REQUIRED_DENSITY
    non_representative_bracket_summary = {
        "high": {"location": "Nord", "location_type": "", "min": 4, "max": 6},
        "low": {"location": "Sud", "location_type": "", "min": -2, "max": 0},
        "mid": {"location": "Milieu", "location_type": "", "min": 1, "max": 3},
    }
    test_non_representative_bracket = (
        [
            [
                [
                    [4, 4, 5, 5, 6, 38],
                    [1, 1, 2, 2, 3, 3],
                    [2, 2, 2, 3, 3, 3],
                    [-2, -2, -1, -1, 0, 0],
                ]
            ]
        ],
        [
            [
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1],
            ],
        ],
        ["Nord", "Centre", "Sud"],
        generate_valid_times(periods=1),
        three_brackets_summary,
    )

    @pytest.mark.parametrize(
        "temperatures,masks,areaNames,valid_times,expected_result",
        [test_1, test_two_brackets, test_three_brackets],
    )
    def test_summary(
        self,
        temperatures: list,
        masks: list,
        areaNames: list,
        valid_times: list,
        expected_result,
    ):

        # bogus coords based on the temperature size
        lat = [i for i in range(len(temperatures[0][0]))]
        lon = [i for i in range(len(temperatures[0][0][0]))]

        areaTypes = ["" for _ in areaNames]

        masks_da = xr.DataArray(
            data=masks,
            dims=["id", "latitude", "longitude"],
            coords={
                "id": [f"{1 + i}" for i in range(len(masks))],
                "latitude": lat,
                "longitude": lon,
                "areaType": (["id"], areaTypes),
                "areaName": (["id"], areaNames),
            },
        )

        t_da = xr.DataArray(
            data=temperatures,
            dims=["id", "valid_times", "latitude", "longitude"],
            coords={
                "id": ["Tempe"],
                "valid_times": valid_times,
                "latitude": lat,
                "longitude": lon,
            },
        )

        t_summary = TemperatureSummary(t_da, masks_da)
        summary = t_summary.generate_summary()

        assert summary == expected_result

    @pytest.mark.parametrize(
        "interval, matched_values",
        [
            ("de -3 à -3°C", [("-3", "-3")]),
            ("de 0 à 0°C", [("0", "0")]),
            ("de 5 à 5°C", [("5", "5")]),
            ("de -3 à 5°C", [("-3", "5")]),
            ("de Strasbourg à 5°C", []),
        ],
    )
    def test_regex_one_value_interval(self, interval, matched_values):
        """Makes sure the regex correctly catches the two values of an interval
        (be they positive or negative)

        Args:
            phrase (str): sentence describing an interval
            match (set): the values caught by the regex
        """
        t = TemperatureBuilder()

        assert t.pattern.findall(interval) == matched_values

    minimal_summary = {"general": {"tempe": {"unit": "°C", "mini": {}, "maxi": {}}}}

    three_neg_summary = {
        "high": {"location": "dans le Nord", "location_type": "", "min": -3, "max": -3},
        "low": {"location": "dans le Sud", "location_type": "", "min": -9, "max": -7},
        "mid": {
            "location": "dans le Centre",
            "location_type": "",
            "min": -5,
            "max": -3,
        },
    }

    three_pos_summary = {
        "high": {"location": "dans le Nord", "location_type": "", "min": 6, "max": 7},
        "low": {"location": "dans le Sud", "location_type": "", "min": 2, "max": 2},
        "mid": {"location": "dans le Centre", "location_type": "", "min": 3, "max": 5},
    }

    summary_one_value_intervals = deepcopy(minimal_summary)
    summary_one_value_intervals["general"]["tempe"]["mini"] = three_neg_summary
    summary_one_value_intervals["general"]["tempe"]["maxi"] = three_pos_summary
    expected_output_one_value_intervals = (
        "Sur toute la période, températures minimales : "
        "-3°C dans le Nord, -5 à -3°C dans le Centre, -9 à -7°C dans le Sud. "
        "Températures maximales : 6 à 7°C dans le Nord, "
        "3 à 5°C dans le Centre, 2°C dans le Sud."
    )

    @pytest.mark.parametrize(
        "summary,expected_sentence",
        [(summary_one_value_intervals, expected_output_one_value_intervals)],
    )
    def test_single_value_interval(self, summary, expected_sentence):
        """makes sure both negative and positive interval are properly managed

        Args:
            summary (dict): summary to be transformed
            expeted_sentence: post processed sentence generated form the summary
        """

        t_builder = TemperatureBuilder()

        t_builder.compute(summary)

        assert t_builder.text == expected_sentence
