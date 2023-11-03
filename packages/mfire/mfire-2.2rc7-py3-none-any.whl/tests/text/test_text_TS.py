from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from random import sample
from typing import Optional
from unittest.mock import patch

import numpy as np
import pytest

from mfire.text.text_manager import TextManager
from mfire.text.weather import (
    WeatherBuilder,
    WeatherDirector,
    WeatherReducer,
    WeatherSelector,
)
from mfire.utils import JsonFile, recursive_format
from mfire.utils.date import Timedelta
from tests.composite.factories import WeatherCompositeFactory
from tests.utils.test_wwmf_utils import dataset_wwmf_label


class TestWeatherSelector:
    def test_0_ts(self):
        selector = WeatherSelector()
        reduction = {}
        assert selector.compute(reduction) == "0xTS"

    @pytest.mark.parametrize(
        "temp,loc,severe,expected",
        [
            (None, None, False, "1xTS"),
            ("temp", None, False, "1xTS_temp"),
            (None, "loc", False, "1xTS_loc"),
            ("temp", "loc", False, "1xTS_temp_loc"),
            (None, None, True, "1xTS_severe"),
            ("temp", None, True, "1xTS_temp_severe"),
            (None, "loc", True, "1xTS_loc_severe"),
            ("temp", "loc", True, "1xTS_temp_loc_severe"),
        ],
    )
    def test_1_ts(self, temp, loc, severe, expected):
        selector = WeatherSelector()
        reduction = {
            "TS1": {
                "temporality": temp,
                "localisation": loc,
                "label": ...,
            }
        }
        if severe:
            reduction["TSsevere"] = ...
        assert selector.compute(reduction) == expected

    @pytest.mark.parametrize(
        "temp1,loc1,temp2,loc2,severe,expected",
        [
            # without severe sentence
            (None, None, None, None, False, "2xTS"),
            ("temp", None, None, None, False, "2xTS_temp1"),
            ("temp", "loc", None, None, False, "2xTS_temp1_loc1"),
            ("temp", None, None, "loc", False, "2xTS_temp1_loc2"),
            ("temp", "loc", None, "loc", False, "2xTS_temp1_loc"),
            (None, None, "temp", None, False, "2xTS_temp2"),
            (None, "loc", "temp", None, False, "2xTS_temp2_loc1"),
            (None, None, "temp", "loc", False, "2xTS_temp2_loc2"),
            (None, "loc", "temp", "loc", False, "2xTS_temp2_loc"),
            ("temp", None, "temp", None, False, "2xTS_temp"),
            ("temp", "loc", "temp", None, False, "2xTS_temp_loc1"),
            ("temp", None, "temp", "loc", False, "2xTS_temp_loc2"),
            ("temp", "loc", "temp", "loc", False, "2xTS_temp_loc"),
            (None, "loc", None, None, False, "2xTS_loc1"),
            (None, None, None, "loc", False, "2xTS_loc2"),
            (None, "loc", None, "loc", False, "2xTS_loc"),
            # with severe sentence
            (None, None, None, None, True, "2xTS_severe"),
            ("temp", None, None, None, True, "2xTS_temp1_severe"),
            (None, None, "temp", None, True, "2xTS_temp2_severe"),
            ("temp", None, "temp", None, True, "2xTS_temp_severe"),
            # We can't have location and severe sentence
            (None, "loc", "temp", None, True, "2xTS_temp2_severe"),
            ("temp", "loc", "temp", None, True, "2xTS_temp_severe"),
            ("temp", "loc", None, None, True, "2xTS_temp1_severe"),
            ("temp", None, None, "loc", True, "2xTS_temp1_severe"),
            ("temp", "loc", None, "loc", True, "2xTS_temp1_severe"),
            (None, None, "temp", "loc", True, "2xTS_temp2_severe"),
            (None, "loc", "temp", "loc", True, "2xTS_temp2_severe"),
            ("temp", None, "temp", "loc", True, "2xTS_temp_severe"),
            ("temp", "loc", "temp", "loc", True, "2xTS_temp_severe"),
            (None, None, None, "loc", True, "2xTS_severe"),
            (None, "loc", None, "loc", True, "2xTS_severe"),
            (None, "loc", None, None, True, "2xTS_severe"),
        ],
    )
    def test_2_ts(self, temp1, loc1, temp2, loc2, severe, expected):
        selector = WeatherSelector()
        reduction = {
            "TS1": {
                "temporality": temp1,
                "localisation": loc1,
                "label": ...,
            },
            "TS2": {
                "temporality": temp2,
                "localisation": loc2,
                "label": ...,
            },
        }
        if severe:
            reduction["TSsevere"] = ...
        assert selector.compute(reduction) == expected

    @pytest.mark.parametrize(
        "temp1,loc1,temp2,loc2,temp3,loc3,expected",
        [
            # without loc
            (None, None, None, None, None, None, "3xTS"),
            ("temp", None, None, None, None, None, "3xTS_temp1"),
            (None, None, "temp", None, None, None, "3xTS_temp2"),
            (None, None, None, None, "temp", None, "3xTS_temp3"),
            ("temp", None, "temp", None, None, None, "3xTS_temp12"),
            ("temp", None, None, None, "temp", None, "3xTS_temp13"),
            (None, None, "temp", None, "temp", None, "3xTS_temp23"),
            ("temp", None, "temp", None, "temp", None, "3xTS_temp123"),
            # with loc
            (None, "loc", None, None, None, None, "3xTS_loc1"),
            ("temp", "loc", None, None, None, None, "3xTS_temp1_loc1"),
            (None, "loc", "temp", None, None, None, "3xTS_temp2_loc1"),
            (None, "loc", None, None, "temp", None, "3xTS_temp3_loc1"),
            ("temp", "loc", "temp", None, None, None, "3xTS_temp12_loc1"),
            ("temp", "loc", None, None, "temp", None, "3xTS_temp13_loc1"),
            (None, "loc", "temp", None, "temp", None, "3xTS_temp23_loc1"),
            ("temp", "loc", "temp", None, "temp", None, "3xTS_temp123_loc1"),
            (None, None, None, "loc", None, None, "3xTS_loc2"),
            ("temp", None, None, "loc", None, None, "3xTS_temp1_loc2"),
            (None, None, "temp", "loc", None, None, "3xTS_temp2_loc2"),
            (None, None, None, "loc", "temp", None, "3xTS_temp3_loc2"),
            ("temp", None, "temp", "loc", None, None, "3xTS_temp12_loc2"),
            ("temp", None, None, "loc", "temp", None, "3xTS_temp13_loc2"),
            (None, None, "temp", "loc", "temp", None, "3xTS_temp23_loc2"),
            ("temp", None, "temp", "loc", "temp", None, "3xTS_temp123_loc2"),
            (None, None, None, None, None, "loc", "3xTS_loc3"),
            ("temp", None, None, None, None, "loc", "3xTS_temp1_loc3"),
            (None, None, "temp", None, None, "loc", "3xTS_temp2_loc3"),
            (None, None, None, None, "temp", "loc", "3xTS_temp3_loc3"),
            ("temp", None, "temp", None, None, "loc", "3xTS_temp12_loc3"),
            ("temp", None, None, None, "temp", "loc", "3xTS_temp13_loc3"),
            (None, None, "temp", None, "temp", "loc", "3xTS_temp23_loc3"),
            ("temp", None, "temp", None, "temp", "loc", "3xTS_temp123_loc3"),
            (None, "loc", None, "loc", None, None, "3xTS_loc12"),
            ("temp", "loc", None, "loc", None, None, "3xTS_temp1_loc12"),
            (None, "loc", "temp", "loc", None, None, "3xTS_temp2_loc12"),
            (None, "loc", None, "loc", "temp", None, "3xTS_temp3_loc12"),
            ("temp", "loc", "temp", "loc", None, None, "3xTS_temp12_loc12"),
            ("temp", "loc", None, "loc", "temp", None, "3xTS_temp13_loc12"),
            (None, "loc", "temp", "loc", "temp", None, "3xTS_temp23_loc12"),
            ("temp", "loc", "temp", "loc", "temp", None, "3xTS_temp123_loc12"),
            (None, "loc", None, None, None, "loc", "3xTS_loc13"),
            ("temp", "loc", None, None, None, "loc", "3xTS_temp1_loc13"),
            (None, "loc", "temp", None, None, "loc", "3xTS_temp2_loc13"),
            (None, "loc", None, None, "temp", "loc", "3xTS_temp3_loc13"),
            ("temp", "loc", "temp", None, None, "loc", "3xTS_temp12_loc13"),
            ("temp", "loc", None, None, "temp", "loc", "3xTS_temp13_loc13"),
            (None, "loc", "temp", None, "temp", "loc", "3xTS_temp23_loc13"),
            ("temp", "loc", "temp", None, "temp", "loc", "3xTS_temp123_loc13"),
            (None, None, None, "loc", None, "loc", "3xTS_loc23"),
            ("temp", None, None, "loc", None, "loc", "3xTS_temp1_loc23"),
            (None, None, "temp", "loc", None, "loc", "3xTS_temp2_loc23"),
            (None, None, None, "loc", "temp", "loc", "3xTS_temp3_loc23"),
            ("temp", None, "temp", "loc", None, "loc", "3xTS_temp12_loc23"),
            ("temp", None, None, "loc", "temp", "loc", "3xTS_temp13_loc23"),
            (None, None, "temp", "loc", "temp", "loc", "3xTS_temp23_loc23"),
            ("temp", None, "temp", "loc", "temp", "loc", "3xTS_temp123_loc23"),
        ],
    )
    def test_3_ts(self, temp1, loc1, temp2, loc2, temp3, loc3, expected):
        selector = WeatherSelector()
        reduction = {
            "TS1": {
                "temporality": temp1,
                "localisation": loc1,
                "label": ...,
            },
            "TS2": {
                "temporality": temp2,
                "localisation": loc2,
                "label": ...,
            },
            "TS3": {
                "temporality": temp3,
                "localisation": loc3,
                "label": ...,
            },
        }
        assert selector.compute(reduction) == expected

    def test_unimplemented(self):
        selector = WeatherSelector()
        reduction = {
            "TS1": ...,
            "TS2": ...,
            "TS3": ...,
            "TS4": ...,
        }
        assert selector.compute(reduction) == "Unimplemented"


class TestWeatherBuilder:
    def test_0_ts(self):
        builder = WeatherBuilder()
        reduction = {}

        builder.compute(reduction)
        assert builder.text == "Pas de phénomène météorologique à enjeu."

    @pytest.mark.parametrize(
        "temp,loc,severe,expected",
        [
            (None, None, None, "Neige."),
            ("Le mercredi matin", None, None, "Le mercredi matin, neige."),
            (None, "au-dessus de 500m", None, "Neige au-dessus de 500m."),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                None,
                "Le mercredi matin, neige au-dessus de 500m.",
            ),
            (
                None,
                None,
                "orages violents",
                "Neige. Autres phénomènes sévères : orages violents.",
            ),
            (
                "Le mercredi matin",
                None,
                "orages violents",
                "Le mercredi matin, neige. Autres phénomènes sévères : orages "
                "violents.",
            ),
            (
                None,
                "au-dessus de 500m",
                "orages violents",
                "Neige au-dessus de 500m. Autres phénomènes sévères : orages "
                "violents.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                "orages violents",
                "Le mercredi matin, neige au-dessus de 500m. Autres phénomènes sévères "
                ": orages violents.",
            ),
        ],
    )
    def test_1_ts(self, temp, loc, severe, expected):
        builder = WeatherBuilder()
        reduction = {
            "TS1": {
                "label": "Neige" if temp is None else "neige",
                "temporality": temp,
                "localisation": loc,
            }
        }
        if severe is not None:
            reduction["TSsevere"] = severe
        builder.compute(reduction)
        assert builder.text == expected

    @pytest.mark.parametrize(
        "temp1,loc1,temp2,loc2,severe,expected",
        [
            # without severe phenomenon
            (None, None, None, None, None, "Neige faible. Neige."),
            (
                "Le mercredi matin",
                None,
                None,
                None,
                None,
                "Le mercredi matin, neige faible. Neige.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                None,
                None,
                None,
                "Le mercredi matin, neige faible au-dessus de 500m. Neige.",
            ),
            (
                "Le mercredi matin",
                None,
                None,
                "au-dessus de 800m",
                None,
                "Le mercredi matin, neige faible. Neige au-dessus de 800m.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                None,
                "au-dessus de 800m",
                None,
                "Le mercredi matin, neige faible au-dessus de 500m. Neige au-dessus de "
                "800m.",
            ),
            (
                None,
                None,
                "Le jeudi matin",
                None,
                None,
                "Neige faible. Le jeudi matin, neige.",
            ),
            (
                None,
                "au-dessus de 500m",
                "Le jeudi matin",
                None,
                None,
                "Neige faible au-dessus de 500m. Le jeudi matin, neige.",
            ),
            (
                None,
                None,
                "Le jeudi matin",
                "au-dessus de 800m",
                None,
                "Neige faible. Le jeudi matin, neige au-dessus de 800m.",
            ),
            (
                None,
                "au-dessus de 500m",
                "Le jeudi matin",
                "au-dessus de 800m",
                None,
                "Neige faible au-dessus de 500m. Le jeudi matin, neige au-dessus de "
                "800m.",
            ),
            (
                "Le mercredi matin",
                None,
                "Le jeudi matin",
                None,
                None,
                "Le mercredi matin, neige faible. Le jeudi matin, neige.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                "Le jeudi matin",
                None,
                None,
                "Le mercredi matin, neige faible au-dessus de 500m. Le jeudi matin, "
                "neige.",
            ),
            (
                "Le mercredi matin",
                None,
                "Le jeudi matin",
                "au-dessus de 800m",
                None,
                "Le mercredi matin, neige faible. Le jeudi matin, neige au-dessus de "
                "800m.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                "Le jeudi matin",
                "au-dessus de 800m",
                None,
                "Le mercredi matin, neige faible au-dessus de 500m. Le jeudi matin, "
                "neige au-dessus de 800m.",
            ),
            (
                None,
                "au-dessus de 500m",
                None,
                None,
                None,
                "Neige faible au-dessus de 500m. Neige.",
            ),
            (
                None,
                None,
                None,
                "au-dessus de 800m",
                None,
                "Neige faible. Neige au-dessus de 800m.",
            ),
            (
                None,
                "au-dessus de 500m",
                None,
                "au-dessus de 800m",
                None,
                "Neige faible au-dessus de 500m. Neige au-dessus de 800m.",
            ),
            # with severe phenomenon
            (
                None,
                None,
                None,
                None,
                "orages violents",
                "Neige faible. Neige. Autres phénomènes sévères : orages violents.",
            ),
            (
                "Le mercredi matin",
                None,
                None,
                None,
                "orages violents",
                "Le mercredi matin, neige faible. Neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                None,
                None,
                "Le jeudi matin",
                None,
                "orages violents",
                "Neige faible. Le jeudi matin, neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                "Le mercredi matin",
                None,
                "Le jeudi matin",
                None,
                "orages violents",
                "Le mercredi matin, neige faible. Le jeudi matin, neige. Autres "
                "phénomènes sévères : orages violents.",
            ),
            # We can't have location and severe sentence
            (
                None,
                "au-dessus de 500m",
                None,
                None,
                "orages violents",
                "Neige faible. Neige. Autres phénomènes sévères : orages violents.",
            ),
            (
                None,
                None,
                None,
                "au-dessus de 800m",
                "orages violents",
                "Neige faible. Neige. Autres phénomènes sévères : orages violents.",
            ),
            (
                None,
                "au-dessus de 500m",
                None,
                "au-dessus de 800m",
                "orages violents",
                "Neige faible. Neige. Autres phénomènes sévères : orages violents.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                None,
                None,
                "orages violents",
                "Le mercredi matin, neige faible. Neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                "Le mercredi matin",
                None,
                None,
                "au-dessus de 800m",
                "orages violents",
                "Le mercredi matin, neige faible. Neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                None,
                "au-dessus de 800m",
                "orages violents",
                "Le mercredi matin, neige faible. Neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                None,
                "au-dessus de 500m",
                "Le jeudi matin",
                None,
                "orages violents",
                "Neige faible. Le jeudi matin, neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                None,
                None,
                "Le jeudi matin",
                "au-dessus de 800m",
                "orages violents",
                "Neige faible. Le jeudi matin, neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                None,
                "au-dessus de 500m",
                "Le jeudi matin",
                "au-dessus de 800m",
                "orages violents",
                "Neige faible. Le jeudi matin, neige. Autres phénomènes sévères : "
                "orages violents.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                "Le jeudi matin",
                None,
                "orages violents",
                "Le mercredi matin, neige faible. Le jeudi matin, neige. Autres "
                "phénomènes sévères : orages violents.",
            ),
            (
                "Le mercredi matin",
                None,
                "Le jeudi matin",
                "au-dessus de 800m",
                "orages violents",
                "Le mercredi matin, neige faible. Le jeudi matin, neige. Autres "
                "phénomènes sévères : orages violents.",
            ),
            (
                "Le mercredi matin",
                "au-dessus de 500m",
                "Le jeudi matin",
                "au-dessus de 800m",
                "orages violents",
                "Le mercredi matin, neige faible. Le jeudi matin, neige. Autres "
                "phénomènes sévères : orages violents.",
            ),
        ],
    )
    def test_2_ts(self, temp1, loc1, temp2, loc2, severe, expected):
        builder = WeatherBuilder()

        reduction = {
            "TS1": {
                "label": "Neige faible" if temp1 is None else "neige faible",
                "temporality": temp1,
                "localisation": loc1,
            },
            "TS2": {
                "label": "Neige" if temp2 is None else "neige",
                "temporality": temp2,
                "localisation": loc2,
            },
        }
        if severe is not None:
            reduction["TSsevere"] = severe
        builder.compute(reduction)
        assert builder.text == expected

    @pytest.mark.parametrize(
        "temp1,loc1,temp2,loc2,temp3,loc3,expected",
        [
            # without loc
            (
                None,
                None,
                None,
                None,
                None,
                None,
                "Neige faible. Neige modérée. Neige forte.",
            ),
            (
                "Mardi",
                None,
                None,
                None,
                None,
                None,
                "Mardi, neige faible. Neige modérée. Neige forte.",
            ),
            (
                None,
                None,
                "Mercredi",
                None,
                None,
                None,
                "Neige faible. Mercredi, neige modérée. Neige forte.",
            ),
            (
                None,
                None,
                None,
                None,
                "Jeudi",
                None,
                "Neige faible. Neige modérée. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                None,
                None,
                None,
                "Mardi, neige faible. Mercredi, neige modérée. Neige forte.",
            ),
            (
                "Mardi",
                None,
                None,
                None,
                "Jeudi",
                None,
                "Mardi, neige faible. Neige modérée. Jeudi, neige forte.",
            ),
            (
                None,
                None,
                "Mercredi",
                None,
                "Jeudi",
                None,
                "Neige faible. Mercredi, neige modérée. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                None,
                "Jeudi",
                None,
                "Mardi, neige faible. Mercredi, neige modérée. Jeudi, neige forte.",
            ),
            # with loc
            (
                None,
                "à loc 1",
                None,
                None,
                None,
                None,
                "Neige faible à loc 1. Neige modérée. Neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                None,
                None,
                None,
                "Mardi, neige faible à loc 1. Neige modérée. Neige forte.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                None,
                None,
                None,
                "Neige faible à loc 1. Mercredi, neige modérée. Neige forte.",
            ),
            (
                None,
                "à loc 1",
                None,
                None,
                "Jeudi",
                None,
                "Neige faible à loc 1. Neige modérée. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                None,
                None,
                None,
                "Mardi, neige faible à loc 1. Mercredi, neige modérée. Neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                None,
                "Jeudi",
                None,
                "Mardi, neige faible à loc 1. Neige modérée. Jeudi, neige forte.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                None,
                "Jeudi",
                None,
                "Neige faible à loc 1. Mercredi, neige modérée. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                None,
                "Jeudi",
                None,
                "Mardi, neige faible à loc 1. Mercredi, neige modérée. Jeudi, neige "
                "forte.",
            ),
            (
                None,
                None,
                None,
                "à loc 2",
                None,
                None,
                "Neige faible. Neige modérée à loc 2. Neige forte.",
            ),
            (
                "Mardi",
                None,
                None,
                "à loc 2",
                None,
                None,
                "Mardi, neige faible. Neige modérée à loc 2. Neige forte.",
            ),
            (
                None,
                None,
                "Mercredi",
                "à loc 2",
                None,
                None,
                "Neige faible. Mercredi, neige modérée à loc 2. Neige forte.",
            ),
            (
                None,
                None,
                None,
                "à loc 2",
                "Jeudi",
                None,
                "Neige faible. Neige modérée à loc 2. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                "à loc 2",
                None,
                None,
                "Mardi, neige faible. Mercredi, neige modérée à loc 2. Neige forte.",
            ),
            (
                "Mardi",
                None,
                None,
                "à loc 2",
                "Jeudi",
                None,
                "Mardi, neige faible. Neige modérée à loc 2. Jeudi, neige forte.",
            ),
            (
                None,
                None,
                "Mercredi",
                "à loc 2",
                "Jeudi",
                None,
                "Neige faible. Mercredi, neige modérée à loc 2. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                "à loc 2",
                "Jeudi",
                None,
                "Mardi, neige faible. Mercredi, neige modérée à loc 2. Jeudi, neige "
                "forte.",
            ),
            (
                None,
                None,
                None,
                None,
                None,
                "à loc 3",
                "Neige faible. Neige modérée. " "Neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                None,
                None,
                None,
                "à loc 3",
                "Mardi, neige faible. Neige modérée. Neige forte à loc 3.",
            ),
            (
                None,
                None,
                "Mercredi",
                None,
                None,
                "à loc 3",
                "Neige faible. Mercredi, neige modérée. Neige forte à loc 3.",
            ),
            (
                None,
                None,
                None,
                None,
                "Jeudi",
                "à loc 3",
                "Neige faible. Neige modérée. Jeudi, neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                None,
                None,
                "à loc 3",
                "Mardi, neige faible. Mercredi, neige modérée. Neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                None,
                None,
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible. Neige modérée. Jeudi, neige forte à loc 3.",
            ),
            (
                None,
                None,
                "Mercredi",
                None,
                "Jeudi",
                "à loc 3",
                "Neige faible. Mercredi, neige modérée. Jeudi, neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                None,
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible. Mercredi, neige modérée. Jeudi, neige forte à "
                "loc 3.",
            ),
            (
                None,
                "à loc 1",
                None,
                "à loc 2",
                None,
                None,
                "Neige faible à loc 1. Neige modérée à loc 2. Neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                "à loc 2",
                None,
                None,
                "Mardi, neige faible à loc 1. Neige modérée à loc 2. Neige forte.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                "à loc 2",
                None,
                None,
                "Neige faible à loc 1. Mercredi, neige modérée à loc 2. Neige forte.",
            ),
            (
                None,
                "à loc 1",
                None,
                "à loc 2",
                "Jeudi",
                None,
                "Neige faible à loc 1. Neige modérée à loc 2. Jeudi, neige forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                "à loc 2",
                None,
                None,
                "Mardi, neige faible à loc 1. Mercredi, neige modérée à loc 2. Neige "
                "forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                "à loc 2",
                "Jeudi",
                None,
                "Mardi, neige faible à loc 1. Neige modérée à loc 2. Jeudi, neige "
                "forte.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                "à loc 2",
                "Jeudi",
                None,
                "Neige faible à loc 1. Mercredi, neige modérée à loc 2. Jeudi, neige "
                "forte.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                "à loc 2",
                "Jeudi",
                None,
                "Mardi, neige faible à loc 1. Mercredi, neige modérée à loc 2. Jeudi, "
                "neige forte.",
            ),
            (
                None,
                "à loc 1",
                None,
                None,
                None,
                "à loc 3",
                "Neige faible à loc 1. Neige modérée. Neige forte à loc 3.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                None,
                None,
                "à loc 3",
                "Mardi, neige faible à loc 1. Neige modérée. Neige forte à loc 3.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                None,
                None,
                "à loc 3",
                "Neige faible à loc 1. Mercredi, neige modérée. Neige forte à loc 3.",
            ),
            (
                None,
                "à loc 1",
                None,
                None,
                "Jeudi",
                "à loc 3",
                "Neige faible à loc 1. Neige modérée. Jeudi, neige forte à loc 3.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                None,
                None,
                "à loc 3",
                "Mardi, neige faible à loc 1. Mercredi, neige modérée. Neige forte à "
                "loc 3.",
            ),
            (
                "Mardi",
                "à loc 1",
                None,
                None,
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible à loc 1. Neige modérée. Jeudi, neige forte à "
                "loc 3.",
            ),
            (
                None,
                "à loc 1",
                "Mercredi",
                None,
                "Jeudi",
                "à loc 3",
                "Neige faible à loc 1. Mercredi, neige modérée. Jeudi, neige forte à "
                "loc 3.",
            ),
            (
                "Mardi",
                "à loc 1",
                "Mercredi",
                None,
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible à loc 1. Mercredi, neige modérée. Jeudi, neige "
                "forte à loc 3.",
            ),
            (
                None,
                None,
                None,
                "à loc 2",
                None,
                "à loc 3",
                "Neige faible. Neige modérée à loc 2. Neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                None,
                "à loc 2",
                None,
                "à loc 3",
                "Mardi, neige faible. Neige modérée à loc 2. Neige forte à loc 3.",
            ),
            (
                None,
                None,
                "Mercredi",
                "à loc 2",
                None,
                "à loc 3",
                "Neige faible. Mercredi, neige modérée à loc 2. Neige forte à loc 3.",
            ),
            (
                None,
                None,
                None,
                "à loc 2",
                "Jeudi",
                "à loc 3",
                "Neige faible. Neige modérée à loc 2. Jeudi, neige forte à loc 3.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                "à loc 2",
                None,
                "à loc 3",
                "Mardi, neige faible. Mercredi, neige modérée à loc 2. Neige forte à "
                "loc 3.",
            ),
            (
                "Mardi",
                None,
                None,
                "à loc 2",
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible. Neige modérée à loc 2. Jeudi, neige forte à "
                "loc 3.",
            ),
            (
                None,
                None,
                "Mercredi",
                "à loc 2",
                "Jeudi",
                "à loc 3",
                "Neige faible. Mercredi, neige modérée à loc 2. Jeudi, neige forte à "
                "loc 3.",
            ),
            (
                "Mardi",
                None,
                "Mercredi",
                "à loc 2",
                "Jeudi",
                "à loc 3",
                "Mardi, neige faible. Mercredi, neige modérée à loc 2. Jeudi, neige "
                "forte à loc 3.",
            ),
        ],
    )
    def test_3_ts(self, temp1, loc1, temp2, loc2, temp3, loc3, expected):
        builder = WeatherBuilder()
        reduction = {
            "TS1": {
                "temporality": temp1,
                "localisation": loc1,
                "label": "Neige faible" if temp1 is None else "neige faible",
            },
            "TS2": {
                "temporality": temp2,
                "localisation": loc2,
                "label": "Neige modérée" if temp2 is None else "neige modérée",
            },
            "TS3": {
                "temporality": temp3,
                "localisation": loc3,
                "label": "Neige forte" if temp3 is None else "neige forte",
            },
        }
        builder.compute(reduction)
        assert builder.text == expected


class TestWeatherReducer:
    """
    This test ensures that the good isolated phenomenon are excluded,
    severe phenomenon are not excluded, indicated localisation for snow, ...
    Thresholds are bigger in order to see the exclusions
    """

    def _compute(
        self,
        codes: list,
        valid_times: list,
        units: str = "wwmf",
        lon: Optional[list] = None,
        lat: Optional[list] = None,
        altitude: Optional[list] = None,
        geos_descriptive: Optional[list] = None,
        requiredDT: float = 0.05,
        requiredDHmax: float = 0.05,
    ):
        if lat is None:
            lat = [30, 31]
        if lon is None:
            lon = [40, 41]
        if geos_descriptive is None:
            geos_descriptive = [[[1] * len(lon)] * len(lat)]
        if altitude is None:
            altitude = [[0] * len(lon)] * len(lat)

        data_vars = {
            "wwmf": (
                ["id", "valid_time", "latitude", "longitude"],
                codes,
                {"units": units},
            )
        }

        composite = WeatherCompositeFactory.create_factory(
            geos_descriptive=geos_descriptive,
            valid_times=valid_times,
            lon=lon,
            lat=lat,
            data_vars=data_vars,
            altitude=altitude,
        )

        self.reducer = WeatherReducer()
        self.reducer.required_DT = defaultdict(lambda: requiredDT)
        self.reducer.required_DHmax = defaultdict(lambda: requiredDHmax)
        return self.reducer.compute(composite)

    def test_several_ids(self):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        # Test with 2 ids
        codes_id1 = 2 * [[[70, 80], [np.nan, np.nan]]]
        codes_id2 = 2 * [[[np.nan, np.nan], [0, 0]]]
        codes = [codes_id1, codes_id2]
        geos_descriptive = [[[1, 1], [0, 0]], [[0, 0], [1, 1]]]
        assert self._compute(
            codes=codes,
            valid_times=valid_times,
            geos_descriptive=geos_descriptive,
        ) == {
            "TS1": {
                "label": "Averses, parfois neigeuses",
                "localisation": "à localisation N°1",
                "temporality": None,
            }
        }

        # Test with 3 ids
        lon = [40, 41, 42]
        lat = [35, 36, 37]
        codes_id1 = 2 * [
            [[0, 0, np.nan], [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]]
        ]
        codes_id2 = 2 * [[[np.nan, np.nan, 60], [60, 60, 60], [np.nan, np.nan, np.nan]]]
        codes_id3 = 2 * [
            [[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan], [61, 61, 62]]
        ]
        codes = [codes_id1, codes_id2, codes_id3]
        geos_descriptive = [
            [[1, 1, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
        ]
        assert self._compute(
            lon=lon,
            lat=lat,
            codes=codes,
            valid_times=valid_times,
            geos_descriptive=geos_descriptive,
        ) == {
            "TS1": {
                "label": "Neige",
                "localisation": "à localisation N°2 et à localisation N°3",
                "temporality": None,
            }
        }

        assert self.reducer.id_axis == "0"

    def test_1_valid_time(self):
        valid_times = [
            datetime(2023, 3, 1),
        ]
        lon, lat = [40], [35]
        assert (
            self._compute(codes=[[[[0]]]], lon=lon, lat=lat, valid_times=valid_times)
            == {}
        )

    @pytest.mark.parametrize(
        "codes,expected_location",
        [
            # No possible loc since all IoL < 0.2 => altitudes are taken
            ([[0, 0, 0], [60, 0, 0], [0, 0, 0]], "au-dessus de 200 m"),
            # Loc 2 isn't taken since IoL = 1/6 < 0.2
            ([[60, 0, 0], [0, 0, 0], [0, 0, 0]], "à localisation N°2"),
            # Loc 2 is taken since IoL > 0.2
            ([[60, 60, 0], [0, 0, 0], [0, 0, 0]], "à localisation N°2"),
            # Several loc
            (
                [[60, 0, 60], [0, 0, 60], [0, 0, 60]],
                "à localisation N°1 et à localisation N°2",
            ),
            # all domain is taken
            ([[60, 60, 60], [60, 60, 60], [60, 60, 60]], "sur tout le domaine"),
            # Only loc 3
            ([[60, 60, 0], [60, 60, 0], [60, 60, 0]], "à localisation N°3"),
            # Loc 3 and 1 are taken but these zones cover all domain
            ([[60, 60, 60], [60, 60, 0], [60, 60, 0]], "sur tout le domaine"),
        ],
    )
    def test_localisation_rules(self, codes, expected_location):
        lon = [40, 41, 42]
        lat = [35, 36, 37]
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        geos_descriptive = [
            [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
            [[1, 1, 0], [0, 0, 0], [0, 0, 0]],
            [[1, 1, 0], [1, 1, 0], [1, 1, 0]],
        ]
        altitude = [[100, 125, 345], [241, 236, 368], [210, 198, 389]]

        codes = np.array(codes)
        codes_id1 = 2 * [codes * np.array(geos_descriptive[0])]
        codes_id2 = 2 * [codes * np.array(geos_descriptive[1])]
        codes_id3 = 2 * [codes * np.array(geos_descriptive[2])]
        codes = [codes_id1, codes_id2, codes_id3]

        assert self._compute(
            codes=codes,
            lon=lon,
            lat=lat,
            valid_times=valid_times,
            geos_descriptive=geos_descriptive,
            altitude=altitude,
            requiredDT=0,  # in order to not exclude isolated point
            requiredDHmax=0,  # in order to not exclude isolated point
        ) == {
            "TS1": {
                "label": "Neige",
                "localisation": expected_location,
                "temporality": None,
            }
        }

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # Indicated phenomenon must last at least 3h
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                {},
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                {},
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "Ce mercredi en fin de matinée et mi-journée",
                        "localisation": None,
                    }
                },
            ),
            # No discontinuity if interruption less than 3 hours
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                {
                    "TS1": {
                        "label": "Brouillard dense",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
        ],
    )
    def test_temporality_rules(self, codes, expected):
        """This test handles the following temporality rules:
        * if the duration is  less than 3h it is not be considered
        * if ts lasts all the time the temporality isn't indicated
        """
        valid_times = [
            datetime(2023, 3, 1, 10),
            datetime(2023, 3, 1, 11),
            datetime(2023, 3, 1, 12),
            datetime(2023, 3, 1, 13),
            datetime(2023, 3, 1, 14),
            datetime(2023, 3, 1, 15),
            datetime(2023, 3, 1, 16),
        ]
        lon, lat = [40], [35, 36]
        assert (
            self._compute(codes=[codes], lon=lon, lat=lat, valid_times=valid_times)
            == expected
        )

    @pytest.mark.parametrize(
        "codes,expected_label",
        sample(dataset_wwmf_label, 10),
    )
    def test_grouping_rules(self, codes, expected_label):
        """This test handles more than 3 distinct phenomenon to ensure that they
        will be well put together"""
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        lon, lat = list(range(len(codes))), [35]
        codes = [
            [codes],
            [codes],
        ]

        result = self._compute(codes=[codes], lon=lon, lat=lat, valid_times=valid_times)
        assert len(result) == 1
        assert result["TS1"]["label"] == expected_label

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # 1 severe TS
            (
                [[[49, 0], [0, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "bruine verglaçante",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                [[[59, 59], [0, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "pluie verglaçante",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                [[[0, 0], [0, 85]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "averses de grêle",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                [[[0, 98], [0, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "orages avec grêle",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                [[[0, 0], [0, 0]], [[99, 0], [0, 99]]],
                {
                    "TS1": {
                        "label": "orages violents",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    }
                },
            ),
            # 2TS: 1 severe + 1 not severe
            (
                [[[49, 0], [0, 0]], [[70, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "bruine verglaçante",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                [[[85, 91], [0, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "averses de grêle et orages possibles",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                },
            ),
            # 3TS: 1 severe + 2 not severe
            (
                [[[49, 59], [70, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations verglaçantes ou averses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                },
            ),
            (
                [[[49, 59], [0, 0]], [[70, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations verglaçantes",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                [[[49, 0], [70, 0]], [[59, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "bruine verglaçante et averses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie verglaçante",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                [[[49, 61], [70, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations parfois verglaçantes, neige",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
        ],
    )
    def test_severe_phenomenon(self, codes, expected):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2), datetime(2023, 3, 3)]

        # to avoid that the phenomenon is over all the period
        codes.append([[0, 0], [0, 0]])

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                valid_times=valid_times,
                requiredDT=0.3,
                requiredDHmax=0.5,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes",
        [
            # No TS
            ("w1", [[[0, -1], [0, 0]], [[0, -1], [0, 0]]]),
            ("wwmf", [[[1, 15], [20, 25]], [[27, 29], [7, 0]]]),
            # DT<50% and DHmax<50% => excluded since isolated
            ("wwmf", [[[90, 0], [0, 0]], [[0, 90], [0, 0]]]),
            ("w1", [[[0, 0], [0, 18]], [[0, 0], [18, 0]]]),
            ("wwmf", [[[90, 0], [0, 0]], [[90, 31], [0, 0]]]),
            ("w1", [[[0, 0], [0, 17]], [[0, 17], [2, 0]]]),
        ],
    )
    def test_ras(self, units, codes):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                units=units,
                valid_times=valid_times,
                requiredDT=0.5,
                requiredDHmax=0.5,
            )
            == {}
        )

    @pytest.mark.parametrize(
        "units,codes,expected",
        [
            # DT>30% + DHmax>50% => not isolated
            (
                "wwmf",
                [[[50, 50], [50, 50]], [[50, 50], [50, 50]]],
                {
                    "TS1": {
                        "label": "pluie",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": None,
                    }
                },
            ),
            (
                "w1",
                [[[9, 9], [9, 9]], [[9, 9], [9, 9]]],
                {
                    "TS1": {
                        "label": "pluie faible",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    }
                },
            ),
            (
                "wwmf",
                [[[50, 50], [50, 50]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "pluie",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                "w1",
                [[[0, 0], [0, 0]], [[9, 9], [9, 9]]],
                {
                    "TS1": {
                        "label": "pluie faible",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    }
                },
            ),
            # DT<30% + DHmax>50% => not isolated
            (
                "wwmf",
                [[[33, 33], [0, 0]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                "w1",
                [[[0, 0], [0, 0]], [[0, 5], [5, 0]]],
                {
                    "TS1": {
                        "label": "brouillard givrant",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    }
                },
            ),
            (
                "wwmf",
                [[[33, 33], [62, 62]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige modérée",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                [[[20, 0], [0, 20]], [[0, 5], [5, 0]]],
                {
                    "TS1": {
                        "label": "averses de pluie et neige mêlées",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "brouillard givrant",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                "wwmf",
                [[[33, 33], [62, 62]], [[33, 0], [62, 0]]],
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige modérée",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                [[[20, 5], [0, 20]], [[0, 5], [5, 20]]],
                {
                    "TS1": {
                        "label": "brouillard givrant",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses de pluie et neige mêlées",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "wwmf",
                [[[31, 32], [60, 62]], [[33, 0], [61, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige et neige modérée",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS3": {
                        "label": "neige faible",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                [[[19, 4], [0, 20]], [[0, 5], [6, 21]]],
                {
                    "TS1": {
                        "label": "brouillard givrant, parfois dense",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses, parfois mêlées de neige",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS3": {
                        "label": "rares averses de neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # Test the localisation (with snow code)
            (
                "wwmf",
                [[[0, 0], [58, 58]], [[0, 0], [58, 58]]],
                {
                    "TS1": {
                        "label": "pluie et neige mêlées",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                "w1",
                [[[13, 13], [13, 13]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "neige faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            # Test of code with nebulosity replacement
            (
                "wwmf",
                [[[72, 72], [72, 72]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "rares averses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                "wwmf",
                [[[73, 73], [73, 73]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                "wwmf",
                [[[0, 78], [0, 78]], [[0, 0], [78, 78]]],
                {
                    "TS1": {
                        "label": "averses de pluie et neige mêlées",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                "wwmf",
                [[[82, 82], [82, 0]], [[0, 82], [0, 0]]],
                {
                    "TS1": {
                        "label": "rares averses de neige",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                "wwmf",
                [[[83, 83], [83, 83]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "averses de neige",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            # 2TS but one with DT<30%
            (
                "wwmf",
                [[[50, 50], [50, 50]], [[31, 50], [31, 50]]],
                {
                    "TS1": {
                        "label": "pluie",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brume",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            # 2TS but one with DT<30% and DHmax<50%
            (
                "wwmf",
                [[[50, 50], [50, 50]], [[31, 50], [0, 50]]],
                {
                    "TS1": {
                        "label": "pluie",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": None,
                    }
                },
            ),
        ],
    )
    def test_1_ts(self, units, codes, expected):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2), datetime(2023, 3, 3)]
        altitude = [[1045, 1501], [2040, 2509]]

        # to avoid that the phenomenon is over all the period
        codes.append([[0, 0], [0, 0]])

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                units=units,
                valid_times=valid_times,
                altitude=altitude,
                requiredDT=0.3,
                requiredDHmax=0.5,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes,expected",
        [
            # 2TS with different families
            (
                "wwmf",
                (50, 31),
                {
                    "TS1": {
                        "label": "pluie",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brume",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                "w1",
                (3, 9),
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie faible",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            # Localisation with snow
            (
                "wwmf",
                (31, 60),
                {
                    "TS1": {
                        "label": "brume",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                (13, 2),
                {
                    "TS1": {
                        "label": "neige faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "brouillard",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                "wwmf",
                (62, 63),
                {
                    "TS1": {
                        "label": "neige modérée",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "neige forte",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                (16, 17),
                {
                    "TS1": {
                        "label": "neige modérée",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "neige forte",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
        ],
    )
    def test_2_ts_different_families(self, units, codes, expected):
        """
        This test handles simple cases with 2 TS over 2 valid_times
        """
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2), datetime(2023, 3, 3)]
        altitude = [[1070], [2099]]

        lon, lat = [40], [35, 36]
        codes = [
            [[codes[0]], [codes[0]]],
            [[codes[1]], [codes[1]]],
            [[0], [0]],  # to avoid that the phenomenon is over all the period
        ]
        assert (
            self._compute(
                codes=[codes],
                lon=lon,
                lat=lat,
                units=units,
                valid_times=valid_times,
                altitude=altitude,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes,durations,expected",
        [
            # 2 TS not severe with 2 (<3) hours of covering and
            # 0.2 (<0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (10, 2, 10),
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "De cette nuit jusqu'à mercredi en début "
                        "d'après-midi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige faible",
                        "temporality": "Ce mercredi de la fin de matinée jusqu'en "
                        "première partie de nuit prochaine",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                (2, 6),
                (10, 2, 10),
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "De cette nuit jusqu'à mercredi en début "
                        "d'après-midi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brouillard dense givrant",
                        "temporality": "Ce mercredi de la fin de matinée jusqu'en "
                        "première partie de nuit prochaine",
                        "localisation": None,
                    },
                },
            ),
            # 2 TS not severe with 4 (>3) hours of covering and
            # 0.2 (<0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (20, 4, 20),
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige faible",
                        "temporality": "De ce mercredi soir à jeudi début de soirée",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                (2, 6),
                (20, 4, 20),
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brouillard dense givrant",
                        "temporality": "De ce mercredi soir à jeudi début de soirée",
                        "localisation": None,
                    },
                },
            ),
            # 2 TS not severe with 2 (<3) hours of covering and
            # 0.5 (>0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (4, 2, 4),
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige faible",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                "w1",
                (2, 6),
                (4, 2, 4),
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brouillard dense givrant",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": None,
                    },
                },
            ),
            # 2 TS not severe with 4 (>3) hours of covering and
            # 0.4 (>0.25) proportion of coverage => same TS
            (
                "wwmf",
                (70, 61),
                (10, 4, 10),
                {
                    "TS1": {
                        "label": "Averses, neige",
                        "temporality": None,
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                "w1",
                (2, 6),
                (10, 4, 10),
                {
                    "TS1": {
                        "label": "Brouillard, parfois dense et givrant",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
            # 2 precipitation TS which 1 severe with 0.4 (>0.25) proportion of
            # intersection  => 2 distinct TS
            # Notice that if it was not severe it would consider as same TS
            (
                "wwmf",
                (70, 98),
                (10, 4, 10),
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "De cette nuit jusqu'à mercredi en début "
                        "d'après-midi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "orages avec grêle",
                        "temporality": "De ce mercredi fin de matinée jusqu'en cours "
                        "de nuit prochaine",
                        "localisation": None,
                    },
                },
            ),
            # 2 precipitation TS which 1 severe with 0.78 (>0.75) proportion of
            # intersection  => same TS
            (
                "wwmf",
                (70, 98),
                (1, 7, 1),
                {
                    "TS1": {
                        "label": "Averses ou orages avec grêle",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
        ],
    )
    def test_2_ts_same_families(self, units, codes, durations, expected):
        """
        This test handles 2 TS  with valid_times which duration is given.
        The first and second period lasts duration[0] and the third one duration[1]
        """
        d0 = datetime(2023, 3, 1)
        valid_times = [
            d0,
            d0 + timedelta(hours=durations[0]),
            d0 + timedelta(hours=durations[0] + durations[1]),
            d0 + timedelta(hours=durations[0] + durations[1] + durations[2]),
        ]

        lon, lat = [40], [35, 36]
        codes = [
            [[0], [0]],
            [[codes[0]], [codes[0]]],
            [[codes[0]], [codes[1]]],
            [[codes[1]], [codes[1]]],
        ]
        assert (
            self._compute(
                codes=[codes], lon=lon, lat=lat, units=units, valid_times=valid_times
            )
            == expected
        )

    @pytest.mark.parametrize(
        "codes,durations,expected",
        [
            # 3 visibility TS
            (
                (30, 32, 33),
                (1, 4),
                {
                    "TS1": {
                        "label": "brume/brouillard",
                        "temporality": "Cette nuit de mardi à mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brouillard, parfois dense",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": None,
                    },
                },
            ),
            (
                (30, 32, 33),
                (4, 1),
                {
                    "TS1": {
                        "label": "brume/brouillard et brouillard",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "brouillard dense",
                        "temporality": "Ce mercredi matin",
                        "localisation": None,
                    },
                },
            ),
            # 3 precipitation TS with 2 subfamily
            (
                (51, 52, 60),
                (1, 4),
                {
                    "TS1": {
                        "label": "pluie faible",
                        "temporality": "Cette nuit de mardi à mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie modérée et neige",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (51, 58, 70),
                (4, 1),
                {
                    "TS1": {
                        "label": "pluie, parfois mêlée de neige",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "averses",
                        "temporality": "Ce mercredi matin",
                        "localisation": None,
                    },
                },
            ),
            # 3 precipitation TS with 1 subfamily
            (
                (51, 52, 53),
                (1, 4),
                {
                    "TS1": {
                        "label": "pluie faible",
                        "temporality": "Cette nuit de mardi à mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie modérée à forte",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": None,
                    },
                },
            ),
            (
                (61, 62, 63),
                (4, 1),
                {
                    "TS1": {
                        "label": "neige parfois modérée",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "neige forte",
                        "temporality": "Ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (70, 71, 77),
                (1, 4),
                {
                    "TS1": {
                        "label": "averses",
                        "temporality": "Cette nuit de mardi à mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses, parfois mêlées de neige",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # 3 precipitation TS with 2 precipitations + 1 visibility
            (
                (32, 71, 77),
                (1, 4),
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "Cette nuit de mardi à mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses, parfois mêlées de neige",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (32, 70, 61),
                (4, 1),
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses, neige",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (71, 32, 77),
                (1, 4),
                {
                    "TS1": {
                        "label": "Averses, parfois mêlées de neige",
                        "temporality": None,
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "brouillard",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                },
            ),
            # 3 precipitation TS with 2 visibilities + 1 precipitation
            (
                (32, 33, 77),
                (4, 1),
                {
                    "TS1": {
                        "label": "brouillard, parfois dense",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses de pluie et neige mêlées",
                        "temporality": "Ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (32, 30, 61),
                (1, 4),
                {
                    "TS1": {
                        "label": "brume/brouillard et brouillard",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige faible",
                        "temporality": "Cette nuit jusqu'à ce mercredi matin",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                (32, 77, 33),
                (4, 1),
                {
                    "TS1": {
                        "label": "Brouillard, parfois dense",
                        "temporality": None,
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "averses de pluie et neige mêlées",
                        "temporality": "Cette nuit jusqu'en début de matinée de "
                        "mercredi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # Phenomenon which can't be grouped by pair (according to their temporality)
            (
                (51, 71, 52),
                (2, 2),
                {
                    "TS1": {
                        "label": "Pluie ou averses",
                        "temporality": None,
                        "localisation": None,
                    }
                },
            ),
        ],
    )
    def test_3_ts_temporalities(self, codes, durations, expected):
        """This test handles 3 phenomenon with two of same temporality
        to ensure that they will be well put together"""
        valid_times = [
            datetime(2023, 3, 1, 0),
            datetime(2023, 3, 1, 3),
            datetime(2023, 3, 1, 3 + durations[0]),
            datetime(2023, 3, 1, 3 + durations[0] + durations[1]),
            datetime(2023, 3, 1, 3 + durations[0] + durations[1] + 3),
        ]

        lon, lat = [40], [35, 36]
        codes = [
            [[0], [0]],
            [[codes[0]], [codes[0]]],
            [[codes[0]], [codes[1]]],
            [[codes[1]], [codes[2]]],
            [[codes[2]], [codes[2]]],
        ]
        assert (
            self._compute(codes=[codes], lon=lon, lat=lat, valid_times=valid_times)
            == expected
        )

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # >3 visibility TS
            (
                [[[31, 32], [33, 38]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense ou "
                        "givrant",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    }
                },
            ),
            (
                [[[31, 32], [33, 38]], [[31, 39], [0, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense ou "
                        "givrant",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": None,
                    }
                },
            ),
            # 3 visibility TS and 1 precipitation
            (
                [[[31, 32], [33, 60]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # 2 visibility TS and 2 precipitation
            (
                [[[31, 61], [33, 60]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brouillard dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige et neige faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # 1 visibility TS and 3 precipitation
            (
                [[[31, 62], [63, 60]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brume",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # >3 precipitation TS and no severe
            (
                [[[51, 61], [70, 71]], [[0, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                [[[51, 61], [70, 71]], [[80, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "averses de neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[51, 61], [70, 71]], [[80, 91], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "orages, averses de neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[51, 61], [70, 71]], [[80, 90], [70, 0]]],
                {
                    "TS1": {
                        "label": "temps perturbé avec orages et précipitations, "
                        "parfois neigeuses",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    }
                },
            ),
            (
                [[[51, 61], [70, 71]], [[80, 90], [50, 60]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS2": {
                        "label": "temps perturbé, orages, précipitations parfois "
                        "neigeuses",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # >3 precipitation TS and 1 severe
            (
                [[[51, 61], [70, 71]], [[98, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TSsevere": "orages avec grêle",
                },
            ),
            (
                [[[51, 61], [70, 71]], [[98, 99], [0, 0]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TSsevere": "orages violents avec grêle",
                },
            ),
            (
                [[[51, 61], [70, 84]], [[98, 71], [0, 85]]],
                {
                    "TS1": {
                        "label": "précipitations, parfois neigeuses",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    },
                    "TSsevere": "orages avec grêle et grésil",
                },
            ),
            # several precipitation + visibility TS
            (
                [[[51, 32], [0, 0]], [[0, 0], [84, 92]]],
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS3": {
                        "label": "averses de grésil parfois orageuses",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": None,
                    },
                },
            ),
            (
                [[[51, 32], [33, 71]], [[80, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brouillard, parfois dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "pluie faible et rares averses",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS3": {
                        "label": "averses de neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 92]]],
                {
                    "TS1": {
                        "label": "brouillard, parfois dense",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "temps perturbé, orages, précipitations, parfois "
                        "sous forme d'averses neigeuses",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 38]]],
                {
                    "TS1": {
                        "label": "brouillard, parfois dense ou givrant",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "temps perturbé, orages, précipitations, parfois "
                        "sous forme d'averses neigeuses",
                        "temporality": "De la nuit de lundi dernier à hier à "
                        "cette nuit",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 98]]],
                {
                    "TS1": {
                        "label": "brouillard, parfois dense",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "temps perturbé, orages, précipitations, parfois sous "
                        "forme d'averses neigeuses",
                        "temporality": "De la nuit de lundi dernier à hier à cette "
                        "nuit",
                        "localisation": "sur tout le domaine",
                    },
                    "TSsevere": "orages avec grêle",
                },
            ),
            # If there is only 2 visibilities with 31 (Haze)
            # => the code and temporality of haze aren't included
            (
                [[[31, 32], [60, 61]], [[31, 0], [0, 0]]],
                {
                    "TS1": {
                        "label": "brouillard",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige et neige faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            # If there is at least 3 visibilities with 31 (Haze)
            # => the temporality of haze isn't included
            (
                [[[31, 32], [33, 61]], [[31, 60], [0, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige faible",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": "sur tout le domaine",
                    },
                    "TS3": {
                        "label": "neige",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
            (
                [[[31, 32], [33, 38]], [[31, 60], [61, 0]]],
                {
                    "TS1": {
                        "label": "temps brumeux avec brouillard, parfois dense ou "
                        "givrant",
                        "temporality": "Du milieu de nuit de lundi à mardi jusqu'en "
                        "cours de nuit suivante",
                        "localisation": None,
                    },
                    "TS2": {
                        "label": "neige et neige faible",
                        "temporality": "De cette nuit jusqu'en cours de nuit de "
                        "mercredi à jeudi",
                        "localisation": "sur tout le domaine",
                    },
                },
            ),
        ],
    )
    def test_more_than_3_ts_temporalities(self, codes, expected):
        valid_times = [
            datetime(2023, 3, 1),
            datetime(2023, 3, 2),
            datetime(2023, 3, 3),
        ]

        # to avoid that the phenomenon is over all the period
        codes.append(
            [
                [0, 0],
                [0, 0],
            ]
        )
        assert self._compute(codes=[codes], valid_times=valid_times) == expected


class TestWeatherDirector:
    @staticmethod
    def _compute(
        codes: list,
        valid_times: list,
        units: str = "wwmf",
        lon: Optional[list] = None,
        lat: Optional[list] = None,
        altitude: Optional[list] = None,
        geos_descriptive: Optional[list] = None,
        requiredDT: float = 0.05,
        requiredDHmax: float = 0.05,
    ):
        if lat is None:
            lat = [30, 31]
        if lon is None:
            lon = [40, 41]
        if geos_descriptive is None:
            geos_descriptive = [[[1] * len(lon)] * len(lat)]
        if altitude is None:
            altitude = [[0] * len(lon)] * len(lat)

        data_vars = {
            "wwmf": (
                ["id", "valid_time", "latitude", "longitude"],
                codes,
                {"units": units},
            )
        }

        composite = WeatherCompositeFactory.create_factory(
            geos_descriptive=geos_descriptive,
            valid_times=valid_times,
            lon=lon,
            lat=lat,
            data_vars=data_vars,
            altitude=altitude,
        )

        director = WeatherDirector()
        director.reducer.required_DT = defaultdict(lambda: requiredDT)
        director.reducer.required_DHmax = defaultdict(lambda: requiredDHmax)
        return director.compute(composite)

    def test_several_ids(self):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        # Test with 2 ids
        codes_id1 = 2 * [[[70, 80], [np.nan, np.nan]]]
        codes_id2 = 2 * [[[np.nan, np.nan], [0, 0]]]
        codes = [codes_id1, codes_id2]
        geos_descriptive = [[[1, 1], [0, 0]], [[0, 0], [1, 1]]]
        assert (
            self._compute(
                codes=codes,
                valid_times=valid_times,
                geos_descriptive=geos_descriptive,
            )
            == "Averses, parfois neigeuses à localisation N°1."
        )

        # Test with 3 ids
        lon = [40, 41, 42]
        lat = [35, 36, 37]
        codes_id1 = 2 * [
            [[0, 0, np.nan], [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]]
        ]
        codes_id2 = 2 * [[[np.nan, np.nan, 60], [60, 60, 60], [np.nan, np.nan, np.nan]]]
        codes_id3 = 2 * [
            [[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan], [61, 61, 62]]
        ]
        codes = [codes_id1, codes_id2, codes_id3]
        geos_descriptive = [
            [[1, 1, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
        ]
        assert (
            self._compute(
                lon=lon,
                lat=lat,
                codes=codes,
                valid_times=valid_times,
                geos_descriptive=geos_descriptive,
            )
            == "Neige à localisation N°2 et à localisation N°3."
        )

    def test_1_valid_time(self):
        valid_times = [
            datetime(2023, 3, 1),
        ]
        lon, lat = [40], [35]
        assert (
            self._compute(codes=[[[[0]]]], lon=lon, lat=lat, valid_times=valid_times)
            == "Pas de phénomène météorologique à enjeu."
        )

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # No possible loc since all IoL < 0.2 => altitudes are taken
            ([[0, 0, 0], [60, 0, 0], [0, 0, 0]], "Neige au-dessus de 200 m."),
            # Loc 2 isn't taken since IoL = 1/6 < 0.2
            ([[60, 0, 0], [0, 0, 0], [0, 0, 0]], "Neige à localisation N°2."),
            # Loc 2 is taken since IoL > 0.2
            ([[60, 60, 0], [0, 0, 0], [0, 0, 0]], "Neige à localisation N°2."),
            # Several loc
            (
                [[60, 0, 60], [0, 0, 60], [0, 0, 60]],
                "Neige à localisation N°1 et à localisation N°2.",
            ),
            # at least 90% of the domain is taken
            # all domain is taken
            ([[60, 60, 60], [60, 60, 60], [60, 60, 60]], "Neige sur tout le domaine."),
            # Only loc 3
            ([[60, 60, 0], [60, 60, 0], [60, 60, 0]], "Neige à localisation N°3."),
            # Loc 3 and 1 are taken but these zones cover all domain
            ([[60, 60, 60], [60, 60, 0], [60, 60, 0]], "Neige sur tout le domaine."),
        ],
    )
    def test_localisation_rules(self, codes, expected):
        lon = [40, 41, 42]
        lat = [35, 36, 37]
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        geos_descriptive = [
            [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
            [[1, 1, 0], [0, 0, 0], [0, 0, 0]],
            [[1, 1, 0], [1, 1, 0], [1, 1, 0]],
        ]
        altitude = [[100, 125, 345], [241, 236, 368], [210, 198, 389]]

        codes = np.array(codes)
        codes_id1 = 2 * [codes * np.array(geos_descriptive[0])]
        codes_id2 = 2 * [codes * np.array(geos_descriptive[1])]
        codes_id3 = 2 * [codes * np.array(geos_descriptive[2])]
        codes = [codes_id1, codes_id2, codes_id3]

        assert (
            self._compute(
                codes=codes,
                lon=lon,
                lat=lat,
                valid_times=valid_times,
                geos_descriptive=geos_descriptive,
                altitude=altitude,
                requiredDT=0,  # in order to not exclude isolated point
                requiredDHmax=0,  # in order to not exclude isolated point
            )
            == expected
        )

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # Indicated phenomenon must last at least 3h
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                "Pas de phénomène météorologique à enjeu.",
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                "Pas de phénomène météorologique à enjeu.",
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                ],
                "Ce mercredi en fin de matinée et mi-journée, brouillard dense.",
            ),
            # No discontinuity if interruption less than 3 hours
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
            (
                [
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
            (
                [
                    [[33], [33]],
                    [[0], [0]],
                    [[33], [33]],
                    [[0], [0]],
                    [[0], [0]],
                    [[33], [33]],
                    [[33], [33]],
                ],
                "Brouillard dense.",
            ),
        ],
    )
    def test_temporality_rules(self, codes, expected):
        """This test handles the temporality rule: if the duration is
        less than 3h it is not be considered"""
        valid_times = [
            datetime(2023, 3, 1, 10),
            datetime(2023, 3, 1, 11),
            datetime(2023, 3, 1, 12),
            datetime(2023, 3, 1, 13),
            datetime(2023, 3, 1, 14),
            datetime(2023, 3, 1, 15),
            datetime(2023, 3, 1, 16),
        ]
        lon, lat = [40], [35, 36]
        assert (
            self._compute(codes=[codes], lon=lon, lat=lat, valid_times=valid_times)
            == expected
        )

    @pytest.mark.parametrize(
        "codes,expected_label",
        sample(dataset_wwmf_label, 10),
    )
    def test_grouping_rules(self, codes, expected_label):
        """This test handles more than 3 distinct phenomenon to ensure that they
        will be well put together"""
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        lon, lat = list(range(len(codes))), [35]
        codes = [
            [codes],
            [codes],
        ]

        assert self._compute(
            codes=[codes], lon=lon, lat=lat, valid_times=valid_times
        ).startswith(expected_label)

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # 1 severe TS
            (
                [[[49, 0], [0, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "bruine verglaçante.",
            ),
            (
                [[[59, 59], [0, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "pluie verglaçante.",
            ),
            (
                [[[0, 0], [0, 85]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "averses de grêle.",
            ),
            (
                [[[0, 98], [0, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "orages avec grêle.",
            ),
            (
                [[[0, 0], [0, 0]], [[99, 0], [0, 99]]],
                "De cette nuit jusqu'en cours de nuit de mercredi à jeudi, "
                "orages violents.",
            ),
            # 2TS: 1 severe + 1 not severe
            (
                [[[49, 0], [0, 0]], [[70, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "bruine verglaçante. De cette nuit jusqu'en cours de nuit de mercredi "
                "à jeudi, averses.",
            ),
            (
                [[[85, 91], [0, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "averses de grêle et orages possibles.",
            ),
            # 3TS: 1 severe + 2 not severe
            (
                [[[49, 59], [70, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations verglaçantes ou averses.",
            ),
            (
                [[[49, 59], [0, 0]], [[70, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit "
                "suivante, précipitations verglaçantes. De cette nuit jusqu'en cours "
                "de nuit de mercredi à jeudi, averses.",
            ),
            (
                [[[49, 0], [70, 0]], [[59, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "bruine verglaçante et averses. De cette nuit jusqu'en cours de nuit "
                "de mercredi à jeudi, pluie verglaçante.",
            ),
            (
                [[[49, 61], [70, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations parfois verglaçantes, neige sur tout le domaine.",
            ),
        ],
    )
    def test_severe_phenomenon(self, codes, expected):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2), datetime(2023, 3, 3)]

        # to avoid that the phenomenon is over all the period
        codes.append([[0, 0], [0, 0]])

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                valid_times=valid_times,
                requiredDT=0.3,
                requiredDHmax=0.5,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes",
        [
            # No TS
            ("w1", [[[0, 0], [0, 0]], [[0, -1], [0, 0]]]),
            ("wwmf", [[[1, 15], [20, 25]], [[27, 29], [7, 10]]]),
            # DT<50% and DHmax<50% => excluded since isolated
            ("wwmf", [[[90, 0], [0, 0]], [[0, 90], [0, 0]]]),
            ("w1", [[[0, 0], [0, 18]], [[0, 0], [18, 0]]]),
            ("wwmf", [[[90, 0], [0, 0]], [[90, 31], [0, 0]]]),
            ("w1", [[[0, 0], [0, 17]], [[0, 17], [2, 0]]]),
        ],
    )
    def test_ras(self, units, codes):
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2)]

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                units=units,
                valid_times=valid_times,
                requiredDT=0.5,
                requiredDHmax=0.5,
            )
            == "Pas de phénomène météorologique à enjeu."
        )

    @pytest.mark.parametrize(
        "units,valid_times,codes,expected",
        [
            # DT>30% and DHmax>50% => not isolated
            (
                "wwmf",
                [datetime(2023, 3, 1, 8, 0, 0), datetime(2023, 3, 1, 11, 0, 0)],
                [[[50, 50], [50, 50]], [[50, 50], [50, 50]]],
                "Cette nuit jusqu'à ce matin, pluie.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1, 8, 0, 0), datetime(2023, 3, 1, 20, 0, 0)],
                [[[9, 9], [9, 9]], [[9, 9], [9, 9]]],
                "De mardi soir à mercredi début de soirée, pluie faible.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1, 14, 0, 0), datetime(2023, 3, 1, 20, 0, 0)],
                [[[50, 50], [50, 50]], [[0, 0], [0, 0]]],
                "En première partie de journée aujourd'hui, pluie.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1, 19, 0, 0), datetime(2023, 3, 1, 22, 0, 0)],
                [[[0, 0], [0, 0]], [[9, 9], [9, 9]]],
                "Ce mercredi soir et première partie de nuit prochaine, pluie faible.",
            ),
            # DT<30% + DHmax>50% => not isolated
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[33, 33], [0, 0]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard dense.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[0, 0], [0, 0]], [[0, 5], [5, 0]]],
                "De cette nuit jusqu'en cours de nuit de mercredi à jeudi, brouillard "
                "givrant.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[33, 33], [62, 62]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard dense. Du milieu de nuit de lundi à mardi jusqu'en cours "
                "de nuit suivante, neige modérée sur tout le domaine.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[20, 0], [0, 20]], [[0, 5], [5, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "averses de pluie et neige mêlées sur tout le domaine. De cette nuit "
                "jusqu'en cours de nuit de mercredi à jeudi, brouillard givrant.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[33, 33], [62, 62]], [[33, 0], [62, 0]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard dense. "
                "De la nuit de lundi dernier à hier à cette nuit, neige modérée sur "
                "tout le domaine.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[20, 5], [0, 20]], [[0, 5], [5, 20]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard givrant. "
                "De la nuit de lundi dernier à hier à cette nuit, averses de pluie et "
                "neige mêlées sur tout le domaine.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[31, 32], [60, 62]], [[33, 0], [61, 0]]],
                "De la nuit de lundi dernier à hier à cette nuit, temps brumeux avec "
                "brouillard, parfois dense. Du milieu de nuit de lundi à mardi "
                "jusqu'en cours de nuit suivante, neige et neige modérée sur tout le "
                "domaine. De cette nuit jusqu'en cours de nuit de mercredi à jeudi, "
                "neige faible sur tout le domaine.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[19, 4], [0, 20]], [[0, 5], [6, 21]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard givrant, "
                "parfois dense. Du milieu de nuit de lundi à mardi jusqu'en cours de "
                "nuit suivante, averses, parfois mêlées de neige sur tout le domaine. "
                "De cette nuit jusqu'en cours de nuit de mercredi à jeudi, "
                "rares averses de neige sur tout le domaine.",
            ),
            # Test the localisation (with snow code)
            (
                "wwmf",
                [datetime(2023, 3, 1, 23, 0, 0), datetime(2023, 4, 1, 4, 0, 0)],
                [[[0, 0], [58, 58]], [[0, 0], [58, 58]]],
                "De lundi 30 janvier dans la soirée à la nuit de vendredi 31 mars à "
                "samedi 1er avril, pluie et neige mêlées sur tout le domaine.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1, 23, 0, 0), datetime(2023, 4, 1, 4, 0, 0)],
                [[[58, 58], [58, 0]], [[58, 58], [58, 58]]],
                "De lundi 30 janvier dans la soirée à la nuit de vendredi 31 mars à "
                "samedi 1er avril, pluie et neige mêlées sur tout le domaine.",
            ),
            (
                "w1",
                [datetime(2023, 3, 1, 23, 30, 0), datetime(2023, 5, 1, 15, 0, 0)],
                [[[13, 13], [13, 13]], [[0, 0], [0, 0]]],
                "De samedi 31 décembre 2022 dans la matinée à cette nuit, "
                "neige faible sur tout le domaine.",
            ),
            # Code replacement test with nebulosity
            # Test of code with nebulosity replacement
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[72, 72], [72, 72]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "rares averses.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[73, 73], [73, 73]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "averses.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[0, 78], [0, 78]], [[0, 0], [78, 78]]],
                "De la nuit de lundi dernier à hier à cette nuit, averses de pluie et "
                "neige mêlées sur tout le domaine.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[82, 82], [82, 0]], [[0, 82], [0, 0]]],
                "De la nuit de lundi dernier à hier à cette nuit, rares averses de "
                "neige sur tout le domaine.",
            ),
            (
                "wwmf",
                [datetime(2023, 3, 1), datetime(2023, 3, 2)],
                [[[83, 83], [83, 83]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "averses de neige sur tout le domaine.",
            ),
        ],
    )
    def test_1_ts(self, units, valid_times, codes, expected):
        """
        This test ensures that the good isolated phenomenon are excluded
        The threshold (50%) is bigger in order to see the exclusions
        """

        altitude = [[1045, 1501], [2040, 2509]]

        # to avoid that the phenomenon is over all the period
        valid_times.append(valid_times[-1] + Timedelta(hours=1))
        codes.append([[0, 0], [0, 0]])

        # We change the requiredDT and requiredDHmax to be able to see the exclusion
        assert (
            self._compute(
                codes=[codes],
                units=units,
                valid_times=valid_times,
                altitude=altitude,
                requiredDT=0.3,
                requiredDHmax=0.5,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes,expected",
        [
            # 2TS with different families
            (
                "wwmf",
                (50, 31),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit "
                "suivante, pluie. De cette nuit jusqu'en cours de nuit de "
                "mercredi à jeudi, brume.",
            ),
            (
                "w1",
                (3, 9),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard dense. De cette nuit jusqu'en cours de nuit de mercredi à "
                "jeudi, pluie faible.",
            ),
            # Localisation with snow
            (
                "wwmf",
                (31, 60),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brume. De cette nuit jusqu'en cours de nuit de mercredi à jeudi, "
                "neige sur tout le domaine.",
            ),
            (
                "w1",
                (13, 2),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "neige faible sur tout le domaine. De cette nuit jusqu'en cours de "
                "nuit de mercredi à jeudi, brouillard.",
            ),
            (
                "wwmf",
                (62, 63),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "neige modérée sur tout le domaine. De cette nuit jusqu'en cours de "
                "nuit de mercredi à jeudi, neige forte sur tout le domaine.",
            ),
            (
                "w1",
                (16, 17),
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "neige modérée sur tout le domaine. De cette nuit jusqu'en cours de "
                "nuit de mercredi à jeudi, neige forte sur tout le domaine.",
            ),
        ],
    )
    def test_2_ts_different_families(self, units, codes, expected):
        """
        This test handles simple cases with 2 TS over 2 valid_times
        """
        valid_times = [datetime(2023, 3, 1), datetime(2023, 3, 2), datetime(2023, 3, 3)]
        altitude = [[1070], [2099]]

        lon, lat = [40], [35, 36]
        codes = [
            [[codes[0]], [codes[0]]],
            [[codes[1]], [codes[1]]],
            [[0], [0]],  # to avoid that the phenomenon is over all the period
        ]
        assert (
            self._compute(
                codes=[codes],
                lon=lon,
                lat=lat,
                units=units,
                valid_times=valid_times,
                altitude=altitude,
            )
            == expected
        )

    @pytest.mark.parametrize(
        "units,codes,durations,expected",
        [
            # 2 TS not severe with 2 (<3) hours of covering and
            # 0.2 (<0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (10, 2, 10),
                "De cette nuit jusqu'à mercredi en début d'après-midi, averses. Ce "
                "mercredi de la fin de matinée jusqu'en première partie de nuit "
                "prochaine, neige faible sur tout le domaine.",
            ),
            (
                "w1",
                (2, 6),
                (10, 2, 10),
                "De cette nuit jusqu'à mercredi en début d'après-midi, brouillard. "
                "Ce mercredi de la fin de matinée jusqu'en première partie de nuit "
                "prochaine, brouillard dense givrant.",
            ),
            # 2 TS not severe with 4 (>3) hours of covering and
            # 0.2 (<0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (20, 4, 20),
                "De cette nuit jusqu'en cours de nuit de mercredi à jeudi, averses. "
                "De ce mercredi soir à jeudi début de soirée, neige faible sur tout "
                "le domaine.",
            ),
            (
                "w1",
                (2, 6),
                (20, 4, 20),
                "De cette nuit jusqu'en cours de nuit de mercredi à jeudi, "
                "brouillard. De ce mercredi soir à jeudi début de soirée, brouillard "
                "dense givrant.",
            ),
            # 2 TS not severe with 2 (<3) hours of covering and
            # 0.5 (>0.25) proportion of coverage => 2 distinct TS
            (
                "wwmf",
                (70, 61),
                (4, 2, 4),
                "Cette nuit jusqu'en début de matinée de mercredi, averses. Cette "
                "nuit jusqu'à ce mercredi matin, neige faible sur tout le domaine.",
            ),
            (
                "w1",
                (2, 6),
                (4, 2, 4),
                "Cette nuit jusqu'en début de matinée de mercredi, brouillard. "
                "Cette nuit jusqu'à ce mercredi matin, brouillard dense givrant.",
            ),
            # 2 TS not severe with 4 (>3) hours of covering and
            # 0.4 (>0.25) proportion of coverage => same TS
            (
                "wwmf",
                (70, 61),
                (10, 4, 10),
                "Averses, neige sur tout le domaine.",
            ),
            (
                "w1",
                (2, 6),
                (10, 4, 10),
                "Brouillard, parfois dense et givrant.",
            ),
            # 2 precipitation TS which 1 severe with 0.4 (>0.25) proportion of
            # intersection  => 2 distinct TS
            # Notice that if it was not severe it would consider as same TS
            (
                "wwmf",
                (70, 98),
                (10, 4, 10),
                "De cette nuit jusqu'à mercredi en début d'après-midi, averses. "
                "De ce mercredi fin de matinée jusqu'en cours de nuit prochaine, "
                "orages avec grêle.",
            ),
            # 2 precipitation TS which 1 severe with 0.78 (>0.75) proportion of
            # intersection  => same TS
            (
                "wwmf",
                (70, 98),
                (1, 7, 1),
                "Averses ou orages avec grêle.",
            ),
        ],
    )
    def test_2_ts_same_families(self, units, codes, durations, expected):
        """
        This test handles 2 TS  with valid_times which duration is given.
        The first and second period lasts duration[0] and the third one duration[1]
        """
        d0 = datetime(2023, 3, 1)
        valid_times = [
            d0,
            d0 + timedelta(hours=durations[0]),
            d0 + timedelta(hours=durations[0] + durations[1]),
            d0 + timedelta(hours=durations[0] + durations[1] + durations[2]),
        ]

        lon, lat = [40], [35, 36]
        codes = [
            [[0], [0]],
            [[codes[0]], [codes[0]]],
            [[codes[0]], [codes[1]]],
            [[codes[1]], [codes[1]]],
        ]
        assert (
            self._compute(
                codes=[codes], lon=lon, lat=lat, units=units, valid_times=valid_times
            )
            == expected
        )

    @pytest.mark.parametrize(
        "codes,durations,expected",
        [
            # 3 visibility TS
            (
                (30, 32, 33),
                (1, 4),
                "Cette nuit de mardi à mercredi, brume/brouillard. Cette nuit jusqu'à "
                "ce mercredi matin, brouillard, parfois dense.",
            ),
            (
                (30, 32, 33),
                (4, 1),
                "Cette nuit jusqu'en début de matinée de mercredi, brume/brouillard "
                "et brouillard. Ce mercredi matin, brouillard dense.",
            ),
            # 3 precipitation TS with 2 subfamily
            (
                (51, 52, 60),
                (1, 4),
                "Cette nuit de mardi à mercredi, pluie faible. Cette nuit jusqu'à ce "
                "mercredi matin, pluie modérée et neige sur tout le domaine.",
            ),
            (
                (51, 58, 70),
                (4, 1),
                "Cette nuit jusqu'en début de matinée de mercredi, pluie, parfois "
                "mêlée de neige sur tout le domaine. Ce mercredi matin, averses.",
            ),
            # 3 precipitation TS with 1 subfamily
            (
                (51, 52, 53),
                (1, 4),
                "Cette nuit de mardi à mercredi, pluie faible. Cette nuit jusqu'à ce "
                "mercredi matin, pluie modérée à forte.",
            ),
            (
                (61, 62, 63),
                (4, 1),
                "Cette nuit jusqu'en début de matinée de mercredi, neige parfois "
                "modérée sur tout le domaine. Ce mercredi matin, neige forte sur tout "
                "le domaine.",
            ),
            (
                (70, 71, 77),
                (1, 4),
                "Cette nuit de mardi à mercredi, averses. Cette nuit jusqu'à ce "
                "mercredi matin, averses, parfois mêlées de neige sur tout le domaine.",
            ),
            # 3 precipitation TS with 2 precipitations + 1 visibility
            (
                (32, 71, 77),
                (1, 4),
                "Cette nuit de mardi à mercredi, brouillard. Cette nuit jusqu'à ce "
                "mercredi matin, averses, parfois mêlées de neige sur tout le domaine.",
            ),
            (
                (32, 70, 61),
                (4, 1),
                "Cette nuit jusqu'en début de matinée de mercredi, brouillard. Cette "
                "nuit jusqu'à ce mercredi matin, averses, neige sur tout le domaine.",
            ),
            (
                (71, 32, 77),
                (1, 4),
                "Averses, parfois mêlées de neige sur tout le domaine. Cette nuit "
                "jusqu'en début de matinée de mercredi, brouillard.",
            ),
            # 3 precipitation TS with 2 visibilities + 1 precipitation
            (
                (32, 33, 77),
                (4, 1),
                "Cette nuit jusqu'en début de matinée de mercredi, brouillard, "
                "parfois dense. Ce mercredi matin, averses de pluie et neige mêlées "
                "sur tout le domaine.",
            ),
            (
                (32, 30, 61),
                (1, 4),
                "Cette nuit jusqu'en début de matinée de mercredi, brume/brouillard "
                "et brouillard. Cette nuit jusqu'à ce mercredi matin, neige faible "
                "sur tout le domaine.",
            ),
            (
                (32, 77, 33),
                (4, 1),
                "Brouillard, parfois dense. Cette nuit jusqu'en début de matinée de "
                "mercredi, averses de pluie et neige mêlées sur tout le domaine.",
            ),
            # Phenomenon which can't be grouped by pair (according to their temporality)
            ((51, 71, 52), (2, 2), "Pluie ou averses."),
        ],
    )
    def test_3_ts_temporalities(self, codes, durations, expected):
        """This test handles 3 phenomenon with two of same temporality
        to ensure that they will be well put together"""
        valid_times = [
            datetime(2023, 3, 1, 0),
            datetime(2023, 3, 1, 3),
            datetime(2023, 3, 1, 3 + durations[0]),
            datetime(2023, 3, 1, 3 + durations[0] + durations[1]),
            datetime(2023, 3, 1, 3 + durations[0] + durations[1] + 3),
        ]

        lon, lat = [40], [35, 36]
        codes = [
            [[0], [0]],
            [[codes[0]], [codes[0]]],
            [[codes[0]], [codes[1]]],
            [[codes[1]], [codes[2]]],
            [[codes[2]], [codes[2]]],
        ]

        assert (
            self._compute(codes=[codes], lon=lon, lat=lat, valid_times=valid_times)
            == expected
        )

    @pytest.mark.parametrize(
        "codes,expected",
        [
            # >3 visibility TS
            (
                [[[31, 32], [33, 38]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "temps brumeux avec brouillard, parfois dense ou givrant.",
            ),
            (
                [[[31, 32], [33, 38]], [[31, 39], [0, 0]]],
                "De la nuit de lundi dernier à hier à cette nuit, temps brumeux avec "
                "brouillard, parfois dense ou givrant.",
            ),
            # 3 visibility TS and 1 precipitation
            (
                [[[31, 32], [33, 60]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "temps brumeux avec brouillard, parfois dense. Du milieu de nuit de "
                "lundi à mardi jusqu'en cours de nuit suivante, neige sur tout le "
                "domaine.",
            ),
            # 2 visibility TS and 2 precipitation
            (
                [[[31, 61], [33, 60]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard dense. Du milieu de nuit de lundi à mardi jusqu'en cours "
                "de nuit suivante, neige et neige faible sur tout le domaine.",
            ),
            # 1 visibility TS and 3 precipitation
            (
                [[[31, 62], [63, 60]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brume. Du milieu de nuit de lundi à mardi jusqu'en cours de nuit "
                "suivante, neige sur tout le domaine.",
            ),
            # >3 precipitation TS and no severe
            (
                [[[51, 61], [70, 71]], [[0, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine.",
            ),
            (
                [[[51, 61], [70, 71]], [[80, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine. De "
                "cette nuit jusqu'en cours de nuit de mercredi à jeudi, averses de "
                "neige sur tout le domaine.",
            ),
            (
                [[[51, 61], [70, 71]], [[80, 91], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine. De cette nuit "
                "jusqu'en cours de nuit de mercredi à jeudi, orages, averses de neige "
                "sur tout le domaine.",
            ),
            (
                [[[51, 61], [70, 71]], [[80, 90], [70, 0]]],
                "De la nuit de lundi dernier à hier à cette nuit, temps perturbé avec "
                "orages et précipitations, parfois neigeuses sur tout le domaine.",
            ),
            (
                [[[51, 61], [70, 71]], [[80, 90], [50, 60]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine. De cette nuit "
                "jusqu'en cours de nuit de mercredi à jeudi, temps perturbé, orages, "
                "précipitations parfois neigeuses sur tout le domaine.",
            ),  # >3 precipitation TS and severe
            (
                [[[51, 61], [70, 71]], [[98, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine. Autres "
                "phénomènes sévères : orages avec grêle.",
            ),
            (
                [[[51, 61], [70, 71]], [[98, 99], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "précipitations, parfois neigeuses sur tout le domaine. Autres "
                "phénomènes sévères : orages violents avec grêle.",
            ),
            (
                [[[51, 61], [70, 84]], [[98, 71], [0, 85]]],
                "De la nuit de lundi dernier à hier à cette nuit, précipitations, "
                "parfois neigeuses sur tout le domaine. Autres phénomènes sévères : "
                "orages avec grêle et grésil.",
            ),
            # several precipitation + visibility TS
            (
                [[[51, 32], [0, 0]], [[0, 0], [84, 92]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard. Du milieu de nuit de lundi à mardi jusqu'en cours de "
                "nuit suivante, pluie faible. De cette nuit jusqu'en cours de nuit de "
                "mercredi à jeudi, averses de grésil parfois orageuses.",
            ),
            (
                [[[51, 32], [33, 71]], [[80, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard, parfois dense. Du milieu de nuit de lundi à mardi "
                "jusqu'en cours de nuit suivante, pluie faible et rares averses. De "
                "cette nuit jusqu'en cours de nuit de mercredi à jeudi, averses de "
                "neige sur tout le domaine.",
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 92]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard, parfois "
                "dense. De la nuit de lundi dernier à hier à cette nuit, temps "
                "perturbé, orages, précipitations, parfois sous forme d'averses "
                "neigeuses sur tout le domaine.",
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 38]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard, parfois "
                "dense ou givrant. De la nuit de lundi dernier à hier à cette nuit, "
                "temps perturbé, orages, précipitations, parfois sous forme d'averses "
                "neigeuses sur tout le domaine.",
            ),
            (
                [[[51, 32], [33, 71]], [[33, 91], [83, 98]]],
                "De la nuit de lundi dernier à hier à cette nuit, brouillard, parfois "
                "dense. De la nuit de lundi dernier à hier à cette nuit, "
                "temps perturbé, orages, précipitations, parfois sous forme d'averses "
                "neigeuses. Autres phénomènes sévères : orages avec grêle.",
            ),
            # If there is only 2 visibilities with 31 (Haze)
            # => the code and temporality of haze aren't included
            (
                [[[31, 32], [60, 61]], [[31, 0], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "brouillard. Du milieu de nuit de lundi à mardi jusqu'en cours de "
                "nuit suivante, neige et neige faible sur tout le domaine.",
            ),
            # If there is at least 3 visibilities with 31 (Haze)
            # => the temporality of haze isn't included
            (
                [[[31, 32], [33, 61]], [[31, 60], [0, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "temps brumeux avec brouillard, parfois dense. Du milieu de nuit de "
                "lundi à mardi jusqu'en cours de nuit suivante, neige faible sur tout "
                "le domaine. De cette nuit jusqu'en cours de nuit de mercredi à "
                "jeudi, neige sur tout le domaine.",
            ),
            (
                [[[31, 32], [33, 38]], [[31, 60], [61, 0]]],
                "Du milieu de nuit de lundi à mardi jusqu'en cours de nuit suivante, "
                "temps brumeux avec brouillard, parfois dense ou givrant. De cette "
                "nuit jusqu'en cours de nuit de mercredi à jeudi, neige et neige "
                "faible sur tout le domaine.",
            ),
        ],
    )
    def test_more_than_3_ts_temporalities(self, codes, expected):
        valid_times = [
            datetime(2023, 3, 1),
            datetime(2023, 3, 2),
            datetime(2023, 3, 3),
        ]

        # to avoid that the phenomenon is over all the period
        codes.append(
            [
                [0, 0],
                [0, 0],
            ]
        )
        assert self._compute(codes=[codes], valid_times=valid_times) == expected


class TestWeatherIntegration:
    @pytest.mark.parametrize(
        "period,expected",
        [
            (
                "20230309",
                {
                    "CD03": "De ce jeudi fin de matinée au petit matin vendredi, temps "
                    "perturbé, orages, précipitations, parfois sous forme d'averses "
                    "neigeuses au-dessus de 1100 m. Autres phénomènes sévères : orages "
                    "avec grêle.\n",
                    "CD06": "En cours de nuit de jeudi à vendredi, neige modérée "
                    "au-dessus de 2500 m. En deuxième partie de nuit de jeudi à "
                    "vendredi, averses parfois neigeuses sur le  haut Var et l'Ouest du"
                    " Mercantour et sur l'Est du Mercantour.\n",
                    "CD20": "De ce jeudi après-midi au petit matin vendredi, temps "
                    "perturbé, précipitations, parfois neigeuses au-dessus de "
                    "1300 m.\n",
                    "CD29": "Ce jeudi et jusqu'en début de matinée vendredi, pluie ou "
                    "averses.\n",
                    "CD31": "Temps perturbé avec orages et précipitations, parfois "
                    "neigeuses au-dessus de 1400 m. Autres phénomènes sévères : orages "
                    "avec grêle.\n",
                    "CD63": "De ce jeudi début d'après-midi au petit matin vendredi, "
                    "orages et averses parfois neigeuses dans le Cézallier et à l'Est "
                    "du Sancy. Autres phénomènes sévères : orages avec grêle.\n",
                },
            ),
            (
                "20230319",
                {
                    "CD06": "Ce dimanche jusqu'en cours de nuit prochaine, averses "
                    "parfois neigeuses sur le Haut Pays.\n",
                    "CD03": "Ce dimanche jusqu'en cours de nuit prochaine, orages et "
                    "averses parfois neigeuses au-dessus de 900 m. En deuxième partie "
                    "de nuit prochaine jusqu'au petit matin lundi, brume.\n",
                    "CD20": "Ce dimanche après-midi jusqu'en première partie de nuit "
                    "prochaine, averses parfois neigeuses au-dessus de 1600 m.\n",
                    "CD29": "En deuxième partie de nuit prochaine jusqu'au petit "
                    "matin lundi, pluie faible à modérée.\n",
                    "CD31": "Ce dimanche jusqu'en cours de nuit prochaine, averses "
                    "parfois neigeuses sur le Cagire et le Luchonnais. En fin de nuit "
                    "prochaine et petit matin de lundi, brume.\n",
                    "CD63": "Orages et averses parfois neigeuses dans le Cézallier, "
                    "dans les Monts du Forez et à l'Est du Sancy. En fin de nuit "
                    "prochaine et petit matin de lundi, brouillard givrant.\n",
                },
            ),
            (
                "20230321",
                {
                    "CD03": "Ce mardi en journée et soirée, pluie faible. En fin de "
                    "nuit prochaine et petit matin de mercredi, brume.\n",
                    "CD06": "Pas de phénomène météorologique à enjeu.\n",
                    "CD20": "Pas de phénomène météorologique à enjeu.\n",
                    "CD31": "Pas de phénomène météorologique à enjeu.\n",
                    "CD29": "En cours de journée mardi, rares averses. La nuit de "
                    "mardi à mercredi jusqu'au petit matin, pluie faible à modérée.\n",
                    "CD63": "Ce mardi après-midi et soirée, pluie faible.\n",
                },
            ),
            (
                "20230401",
                {
                    "CD03": "Temps perturbé avec orages et précipitations, parfois "
                    "neigeuses au-dessus de 800 m.\n",
                    "CD06": "De ce samedi après-midi jusqu'en cours de nuit prochaine, "
                    "averses parfois neigeuses sur le  haut Var et l'Ouest du "
                    "Mercantour et sur l'Est du Mercantour.\n",
                    "CD20": "De ce samedi après-midi jusqu'en cours de nuit prochaine, "
                    "averses parfois neigeuses en montagne du col de Vergio au col de "
                    "Bavella et du massif du Monte Cinto au relief du Fiumorbo. En "
                    "deuxième partie de nuit prochaine jusqu'au petit matin dimanche, "
                    "pluie, neige dans la région de Niolo et en montagne du col de "
                    "Vergio au col de Bavella.\n",
                    "CD29": "Ce samedi jusqu'en fin de nuit prochaine, orages ou "
                    "averses.\n",
                    "CD31": "Ce samedi jusqu'en cours de nuit prochaine, orages et "
                    "averses parfois neigeuses sur le Cagire et le Luchonnais. En "
                    "deuxième partie de nuit prochaine jusqu'au petit matin dimanche, "
                    "pluie, neige sur le Cagire et le Luchonnais.\n",
                    "CD63": "Temps perturbé avec orages et précipitations, parfois "
                    "neigeuses sur le Sancy, l'Artense et le Cézallier et dans les "
                    "Monts du Forez.\n",
                },
            ),
        ],
    )
    @patch(
        "mfire.composite.weather.TEXT_ALGO",
        {
            "weather": {
                "generic": {
                    "params": {
                        "wwmf": {"field": "WWMF__SOL", "default_units": "Code WWMF"}
                    }
                }
            }
        },
    )  # this patch avoids to have to use all (useless) data files
    def test_generated_text(self, period: str, expected: str, test_path: Path):
        path = test_path / "test_data/text_TS/"
        config = JsonFile(str(path / f"prod_task_config_{period}.json")).load()

        # Replace "test_data_dir" by appropriate values
        data: dict = recursive_format(
            config,
            values={
                "test_data_dir": str(path),
            },
        )
        for value in data.values():
            compo = value["components"][0]
            text_manager = TextManager(component=compo)
            generated_text = text_manager.compute()
            assert expected[compo["name"]] == "\n".join(generated_text.split("\n")[1:])
