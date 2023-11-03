from pathlib import Path

from mfire.composite import (
    Aggregation,
    EventComposite,
    FieldComposite,
    ProductionComposite,
    TextComponentComposite,
    WeatherComposite,
)
from mfire.settings import ALT_MAX, ALT_MIN
from mfire.settings.constants import SETTINGS_DIR
from mfire.utils import JsonFile, recursive_format
from mfire.utils.date import Datetime

# ==============================
# Testing a Text Configuration
# ==============================

path = Path(
    "./data/20210916T0000/promethee/FRANXL1S100/R_SN_DRIFT__SOL.0016_0048_0001.netcdf"
)

TEST_DATA_DIR = TEST_DATA_DIR = Path(__file__).absolute().parent.parent / "test_data"
DEFAULT_VALUES = {"settings_dir": SETTINGS_DIR}


def test_production():
    """
    teste la validité d'un objet Production à partir d'un fichier json
    """
    file_path = TEST_DATA_DIR / "conf_text_config_example.json"

    data = JsonFile(file_path).load()
    for _, data_prod in data.items():
        prod = ProductionComposite(**recursive_format(data_prod, values=DEFAULT_VALUES))

    assert prod.id == "e1d59d7a-8bc3-4ad6-b7ff-a8c9db091ee3"
    assert prod.name == "Promethee_CD01-duplicate"
    assert prod.config_hash == "4d4b1473"
    assert prod.prod_hash == "f5093703"
    assert prod.mask_hash == "66e8bc38"
    assert len(prod.components) == 1


def test_component():
    """
    teste la validité d'un objet composant type texte à partir d'un fichier json
    """
    file_path = TEST_DATA_DIR / "conf_text_config_example.json"

    data = JsonFile(file_path).load()
    for data_prod in data.values():
        for component in data_prod["components"]:
            compo = TextComponentComposite(
                **recursive_format(component, values=DEFAULT_VALUES)
            )

    for weather in compo.weathers:
        assert weather.id == "tempe"
        assert weather.condition.plain.threshold == 0
        assert weather.condition.plain.comparison_op == "sup"
        assert weather.condition.plain.units == "celsius"
        assert weather.condition.category == "quantitative"
        assert weather.condition.aggregation.kwargs.dr == 0.05
        assert weather.condition.aggregation.method == "requiredDensity"
        assert "tempe" in weather.params

    assert compo.name == "CB_TEMPE"
    assert compo.type == "text"
    assert compo.time_dimension == "valid_time"


def test_weather_event():
    """teste la validité d'un objet Weather et d'un objet
    Condition avec les types d'aggregation amont et aval
    """

    sel = {"slice": {"valid_time": ["20210916T170000", "20210917T150000"]}}
    field = FieldComposite(file=path, selection=sel, grid_name="grid_name", name="name")
    plain = {"threshold": 0, "comparison_op": "inf", "units": "celsius"}
    aggregation = Aggregation(method="requiredDensity", kwargs={"dr": 10})

    condition = EventComposite(
        field=field,
        plain=plain,
        category="quantitative",
        aggregation=aggregation,
        altitude={"filename": SETTINGS_DIR / "geos/altitudes/franxl1s100.nc"},
        geos={"file": "toto.nc"},
    )

    assert condition.field.selection.slice == {
        "valid_time": slice(
            Datetime("20210916T170000").as_np_datetime64(),
            Datetime("20210917T150000").as_np_datetime64(),
        )
    }
    assert condition.field.file == path
    assert condition.plain.threshold == 0
    assert condition.plain.comparison_op == "inf"
    assert condition.plain.units == "celsius"
    assert condition.category == "quantitative"
    assert condition.aggregation.method == "requiredDensity"
    assert condition.aggregation.kwargs.dr == 10
    assert condition.altitude.alt_min == ALT_MIN
    assert condition.altitude.alt_max == ALT_MAX

    params = {"gust": field, "wind": field, "direction": field}

    localisation = {
        "compass_split": True,
        "altitude_split": True,
        "geos_descriptice": [],
    }

    units = {"wind": "km/h", "gust": "km/h", "direction": "°"}
    weather = WeatherComposite(
        id="wind",
        condition=condition,
        params=params,
        localisation=localisation,
        units=units,
        geos={"file": "toto.nc"},
    )

    assert weather.id == "wind"
    assert "wind" and "gust" in weather.params
    assert weather.geos == weather.condition.geos
