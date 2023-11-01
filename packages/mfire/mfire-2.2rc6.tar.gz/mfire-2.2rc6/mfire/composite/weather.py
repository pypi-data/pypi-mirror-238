"""
    Module d'interprétation de la configuration des geos
"""

from typing import Dict, Optional

from pydantic import validator

import mfire.utils.mfxarray as xr
from mfire import Settings
from mfire.composite.base import BaseComposite
from mfire.composite.events import EventComposite
from mfire.composite.fields import FieldComposite
from mfire.composite.geos import AltitudeComposite, GeoComposite
from mfire.composite.levels import LocalisationConfig
from mfire.settings import TEXT_ALGO, get_logger
from mfire.utils.date import Datetime
from mfire.utils.xr_utils import Loader, mask_set_up, ArrayLoader

# Logging
LOGGER = get_logger(name="weather.mod", bind="weather")


class WeatherComposite(BaseComposite):
    """Création d'un objet weather contenant la configuration des weathers
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Weather
    """

    id: str
    condition: Optional[EventComposite]
    params: Dict[str, FieldComposite]
    altitude: Optional[AltitudeComposite]
    geos: Optional[GeoComposite]
    geo_id: Optional[str]  # Id of the axis for with we compute the text
    localisation: LocalisationConfig
    production_datetime: Optional[Datetime] = Datetime()
    units: Dict[str, Optional[str]]
    algorithm: Optional[str] = "generic"
    _weathers_ds: xr.Dataset = xr.Dataset()
    _data: xr.Dataset = None

    @validator("params")
    def validate_params(cls, v, values):
        """validate param's keys"""

        params_expected = TEXT_ALGO[values["id"]][values.get("algo", "generic")][
            "params"
        ].keys()

        if v.keys() != params_expected:
            raise ValueError(
                f"Wrong field: {list(v.keys())}, expected {list(params_expected)}"
            )
        return v

    @validator("production_datetime", pre=True)
    def init_datetime(cls, v: Datetime) -> Datetime:
        return Datetime(v)

    @property
    def _cached_attrs(self) -> dict:
        return {"data": Loader}

    @property
    def check_condition(self) -> bool:
        if self.condition is None:
            return False
        event_da = self.condition.compute()

        return bool(event_da.any().values)

    def _compute(self) -> xr.Dataset:

        # 1. initialisation des fields
        fields_ds = xr.Dataset(
            {
                name: field.compute().reset_coords(drop=True)
                for name, field in self.params.items()
            }
        )

        # 2. ajout du champs altitude et création d'un masque altitude
        alt_mask_da = None
        if self.altitude is not None:
            fields_ds["altitude"] = mask_set_up(self.altitude.compute(), fields_ds)
            alt_mask_da = fields_ds["altitude"] >= self.altitude.alt_min

        # 3. création du masque geo
        geo_mask_da = None
        if self.geos is not None:
            geo_mask_da = mask_set_up(self.geos.compute(), fields_ds)
        if geo_mask_da is None:
            if alt_mask_da is None:
                output_ds = fields_ds
            else:
                output_ds = fields_ds * alt_mask_da
        elif alt_mask_da is None:
            output_ds = fields_ds * geo_mask_da
        else:
            output_ds = fields_ds * (geo_mask_da * alt_mask_da)

        # On check que les variables sont bien presentes.
        for coord in ("areaName", "areaType"):
            if coord not in output_ds.coords:
                output_ds.coords[coord] = ("id", ["unknown"] * output_ds.id.size)

        return output_ds

    @property
    def geos_descriptive(self) -> xr.DataArray:
        """
        Returns the descriptive geos DataArray.

        Returns:
            xr.DataArray: The descriptive geos DataArray.
        """
        geos = self.geos.mask_da
        allowed_area_types = []
        if self.localisation.altitude_split:
            allowed_area_types += ["Altitude"]
        if self.localisation.compass_split:
            allowed_area_types += ["compass"]
        ids = [
            id
            for id in geos.id.data
            if (
                (
                    id.startswith(f"{self.geo_id}_")
                    and geos.sel(id=id).areaType in allowed_area_types
                )
                or id in self.localisation.geos_descriptive
            )
        ]

        return geos.sel(id=ids)

    def altitudes(self, param: str) -> Optional[xr.DataArray]:
        try:
            grid_name = self.params[param].grid_name
            return ArrayLoader(
                filename=Settings().altitudes_dirname / f"{grid_name}.nc"
            ).load()
        except KeyError:
            return None
