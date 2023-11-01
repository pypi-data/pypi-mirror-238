"""test_templates.py

Unit tests of the text.template.py module.
"""
from configparser import ConfigParser

# Standard packages
from pathlib import Path

import numpy as np
import pandas as pd

# Third parties packages
import pytest

# Own package
from mfire.settings import TEMPLATES_FILENAMES
from mfire.text import template
from mfire.utils import JsonFile

# numpy.random seed
np.random.seed(42)


def get_filename(dirname: Path, ext: str, opt: str = "") -> Path:
    """get_gilename : function which generate a name for a template file."""
    return Path(dirname) / f"{ext}_tpl{opt}.{ext}"


@pytest.mark.filterwarnings("ignore: warnings")
def test_templates():
    """test_templates : test the validity of templates files given in conf"""
    for tpl_type in ("period", "multizone", "monozone"):
        elt = TEMPLATES_FILENAMES["fr"][tpl_type]
        if isinstance(elt, dict):
            for filename in elt.values():
                assert filename.is_file()
                tpl_rtr = template.read_file(filename)
                if filename.suffix == ".json":
                    assert isinstance(tpl_rtr, template.JsonTemplateRetriever)
                elif filename.suffix == ".ini":
                    assert isinstance(tpl_rtr, template.IniTemplateRetriever)
        else:
            filename = elt
            assert filename.is_file()
            tpl_rtr = template.read_file(filename)
            if filename.suffix == ".json":
                assert isinstance(tpl_rtr, template.JsonTemplateRetriever)
            elif filename.suffix == ".ini":
                assert isinstance(tpl_rtr, template.IniTemplateRetriever)


def test_template_format():
    """test_template_format : test the method format()"""

    my_str = (
        "This is a {adj} template made by {template_author_name} in "
        "{template_date_year} !!"
    )
    vars = {
        "template": {
            "author": {"name": "toto", "age": 30},
            "date": {"month": "may", "year": 2022},
        },
        "adj": "beautiful",
    }

    my_tmplt = template.Template(my_str)
    text = my_tmplt.format(**vars)

    result = "This is a beautiful template made by toto in 2022 !!"
    assert text == result

    vars = {}
    text_empty = my_tmplt.format(**vars)

    assert text_empty == my_str


class TestTemplateRetrievers:
    """TestTemplateRetrievers : class for testing the template retrievers classes"""

    json_templates = {"A": "toto", "B": ["tata", "titi", "tutu"], "D": {"E": "tyty"}}
    csv_templates = pd.DataFrame(
        [[0, 0, "toto"], [0, 1, "tata"], [1, 0, "titi"], [1, 1, "tutu"]],
        columns=["A", "B", "template"],
    ).set_index(["A", "B"])
    csv_weights = [0.7, 0.25]

    @property
    def ini_templates(self):
        """ini_templates: property initializing an ini-like templates table"""
        config = ConfigParser()
        config["DEFAULT"]["A"] = "toto"
        config["DEFAULT"]["B"] = "tata"
        config.add_section("D")
        config["D"]["E"] = "tyty"
        return config

    @pytest.fixture(scope="session")
    def local_working_dir(self, working_dir):
        """local_working_dir : pytest fixture for creating a new
        tmp working directory
        """

        # json
        JsonFile(get_filename(working_dir, "json")).dump(self.json_templates)

        # ini
        with open(get_filename(working_dir, "ini"), "w") as ini_f:
            self.ini_templates.write(ini_f)

        # csv
        self.csv_templates.to_csv(get_filename(working_dir, "csv"))

        # centroids
        df = pd.read_csv(get_filename(working_dir, "csv"))
        df.loc["weights"] = self.csv_weights + [None]
        df.to_csv(get_filename(working_dir, "csv", "centroids"))

        return working_dir

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_json_template_retriever(self, local_working_dir):
        """test_json_template_retriever : Test the JsonTemplateRetriever class

        Args:
            local_working_dir (pathlib.Path): fixture which provides a temporary
            directory unique to the test invocation
        """
        # testing simple instantiation
        tpl_rtr = template.JsonTemplateRetriever(self.json_templates)
        assert tpl_rtr.get("A") == self.json_templates.get("A")
        assert tpl_rtr.get("B") in self.json_templates.get("B")
        assert tpl_rtr.get("B", pop_method="first") == self.json_templates.get("B")[0]
        assert tpl_rtr.get("B", pop_method="last") == self.json_templates.get("B")[-1]
        pop_method = "-".join
        assert tpl_rtr.get("B", pop_method=pop_method) == pop_method(
            self.json_templates.get("B")
        )
        assert tpl_rtr.get("C", default="tete") == "tete"
        assert tpl_rtr.get(("D", "E")) == self.json_templates.get("D").get("E")

        # testing opening
        tpl_rtr_2 = template.JsonTemplateRetriever.read_file(
            get_filename(local_working_dir, "json")
        )
        assert tpl_rtr_2 == tpl_rtr
        tpl_rtr_3 = template.read_file(get_filename(local_working_dir, "json"))
        assert tpl_rtr_3 == tpl_rtr

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_ini_template_retriever(self, local_working_dir):
        """test_ini_template_retriever : Test the IniTemplateRetriever class

        Args:
            local_working_dir (py.path.local): fixture which provides a temporary
            directory unique to the test invocation
        """
        # testing simple instantiation
        tpl_rtr = template.IniTemplateRetriever(self.ini_templates)
        assert tpl_rtr.get("A") == self.ini_templates.get("DEFAULT", "A")
        assert tpl_rtr.get("B") == self.ini_templates.get("DEFAULT", "B")
        assert tpl_rtr.get("C", "tete") == "tete"
        assert tpl_rtr.get(("D", "E")) == self.ini_templates.get("D", "E")

        # testing opening
        tpl_rtr_2 = template.IniTemplateRetriever.read_file(
            get_filename(local_working_dir, "ini")
        )
        assert tpl_rtr_2 == tpl_rtr
        tpl_rtr_3 = template.read_file(get_filename(local_working_dir, "ini"))
        assert tpl_rtr_3 == tpl_rtr

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_csv_template_retriever(self, local_working_dir):
        """test_csv_template_retriever : Test the csvTemplateRetriever class

        Args:
            local_working_dir (py.path.local): fixture which provides a temporary
            directory unique to the test invocation
        """
        # testing simple instantiation
        tpl_rtr = template.CsvTemplateRetriever(self.csv_templates)
        assert tpl_rtr.get((0, 0)) == "toto"
        assert tpl_rtr.get((0, 1)) == "tata"
        assert tpl_rtr.get((1, 0)) == "titi"
        assert tpl_rtr.get((1, 1)) == "tutu"
        assert tpl_rtr.get((1, 2), "wrong key again") == "wrong key again"
        assert tpl_rtr.get([1, 1], "not a tuple key") == "not a tuple key"

        # testing opening
        tpl_rtr2 = template.CsvTemplateRetriever.read_file(
            get_filename(local_working_dir, "csv"),
            index_col=["A", "B"],
        )
        assert tpl_rtr == tpl_rtr2

        tpl_rtr3 = template.read_file(
            get_filename(local_working_dir, "csv"),
            index_col=["A", "B"],
        )
        assert tpl_rtr == tpl_rtr3

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_centroid_template_retriever(self, local_working_dir):
        """test_centroid_template_retriever : Test the CentroidTemplateRetriever class

        Args:
            local_working_dir (py.path.local): fixture which provides a temporary
            directory unique to the test invocation
        """
        # testing simple instantiation
        tpl_rtr = template.CentroidTemplateRetriever(
            self.csv_templates,
            col="template",
            weights=self.csv_weights,
        )
        assert tpl_rtr.get([1, 2]) == "tutu"
        assert tpl_rtr.get([-1, 0.8]) == "tata"

        # testing opening
        tpl_rtr2 = template.CentroidTemplateRetriever.read_file(
            get_filename(local_working_dir, "csv", "centroids")
        )
        assert tpl_rtr == tpl_rtr2

        tpl_rtr3 = template.read_file(
            get_filename(local_working_dir, "csv", "centroids")
        )
        assert tpl_rtr == tpl_rtr3

        # testing opening of SHORT_TERM_CONFIG
        tpl_rtr4 = template.CentroidTemplateRetriever.read_file(
            TEMPLATES_FILENAMES["fr"]["period"]["short"]
        )
        assert (
            tpl_rtr4.get([1, 16, 18, 42])
            == "de ce {weekday} soir à {weekday_p1} début de soirée"
        )
        assert (
            tpl_rtr4.get([0, 16, 18, 42])
            == "de {weekday} soir à {weekday_p1} début de soirée"
        )

        # testing dtw in get method
        tpl_rtr5 = template.CentroidTemplateRetriever(
            self.csv_templates,
            col="template",
        )

        tpl_dict = tpl_rtr5.get_by_dtw([1, 1, 1, 0, 0, 0, 0])

        assert tpl_dict["template"] == "titi"
        assert tpl_dict["centroid"] == (1, 0)
