from __future__ import annotations

from typing import Optional

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindCase
from mfire.text.wind.selectors import WindSelector

LOGGER = get_logger(
    name="flagged_block1_summary_builder.mod", bind="flagged_block1_summary_builder"
)


class SummaryBuilderMixin:
    """SummaryBuilderMixin class."""

    SELECTOR_KEY: str = WindSelector.KEY

    def __init__(self):
        self._summary: dict = {}

    @property
    def case_value(self) -> Optional[str]:
        """Get the case value stored in the summary."""
        return self._summary.get(self.SELECTOR_KEY)

    def _set_summary_wind_case(self, case: WindCase) -> None:
        """Set the wind case in the summary"""
        self._summary[self.SELECTOR_KEY] = case.value

    @classmethod
    def __add_problem_case_in_summary(
        cls, case: WindCase, summary: dict, msg: str
    ) -> None:
        """Add a case regarding a problem in the summary.

        A message msg is also added.
        """
        summary.update(
            {
                cls.SELECTOR_KEY: case.value,
                "msg": msg,
            }
        )
        LOGGER.error(msg)

    @classmethod
    def _add_error_case_in_summary(cls, summary: dict, msg: str) -> None:
        """Add ERROR case nbr in summary."""
        cls.__add_problem_case_in_summary(WindCase.ERROR, summary, msg)

    @classmethod
    def _add_not_implemented_case_in_summary(cls, summary: dict, msg: str) -> None:
        """Add NOT_IMPLEMENTED case nbr in summary."""
        cls.__add_problem_case_in_summary(WindCase.NOT_IMPLEMENTED, summary, msg)
