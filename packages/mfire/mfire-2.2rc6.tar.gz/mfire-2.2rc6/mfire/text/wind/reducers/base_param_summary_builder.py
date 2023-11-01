from abc import ABC, abstractmethod
from typing import Optional

import xarray as xr

from mfire.composite import WeatherComposite
from mfire.settings import TEXT_ALGO
from mfire.utils.unit_converter import convert_dataarray


class BaseParamSummaryBuilder(ABC):
    """BaseParamSummaryBuilder."""

    USED_DIMS: list = ["valid_time", "latitude", "longitude"]

    @abstractmethod
    def __init__(self, compo: WeatherComposite, data_arrays: dict):
        pass

    @staticmethod
    def _get_composite_units(compo: WeatherComposite, param_name: str) -> str:
        """Get the units of the param regarding the WeatherComposite."""
        return compo.units.get(
            param_name,
            TEXT_ALGO[compo.id][compo.algorithm]["params"][param_name]["default_units"],
        )

    def _count_data_points(self, data: xr.DataArray) -> int:
        """Count the number of points of a term grid data."""
        latitude_size: int = int(data[self.USED_DIMS[1]].size)
        longitude_size: int = int(data[self.USED_DIMS[2]].size)
        return latitude_size * longitude_size

    def _clean_data_dims(self, data: xr.DataArray) -> xr.DataArray:
        """Remove useless dimensions of a DataArray."""
        useless_dims = []
        for dim in data.dims:
            if dim not in self.USED_DIMS:
                useless_dims.append(dim)
        xarray_selector = {dim: data[dim][0] for dim in useless_dims}

        return data.sel(**xarray_selector)

    def _get_data_array(
        self,
        data_array: xr.DataArray,
        param_name: str,
        units: Optional[str] = None,
        nan_replace: Optional[float] = None,
    ) -> xr.DataArray:
        """Clean and convert the input data_array."""
        data_array: xr.DataArray = self._clean_data_dims(data_array[param_name])

        if units:
            data_array = convert_dataarray(data_array, units)

        if nan_replace is not None:
            data_array = data_array.fillna(nan_replace)

        return data_array

    @abstractmethod
    def compute(self, **kwargs) -> dict:
        """Compute the summary."""
        pass
