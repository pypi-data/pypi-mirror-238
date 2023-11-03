"""
    Test du builder pour la situation générale.
"""

from pathlib import Path

import pytest

from mfire.text.sit_gen.builders import SitGenBuilder
from mfire.utils import JsonFile

REDUCTION = JsonFile(
    str(Path(__file__).absolute().parent.parent / "test_data/reduction.json")
).load()

EXPECTED = {
    "large_mediterranee": "Dépression 1008 hPa au Nord de la Riviera italienne se "
    "creusant lentement, prévue 1005 hPa quasi-stationnaire à la fin.\n",
    "grand_large_smdsm": "Dépression 984 hPa au Sud-Est de Terre Neuve se creusant "
    "lentement, prévue 976 hPa au Sud-Est du Groenland à la fin.\nFront froid associé "
    "sur l'Atlantique Nord, se déplaçant vers le Sud-Est.\nDépression 1007 hPa au "
    "Sud-Ouest de l'Algérie évoluant peu.\nDépression 996 hPa au Nord-Ouest de "
    "l'Irlande se décalant vers le Nord de l'Irlande plus tard. Puis, se comblant "
    "lentement, prévue 999 hPa quasi-stationnaire à la fin.\nDépression 999 hPa au "
    "Sud-Est du Groenland se décalant vers le Nord-Est, prévue au Sud-Est du "
    "Groenland à la fin.\nAnticyclone 1025 hPa sur les Açores évoluant peu.\nFront "
    "froid sur l'Europe de l'Ouest, se déplaçant vers le Sud-Est.\n",
    "large_atlantique_navtex_ism": "Dépression 1003 hPa au Sud-Ouest de la Scandinavie "
    "se décalant vers le Nord-Est, prévue au Nord-Ouest de la Mer Baltique à la "
    "fin.\nFront froid associé sur la Mer Baltique, se déplaçant vers le Nord-Est.\n"
    "Dépression 996 hPa au Nord-Ouest de l'Irlande se décalant vers le Nord de "
    "l'Irlande plus tard. Puis, se comblant lentement, prévue 999 hPa "
    "quasi-stationnaire à la fin.\nDépression 999 hPa au Sud-Est du Groenland se "
    "décalant vers le Nord-Est, prévue au Sud-Est du Groenland à la fin.\nDépression "
    "1008 hPa au Nord de la Riviera italienne se creusant lentement, prévue 1005 "
    "hPa quasi-stationnaire à la fin.\nDépression 1002 hPa au Sud-Est de la Mer du "
    "Nord évoluant peu.\nAnticyclone 1025 hPa sur les Açores évoluant peu.\nFront "
    "froid sur l'Europe de l'Ouest, se déplaçant vers le Sud-Est.\nFront froid sur la "
    "Scandinavie, se déplaçant vers le Nord.\n",
    "cote_manche_atlantique": "Dépression 996 hPa au Nord-Ouest de l'Irlande se "
    "décalant vers le Nord de l'Irlande plus tard. Puis, se comblant lentement, "
    "prévue 999 hPa quasi-stationnaire à la fin.\nDépression 1002 hPa au Sud-Est "
    "de la Mer du Nord évoluant peu.\nFront froid sur l'Europe de l'Ouest, se "
    "déplaçant vers le Sud-Est.\n",
}


@pytest.mark.parametrize("key, expected", EXPECTED.items())
def test_builder(key: str, expected: str):
    builder = SitGenBuilder()
    builder.compute(REDUCTION[key])
    assert builder._text == expected
