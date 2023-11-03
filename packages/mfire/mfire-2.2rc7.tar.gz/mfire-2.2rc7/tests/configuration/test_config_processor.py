import os
from pathlib import Path
from typing import Optional

import numpy as np
import pytest

from mfire.configuration import VersionConfig
from mfire.configuration.config_processor import ConfigMetronomeProcessor
from mfire.settings import SETTINGS_DIR, Settings
from mfire.utils import JsonFile, json_diff
from mfire.utils.date import Datetime

# numpy.random seed
np.random.seed(42)

# Basic tests configuration
DRAFTING_DATETIME = Datetime(2021, 10, 20, 8)


class TestConfigProcessor:
    """New class for testing the config processing step"""

    origin_configs_dir: Path = (
        Path(__file__).absolute().parent.parent / "test_data/20211020T0800P/configs/"
    )
    config_basename: Path = Path("prometheeInit.json")

    @pytest.fixture(scope="session")
    def local_working_dir(self, working_dir) -> Path:
        """pytest fixture for creating a new tmp working
        directory
        """
        config_filename = self.origin_configs_dir / self.config_basename
        os.environ["mfire_config_filename"] = str(config_filename)

        # creating a new configs dir
        config_filename.parent.mkdir(parents=True, exist_ok=True)
        return working_dir

    def get_ref_filename(self, rules: Optional[str], basename: str) -> Path:
        if rules is None:
            return self.origin_configs_dir / basename
        return self.origin_configs_dir / rules / basename

    def single_config_test(self, dirname: Path, rules: str):
        settings = Settings()
        cp = ConfigMetronomeProcessor(
            config_filename=settings.config_filename,
            rules=rules,
            drafting_datetime=DRAFTING_DATETIME,
        )
        assert cp.version_config == VersionConfig(
            version="d06fb0a3",
            drafting_datetime=Datetime(2021, 10, 20, 8),
            reference_datetime=Datetime(2021, 10, 20, 8),
            production_datetime=Datetime(2021, 10, 20, 9),
            configuration_datetime=Datetime(2021, 10, 19, 20, 45, 12),
        )

        mask_dico, data_dico, prod_dico = cp.process_single_config(0)
        rules_dirname = dirname / rules
        rules_dirname.mkdir(parents=True, exist_ok=True)
        # mask
        mask_config_filename = rules_dirname / "mask.json"
        JsonFile(str(mask_config_filename)).dump(mask_dico)
        assert json_diff(
            left=mask_config_filename,
            right=self.get_ref_filename(rules, "single_mask.json"),
            working_dir=dirname,
        )

        # data
        new_data_dico = {" ".join(key): value for key, value in data_dico.items()}
        data_config_filename = rules_dirname / "data.json"
        JsonFile(str(data_config_filename)).dump(new_data_dico)
        assert json_diff(
            left=data_config_filename,
            right=self.get_ref_filename(rules, "single_data.json"),
            working_dir=dirname,
        )

        # prod
        prod_config_filename = rules_dirname / "prod.json"
        JsonFile(str(prod_config_filename)).dump(prod_dico)
        assert json_diff(
            left=prod_config_filename,
            right=self.get_ref_filename(rules, "single_prod.json"),
            working_dir=dirname,
            SETTINGS_DIR=SETTINGS_DIR,
        )

    def test_single_config_alpha(self, local_working_dir: Path):
        self.single_config_test(dirname=local_working_dir, rules="alpha")

    def test_single_config_psym(self, local_working_dir: Path):
        self.single_config_test(dirname=local_working_dir, rules="psym")

    def test_single_config_psym_archive(self, local_working_dir: Path):
        self.single_config_test(dirname=local_working_dir, rules="psym_archive")

    # def test_single_config_arpege(self, local_working_dir: Path):
    #     self.single_config_test(dirname=local_working_dir, rules="arpege")

    def test_source_file_terms(self, local_working_dir: Path):
        settings = Settings()
        cp = ConfigMetronomeProcessor(
            config_filename=settings.config_filename,
            rules="alpha",
            drafting_datetime=DRAFTING_DATETIME,
        )

        assert cp.version_config == VersionConfig(
            version="d06fb0a3",
            drafting_datetime=Datetime(2021, 10, 20, 8),
            reference_datetime=Datetime(2021, 10, 20, 8),
            production_datetime=Datetime(2021, 10, 20, 9),
            configuration_datetime=Datetime(2021, 10, 19, 20, 45, 12),
        )

        source_terms_dico = cp.source_files_terms(
            file_id="france_jj1_2021-10-20T00:00:00+00:00_maj08",
            param="FF__HAUTEUR10",
            accum=None,
        )
        sources_terms_ref = {
            "pprod_frjj1_2021-10-20T00:00:00+00:00_maj8": {
                "terms": list(range(8, 49)),
                "step": 1,
            }
        }
        assert source_terms_dico == sources_terms_ref
        data_config_filename = local_working_dir / "data_config.json"
        JsonFile(str(data_config_filename)).dump(cp.data_config)
        assert json_diff(
            left=data_config_filename,
            right=self.get_ref_filename(None, "data_config.json"),
            working_dir=local_working_dir,
        )
