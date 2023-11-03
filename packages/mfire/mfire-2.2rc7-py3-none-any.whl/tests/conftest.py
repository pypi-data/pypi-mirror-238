""" conftest.py : script for configuring pytest sessions
"""
import datetime as dt
import operator
from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from mfire.settings import Settings


def computing_RR_futur(RR, n=6, dim="step"):
    """
    Fonction qui calcul la somme du champ sur les n prochaines steps
    """
    nb_step = RR[dim].size
    RR6_beg = (
        RR.rolling({dim: n}, min_periods=1)
        .sum()
        .shift(step=-(n) + 1)
        .isel({dim: range(nb_step - n + 1)})
    )
    RR6_end = (
        RR.shift(step=-n + 1)
        .rolling({dim: n}, min_periods=1)
        .sum()
        .isel({dim: range(nb_step - n + 1, nb_step)})
    )
    RR6_beg.name = RR.name
    RR6_end.name = RR.name
    return xr.merge([RR6_beg, RR6_end])[RR.name]


def computing_RR_futur_new(RR, n=6, dim="valid_time"):
    """
    Fonction qui calcul la somme du champ sur les n prochaines steps
    """
    nb_step = RR[dim].size
    RR6_beg = (
        RR.rolling({dim: n}, min_periods=1)
        .sum()
        .shift(valid_time=-(n) + 1)
        .isel({dim: range(nb_step - n + 1)})
    )
    RR6_end = (
        RR.shift(valid_time=-n + 1)
        .rolling({dim: n}, min_periods=1)
        .sum()
        .isel({dim: range(nb_step - n + 1, nb_step)})
    )
    RR6_beg.name = RR.name
    RR6_end.name = RR.name
    return xr.merge([RR6_beg, RR6_end])[RR.name]


def create_nc_field_SG(name: str, vmin: float, vmax: float, units: str):
    coords = dict(
        valid_time=[np.datetime64("2022-06-08T00:00:00.000000000")],
        latitude=np.arange(90, -90.25, -0.25),
        longitude=np.arange(-180, 180, 0.25),
    )
    dims = tuple([len(v) for v in coords.values()])
    arr = np.random.randint(vmin, vmax, dims)
    da = (vmax - vmin) * xr.DataArray(arr, coords=coords, dims=coords, name=name) + vmin
    da.attrs["units"] = units
    return da


@pytest.fixture(scope="session")
def working_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    working_dir = tmp_path_factory.mktemp("working_dir")
    Settings().set_full_working_dir(working_dir=working_dir)

    data_dir = Settings().data_dirname
    data_dir.mkdir(parents=True, exist_ok=True)

    # Creation du champ
    np.random.seed(10)
    nb_lat = 50
    lat_b = 35
    nb_lon = 50
    lon_b = -10
    field = 273.15 + np.random.randint(-2, 4, size=(nb_lat, nb_lon, 2))
    field[:, :, 1] = field[:, :, 1] + 2
    lat = range(lat_b, lat_b + nb_lat)
    lon = range(lon_b, lon_b + nb_lon)
    step = [dt.timedelta(hours=1), dt.timedelta(hours=3)]

    # Cération du champ à jour avec valid_time
    field_ds = xr.Dataset()
    field_ds["temperature"] = (("latitude", "longitude", "valid_time"), field)
    field_ds.temperature.attrs["units"] = "K"
    field_ds.temperature.attrs["PROMETHEE_z_ref"] = "mask"
    field_ds["latitude"] = lat
    field_ds["longitude"] = lon
    field_ds["valid_time"] = step
    field_ds.coords["time"] = dt.datetime(2019, 12, 10)
    field_ds["valid_time"] = field_ds["time"] + field_ds["valid_time"]
    field_ds.to_netcdf(data_dir / "field.nc")

    # Creation du mask
    mask = xr.Dataset()
    nb_lat_mask = int(nb_lat / 2)
    nb_lon_mask = int(nb_lon / 2)
    nb_mid_lat = int(nb_lat / 4)
    nb_mid_lon = int(nb_lon / 4)
    np_mask = np.zeros((nb_lat_mask, nb_lon_mask, 2)) * np.nan
    np_mask[:nb_mid_lat, :, 0] = 1
    np_mask[nb_mid_lat:, :, 1] = 1
    mask["mask"] = (("latitude_mask", "longitude_mask", "id"), np_mask)
    mask["latitude_mask"] = range(lat_b + nb_mid_lat, lat_b + nb_mid_lat + nb_lat_mask)
    mask["longitude_mask"] = range(lon_b + nb_mid_lon, lon_b + nb_mid_lon + nb_lon_mask)
    mask["id"] = ["FirstArea", "SecondArea"]
    mask.to_netcdf(data_dir / "mask.nc")
    # Creation de la zone centrale
    dcentral = mask.mask.isel(id=0).where(
        operator.and_(
            operator.and_(mask.latitude_mask > 52, mask.longitude_mask < 20),
            mask.longitude_mask > 10,
        )
    )
    dcentral = dcentral.expand_dims("id")
    dcentral["id"] = ["Central"]
    dcentral.to_netcdf(data_dir / "central_mask.nc")

    # Creation d'un fichier d'altitude
    altitude_ds = xr.Dataset()
    x, y = np.indices((nb_lat, nb_lon))
    field = (
        nb_lat_mask**2
        + nb_lon_mask**2
        - (
            (x + lat_b - field_ds.latitude.mean().values) ** 2
            + (y + lon_b - field_ds.longitude.mean().values) ** 2
        )
        - 5
    )
    altitude_ds["mask"] = (("latitude", "longitude"), field)
    altitude_ds["latitude_mask"] = field_ds.latitude
    altitude_ds["longitude_mask"] = field_ds.longitude
    altitude_ds["mask"].to_netcdf(data_dir / "altitude.nc")

    # Calcul pour les données de pluie
    # RR1 field
    rr1_field_ds = xr.Dataset()
    ex_bertrand_3D = [
        [
            [0, 4, 6, 7, 5, 3, 0, 0, 1, 0, 0, 0, 0],
            [1, 2, 8, 5, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ],
        [
            [1, 10, 10, 2, 2, 3, 0, 0, 3, 5, 5, 1, 0],
            [1, 10, 10, 2, 2, 3, 0, 0, 3, 5, 5, 1, 0],
        ],
    ]
    rr1_field_ds["tp"] = (("latitude", "longitude", "valid_time"), ex_bertrand_3D)
    rr1_field_ds.tp.attrs["units"] = "mm"
    rr1_field_ds.tp.attrs["PROMETHEE_z_ref"] = "mask"
    rr1_field_ds.tp.attrs["GRIB_stepUnits"] = 1
    rr1_field_ds.tp.attrs["accum_hour"] = 1
    rr1_field_ds["latitude"] = [1, 2]
    rr1_field_ds["longitude"] = [1, 2]
    rr1_field_ds["valid_time"] = [
        dt.datetime(2019, 12, 10) + dt.timedelta(hours=int(n)) for n in np.arange(13)
    ]
    rr1_field_ds.to_netcdf(data_dir / "RR1.nc")

    # RR1 grib style (using step and date coords)
    rr1_grib_ds = xr.Dataset()
    rr1_grib_ds["tp"] = (("latitude", "longitude", "step"), ex_bertrand_3D)
    rr1_grib_ds.tp.attrs["units"] = "mm"
    rr1_grib_ds.tp.attrs["PROMETHEE_z_ref"] = "mask"
    rr1_grib_ds.tp.attrs["GRIB_stepUnits"] = 1
    rr1_grib_ds.tp.attrs["accum_hour"] = 1
    rr1_grib_ds["step"] = [dt.timedelta(hours=int(n)) for n in np.arange(13)]
    rr1_grib_ds["latitude"] = [1, 2]
    rr1_grib_ds["longitude"] = [1, 2]

    rr1_grib_ds.coords["time"] = dt.datetime(2019, 12, 10)
    rr1_grib_ds.to_netcdf(data_dir / "RR1_grib.nc")

    # RR6 field
    rr6_field_ds = computing_RR_futur_new(rr1_field_ds.tp, n=6, dim="valid_time")
    rr6_field_ds.attrs["units"] = "mm"
    rr6_field_ds.attrs["PROMETHEE_z_ref"] = "mask"
    rr6_field_ds.attrs["accum_type"] = "futur"
    rr6_field_ds.attrs["accum_hour"] = 6
    rr6_field_ds.attrs["GRIB_stepUnits"] = 1
    rr6_field_ds.to_netcdf(data_dir / "RR6.nc")

    # RR3 field
    rr3_field_ds = rr1_field_ds.tp.rolling(valid_time=3, min_periods=1).sum()[
        :, :, 2::3
    ]  # computing_RR_futur(ds.tp,n=3,dim="step")
    rr3_field_ds.name = "RR"
    rr3_field_ds.attrs["units"] = "mm"
    rr3_field_ds.attrs["PROMETHEE_z_ref"] = "mask"
    rr3_field_ds.attrs["accum_type"] = "futur"
    rr3_field_ds.attrs["accum_hour"] = 3
    rr3_field_ds.attrs["GRIB_stepUnits"] = 1
    rr3_field_ds.attrs["accum_hour"] = 3
    rr3_field_ds.to_netcdf(data_dir / "RR3.nc")

    # RR3 grib style (using step and date coords)
    rr3_grib_ds = rr1_grib_ds.tp.rolling(step=3, min_periods=1).sum()[
        :, :, 2::3
    ]  # computing_RR_futur(ds.tp,n=3,dim="step")
    rr3_grib_ds.name = "RR"
    rr3_grib_ds.attrs["units"] = "mm"
    rr3_grib_ds.attrs["PROMETHEE_z_ref"] = "mask"
    rr3_grib_ds.attrs["accum_type"] = "futur"
    rr3_grib_ds.attrs["accum_hour"] = 3
    rr3_grib_ds.attrs["GRIB_stepUnits"] = 1
    rr3_grib_ds.attrs["accum_hour"] = 3
    rr3_grib_ds.to_netcdf(data_dir / "RR3_grib.nc")

    # RR6 bis field
    rr6_bis_field_ds = computing_RR_futur_new(rr3_field_ds, n=2, dim="valid_time")
    rr6_bis_field_ds.attrs["units"] = "mm"
    rr6_bis_field_ds.attrs["PROMETHEE_z_ref"] = "mask"
    rr6_bis_field_ds.attrs["accum_type"] = "futur"
    rr6_bis_field_ds.attrs["accum_hour"] = 6
    rr6_bis_field_ds.attrs["GRIB_stepUnits"] = 1
    rr6_bis_field_ds.to_netcdf(data_dir / "RR6_b.nc")

    # RR_mask
    mask = xr.Dataset()
    np_mask = np.zeros((2, 2, 2)) * np.nan
    np_mask[:, :, 0] = 1
    np_mask[1, :, 1] = 1
    mask["mask"] = (("latitude", "longitude", "id"), np_mask)
    mask["latitude"] = [1, 2]
    mask["longitude"] = [1, 2]
    mask["id"] = ["FirstArea", "SecondArea"]
    mask.to_netcdf(data_dir / "RR_mask.nc")

    # Settings SG files
    sg_fields = (
        ("r_700", 0, 100, "%"),
        ("msl", 94036, 105782, "hPa"),
        ("t2m", 194, 323, "K"),
        ("wbpt_850", 232, 302, "K"),
        ("u10", -25, 31, "m/s"),
        ("v10", -28, 26, "m/s"),
        ("u_850", -48, 45, "m/s"),
        ("v_850", -50, 35, "m/s"),
    )

    for field in sg_fields:
        create_nc_field_SG(*field).to_netcdf(data_dir / f"{field[0]}.nc")

    # Setting SG mask
    coords = dict(
        latitude=np.arange(80, -0.25, -0.25),
        longitude=np.arange(-50, 60.25, 0.25),
        id=["global"],
    )
    xr.DataArray(
        np.ones([len(v) for v in coords.values()]),
        coords=coords,
        dims=tuple(coords),
        name="globd025",
    ).to_netcdf(data_dir / "situation_generale_marine.nc")

    return working_dir


@pytest.fixture()
def root_path(request):
    return request.config.rootdir


@pytest.fixture()
def test_path(request) -> Path:
    return Path(request.config.rootdir) / "tests"


@pytest.fixture()
def test_file_path(request) -> Path:
    return Path(request.config.rootdir) / "tests" / "__temp__.txt"


@pytest.fixture()
def test_file(request):
    path = Path(request.config.rootdir) / "tests" / "__temp__.txt"
    if path.exists():
        path.unlink()

    f = open(path, "w")
    yield f
    path.unlink()
