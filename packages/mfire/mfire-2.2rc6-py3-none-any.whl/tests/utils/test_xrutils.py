import datetime as dt
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import mfire.utils.xr_utils as xru
from mfire.utils.unit_converter import convert_dataarray

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


def load_dataset(dirname: Path, decalage: int):
    """
    Permet de charger le dataset à tester.

    Args:
        decalage (int, optional): [description]. Defaults to 12.
            Decalage de la serie des RR3.
            Permet de gérer differnts cas test en conservant un code commun.

    Returns:
        (dataArray,dataArray): Le premier dataarray correspond aux valeurs à cumulées.
            Le second correspond aux stepUnits présentes dans les fichiers.
    """
    rr1 = xr.open_dataarray(dirname / "RR1_grib.nc")
    rr3 = xr.open_dataarray(dirname / "RR3_grib.nc")
    # On va
    rr3_shift = rr3.copy()
    rr3_shift.name = "tp"
    rr3_shift.coords["step"] = pd.to_timedelta(rr3["step"].values) + dt.timedelta(
        hours=decalage
    )
    rr_merge = xr.merge([rr1, rr3_shift])
    stepsize = []
    stepsize.extend([rr1.attrs["accum_hour"]] * rr1.step.size)
    stepsize.extend([rr3_shift.attrs["accum_hour"]] * rr3_shift.step.size)
    ds_step = xr.Dataset()
    ds_step["stepSize"] = ("step", stepsize)
    ds_step.coords["step"] = rr_merge.step
    return (rr_merge.tp, ds_step.stepSize)


class TestXrUtils:
    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_cumul(self, working_dir: Path):
        data_dirname = working_dir / "data"
        # Dans ce cas on test une desagregation puis cumul conventionels
        tp, stepsize = load_dataset(data_dirname, 13)
        dout_13 = xru.compute_sum_futur(
            tp.isel(latitude=0).isel(longitude=0), da_step=stepsize
        )
        da = xr.DataArray(
            [
                25.0,
                25.0,
                21.0,
                16.0,
                9.0,
                4.0,
                1.0,
                1.0,
                4.3333333,
                6.6666666,
                10.0,
                15.0,
                20.0,
                25.0,
                22.0,
                19.0,
                16.0,
                11.0,
                6.0,
                1.0,
                0.6666666,
                0.3333333,
                0.0,
                0.0,
                0.0,
            ],
            dims=("step"),
            name="tp",
        ).astype("float32")
        assert (dout_13.round(5).values == da.round(5).values).all()

        # Dans ce cas on test la desagregation (non conventionnelle)
        tp, stepsize = load_dataset(data_dirname, 12)
        dout_12 = xru.compute_sum_futur(
            tp.isel(latitude=0).isel(longitude=0), da_step=stepsize
        )
        da = xr.DataArray(
            [
                25.0,
                25.0,
                21.0,
                16.0,
                9.0,
                4.0,
                1.0,
                1.0,
                4.3333333,
                6.6666666,
                11.6666666,
                16.6666666,
                21.6666666,
                22.0,
                19.0,
                16.0,
                11.0,
                6.0,
                1.0,
                0.6666666,
                0.3333333,
                0.0,
                0.0,
                0.0,
            ],
            dims=("step"),
        ).astype("float32")
        assert (dout_12.round(5).values == da.round(5).values).all()

        # On test maintenant qu'une exception est bien levee dans ce cas
        tp, stepsize = load_dataset(data_dirname, 18)
        with pytest.raises(xru.InputError):
            xru.compute_sum_futur(
                tp.isel(latitude=0).isel(longitude=0), da_step=stepsize
            )

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_fill_dataarray(self):
        """Test xr_utils.fill_dataarray"""
        time_dim = "time"
        freq_base = "h"
        # Source data_array
        source_da = xr.DataArray(
            [0, 1, 2, 4, 5],
            dims=time_dim,
            coords={
                time_dim: [
                    np.datetime64("2021-06-17T09:00:00"),
                    np.datetime64("2021-06-17T12:00:00"),
                    np.datetime64("2021-06-17T15:00:00"),
                    np.datetime64("2021-06-17T21:00:00"),
                    np.datetime64("2021-06-18T03:00:00"),
                ]
            },
        )
        source_steps = [3, 3, 3, 3, 6]

        # Target data_array
        start = np.datetime64("2021-06-17T08:00:00")
        stop = np.datetime64("2021-06-18T00:00:00")
        target_step = 1
        td_step = np.timedelta64(target_step, freq_base)
        target_da = xr.DataArray(
            [0, 0, 1, 1, 1, 2, 2, 2, np.nan, np.nan, np.nan, 4, 4, 4, 5, 5, 5],
            dims=time_dim,
            coords={time_dim: np.arange(start, stop + td_step, td_step)},
        ).dropna(dim=time_dim)

        # Filling source_da
        new_da = xru.fill_dataarray(
            da=source_da,
            source_steps=source_steps,
            target_step=target_step,
            dim=time_dim,
            freq_base=freq_base,
        )

        new_da = xru.slice_dataarray(
            da=new_da,
            start=start,
            stop=stop,
            dim=time_dim,
        )

        xr.testing.assert_equal(new_da, target_da)

    def test_convert_dataarray(self):
        da_w1 = xr.DataArray([4, 10, 20, 24], attrs={"units": "w1"})
        da_wwmf = xr.DataArray([38, 52, 77, 91], attrs={"units": "wwmf"})
        xr.testing.assert_identical(convert_dataarray(da_w1, "wwmf"), da_wwmf)
