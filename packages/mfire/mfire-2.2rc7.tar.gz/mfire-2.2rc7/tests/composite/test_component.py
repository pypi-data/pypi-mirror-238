import shutil
from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from mfire.localisation.localisation_manager import Localisation
from mfire.localisation.spatial_localisation import SpatialIngredient
from mfire.localisation.table import SummarizedTable
from mfire.localisation.temporal_localisation import TemporalLocalisation
from mfire.settings.constants import SETTINGS_DIR
from mfire.text.comment.multizone import ComponentHandlerLocalisation
from mfire.utils import JsonFile, recursive_format
from mfire.utils.date import Datetime, Period, Timedelta

np.random.seed(0)


TEST_DATA_DIR = TEST_DATA_DIR = Path(__file__).absolute().parent.parent / "test_data"


# On doit créer le tableau spatial
def define_spatial_table(evt_size, risk_level=1):
    spatial_table = xr.Dataset()
    spatial_table.coords["id"] = [
        "CD38_domain_compass__Est",
        "CD38_domain_compass__NordOuest",
        "cde3bf79-4afd-43bb-88e7-7658c52f51b6",
    ]
    spatial_table.coords["risk_level"] = [risk_level]
    spatial_table.coords["evt"] = [i for i in range(0, evt_size)]
    spatial_table.coords["valid_time"] = [
        (Datetime(2020, 12, 8, 0) + Timedelta(hours=i)).as_np_datetime64()
        for i in range(12)
    ]
    spatial_table["areaName"] = (("id"), ["Est", "NordOuest", "SudOuest"])
    spatial_table = spatial_table.swap_dims({"id": "areaName"}).swap_dims(
        {"areaName": "id"}
    )
    spatial_table["weatherVarName"] = (
        ("risk_level", "evt"),
        [["var_" + str(i) for i in range(0, evt_size)]],
    )
    dim_id = spatial_table.id.size
    dim_risk = spatial_table.risk_level.size
    dim_time = spatial_table.valid_time.size

    spatial_table["density"] = (
        ("risk_level", "evt", "valid_time", "id"),
        np.random.rand(dim_risk, evt_size, dim_time, dim_id),
    )
    spatial_table["rep_value_plain"] = (
        ("risk_level", "evt", "valid_time", "id"),
        4 + np.random.randn(dim_risk, evt_size, dim_time, dim_id),
    )
    spatial_table["risk_density"] = (
        ("risk_level", "valid_time", "id"),
        np.random.rand(dim_risk, dim_time, dim_id),
    )
    if evt_size == 1:
        spatial_table["risk_density"].values[0, 11, 1] = 0
    spatial_table["occurrence"] = spatial_table["risk_density"] > 0.6
    return spatial_table


def define_param():
    """
    On definit des "aleas" random.
    Le random étant fixé on connait cependant ce qu'on souhaite avoir.

    Returns:
        xr.Dataset : Le dataset contenant un retour de type paramGenerator.
    """
    spatial_one = define_spatial_table(evt_size=1, risk_level=3)
    spatial_two = define_spatial_table(evt_size=3, risk_level=1)
    ds = xr.merge([spatial_one, spatial_two])
    return ds


def define_LocaInfo():
    return {
        "geo_id": "CD38_domain",
        "period": ["2020-12-08T08:00:00.000000000", "2020-12-08T09:00:00.000000000"],
        "risk_level": 3,
    }


def get_json_spatialIngredient(dirname: Path):
    dout = {
        "geos": {
            "file": dirname / "SpatialIngredient.nc",
            "grid_name": "eurw1s100",
            "domain_id": "CD38_domain",
            "full_list_id": [
                "CD38_domain_alt__sup_350",
                "CD38_domain_alt__sup_1200",
                "CD38_domain_alt__inf_500",
                "CD38_domain_alt__sup_800",
                "CD38_domain_compass__SudEst",
                "CD38_domain_alt__inf_300",
                "CD38_domain_alt__sup_700",
                "CD38_domain_alt__sup_1400",
                "CD38_domain_alt__inf_400",
                "CD38_domain_compass__SudOuest",
                "CD38_domain_alt__sup_600",
                "CD38_domain_compass__Nord",
                "CD38_domain_alt__sup_1000",
                "CD38_domain_alt__sup_300",
                "CD38_domain_alt__sup_1600",
                "CD38_domain_compass__Est",
                "CD38_domain_alt__sup_1800",
                "CD38_domain_compass__NordOuest",
                "CD38_domain_alt__sup_500",
                "CD38_domain_alt__sup_400",
                "CD38_domain_compass__Sud",
                "CD38_domain_alt__inf_250",
                "CD38_domain_compass__NordEst",
                "CD38_domain_alt__sup_900",
                "CD38_domain_compass__Ouest",
                "CD38_domain_alt__sup_250",
            ],
        },
        "localized": {
            "file": dirname / "SpatialIngredientlocalized.nc",
            "grid_name": "eurw1s100",
        },
    }
    return dout


def define_data(dirname: Path = Path("working_dir")):
    """
    Permet de définir pas mal de chose.

    Args:
        dirname (str, optional): [description]. Defaults to "working_dir".
    """
    dirname.mkdir(parents=True, exist_ok=True)
    spatial_table = define_param()
    spatial_table.to_netcdf(dirname / "spatial_table.nc")
    fname = "LocalisationInfo.json"
    JsonFile(dirname / fname).dump(define_LocaInfo())

    dictIngredient = get_json_spatialIngredient(dirname)
    JsonFile(dirname / "SpatialIngredient.json").dump(dictIngredient)

    shutil.copyfile(
        TEST_DATA_DIR / "SpatialIngredient.nc",
        dirname / "SpatialIngredient.nc",
    )
    shutil.copyfile(
        TEST_DATA_DIR / "SpatialIngredientlocalized.nc",
        dirname / "SpatialIngredientlocalized.nc",
    )

    JsonFile(dirname / "component.json").dump(
        recursive_format(
            JsonFile(TEST_DATA_DIR / "component_config.json").load(),
            values={"settings_dir": SETTINGS_DIR},
        )
    )

    spatial_ingredient = SpatialIngredient.load(dirname / "SpatialIngredient")
    tempo_handler = TemporalLocalisation(
        spatial_table["occurrence"].isel(risk_level=1),
        area_dimension="id",
        time_dimension="valid_time",
    )
    table_3p = tempo_handler.new_division()
    period = Period(
        spatial_table.valid_time.min().values, spatial_table.valid_time.max().values
    )
    summarized_handler = SummarizedTable(
        table_3p,
        spatial_ingredient=spatial_ingredient,
        request_time=Datetime(2020, 12, 8, 0).strftime("%Y%m%dT%H"),
        full_period=period,
    )
    print("Before saving", summarized_handler.unique_table)
    summarized_handler.auto_save(dirname)


class TestLocalisation:
    @pytest.fixture(scope="class")
    def local_working_dir(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        np.random.seed(0)
        return tmp_path_factory.mktemp(self.__class__.__name__)

    def testTemporalDivision(self, local_working_dir: Path):
        local_working_dir.mkdir(parents=True, exist_ok=True)
        spatial_table = define_param()
        spatial_table.to_netcdf(local_working_dir / "spatial_table.nc")
        JsonFile(local_working_dir / "LocalisationInfo.json").dump(define_LocaInfo())

        dictIngredient = get_json_spatialIngredient(local_working_dir)
        JsonFile(local_working_dir / "SpatialIngredient.json").dump(dictIngredient)
        shutil.copyfile(
            TEST_DATA_DIR / "SpatialIngredient.nc",
            local_working_dir / "SpatialIngredient.nc",
        )
        shutil.copyfile(
            TEST_DATA_DIR / "SpatialIngredientlocalized.nc",
            local_working_dir / "SpatialIngredientlocalized.nc",
        )

        JsonFile(local_working_dir / "component.json").dump(
            recursive_format(
                JsonFile(TEST_DATA_DIR / "component_config.json").load(),
                values={"settings_dir": SETTINGS_DIR},
            )
        )
        spatial_ingredient = SpatialIngredient.load(
            local_working_dir / "SpatialIngredient"
        )
        tempo_handler = TemporalLocalisation(
            spatial_table["occurrence"].isel(risk_level=1),
            area_dimension="id",
            time_dimension="valid_time",
        )
        table_3p = tempo_handler.new_division()
        da = xr.DataArray(
            [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 1.0]],
            dims=("period", "id"),
            coords={
                "id": [
                    "CD38_domain_compass__Est",
                    "CD38_domain_compass__NordOuest",
                    "cde3bf79-4afd-43bb-88e7-7658c52f51b6",
                ],
                "period": [
                    "20201208T00_to_20201208T02",
                    "20201208T03_to_20201208T05",
                    "20201208T06_to_20201208T10",
                ],
                "risk_level": 3,
                "areaName": ("id", ["Est", "NordOuest", "SudOuest"]),
            },
        )
        xr.testing.assert_equal(table_3p, da)

        period = Period(
            spatial_table.valid_time.min().values, spatial_table.valid_time.max().values
        )
        summarized_handler = SummarizedTable(
            table_3p,
            spatial_ingredient=spatial_ingredient,
            request_time=Datetime(2020, 12, 8, 0).strftime("%Y%m%dT%H"),
            full_period=period,
        )
        da = xr.DataArray(
            [[0.0, 1.0, 1.0], [1.0, 1.0, 0.0]],
            dims=("id", "period"),
            coords={
                "id": [
                    "CD38_domain_compass__Est_+_cde3bf79-4afd-43bb-88e7-7658c52f51b6",
                    "CD38_domain_compass__NordOuest",
                ],
                "period": [
                    "20201208T00_to_20201208T02",
                    "20201208T03_to_20201208T05",
                    "20201208T06_to_20201208T10",
                ],
                "risk_level": 3,
                "areaName": ("id", ["Est_+_SudOuest", "NordOuest"]),
                "areaType": ("id", ["mergedArea", ""]),
            },
        )
        fname = local_working_dir / "tmp.nc"
        da.to_netcdf(fname)
        db = xr.open_dataarray(fname)
        db = db.drop_vars(["areaName", "areaType"])
        unique_table = summarized_handler.get_unique_table().drop_vars(
            ["areaName", "areaType"]
        )
        xr.testing.assert_equal(db, unique_table)


class TestComponent:
    """TestComponent : class for testing that component is well performed well."""

    @pytest.fixture(scope="class")
    def local_working_dir(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        """
        pytest fixture for creating a new
        tmp working directory
        """
        np.random.seed(0)
        local_working_dir = tmp_path_factory.mktemp(self.__class__.__name__)
        define_data(dirname=local_working_dir)
        return local_working_dir

    def testA(self, local_working_dir: Path):
        loca_handler = Localisation.load(repo=local_working_dir)
        component = ComponentHandlerLocalisation(loca_handler)
        assert "P3_3_6" == component.get_template_key()
        da = xr.DataArray(
            [[0.0, 1.0, 1.0], [1.0, 1.0, 0.0]],
            dims=("id", "period"),
            coords={
                "id": [
                    "CD38_domain_compass__Est_+_cde3bf79-4afd-43bb-88e7-7658c52f51b6",
                    "CD38_domain_compass__NordOuest",
                ],
                "period": [
                    "20201208T00_to_20201208T02",
                    "20201208T03_to_20201208T05",
                    "20201208T06_to_20201208T10",
                ],
                "risk_level": 3,
                "areaName": ("id", ["Est_+_SudOuest", "NordOuest"]),
                "areaType": ("id", ["mergedArea", ""]),
            },
        )
        fname = local_working_dir / "tmp.nc"
        da.to_netcdf(fname)
        db = xr.open_dataarray(fname)
        db = db.drop_vars(["areaName", "areaType"])
        unique_table = component.get_unique_table().drop_vars(["areaName", "areaType"])
        xr.testing.assert_equal(db, unique_table)

        # On va aussi tester les valeurs critiques
        critical_values = component.get_critical_value()
        assert critical_values == {
            "var_0": {
                "mountain_altitude": 1000,
                "plain": {
                    "critical_hour": np.datetime64("2020-12-08T05:00:00.000000000"),
                    "id": "CD38_domain_compass__Est",
                    "next_critical": None,
                    "operator": "sup",
                    "units": None,
                    "value": 5.95077539523179,
                    "threshold": 3,
                },
            }
        }
