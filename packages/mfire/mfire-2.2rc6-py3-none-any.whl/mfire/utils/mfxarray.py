from __future__ import annotations

from typing import Union

import numpy as np
import xarray as xr
from pandas.core.dtypes.common import is_float_dtype, is_bool_dtype


@xr.register_dataarray_accessor("wheretype")
class TypeAccessor:
    """
    Ajout un attribut wheretype aux datarray
    et les méthodes suivantes
    qui permettent de convertir le résultat d'un where dans le type souhaité
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def bool(self, *args, **kwargs):
        return self._obj.where(*args, **kwargs).astype("bool", copy=False)

    def f32(self, *args, **kwargs):
        return self._obj.where(*args, **kwargs).astype("float32", copy=False)


@xr.register_dataarray_accessor("mask")
class MaskAccessor:
    """
    Custom accessor that adds a 'mask' attribute to DataArrays.
    """

    def __init__(self, xarray_obj: xr.DataArray):
        if not is_float_dtype(xarray_obj) and not is_bool_dtype(xarray_obj):
            raise ValueError(
                "Dtype for DataArray of MaskAccessor must be float or boolean"
            )
        self._obj = xarray_obj > 0

    @property
    def bool(self) -> xr.DataArray:
        """
        Returns the mask as a boolean DataArray.
        """
        return self._obj

    @property
    def bool_dropped(self) -> xr.DataArray:
        """
        Returns the mask as a boolean DataArray with dropped dimensions where the mask
        is False.
        """
        return self._obj.where(self._obj, drop=True)

    @property
    def f32(self) -> xr.DataArray:
        """
        Returns the mask as a float32 DataArray.
        """
        return self._obj.where(self._obj).astype("float32", copy=False)

    @property
    def f32_dropped(self):
        """
        Returns the mask as a float32 DataArray with dropped dimensions where the mask
        is False.
        """
        return self._obj.where(self._obj, drop=True).astype("float32", copy=False)

    def union(self, other: Union[xr.DataArray, MaskAccessor]) -> MaskAccessor:
        """
        Make union of two masks by filling in missing values with the other mask.

        Args:
            other (Union[xr.DataArray, MaskAccessor]): The other mask to make the union.

        Returns:
            The union of the two masks.
        """
        if isinstance(other, xr.DataArray):
            other = other.mask

        return MaskAccessor(np.logical_or(self._obj, other.bool))

    @staticmethod
    def make_union(*args: Union[xr.DataArray, MaskAccessor]):
        """
        Make union of several masks.

        Args:
            *args (Union[xr.DataArray, MaskAccessor]): Masks to make the union.

        Returns:
            The union of all masks.
        """
        if len(args) == 0:
            return []

        result = args[0]
        if isinstance(result, xr.DataArray):
            result = result.mask

        for arg in args[1:]:
            result = result.union(arg)
        return result


DataArray = xr.DataArray
Dataset = xr.Dataset
merge = xr.merge
"""
remplacé en utilisant l'équivalent numpy
fmax = xr.ufuncs.fmax
"""
align = xr.align
apply_ufunc = xr.apply_ufunc
concat = xr.concat
where = xr.where
"""
remplacé directement par xr.DataArray dans le code l'utilisant
xda = xr.core.dataarray.DataArray
"""
zeros_like = xr.zeros_like
ones_like = xr.ones_like
open_dataarray = xr.open_dataarray
open_dataset = xr.open_dataset
set_options = xr.set_options
