"""test_templates.py

Unit tests of the text.template.py module.
"""
# Standard packages
import json

import numpy as np

# Third parties packages
import pytest

# Own package
from mfire.settings import TEMPLATES_FILENAMES, Settings
from mfire.text.comment import FFRafBuilder, RepresentativeValueBuilder

# numpy.random seed
np.random.seed(42)


class TestRepresentativeBuilder:
    """TestRepresentativeBuilder : class for testing the representative builder
    classes"""

    @pytest.mark.filterwarnings("ignore: warnings")
    def test_json_template_retriever(self):
        """test_json_template_retriever : Test the JsonTemplateRetriever class

        Args:
            working_dir (py.path.local): fixture which provides a temporary
            directory unique to the test invocation
        """

        with open(
            TEMPLATES_FILENAMES[Settings().language]["multizone"]["rep_val"]
        ) as fp:
            template_rr = json.load(fp)

        with open(
            TEMPLATES_FILENAMES[Settings().language]["multizone"]["rep_val_FFRaf"]
        ) as fp:
            template_raf = json.load(fp)

        ref_dict = {
            "RAF__HAUTEUR10": ["plain", "plain_mountain"],
            "NEIPOT24__SOL": ["plain", "plain_mountain"],
        }

        ref_builder = {
            "RAF__HAUTEUR10": FFRafBuilder(),
            "NEIPOT24__SOL": RepresentativeValueBuilder(),
        }

        ref_template = {"RAF__HAUTEUR10": template_raf, "NEIPOT24__SOL": template_rr}

        for key, sentence_type_list in ref_dict.items():
            builder = ref_builder[key]
            for sentence_type in sentence_type_list:
                assert (
                    builder.get_sentence(key, sentence_type)
                    in ref_template[key][sentence_type]
                )
