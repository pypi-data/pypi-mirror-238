"""
    Module d'interprétation de la configuration, objet fields
"""

from pathlib import Path
from typing import Any, Iterable, List, Optional

from pydantic import BaseModel, root_validator, validator

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseComposite
from mfire.settings import get_logger
from mfire.utils.date import Datetime
from mfire.utils.unit_converter import convert_dataarray
from mfire.utils.xr_utils import ArrayLoader, change_grid

# Logging
LOGGER = get_logger(name="composite.fields.mod", bind="composite.fields")


class Selection(BaseModel):
    """Création d'un objet Selection

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Selection
    """

    sel: Optional[dict] = dict()
    slice: Optional[dict] = dict()
    isel: Optional[dict] = dict()
    islice: Optional[dict] = dict()

    @root_validator(pre=True)
    def check_all_keys(cls, values: dict):
        _ = dict(
            **values.get("sel", dict()),
            **values.get("slice", dict()),
            **values.get("isel", dict()),
            **values.get("islice", dict()),
        )
        return values

    @validator("sel", "slice", pre=True)
    def check_valid_times(cls, value: dict):
        if isinstance(value.get("valid_time"), Iterable):
            value["valid_time"] = [
                Datetime(dt).as_np_datetime64() for dt in value["valid_time"]
            ]
        return value

    @validator("slice", "islice")
    def init_slices(cls, value: dict) -> dict:
        dico = dict()
        for key, val in value.items():
            if isinstance(val, Iterable):
                dico[key] = slice(*val)
            else:
                dico[key] = val
        return dico

    def select(self, da: xr.DataArray) -> xr.DataArray:
        return da.isel(**self.isel, **self.islice).sel(**self.sel, **self.slice)

    def get_all(self) -> dict:
        return dict(**self.sel, **self.slice, **self.isel, **self.islice)

    def update(
        self,
        sel: dict = dict(),
        slice: dict = dict(),
        isel: dict = dict(),
        islice: dict = dict(),
    ):
        """Method for updating the current selection dict with new ones

        Args:
            sel (dict, optional): Dictionary sel. Defaults to None.
            slice (dict, optional): Dictionary slice. Defaults to None.
            isel (dict, optional): Dictionary isel. Defaults to None.
            islice (dict, optional): Dictionary islice. Defaults to {}.
        """
        # creating new selection
        new_sel = Selection(sel=sel, slice=slice, isel=isel, islice=islice)
        # dropping updated keys in self
        for dico in (self.sel, self.slice, self.isel, self.islice):
            _ = [dico.pop(key, None) for key in set(new_sel.get_all())]
        # updating old self selection
        self.sel.update(new_sel.sel)
        self.slice.update(new_sel.slice)
        self.isel.update(new_sel.isel)
        self.islice.update(new_sel.islice)


class FieldComposite(BaseComposite):
    """Création d'un objet Field contenant la configuration des champs
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Field
    """

    file: Path | List[Path]
    selection: Optional[Selection] = None
    grid_name: str
    name: str

    @validator("selection", always=True)
    def check_selection(cls, v):
        if v is None:
            return Selection()
        return v

    def _compute(self) -> xr.DataArray:

        field_da = None

        # we can either have a single file (if all the data for the Period have the same
        # time step)
        # or a list of files (if the data have heterogeneous time steps).
        if isinstance(self.file, list):
            for file in self.file:
                new_field_da = ArrayLoader(filename=file).load()
                # we filter out the useless data (out of bound points and dates)
                # for each file instead of doing it after the concat to heavily reduce
                # memory use (on "big" axes, like EIC20, we divide it by 3)
                new_field_da = self.selection.select(new_field_da)
                if field_da is None:
                    field_da = new_field_da
                    if field_da.units == "w1":
                        field_da = convert_dataarray(field_da, "wwmf")
                else:
                    # first, we make sure all tha data are on the same grid
                    # then we remove the dates that are on both DataArrays
                    # (we keep the first because it's the one which
                    # has not been interplotated : the further in the future we are, the
                    # coarser the grid is)
                    new_field_da = change_grid(new_field_da, self.grid_name)
                    new_field_da = convert_dataarray(new_field_da, field_da.units)
                    field_da = xr.concat(
                        [field_da, new_field_da], dim="valid_time"
                    ).drop_duplicates(dim="valid_time", keep="first")
        else:
            field_da = ArrayLoader(filename=self.file).load()
            field_da = self.selection.select(field_da)
            if field_da.units == "w1":
                field_da = convert_dataarray(field_da, "wwmf")

        field_da.name = self.name

        return field_da

    def get_coord(self, coord_name: str) -> Any:
        if self._data is None:
            with xr.open_dataarray(self.file) as tmp_da:
                return tmp_da[coord_name].load()
        return self._data[coord_name]
