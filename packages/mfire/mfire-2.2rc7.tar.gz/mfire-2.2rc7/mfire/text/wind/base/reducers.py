from abc import ABC
from typing import Optional

import xarray as xr

from mfire.composite import BaseComposite
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="base_reducer.mod", bind="base_reducer")


class BaseReducer(ABC):
    """BaseReducer class.

    Its is used to compute a data summary as a dictionary.
    """

    PARAM_SUMMARIES_KEY = "params"
    META_KEY = "meta"

    def __init__(self) -> None:
        self.data: Optional[xr.DataArray] = None
        self.summary: dict = dict()

    def reset(self) -> None:
        """Reset data attribute."""
        self.data = None
        self.summary: dict = dict()

    def compute(self, compo: BaseComposite) -> dict:
        """Build a summary as a dictionary."""
        self.reset()
        self.data = compo.compute()

        return self.summary
