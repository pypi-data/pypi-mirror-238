import pytest

from mfire.text.wind.builders import WindBuilder


class TestWindBuilder:
    @pytest.mark.parametrize(
        "summary",
        [
            (
                {
                    "params": {
                        "gust": {
                            "case": "gust_case_2",
                            "units": "km/h",
                            "gust_interval": (50, 60),
                        },
                        "wind": {"case": "bad_case"},
                    }
                }
            ),
            (
                {
                    "params": {
                        "gust": {"case": "bad_case"},
                        "wind": {
                            "case": "wind_case_2",
                            "units": "km/h",
                            "wf_intensity": "modéré",
                            "wd_periods": [],
                        },
                    }
                }
            ),
            (
                {
                    "params": {
                        "wind": {
                            "case": "wind_case_2",
                            "units": "km/h",
                            "wf_intensity": "modéré",
                            "wd_periods": [],
                        }
                    }
                }
            ),
            (
                {
                    "params": {
                        "gust": {
                            "case": "gust_case_2",
                            "units": "km/h",
                            "gust_interval": (50, 60),
                        },
                    }
                }
            ),
        ],
    )
    def test_bad_summary(self, summary):
        builder: WindBuilder = WindBuilder()
        text, _ = builder.compute(summary)

        assert text == "Erreur dans la génération des synthèses de vent"
