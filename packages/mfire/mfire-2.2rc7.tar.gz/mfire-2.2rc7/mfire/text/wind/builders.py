from __future__ import annotations

from typing import Optional

from mfire.settings import get_logger
from mfire.settings.text.synthesis.wind import TEMPLATES_DICT as WIND_TEMPLATES_DICT
from mfire.text.wind.base import BaseMultiParamsBuilder, BaseParamBuilder
from mfire.text.wind.selectors import GustSelector, WindSelector

# Logging
LOGGER = get_logger(name="wind_builder.mod", bind="wind_builder")


class WindParamsBuilder(BaseParamBuilder):
    """WindParamsBuilder class."""

    DEFAULT_OUTPUT = "Vent faible"
    PARAM_NAME = "wind"
    SELECTOR_KEY = WindSelector.KEY
    TEMPLATES_DICT = WIND_TEMPLATES_DICT


class GustParamsBuilder(BaseParamBuilder):
    """GustParamsBuilder class."""

    DEFAULT_OUTPUT = WindParamsBuilder.DEFAULT_OUTPUT
    PARAM_NAME = "gust"
    SELECTOR_KEY = GustSelector.KEY
    TEMPLATES_DICT = WIND_TEMPLATES_DICT


class WindBuilder(BaseMultiParamsBuilder):
    """WindBuilder class."""

    PARAM_BUILDER_CLASSES = [WindParamsBuilder, GustParamsBuilder]

    def compute(
        self, summary: dict, with_extra: bool = False
    ) -> tuple[Optional[str], Optional[str]]:
        """Compute the synthesis text from a dict summary."""
        text, extra_content = super().compute(summary, with_extra)

        if text is None:
            text = self.DEFAULT_OUTPUT

        return text, extra_content
