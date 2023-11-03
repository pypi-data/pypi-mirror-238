import numpy as np
import xarray as xr

from mfire.composite import WeatherComposite
from mfire.settings import get_logger
from mfire.text.wind.builders import GustParamsBuilder
from mfire.text.wind.reducers.base_param_force import BaseParamForce
from mfire.text.wind.reducers.base_param_summary_builder import BaseParamSummaryBuilder

from .gust_enum import GustCase

# Logging
LOGGER = get_logger(name="gust_summary_builder.mod", bind="gust_summary_builder")


class GustForce(BaseParamForce):
    """GustForce class."""

    DEFAULT_PRECISION: int = 10
    PERCENTILE_NUM: int = 95

    @classmethod
    def data_array_to_value(cls, data_array: xr.DataArray) -> float:
        """Find the value which represents the input DataArray."""
        return float(np.nanpercentile(data_array.values, cls.PERCENTILE_NUM))


class GustSummaryBuilder(BaseParamSummaryBuilder):

    FORCE_MIN: int = 50
    GUST: str = "gust"

    def __init__(self, compo: WeatherComposite, data_array: xr.DataArray):
        self.units: str = self._get_composite_units(compo, self.GUST)
        self.data: xr.DataArray = self._get_data_array(
            data_array, self.GUST, self.units
        )

    def compute(self, **kwargs) -> dict:
        """Compute the gust summary."""
        summary: dict = {self.GUST: {}}
        case: GustCase

        data_array: xr.DataArray = self.data.where(self.data > self.FORCE_MIN)

        # If all gust are nan or <= FORCE_MIN, then case is case 1
        if np.isnan(data_array).all():
            case = GustCase.CASE_1
        # Else, we get the gust force interval
        else:
            gust_force: GustForce = GustForce.from_term_data_array(data_array)

            summary[self.GUST].update(
                {
                    "units": self.units,
                    "gust_interval": gust_force.interval,
                }
            )
            case = GustCase.CASE_2

        # Set case nbr
        summary[self.GUST][GustParamsBuilder.SELECTOR_KEY] = case.value

        return summary
