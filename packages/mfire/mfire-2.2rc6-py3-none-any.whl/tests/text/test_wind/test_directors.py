from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import numpy as np
import pytest

import mfire
from mfire.text.wind.base import BaseParamBuilder
from mfire.text.wind.builders import GustParamsBuilder, WindParamsBuilder
from mfire.text.wind.directors import WindDirector
from mfire.text.wind.reducers.gust_summary_builder.gust_enum import GustCase
from mfire.text.wind.reducers.wind_summary_builder.helpers import WindCase
from tests.text.utils import generate_valid_times

from .factories import CompositeFactory1x1, WindWeatherCompositeFactory

FILE_PATH: Path = Path("unit_test_synthesis.txt")
FILE_PATH.unlink(missing_ok=True)


class TestDirectorsForOneParam:
    """TestDirectorsForOneParam class."""

    COMPOSITE_FACTORY: WindWeatherCompositeFactory = CompositeFactory1x1
    EXCLUDED_SUMMARY_KEYS: dict[str, list[str]] = {
        WindParamsBuilder.PARAM_NAME: [
            WindParamsBuilder.EXTRA_KEY,
            "fingerprint_raw",
            "fingerprint_filtered",
            "fingerprint_blocks",
        ]
    }
    BUILDERS: list[BaseParamBuilder] = [GustParamsBuilder, WindParamsBuilder]
    TESTED_BUILDER: BaseParamBuilder = None

    @classmethod
    def _get_fakes_builder(cls) -> BaseParamBuilder:
        """Get builder which needs to be faked."""
        for builder in cls.BUILDERS:
            if builder != cls.TESTED_BUILDER:
                return builder

    def _check(
        self,
        valid_times,
        data_gust,
        data_wf,
        data_wd,
        case_exp,
        text_exp,
    ):
        """Check directors process by testing wind data, produced summary and text."""
        # Get or set data
        if data_gust is None:
            data_gust = [0.0] * len(data_wf)
        elif data_wf is None and data_wd is None:
            data_wf = [0.0] * len(data_gust)
            data_wd = [np.nan] * len(data_gust)
        else:
            raise ValueError("Bad input arguments !")

        # Create composite
        composite = self.COMPOSITE_FACTORY.get_composite_when_term_data_is_one_number(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        # Create director
        director: WindDirector = WindDirector()

        # Run director
        text: str = director.compute(component=composite)

        # Check WindCaseNbr
        param_summary = director.reducer.summary["params"][
            self.TESTED_BUILDER.PARAM_NAME
        ]
        case_value: str = param_summary[self.TESTED_BUILDER.SELECTOR_KEY]
        assert case_value == case_exp.value

        # Check text
        assert text == text_exp


class TestGustDirectors(TestDirectorsForOneParam):
    """TestGustDirectors class."""

    TESTED_BUILDER = GustParamsBuilder

    @pytest.mark.parametrize(
        "valid_times, data_gust, case_exp, text_exp",
        [
            (
                # No gust(Case 1)
                generate_valid_times(periods=3),
                [0.0, 0.0, 0.0],
                GustCase.CASE_1,
                "Vent faible",
            ),
            (
                # No gust(Case 1)
                generate_valid_times(periods=3),
                [50.0, 51.0, 52.0],
                GustCase.CASE_2,
                "Rafales pouvant atteindre 50 à 60 km/h.",
            ),
        ],
    )
    def test(
        self,
        valid_times,
        data_gust,
        case_exp: WindCase,
        text_exp,
    ):
        """Test function which call _check method."""
        self._check(
            valid_times,
            data_gust,
            None,
            None,
            case_exp,
            text_exp,
        )


class TestWindDirectors(TestDirectorsForOneParam):
    """TestWindDirectors class."""

    TESTED_BUILDER = WindParamsBuilder

    @classmethod
    def print_title_in_file(cls, title: str):
        with open(FILE_PATH, "a") as f:
            out: str = f"# {title}:"
            f.write(f"\n{out}\n{len(out) * '-'}\n\n")

    @classmethod
    def _print_text_synthesis_in_file(cls, case_value: Optional[str], text: str):
        with open(FILE_PATH, "a") as f:
            if case_value is not None:
                res = re.match(".*_([0-9]*)$", case_value)
                case_short: str = res.group(1)
                f.write(f"cas {case_short}:\n{text}\n\n")
            else:
                f.write(f"{text}\n\n")


class TestDirectorsWindCase1(TestWindDirectors):
    """Test Directors for case 1."""

    @classmethod
    def setup_class(cls):
        cls.print_title_in_file("Case 1")

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd, case_exp, text_exp",
        [
            (
                # type 1 terms (Case 1)
                generate_valid_times(periods=3),
                [10.0, 11.0, 12.0],
                [0.0, 1.0, 2.0],
                WindCase.CASE_1,
                "Vent faible",
            )
        ],
    )
    def test(
        self,
        valid_times,
        data_wf,
        data_wd,
        case_exp: WindCase,
        text_exp: str,
    ):
        """Test function which call _check method."""
        self._check(
            valid_times,
            None,
            data_wf,
            data_wd,
            case_exp,
            text_exp,
        )
        self._print_text_synthesis_in_file(None, text_exp)


class TestDirectorsWindCase2(TestWindDirectors):
    """TestDirectorsWindCase2 class.

    Test Directors for case 2.
    """

    @classmethod
    def setup_class(cls):
        cls.print_title_in_file("Case 2")

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd, case_exp, text_exp",
        [
            (
                # Type 2 terms (Case 2):
                # All terms have a wind direction but there is not a common direction
                generate_valid_times(periods=3),
                [15.0, 16.0, 20.0],
                [0.0, 180.0, 250.0],
                WindCase.CASE_2,
                "Vent modéré de direction variable.",
            ),
            (
                # Type 1 and 2 terms (Case 2):
                # But there are not enough term to build a common wind direction period
                # (we need at least 3 type 2 terms).
                generate_valid_times(periods=3),
                [1.0, 16.0, 20.0],
                [np.nan, 180.0, 250.0],
                WindCase.CASE_2,
                "Vent faible à modéré de direction variable.",
            ),
            (
                # Type 2 terms (Case 2):
                # All terms have a wind direction but there is not a common direction
                generate_valid_times(periods=3),
                [15.0, 16.0, 20.0],
                [0.0, 20.0, 190.0],
                WindCase.CASE_2,
                "Vent modéré de direction variable.",
            ),
            (
                # Type 2 terms (Case 2):
                # The first 3 terms has a common wind direction but the last term
                # has no wind direction. So no wind direction period found.
                generate_valid_times(periods=4),
                [15.0, 16.0, 20.0, 21.0],
                [20.0, 20.0, 20.0, np.nan],
                WindCase.CASE_2,
                "Vent modéré de direction variable.",
            ),
            (
                # Only type 2 terms with the direction 270 (Case 2)
                # So There is a common wind direction: 270 ie 'Ouest'
                generate_valid_times(periods=3),
                [15.0, 16.0, 20.0],
                [270.0, 270.0, 270.0],
                WindCase.CASE_2,
                "Vent modéré d'Ouest.",
            ),
            (
                # Type 1 and 2 (Case 2)
                # All terms 2 have a wind direction which is 'Ouest'. So There is a
                # common wind direction: 270 ie 'Ouest'
                generate_valid_times(periods=4),
                [15.0, 16.0, 20.0, 1.0],
                [270.0, 270.0, 270.0, np.nan],
                WindCase.CASE_2,
                "Vent faible à modéré d'Ouest.",
            ),
            (
                # Type 2 terms (Case 2)
                # All terms 2 have a wind direction.
                # There are 3 common direction periods:
                # - period 0: term 0 to 2 with 0 direction ie 'Nord'
                # - period 1: term 3 to 5 with 160 direction ie 'Sud-Sud-Est'
                # - period 2: term 6 to 8 with 320 direction ie 'Nord-Ouest'
                generate_valid_times(periods=9),
                [15.0, 16.0, 20.0, 15.0, 16.0, 20.0, 15.0, 16.0, 20.0],
                [0.0, 0.0, 0.0, 160.0, 160.0, 160.0, 320.0, 320.0, 320.0],
                WindCase.CASE_2,
                "Vent modéré de Nord s'orientant Nord-Ouest cette fin de nuit de "
                "dimanche à lundi.",
            ),
            (
                # Type 1 and 2 terms (Case 2)
                # All terms 2 have a wind direction.
                # There are 3 common direction periods:
                # - period 0: term 0 to 2 with 0 direction ie 'Nord'
                # - period 1: term 3 to 5 with 160 direction ie 'Sud-Sud-Est'
                # - period 2: term 6 to 8 with 320 direction ie 'Nord-Ouest'
                generate_valid_times(periods=10),
                [15.0, 16.0, 20.0, 15.0, 16.0, 20.0, 15.0, 16.0, 20.0, 1.0],
                [0.0, 0.0, 0.0, 160.0, 160.0, 160.0, 320.0, 320.0, 320.0, np.nan],
                WindCase.CASE_2,
                "Vent faible à modéré de Nord s'orientant Nord-Ouest cette fin de "
                "nuit de dimanche à lundi.",
            ),
        ],
    )
    def test(
        self,
        valid_times,
        data_wf,
        data_wd,
        case_exp,
        text_exp,
    ):
        """Test function which call _check method."""
        self._check(
            valid_times,
            None,
            data_wf,
            data_wd,
            case_exp,
            text_exp,
        )
        self._print_text_synthesis_in_file(None, text_exp)


class TestDirectorsWindCase31Block(TestWindDirectors):
    """TestDirectorsWindCase31Block class

    Test Directors for case 3 with 1 block.
    """

    @classmethod
    def setup_class(cls):
        cls.print_title_in_file("Case 3 (1 block)")

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd, case_exp, text_exp",
        [
            (
                # Case 3_1B
                # - 1 wind force period: 30 km/h wind force
                # - 1 wind direction period: 0° (sympo code 0)
                generate_valid_times(periods=3),
                [30.0, 30.0, 30.0],
                [0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_1,
                "Vent de Nord, 30 à 35 km/h.",
            ),
            (
                # Case 3_1B_2
                # - 1 wind force period: 30 km/h wind force
                # - 2 wind direction period: 0° and 4° (0 and 8 sympo codes)
                generate_valid_times(periods=6),
                [30.0, 30.0, 30.0, 30.0, 30.0, 30.0],
                [0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_2,
                "Vent de Nord s'orientant Sud en ce milieu de nuit de dimanche à "
                "lundi, 30 à 35 km/h.",
            ),
            (
                # Case 3_1B_3
                # Only type 3 terms:
                # - without wind direction
                # - all terms has a 30 km/h wind force
                generate_valid_times(periods=3),
                [30.0, 30.0, 30.0],
                [np.nan, np.nan, np.nan],
                WindCase.CASE_3_1B_3,
                "Vent de direction variable, 30 à 35 km/h.",
            ),
            (
                # Case CASE_3_1B_3
                # Input Fingerprint: 222222223223222222222222
                # 2 type 3 terms with the max wind force for each of us
                generate_valid_times(periods=24),
                [15.0] * 8 + [30.0] * 1 + [15.0] * 2 + [30.0] * 1 + [15.0] * 12,
                [np.nan] * 24,
                WindCase.CASE_3_1B_3,
                "Vent de direction variable, 30 à 35 km/h.",
            ),
            (
                # Case 3_1B_4: 2 not juxtaposed force intervals WF1 < WF2
                # - 2 not juxtaposed wind force periods: 30 km/h and 40 km/h
                # - 1 wind direction period: 0° (sympo code 0)
                generate_valid_times(periods=6),
                [30.0, 30.0, 30.0, 40.0, 40.0, 40.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_4,
                "Vent de Nord, 30 à 35 km/h, se renforçant 40 à 45 km/h en ce milieu "
                "de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_4: 2 not juxtaposed force intervals WF1 > WF2
                # - 2 not juxtaposed wind force periods: 30 km/h and 40 km/h
                # - 1 wind direction period: 0° (sympo code 0)
                generate_valid_times(periods=6),
                [40.0, 40.0, 40.0, 30.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_4,
                "Vent de Nord, 40 à 45 km/h, faiblissant 30 à 35 km/h en ce milieu de "
                "nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_5: juxtaposed force intervals WF1 + 5 = WF2
                # - 2 not juxtaposed wind force periods: 30 km/h and 35 km/h
                # - 1 wind direction period: 0° (sympo code 0)
                generate_valid_times(periods=6),
                [30.0, 30.0, 30.0, 35.0, 35.0, 35.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_5,
                "Vent de Nord, 30 à 40 km/h.",
            ),
            (
                # Case 3_1B_5: juxtaposed force intervals WF1 = WF2 + 5
                # - 2 not juxtaposed wind force periods: 35 km/h and 30 km/h
                # - 1 wind direction period: 0° (sympo code 0)
                generate_valid_times(periods=6),
                [35.0, 35.0, 35.0, 30.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_5,
                "Vent de Nord, 30 à 40 km/h.",
            ),
            (
                # Case 3_1B_6
                # - 2 not juxtaposed wind force periods WF1 < WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are not simultaneous
                generate_valid_times(periods=7),
                [30.0, 30.0, 30.0, 40.0, 40.0, 40.0, 40.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_6,
                "Vent de Nord s'orientant Sud, 30 à 35 km/h, se renforçant 40 à 45 "
                "km/h en ce milieu de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_6
                # - 2 not juxtaposed wind force periods WF1 > WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are not simultaneous
                generate_valid_times(periods=7),
                [40.0, 40.0, 40.0, 30.0, 30.0, 30.0, 30.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_6,
                "Vent de Nord s'orientant Sud, 40 à 45 km/h, faiblissant 30 à 35 km/h "
                "en ce milieu de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_7
                # - 2 not juxtaposed wind force periods WF1 < WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are simultaneous
                generate_valid_times(periods=7),
                [30.0, 30.0, 30.0, 30.0, 40.0, 40.0, 40.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_7,
                "Vent de Nord, 30 à 35 km/h, se renforçant 40 à 45 km/h avec une "
                "orientation Sud cette fin de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_7
                # - 2 not juxtaposed wind force periods WF1 > WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are simultaneous
                generate_valid_times(periods=7),
                [40.0, 40.0, 40.0, 40.0, 30.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_7,
                "Vent de Nord, 40 à 45 km/h, faiblissant 30 à 35 km/h avec une "
                "orientation Sud cette fin de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_8
                # - 2 juxtaposed wind force periods WF1 < WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are simultaneous
                generate_valid_times(periods=7),
                [30.0, 30.0, 30.0, 30.0, 35.0, 35.0, 35.0],  # WF1 < WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_8,
                "Vent de Nord s'orientant Sud cette fin de nuit de dimanche à lundi, "
                "30 à 40 km/h.",
            ),
            (
                # Case 3_1B_8
                # - 2 juxtaposed wind force periods WF1 > WF2
                # - 2 wind direction period: 0° and 180°
                # wf and wd changes are simultaneous
                generate_valid_times(periods=7),
                [35.0, 35.0, 35.0, 35.0, 30.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_8,
                "Vent de Nord s'orientant Sud cette fin de nuit de dimanche à lundi, "
                "30 à 40 km/h.",
            ),
            (
                # Case 3_1B_9
                # - 2 not juxtaposed wind force periods WF1 < WF2
                # - no wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=4),
                [30.0, 30.0, 40.0, 40.0],  # WF1 < WF2
                [0.0, 0.0, np.nan, np.nan],
                WindCase.CASE_3_1B_9,
                "Vent de direction variable, 30 à 35 km/h, se renforçant 40 à 45 km/h "
                "en ce milieu de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_1B_9
                # - 2 not juxtaposed wind force periods WF1 > WF2
                # - no wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=4),
                [40.0, 40.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, np.nan, np.nan],
                WindCase.CASE_3_1B_9,
                "Vent de direction variable, 40 à 45 km/h, faiblissant 30 à 35 km/h "
                "en ce milieu de nuit de dimanche à lundi.",
            ),
            (
                # Case CASE_3_1B_9
                # Input Fingerprint: 222222223223222222222222
                # 2 type 3 terms: the max wind force is on the second term
                generate_valid_times(periods=24),
                [15.0] * 8 + [30.0] * 1 + [15.0] * 2 + [40.0] * 1 + [15.0] * 12,
                [np.nan] * 24,
                WindCase.CASE_3_1B_9,
                "Vent de direction variable, 30 à 35 km/h, se renforçant 40 à 45 km/h "
                "ce lundi en matinée.",
            ),
            (
                # Case CASE_3_1B_9
                # Input Fingerprint: 222222223223222322222222
                # 3 type 3 terms: the max wind force is on the second and the third term
                generate_valid_times(periods=24),
                [15.0] * 8
                + [30.0] * 1
                + [15.0] * 2
                + [40.0] * 1
                + [15.0] * 3
                + [40.0] * 1
                + [15.0] * 8,
                [np.nan] * 24,
                WindCase.CASE_3_1B_9,
                "Vent de direction variable, 30 à 35 km/h, se renforçant 40 à 45 km/h "
                "ce lundi en matinée.",
            ),
            (
                # Case 3_1B_10
                # - 2 juxtaposed wind force periods WF1 < WF2
                # - no wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=4),
                [30.0, 30.0, 35.0, 35.0],  # WF1 < WF2
                [0.0, 0.0, np.nan, np.nan],
                WindCase.CASE_3_1B_10,
                "Vent de direction variable, 30 à 40 km/h.",
            ),
            (
                # Case 3_1B_10
                # - 2 juxtaposed wind force periods WF1 > WF2
                # - no wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=4),
                [35.0, 35.0, 30.0, 30.0],  # WF1 > WF2
                [0.0, 0.0, np.nan, np.nan],
                WindCase.CASE_3_1B_10,
                "Vent de direction variable, 30 à 40 km/h.",
            ),
            (
                # Case 3_1B_11
                # - variable wind forces: 3 wf periods 35km/h, 50 km/h, 40 km/h
                # - 1 wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=3),
                [39.0, 46.0, 40.0],
                [0.0, 0.0, 0.0],
                WindCase.CASE_3_1B_11,
                "Vent de Nord, entre 35 et 50 km/h.",
            ),
            (
                # Case 3_1B_12
                # - variable wind forces: 6 wf periods
                # - 2 wind direction periods
                # wf and wd changes are simultaneous
                generate_valid_times(periods=6),
                [39.0, 46.0, 40.0, 39.0, 46.0, 40.0],
                [0.0, 0.0, 0.0, 180.0, 180.0, 180.0],
                WindCase.CASE_3_1B_12,
                "Vent de Nord s'orientant Sud en ce milieu de nuit de dimanche à "
                "lundi, entre 35 et 50 km/h.",
            ),
            (
                # Case 3_1B_13
                # - variable wind forces: 3 wf periods 35km/h, 45 km/h, 40 km/h
                # - no wind direction period
                # wf and wd changes are simultaneous
                generate_valid_times(periods=3),
                [39.0, 46.0, 40.0],
                [0.0, 180.0, np.nan],
                WindCase.CASE_3_1B_13,
                "Vent de direction variable, entre 35 et 50 km/h.",
            ),
        ],
    )
    def test_one_type3_block(
        self,
        valid_times,
        data_wf,
        data_wd,
        case_exp: WindCase,
        text_exp,
    ):
        """Test when there is 1 type 3 WIndBlock."""
        self._check(
            valid_times,
            None,
            data_wf,
            data_wd,
            case_exp,
            text_exp,
        )
        self._print_text_synthesis_in_file(case_exp.value, text_exp)


class TestDirectorsWindCase32Blocks(TestWindDirectors):
    """TestDirectorsWindCase32Blocks class.

    Test Directors for case 3 with 2 blocks.
    """

    @classmethod
    def setup_class(cls):
        cls.print_title_in_file("Case 3 (2 blocks)")

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd, case_exp, text_exp",
        [
            (
                # Case 3_2B_1
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD0 = WD1 = 0° (sympo code 0)
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 24,
                WindCase.CASE_3_2B_1,
                "Vent de Nord, 30 à 35 km/h, la nuit de dimanche à lundi jusqu'au "
                "petit matin ainsi que ce lundi après-midi jusqu'en première partie "
                "de nuit prochaine.",
            ),
            (
                # Case 3_2B_2
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD0 = 0° != WD1 = 90°
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 7 + [np.nan] * 8 + [90.0] * 9,
                WindCase.CASE_3_2B_2,
                "Vent 30 à 35 km/h, de Nord en première partie de nuit de dimanche à "
                "lundi s'orientant Est aujourd'hui lundi en milieu de journée.",
            ),
            (
                # Case 3_2B_3
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD0 = 0°, no WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 7 + [np.nan] * 17,
                WindCase.CASE_3_2B_3,
                "Vent 30 à 35 km/h, de Nord la nuit de dimanche à lundi jusqu'au "
                "petit matin.",
            ),
            (
                # Case 3_2B_4
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - no WD0, WD1 = 0°
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [np.nan] * 15 + [0] * 9,
                WindCase.CASE_3_2B_4,
                "Vent 30 à 35 km/h, de Nord ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_5
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD00, WD01 and WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 8 + [271.0] * 9,
                WindCase.CASE_3_2B_5,
                "Vent 30 à 35 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "de Nord puis Sud-Est, et ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine d'Ouest.",
            ),
            (
                # Case 3_2B_6
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD00, WD01 and no WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 17,
                WindCase.CASE_3_2B_6,
                "Vent 30 à 35 km/h, de Nord en première partie de nuit de dimanche à "
                "lundi s'orientant Sud-Est cette fin de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_2B_7
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD0, WD10 and WD1
                generate_valid_times(periods=24),
                [30.0] * 9 + [15.0] * 8 + [30.0] * 7,
                [271.0] * 9 + [np.nan] * 8 + [0.0] * 4 + [136.0] * 3,
                WindCase.CASE_3_2B_7,
                "Vent 30 à 35 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "d'Ouest, et ce lundi après-midi et première partie de nuit prochaine "
                "de Nord puis Sud-Est.",
            ),
            (
                # Case 3_2B_8
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - no WD00 and WD10, WD11
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [np.nan] * 15 + [0.0] * 4 + [136.0] * 5,
                WindCase.CASE_3_2B_8,
                "Vent 30 à 35 km/h, de Nord aujourd'hui lundi en milieu de journée "
                "s'orientant Sud-Est ce lundi en soirée.",
            ),
            (
                # Case 3_2B_9
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - WD00, WD01 and WD10, WD11
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 8 + [22.5] * 4 + [158.0] * 5,
                WindCase.CASE_3_2B_9,
                "Vent 30 à 35 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "de Nord puis Sud-Est, et ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine de Nord-Nord-Est puis Sud-Sud-Est.",
            ),
            (
                # Case 3_2B_10
                # Input Fingerprint: 333333322222222333333333
                # - WF0 = WF1 = 30 km/h
                # - no WD
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [30.0] * 9,
                [np.nan] * 24,
                WindCase.CASE_3_2B_10,
                "Vent de direction variable, 30 à 35 km/h, la nuit de dimanche à "
                "lundi jusqu'au petit matin ainsi que ce lundi après-midi jusqu'en "
                "première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_12
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD0 = WD1 = 0° (sympo code 0)
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 24,
                WindCase.CASE_3_2B_12,
                "Vent de Nord, 30 à 40 km/h, la nuit de dimanche à lundi jusqu'au "
                "petit matin ainsi que ce lundi après-midi jusqu'en première partie "
                "de nuit prochaine.",
            ),
            (
                # Case 3_2B_14
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD0 = 0° != WD1 = 90°
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 7 + [np.nan] * 8 + [90.0] * 9,
                WindCase.CASE_3_2B_14,
                "Vent 30 à 40 km/h, de Nord en première partie de nuit de dimanche à "
                "lundi s'orientant Est aujourd'hui lundi en milieu de journée.",
            ),
            (
                # Case 3_2B_16
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD0 = 0°, no WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 7 + [np.nan] * 17,
                WindCase.CASE_3_2B_16,
                "Vent 30 à 40 km/h, de Nord la nuit de dimanche à lundi jusqu'au "
                "petit matin.",
            ),
            (
                # Case 3_2B_18
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - no WD0, WD1 = 0°
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 15 + [0.0] * 9,
                WindCase.CASE_3_2B_18,
                "Vent 30 à 40 km/h, de Nord ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_20
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD00, WD01 and WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 8 + [271.0] * 9,
                WindCase.CASE_3_2B_20,
                "Vent 30 à 40 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "de Nord puis Sud-Est, et ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine d'Ouest.",
            ),
            (
                # Case 3_2B_22
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD00 , WD01 and no WD1
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 3 + [136.0] * 4 + [np.nan] * 17,
                WindCase.CASE_3_2B_22,
                "Vent 30 à 40 km/h, de Nord en première partie de nuit de dimanche à "
                "lundi s'orientant Sud-Est en ce milieu de nuit de dimanche à lundi.",
            ),
            (
                # Case 3_2B_24
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD0, WD10 and WD11
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [271.0] * 7 + [np.nan] * 8 + [0.0] * 4 + [136.0] * 5,
                WindCase.CASE_3_2B_24,
                "Vent 30 à 40 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "d'Ouest, et ce lundi après-midi jusqu'en première partie de nuit "
                "prochaine de Nord puis Sud-Est.",
            ),
            (
                # Case 3_2B_26
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - no WD0 , WD10 and WD11
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 15 + [0.0] * 4 + [136.0] * 5,
                WindCase.CASE_3_2B_26,
                "Vent 30 à 40 km/h, de Nord aujourd'hui lundi en milieu de journée "
                "s'orientant Sud-Est ce lundi en soirée.",
            ),
            (
                # Case 3_2B_28
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - WD0, WD1, WD10 and WD12
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 8 + [22.5] * 4 + [158.0] * 5,
                WindCase.CASE_3_2B_28,
                "Vent 30 à 40 km/h, la nuit de dimanche à lundi jusqu'au petit matin "
                "de Nord puis Sud-Est, et ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine de Nord-Nord-Est puis Sud-Sud-Est.",
            ),
            (
                # Case 3_2B_30
                # Input Fingerprint: 333333322222222333333333
                # - WF0 30 km/h juxtaposed with WF1
                # - no WD
                generate_valid_times(periods=24),
                [30.0] * 7 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 24,
                WindCase.CASE_3_2B_30,
                "Vent de direction variable, 30 à 40 km/h, la nuit de dimanche à "
                "lundi jusqu'au petit matin ainsi que ce lundi après-midi jusqu'en "
                "première partie de nuit prochaine.",
            ),
        ],
    )
    def test_two_type3_blocks(
        self,
        valid_times,
        data_wf,
        data_wd,
        case_exp: WindCase,
        text_exp,
    ):
        """Test when there are 2 type 3 WindBlocks."""
        self._check(
            valid_times,
            None,
            data_wf,
            data_wd,
            case_exp,
            text_exp,
        )
        self._print_text_synthesis_in_file(case_exp.value, text_exp)

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd, case_exp, text_exp",
        [
            (
                # Case 3_2B_11
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0 = WD1 = 0° (sympo code 0)
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [0.0] * 24,
                WindCase.CASE_3_2B_11,
                "Vent de Nord, 30 à 35 km/h la nuit de dimanche à lundi jusqu'à "
                "lundi après-midi, 45 à 50 km/h ce lundi soir et première partie de "
                "nuit prochaine.",
            ),
            (
                # Case 3_2B_13
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0 = 0° and WD1 = 140°
                # WF and WD changes are not simultaneous
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [0.0] * 16 + [np.nan] * 4 + [140.0] * 4,
                WindCase.CASE_3_2B_13,
                "Vent de Nord, 30 à 35 km/h la nuit de dimanche à lundi jusqu'à lundi "
                "après-midi, puis 45 à 50 km/h avec une orientation Sud-Est ce lundi "
                "soir et première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_15
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0 = 0°, no WD1
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [0.0] * 16 + [np.nan] * 8,
                WindCase.CASE_3_2B_15,
                "Vent de Nord, 30 à 35 km/h la nuit de dimanche à lundi jusqu'à lundi "
                "après-midi, 45 à 50 km/h ce lundi soir et première partie de nuit "
                "prochaine.",
            ),
            (
                # Case 3_2B_17
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - no WD0, WD1 = 0°
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [np.nan] * 20 + [0.0] * 4,
                WindCase.CASE_3_2B_17,
                "Vent 30 à 35 km/h la nuit de dimanche à lundi jusqu'à lundi "
                "après-midi, 45 à 50 km/h de Nord ce lundi soir et première partie de "
                "nuit prochaine.",
            ),
            (
                # Case 3_2B_19
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD00, WD01 and WD1
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [0.0] * 8 + [136.0] * 8 + [np.nan] * 4 + [271.0] * 4,
                WindCase.CASE_3_2B_19,
                "Vent de Nord s'orientant Ouest, 30 à 35 km/h, la nuit de dimanche à "
                "lundi jusqu'à lundi après-midi, 45 à 50 km/h ce lundi soir et "
                "première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_21
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD00, WD01 and no WD1
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [0.0] * 8 + [136.0] * 8 + [np.nan] * 8,
                WindCase.CASE_3_2B_21,
                "Vent de Nord s'orientant Sud-Est, 30 à 35 km/h, la nuit de dimanche "
                "à lundi jusqu'à lundi après-midi, 45 à 50 km/h ce lundi soir et "
                "première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_23
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0, WD10 and WD12
                generate_valid_times(periods=24),
                [34.9] * 10 + [15.0] * 4 + [45.0] * 10,
                [0.0] * 10 + [np.nan] * 4 + [135.0] * 5 + [271.0] * 5,
                WindCase.CASE_3_2B_23,
                "Vent de Nord s'orientant Ouest, 30 à 35 km/h, la nuit de dimanche à "
                "lundi jusqu'en matinée lundi, 45 à 50 km/h ce lundi après-midi "
                "jusqu'en première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_25
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - no WD0, WD10 and WD12
                generate_valid_times(periods=24),
                [34.9] * 10 + [15.0] * 4 + [45.0] * 10,
                [np.nan] * 14 + [0.0] * 5 + [136.0] * 5,
                WindCase.CASE_3_2B_25,
                "Vent de Nord s'orientant Sud-Est, 30 à 35 km/h, la nuit de dimanche à "
                "lundi jusqu'en matinée lundi, 45 à 50 km/h ce lundi après-midi "
                "jusqu'en première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_27
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0, WD1, WD10 and WD12
                generate_valid_times(periods=24),
                [34.9] * 10 + [15.0] * 4 + [45.0] * 10,
                [0.0] * 5 + [136.0] * 5 + [np.nan] * 4 + [22.5] * 5 + [158.0] * 5,
                WindCase.CASE_3_2B_27,
                "Vent de Nord s'orientant Sud-Sud-Est, 30 à 35 km/h, la nuit de "
                "dimanche à lundi jusqu'en matinée lundi, 45 à 50 km/h ce lundi "
                "après-midi jusqu'en première partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_29
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - no WD0
                generate_valid_times(periods=24),
                [34.9] * 16 + [15.0] * 4 + [45.0] * 4,
                [np.nan] * 24,
                WindCase.CASE_3_2B_29,
                "Vent de direction variable, 30 à 35 km/h la nuit de dimanche à lundi "
                "jusqu'à lundi après-midi, 45 à 50 km/h ce lundi soir et première "
                "partie de nuit prochaine.",
            ),
            (
                # Case 3_2B_31
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - Wd0, no WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 24,
                WindCase.CASE_3_2B_31,
                "Vent de Nord, entre 30 et 50 km/h.",
            ),
            (
                # Case 3_2B_32
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD0, WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 7 + [np.nan] * 8 + [90.0] * 9,
                WindCase.CASE_3_2B_32,
                "Vent de Nord en première partie de nuit de dimanche à lundi "
                "s'orientant Est aujourd'hui lundi en milieu de journée, entre 30 et "
                "50 km/h.",
            ),
            (
                # Case 3_2B_33
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD0, no WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 7 + [np.nan] * 17,
                WindCase.CASE_3_2B_33,
                "Vent de Nord la nuit de dimanche à lundi jusqu'au petit matin, "
                "entre 30 et 50 km/h.",
            ),
            (
                # Case 3_2B_34
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - no WD0, WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 15 + [0.0] * 9,
                WindCase.CASE_3_2B_34,
                "Vent de Nord ce lundi après-midi jusqu'en première partie de nuit "
                "prochaine, entre 30 et 50 km/h.",
            ),
            (
                # Case 3_2B_35
                # Input Fingerprint: 333333333333333322223333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD00, WD01 and WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 8 + [271.0] * 9,
                WindCase.CASE_3_2B_35,
                "Vent entre 30 et 50 km/h, la nuit de dimanche à lundi jusqu'au petit "
                "matin de Nord puis Sud-Est, et ce lundi après-midi jusqu'en première "
                "partie de nuit prochaine d'Ouest.",
            ),
            (
                # Case 3_2B_36
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD00, WD01 and no WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 4 + [136.0] * 3 + [np.nan] * 17,
                WindCase.CASE_3_2B_36,
                "Vent de Nord en première partie de nuit de dimanche à lundi "
                "s'orientant Sud-Est cette fin de nuit de dimanche à lundi, entre 30 "
                "et 50 km/h.",
            ),
            (
                # Case 3_2B_37
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD0, WD10, WD11
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 7 + [np.nan] * 8 + [135.0] * 4 + [271.0] * 5,
                WindCase.CASE_3_2B_37,
                "Vent entre 30 et 50 km/h, la nuit de dimanche à lundi jusqu'au petit "
                "matin de Nord, et ce lundi après-midi jusqu'en première partie de "
                "nuit prochaine de Sud-Est puis Ouest.",
            ),
            (
                # Case 3_2B_38
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - WD00, WD01 and no WD1
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 7 + [np.nan] * 8 + [0.0] * 4 + [136.0] * 5,
                WindCase.CASE_3_2B_38,
                "Vent de Nord aujourd'hui lundi en milieu de journée s'orientant "
                "Sud-Est ce lundi en soirée, entre 30 et 50 km/h.",
            ),
            (
                # Case 3_2B_39
                # Input Fingerprint: 333333333333333322223333
                # - WF0 != WF1 not juxtaposed
                # - WD0, WD1, WD10 and WD12
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [0.0] * 3 + [136.0] * 4 + [np.nan] * 8 + [22.5] * 5 + [158.0] * 4,
                WindCase.CASE_3_2B_39,
                "Vent entre 30 et 50 km/h, de Nord en première partie de nuit de "
                "dimanche à lundi s'orientant Sud-Sud-Est ce lundi en soirée.",
            ),
            (
                # Case 3_2B_40
                # Input Fingerprint: 333333322222222333333333
                # - WF00 = 30 km/h, WF01 = 50 km/h, WF1 = 40 km/h
                # - no WD
                generate_valid_times(periods=24),
                [34.9] * 3 + [45.0] * 4 + [15.0] * 8 + [35.0] * 9,
                [np.nan] * 24,
                WindCase.CASE_3_2B_40,
                "Vent de direction variable, entre 30 et 50 km/h.",
            ),
        ],
    )
    def test_two_type3_blocks_threshold_minus_num_11(
        self,
        valid_times,
        data_wf,
        data_wd,
        case_exp: WindCase,
        text_exp,
    ):
        """Test when there are 2 type 3 WindBlocks with THRESHOLD_MINUS_NUM = 11."""
        builder = mfire.text.wind.reducers.wind_summary_builder.WindSummaryBuilder
        builder.THRESHOLD_MINUS_NUM = 11
        self._check(
            valid_times,
            None,
            data_wf,
            data_wd,
            case_exp,
            text_exp,
        )
        builder.THRESHOLD_MINUS_NUM = 10
        self._print_text_synthesis_in_file(case_exp.value, text_exp)


class TestDirectors:
    """TestDirectors class."""

    COMPOSITE_FACTORY: WindWeatherCompositeFactory = CompositeFactory1x1

    def _check(
        self,
        valid_times,
        data_gust,
        data_wf,
        data_wd,
        text_exp,
    ):
        """Check directors resulting text."""

        # Create composite
        composite = self.COMPOSITE_FACTORY.get_composite_when_term_data_is_one_number(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        # Create director
        director: WindDirector = WindDirector()

        # Run director
        text: str = director.compute(component=composite)

        # Check text
        assert text == text_exp

    @pytest.mark.parametrize(
        "valid_times, data_gust, data_wf, data_wd, text_exp",
        [
            (
                # No wind, no gust
                generate_valid_times(periods=3),
                [0.0] * 3,
                [0.0] * 3,
                [np.nan] * 3,
                "Vent faible",
            ),
            (
                # Only wind with type 1
                generate_valid_times(periods=3),
                [0.0] * 3,
                [14.0] * 3,
                [np.nan] * 3,
                "Vent faible",
            ),
            (
                # Only wind with type 2
                generate_valid_times(periods=3),
                [0.0] * 3,
                [16.0] * 3,
                [np.nan] * 3,
                "Vent modéré de direction variable.",
            ),
            (
                # Only Gust
                generate_valid_times(periods=3),
                [60.0] * 3,
                [np.nan] * 3,
                [np.nan] * 3,
                "Rafales pouvant atteindre 60 à 70 km/h.",
            ),
            (
                # Gust and type 1 wind
                generate_valid_times(periods=3),
                [60.0] * 3,
                [14.0] * 3,
                [np.nan] * 3,
                "Rafales pouvant atteindre 60 à 70 km/h.",
            ),
            (
                # Gust and type 2 wind
                generate_valid_times(periods=3),
                [60.0] * 3,
                [16.0] * 3,
                [np.nan] * 3,
                "Vent modéré de direction variable. Rafales pouvant atteindre 60 à "
                "70 km/h.",
            ),
        ],
    )
    def test(self, valid_times, data_gust, data_wf, data_wd, text_exp):
        """Test function which call _check method."""
        self._check(
            valid_times,
            data_gust,
            data_wf,
            data_wd,
            text_exp,
        )


class TestWindDirectorExtra:
    """TestWindDirectorExtra class."""

    class WindDirectorWithExtra(WindDirector):
        WITH_EXTRA: bool = True

    class WindDirectorWithoutExtra(WindDirector):
        WITH_EXTRA: bool = False

    @pytest.mark.parametrize(
        "valid_times, data_gust, data_wf, data_wd",
        [
            (
                # Gust and type 2 wind
                generate_valid_times(periods=3),
                [60.0] * 3,
                [16.0] * 3,
                [np.nan] * 3,
            )
        ],
    )
    def test(self, valid_times, data_gust, data_wf, data_wd):
        """Test extra content produced by a director."""
        # Create composite
        composite = CompositeFactory1x1.get_composite_when_term_data_is_one_number(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        director = self.WindDirectorWithExtra()
        _, extra_content_text = director._compute_synthesis_elements(composite)
        assert extra_content_text is not None

        director = self.WindDirectorWithoutExtra()
        _, extra_content_text = director._compute_synthesis_elements(composite)
        assert extra_content_text is None
