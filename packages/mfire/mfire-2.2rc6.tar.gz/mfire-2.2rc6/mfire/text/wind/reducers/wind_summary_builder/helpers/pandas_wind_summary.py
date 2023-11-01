from pathlib import Path
from tempfile import gettempdir
from typing import Any, Optional, Union
from uuid import uuid4

import numpy as np
import pandas as pd
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindType
from mfire.utils.date import Datetime

LOGGER = get_logger(name="pands_wind_summary.mod", bind="pands_wind_summary")


class PandasWindSummary:
    """PandasWindSummary class.

    Class used to keep the characteristics of each term.
    """

    COL_PREVIOUS_TIME: str = "previous_time"
    COL_WF_MAX: str = "wf_max"
    COL_WT: str = "wt"
    VALID_TIME_INDEX: str = "valid_time"

    def __init__(
        self,
        valid_time: Optional[Union[xr.DataArray, np.ndarray, list]] = None,
        file_path: Optional[Path] = None,
    ) -> None:
        self.data: pd.DataFrame
        self.pd_index: pd.Index
        self.ind_max: int

        if valid_time is not None:
            self.data = self.initialize_from_valid_time(valid_time)
        elif file_path is not None:
            self.data = self.initialize_from_file(file_path)
        else:
            raise ValueError("No input argument value was found!")

    def initialize_from_valid_time(self, valid_time: xr.DataArray) -> pd.DataFrame:
        """Create an empty DataFrame from a valid_time DataArray."""
        data = pd.DataFrame(
            index=pd.Series(valid_time),
            columns=[
                self.COL_PREVIOUS_TIME,
                self.COL_WT,
                self.COL_WF_MAX,
            ],
            copy=False,
        )
        data.index.name = self.VALID_TIME_INDEX
        return data

    @staticmethod
    def initialize_from_file(file_path: Path):
        """Read a pickle file."""
        data = pd.read_pickle(file_path)
        return data

    @property
    def index(self) -> pd.Index:
        return self.data.index

    @property
    def wind_types(self) -> tuple[WindType, ...]:
        """Get the wind types of all terms as a tuple."""
        return tuple(WindType(value) for value in self.data[self.COL_WT])

    @property
    def wind_types_set(self) -> set[WindType]:
        """Get the wind types of all terms as a set."""
        return set(self.wind_types)

    def create_column(self, col_name: str, init_value: Optional[Any] = None) -> None:
        """Create a column."""
        if col_name not in self.data:
            self.data[col_name] = init_value

    def find_type_3_wf_max(self, store: Optional[bool] = True) -> np.float64:
        """Find the maximum of the wf_max column."""
        data_frame: pd.DataFrame = self.data[self.data[self.COL_WT] == WindType.TYPE_3]
        if data_frame.empty:
            raise pd.errors.EmptyDataError("No wind type terms found !")

        type_3_wf_max: np.float64 = np.float64(np.max(data_frame[self.COL_WF_MAX]))

        # Set type_3_wf_max in Data Frame attributes
        if store:
            self.add_attr(self.COL_WF_MAX, type_3_wf_max)

        return type_3_wf_max

    def add_attr(self, attr_name: str, attr_value):
        """Add an attribute to the data."""
        self.data.attrs[attr_name] = attr_value

    def get_term_previous_time(
        self, valid_time: np.datetime64, convert: bool = True
    ) -> np.datetime64 | Datetime:
        """Get the previous_time of the term with the given valid_time"""
        previous_time: np.datetime64 = self.data.loc[valid_time, self.COL_PREVIOUS_TIME]
        if convert:
            return Datetime(previous_time)
        return previous_time

    def get_term_wind_type(self, valid_time: np.datetime64) -> WindType:
        return self.data.loc[valid_time, self.COL_WT]

    def to_pickle(self, file_path: Optional[Path] = None) -> Path:
        """Export he data to a pickle file."""
        if file_path is None:
            filename: str = f"pd_summary_{uuid4().hex}.pkl"
            file_path = Path(gettempdir(), filename)
        LOGGER.debug(f"--> pandas summary pkl file path: {file_path}")
        self.data.to_pickle(str(file_path))
        return file_path
