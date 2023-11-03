import json
from pathlib import Path

import pytest
import xarray as xr

from mfire.tasks.process_mask import main
from mfire.utils.xr_utils import compress_netcdf

ROOT_DIR = Path(__file__).parent

MASK_CONFIG = Path(ROOT_DIR, "input", "mask_config.json")


def create_compress_mask():
    """
        Create the netcdf mask file from config
        with compression option

        to be executed once config file changed
        to re-create the reference mask file
        for example with the command :

    python -c 'from test_mask_processor import create_compress_mask;
    create_compress_mask()'

    """
    conf, reference, fout = load_conf("0")
    fout = Path(fout)
    if fout.exists():
        fout.unlink()
    main(conf)
    dtest = xr.open_dataset(fout)
    compress_netcdf(dtest, reference)


def load_conf(keyconf):
    with open(MASK_CONFIG, "r") as fp:
        data = json.load(fp)
    data[keyconf]["name"] = keyconf
    conf = data[keyconf]
    reference = Path(ROOT_DIR, conf["file"].replace("test_output", "reference_output"))
    fout = conf["file"]
    return conf, reference, fout


class TestMask:
    @pytest.mark.skip
    @pytest.mark.filterwarnings("ignore: warnings")
    def test_mask31(self):
        conf, reference, fout = load_conf("0")
        fout = Path(fout)
        if fout.exists():
            fout.unlink()
        main(conf)
        dtest = xr.open_dataset(fout)
        dvalid = xr.open_dataset(reference)
        xr.testing.assert_equal(dtest, dvalid)
        assert dtest == dvalid
        dtest.close()
        dvalid.close()
        fout.unlink()

    @pytest.mark.skip
    def test_maskCEI11(self):
        conf, reference, fout = load_conf("1")
        fout = Path(fout)
        if fout.exists():
            fout.unlink()
        main(conf)
        dtest = xr.open_dataset(fout)
        dvalid = xr.open_dataset(reference)
        xr.testing.assert_equal(dtest, dvalid)
        assert dtest == dvalid
        dtest.close()
        fout.unlink()
