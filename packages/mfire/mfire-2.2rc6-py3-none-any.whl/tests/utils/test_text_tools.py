"""test_text_tools.py

Unit tests of the utils.text_tools module.
"""

# Third parties packages
import pytest

# Own package
from mfire.utils import text_tools as tt


@pytest.mark.filterwarnings("ignore: warnings")
def test_capitalize():
    origin = (
        "je suis un petit test.Et je suis pas trop content."
        "     par contre c'etr Trop     classe lea Completion"
    )
    expected = (
        "Je suis un petit test. Et je suis pas trop content."
        " Par contre c'etr Trop classe lea Completion"
    )
    assert tt.start_sentence_with_capital(origin) == expected


def test_ellipsis():
    origin = (
        "je suis un petit test.Et je suis pas trop content."
        "     par contre c'etr Trop     classe lea Completion..."
    )
    expected = (
        "Je suis un petit test. Et je suis pas trop content."
        " Par contre c'etr Trop classe lea Completion."
    )
    assert tt.start_sentence_with_capital(origin) == expected


def test_transforme_syntaxe():
    origin = (
        "à partir de en ce milieu de nuit"
        "à partir de aujourd'hui"
        "à partir de en première partie de"
        "à partir de en milieu de"
        "à partir de en fin de"
        "jusqu'à en ce milieu de nuit"
        ".."
        ".    ."
        ",."
        ",     ."
    )

    expected = (
        "à partir du milieu de nuit"
        "à partir d'aujourd'hui"
        "à partir de la première partie de"
        "à partir du milieu de"
        "à partir de la fin de"
        "jusqu'en ce milieu de nuit"
        "."
        "."
        "."
        "."
    )

    assert tt.transforme_syntaxe(origin) == expected
