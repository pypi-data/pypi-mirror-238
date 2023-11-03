from copy import deepcopy
from pathlib import Path

import pytest

from mfire.utils import JsonFile, dict_diff, json_diff


class TestJsonDiff:
    """File for testing the Json diff functions"""

    base = {
        "id": "13616845",
        "name": "toto",
        "components": [
            {
                "hazard": "5421",
                "levels": [
                    {
                        "level": 1,
                        "elementsEvent": [
                            {"field": {"file": "toto.nc"}},
                            {"field": {"file": "tata.nc"}},
                        ],
                    },
                    {
                        "level": 2,
                        "elementsEvent": [
                            {"field": {"file": "tutu.nc"}},
                        ],
                    },
                ],
            },
            {
                "hazard": "3116",
                "levels": [
                    {
                        "level": 2,
                        "elementsEvent": [
                            {"field": {"file": "titi.nc"}},
                        ],
                    }
                ],
            },
        ],
    }
    basename = "base.json"

    @pytest.fixture(scope="session")
    def local_working_dir(self, working_dir) -> Path:
        """local_working_dir : pytest fixture for creating a new
        tmp working directory
        """
        JsonFile(working_dir / self.basename).dump(self.base)
        return working_dir

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_dict_diff(self):
        # checking copies
        assert dict_diff(left=self.base, right=self.base.copy())
        assert dict_diff(left=self.base, right=deepcopy(self.base))

        # checking small inversions in lists
        inv_compos = deepcopy(self.base)
        inv_compos["components"] = list(reversed(inv_compos["components"]))
        assert dict_diff(left=self.base, right=inv_compos)

        # checking adding or removing of keys
        new_keys = deepcopy(self.base)
        new_keys["toto"] = "jiej"
        assert not dict_diff(left=self.base, right=new_keys)

        missing_keys = {
            "name": self.base["name"],
            "components": deepcopy(self.base["components"]),
        }
        assert not dict_diff(left=self.base, right=missing_keys)

        # checking list lenghts changes
        list_lengths = deepcopy(self.base)
        list_lengths["components"][0]["levels"] += [{"level": 3, "fan": "zizou"}]
        assert not dict_diff(left=self.base, right=list_lengths)

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_json_diff(self, local_working_dir: Path):
        local_dico = deepcopy(self.base)
        local_dico["components"] = list(reversed(local_dico["components"]))

        base_filename = local_working_dir / self.basename
        local_filename = local_working_dir / "local.json"

        JsonFile(local_filename).dump(local_dico)

        assert json_diff(base_filename, local_filename)
