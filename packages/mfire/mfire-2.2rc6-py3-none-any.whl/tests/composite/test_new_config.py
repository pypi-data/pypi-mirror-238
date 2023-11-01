from pathlib import Path

from mfire.composite import (
    Aggregation,
    AggregationMethod,
    AggregationType,
    EventComposite,
    FieldComposite,
    GeoComposite,
    LevelComposite,
    LocalisationConfig,
    Period,
    ProductionComposite,
    RiskComponentComposite,
)
from mfire.settings.constants import SETTINGS_DIR
from mfire.utils import JsonFile, recursive_format
from mfire.utils.date import Datetime

# ==============================
# Testing Configuration
# ==============================

path = Path(
    "./data/20210916T0000/promethee/FRANXL1S100/R_SN_DRIFT__SOL.0016_0048_0001.netcdf"
)

TEST_DATA_DIR = Path(__file__).absolute().parent.parent / "test_data"

DEFAULT_VALUES = {"settings_dir": SETTINGS_DIR}


def test_production():
    """
    teste la validité d'un objet Production à partir d'un fichier json
    """
    file_path = TEST_DATA_DIR / "conf_test_example.json"

    data = JsonFile(file_path).load()
    for _, data_prod in data.items():
        prod = ProductionComposite(**recursive_format(data_prod, values=DEFAULT_VALUES))

    assert prod.id == "afe389a0-145c-4836-8643-e2ad28b66dfc"
    assert prod.name == "Promethee_CD01"
    assert prod.config_hash == "867a84e5"
    assert prod.prod_hash == "e4dd70f8"
    assert prod.mask_hash == "3b00fd12"
    assert len(prod.components) == 1


def test_component():
    """
    teste la validité d'un objet composant à partir d'un fichier json
    """
    file_path = TEST_DATA_DIR / "conf_test_example.json"

    data = JsonFile(file_path).load()
    for data_prod in data.values():
        for component in data_prod["components"]:
            compo = RiskComponentComposite(
                **recursive_format(component, values=DEFAULT_VALUES)
            )

    for level in compo.levels:
        assert level.time_dimension == "valid_time"
        assert level.localisation.compass_split
        assert level.localisation.altitude_split
        assert len(level.localisation.geos_descriptive) == 9
        for elmt in level.elements_event:
            assert elmt.time_dimension == "valid_time"
            assert elmt.geos.file == Path(
                "./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc"
            )
            assert elmt.geos.mask_id == ["da21482f-f56e-4088-b5e9-3200ff5cfa9a"]
            assert elmt.altitude.alt_min == -100
            assert elmt.altitude.alt_max == 1600

    assert str(compo.hazard) == "5e1a5e93-4c64-4f1d-957a-bcf8fdbf93cc"
    assert compo.name == "MSB CD01"
    assert compo.type == "risk"
    assert len(compo.levels) == 3


def test_period():
    """teste la validité d'un objet période
    doit être composée de 4 attributs
    """
    period = Period(
        id="751410a0-a404-45de-8548-1944af4c6e60",
        name="My period",
        start="20210922T000000",
        stop="20210922T160000",
    )
    assert period.name == "My period"
    assert period.id == "751410a0-a404-45de-8548-1944af4c6e60"
    assert period.start == Datetime("20210922T000000")
    assert period.stop == Datetime("20210922T160000")


def test_geo():
    """teste la validité d'un objet géo"""
    geo = GeoComposite(
        file="./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc",
        mask_id=["da21482f-f56e-4088-b5e9-3200ff5cfa9a"],
    )
    assert geo.file == Path("./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc")
    assert geo.mask_id == ["da21482f-f56e-4088-b5e9-3200ff5cfa9a"]


def test_aggregation():
    """teste la validité d'un objet Aggregation
    avec les différentes méthodes
    """
    aggregation = Aggregation(method="requiredDensity", kwargs={"dr": 0.05})
    assert aggregation.method == AggregationMethod.RDENSITY
    assert aggregation.kwargs.dr == 0.05
    assert aggregation.kwargs.central_weight is None
    assert aggregation.kwargs.outer_weight is None
    assert aggregation.kwargs.central_mask_id is None

    aggregation = Aggregation(
        method="requiredDensityWeighted",
        kwargs={
            "central_weight": 7,
            "outer_weight": "2",
            "central_mask_id": GeoComposite(
                file="./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc",
                mask_id="da21482f-f56e-4088-b5e9-3200ff5cfa9a",
            ),
            "dr": 0.35,
        },
    )
    assert aggregation.method == AggregationMethod.RDENSITY_WEIGHTED
    assert aggregation.kwargs.central_weight == 7
    assert aggregation.kwargs.outer_weight == 2
    assert aggregation.kwargs.central_mask_id.file == Path(
        "./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc"
    )
    assert aggregation.kwargs.central_mask_id.mask_id == (
        "da21482f-f56e-4088-b5e9-3200ff5cfa9a"
    )
    assert aggregation.kwargs.dr == 0.35

    aggregation = Aggregation(
        method="requiredDensityConditional",
        kwargs={
            "central_mask_id": GeoComposite(
                file="./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc",
                mask_id="da21482f-f56e-4088-b5e9-3200ff5cfa9a",
            ),
            "dr": 0.35,
        },
    )
    assert aggregation.method == AggregationMethod.RDENSITY_CONDITIONAL
    assert aggregation.kwargs.central_weight is None
    assert aggregation.kwargs.outer_weight is None
    assert aggregation.kwargs.central_mask_id.file == Path(
        "./mask/afe389a0-145c-4836-8643-e2ad28b66dfc.nc"
    )
    assert aggregation.kwargs.central_mask_id.mask_id == (
        "da21482f-f56e-4088-b5e9-3200ff5cfa9a"
    )
    assert aggregation.kwargs.dr == 0.35


def test_element_level():
    """teste la validité d'un objet Element et d'un level
    avec les types d'aggregation amont et aval
    """

    sel = {"slice": {"valid_time": ["20210916T170000", "20210917T150000"]}}
    field = FieldComposite(file=path, selection=sel, grid_name="grid_name", name="name")
    plain = {"threshold": [33, 38, 39, 32], "comparison_op": "isin", "units": "wwmf"}
    element = EventComposite(
        category="categorical",
        field=field,
        plain=plain,
        altitude={"filename": SETTINGS_DIR / "geos/altitudes/franxl1s100.nc"},
        geos={"file": "toto.nc"},
    )

    assert element.field.selection.slice == {
        "valid_time": slice(
            Datetime("20210916T170000").as_np_datetime64(),
            Datetime("20210917T150000").as_np_datetime64(),
        )
    }
    assert element.field.file == path
    assert element.plain.threshold == [33, 38, 39, 32]
    assert element.plain.comparison_op == "isin"
    assert element.plain.units == "wwmf"
    assert element.category == "categorical"

    aggregation = Aggregation(method="requiredDensity", kwargs={"dr": 0.05})
    localisation = LocalisationConfig(compass_split=True, altitude_split=True)

    level_down = LevelComposite(
        level=1,
        probability="no",
        logical_op_list=[],
        aggregation_type="downStream",
        aggregation=aggregation,
        elements_event=[element],
        localisation=localisation,
    )

    assert level_down.level == 1
    assert level_down.probability == "no"
    assert level_down.aggregation_type == AggregationType.DOWN_STREAM
    assert level_down.elements_event[0].aggregation is None

    plain2 = {
        "threshold": [40, 41, 42, 43, 44, 45],
        "comparison_op": "isin",
        "units": "wwmf",
    }

    element2 = EventComposite(
        category="categorical",
        field=field,
        plain=plain2,
        aggregation=aggregation,
        altitude={"filename": SETTINGS_DIR / "geos/altitudes/franxl1s100.nc"},
        geos={"file": "toto.nc"},
    )

    element.aggregation = aggregation

    level_up = LevelComposite(
        level=1,
        probability="no",
        logical_op_list=["or"],
        aggregation_type="upStream",
        elements_event=[element, element2],
        localisation=localisation,
    )
    assert level_up.aggregation_type == AggregationType.UP_STREAM
    assert len(level_up.elements_event) == 2
    assert level_up.elements_event[0].aggregation.method == "requiredDensity"
    assert level_up.elements_event[1].aggregation.method == "requiredDensity"
    assert level_up.aggregation is None
