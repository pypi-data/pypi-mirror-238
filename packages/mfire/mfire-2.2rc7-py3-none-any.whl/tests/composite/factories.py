import random
from pathlib import Path
from typing import List, Optional, Union, cast, Dict

import mfire.utils.mfxarray as xr
from mfire import Datetime
from mfire.composite import (
    Aggregation,
    AltitudeComposite,
    BaseComposite,
    ComparisonOperator,
    EventBertrandComposite,
    FieldComposite,
    GeoComposite,
    RiskComponentComposite,
    LevelComposite,
    Period,
    AggregationType,
    LocalisationConfig,
    WeatherComposite,
)
from mfire.composite.components import TypeComponent, TextComponentComposite
from mfire.composite.events import Category, EventComposite, Threshold
from mfire.composite.fields import Selection
from mfire.data.aggregator import AggregationMethod
from mfire.settings import SETTINGS_DIR


class PeriodFactory(Period):

    id = "period_id"
    name = "period_name"
    start = Datetime(2023, 3, 1)
    stop = Datetime(2023, 3, 5)


class SelectionFactory(Selection):
    sel = {"id": random.randint(0, 42)}
    islice = {"valid_time": slice(random.randint(0, 42), random.randint(0, 42))}
    isel = {"latitude": random.randint(0, 42)}
    slice = {"longitude": slice(random.randint(0, 42), random.randint(0, 42))}


class BaseCompositeFactory(BaseComposite):
    """Base composite factory class."""

    def __init__(
        self, data: Optional[Union[xr.DataArray, xr.Dataset]] = None, **kwargs
    ):
        """Initialize the base composite factory.

        Args:
            data: Result value.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self._data = data

    def compute(self, keep_data: bool = False, **kwargs) -> xr.DataArray:
        return super().compute(keep_data=True, **kwargs)


class TextComponentCompositeFactory(TextComponentComposite):

    id = "id"
    name = "name"
    production_id = "production_id"
    production_name = "production_name"
    production_datetime = Datetime("20230301T06")
    period = PeriodFactory()

    product_comment = False
    weathers: List[WeatherComposite] = []


class FieldCompositeFactory(BaseCompositeFactory, FieldComposite):
    """Field composite factory class."""

    file: Path = Path("field_composite_path")
    grid_name: str = "franxl1s100"
    name: str = "field_name"


class GeoCompositeFactory(GeoComposite, BaseCompositeFactory):
    """Geo composite factory class."""

    file: Path = Path("geo_composite_file")
    mask_id: Union[List[str], str] = "mask_id"
    grid_name: Optional[str] = "franxl1s100"


class AltitudeCompositeFactory(AltitudeComposite, BaseCompositeFactory):
    """Altitude composite factory class."""

    filename = Path(SETTINGS_DIR / "geos/altitudes/franxl1s100.nc")
    grid_name = "franxl1s100"
    name = "name"


class EventCompositeFactory(EventComposite):
    """Factory class for creating EventComposite objects."""

    field: FieldComposite = FieldCompositeFactory(None)
    category: Category = Category.BOOLEAN
    altitude: AltitudeComposite = AltitudeCompositeFactory()
    geos: Union[GeoComposite, xr.DataArray] = GeoCompositeFactory()
    time_dimension: Optional[str] = "valid_time"
    plain: Threshold = Threshold(
        threshold=20, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
    )
    aggregation: Optional[Aggregation] = Aggregation(
        method=AggregationMethod.MEAN, kwargs=None
    )
    aggregation_aval: Optional[Aggregation] = None


class EventBertrandCompositeFactory(EventCompositeFactory, EventBertrandComposite):
    """Factory class for creating EventBertrandComposite objects."""

    field_1 = FieldCompositeFactory(None)
    cum_period = 6


class LevelCompositeFactory(LevelComposite, BaseCompositeFactory):

    level: int = 2
    aggregation: Optional[Aggregation] = None
    aggregation_type: AggregationType = AggregationType.UP_STREAM
    probability: str = "no"
    elements_event: List[Union[EventBertrandComposite, EventComposite]] = [
        EventCompositeFactory()
    ]
    time_dimension: Optional[str] = "valid_time"
    localisation: LocalisationConfig = LocalisationConfig()


class RiskComponentCompositeFactory(RiskComponentComposite, BaseCompositeFactory):

    period = PeriodFactory()
    id = "risk_id"
    type = TypeComponent.RISK
    name = "risk_name"
    production_id = "production_id"
    production_name = "production_name"
    production_datetime = Datetime(2023, 3, 1, 6)

    levels: List[LevelComposite] = []
    hazard = "hazard"
    hazard_name = "hazard_name"
    product_comment = True


class WeatherCompositeFactory(BaseCompositeFactory, WeatherComposite):

    id: str = "id_weather"
    params: Dict[str, FieldComposite] = {}
    units: Dict[str, Optional[str]] = {}
    localisation: LocalisationConfig = LocalisationConfig()
    _geos_descriptive: Optional[xr.DataArray] = None
    _altitudes: Optional[xr.DataArray] = None

    @property
    def geos_descriptive(self) -> xr.DataArray:
        """
        Returns the descriptive geos DataArray.

        Returns:
            xr.DataArray: The descriptive geos DataArray.
        """
        return (
            self._geos_descriptive
            if self._geos_descriptive is not None
            else super().geos_descriptive
        )

    def altitudes(self, param: str) -> Optional[xr.DataArray]:
        """
        Returns the altitudes DataArray for a given parameter.

        Args:
            param: The parameter name.

        Returns:
            Optional[xr.DataArray]: The altitudes DataArray or None if not found.
        """
        return self._altitudes

    @classmethod
    def create_factory(
        cls,
        geos_descriptive: list,
        valid_times: list,
        lon: list,
        lat: list,
        data_vars: dict,
        altitude: Optional[list],
        **kwargs,
    ) -> WeatherComposite:

        ids = list(map(str, list(range(len(geos_descriptive)))))
        data_ds = xr.Dataset(
            data_vars=xr.Dataset(data_vars),
            coords={
                "id": ids,
                "valid_time": valid_times,
                "latitude": lat,
                "longitude": lon,
                "areaType": (["id"], ["Axis"] + (len(ids) - 1) * [""]),
                "areaName": (
                    ["id"],
                    [f"localisation N°{i+1}" for i in range(len(ids))],
                ),
            },
        )

        compo = cls(data=data_ds, production_datetime=data_ds.valid_time[0], **kwargs)

        compo._geos_descriptive = xr.DataArray(
            data=geos_descriptive,
            dims=["id", "latitude", "longitude"],
            coords={
                "id": ids,
                "latitude": lat,
                "longitude": lon,
                "areaType": (["id"], ["Axis"] + (len(ids) - 1) * [""]),
                "areaName": (
                    ["id"],
                    [f"à localisation N°{i+1}" for i in range(len(ids))],
                ),
            },
        )
        compo.geos = compo._geos_descriptive.sum(dim=("id",)) > 0

        compo._altitudes = xr.DataArray(
            data=altitude,
            dims=["latitude", "longitude"],
            coords={
                "latitude": lat,
                "longitude": lon,
            },
        )

        return cast(WeatherComposite, compo)
