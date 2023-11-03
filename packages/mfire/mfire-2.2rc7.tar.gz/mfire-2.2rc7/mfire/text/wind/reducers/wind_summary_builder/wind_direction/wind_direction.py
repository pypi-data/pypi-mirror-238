from __future__ import annotations

from typing import Optional

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers import BaseWindPeriod
from mfire.utils.date import Datetime

from .sympo_code_direction import SympoCodeDirection

# Logging
LOGGER = get_logger(name="wind_direction.mod", bind="wind_direction")


class WindDirection:
    """WindDirection class."""

    SYMPO_INTERVAL_SIZE: float = 22.5

    def __init__(self, degrees: list[float]):
        self._lower_bound: float = 0
        self._upper_bound: float = 0
        self._size: float = 0
        self._sympo_code: int = 0
        self._initialize(degrees)

    def _initialize(self, degrees: list[float]):
        """Initialize WindDirection attributes from list of degrees."""
        self._lower_bound = min(degrees)
        self._upper_bound = max(degrees)

        if self._upper_bound - self._lower_bound <= 180:
            self._size = self._upper_bound - self._lower_bound
            self._sympo_code: int = self.to_sympo_code()
            return

        for i in range(len(degrees)):
            if (degrees[i] - self._lower_bound) > 180:
                degrees[i] = -(360 - degrees[i])

        self._lower_bound = min(degrees)
        self._upper_bound = max(degrees)
        self._size = (self._upper_bound - self._lower_bound) % 360

        self._sympo_code: int = self.to_sympo_code()

    @property
    def size(self):
        return self._size

    @property
    def lower_bound(self):
        return self._lower_bound

    @property
    def upper_bound(self):
        return self._upper_bound

    def check_size(self, size_max: float) -> bool:
        return self._size <= size_max

    @property
    def middle(self) -> float:
        return (self._upper_bound - self._size / 2) % 360

    @property
    def sympo_code(self) -> int:
        return self._sympo_code

    def to_sympo_code(self) -> int:
        """Get the sympo code of the WindDirection."""
        tmp = self.middle / self.SYMPO_INTERVAL_SIZE
        return int(round(tmp, 0)) % 16

    def is_opposite_to(self, other: WindDirection) -> bool:
        """Check if the WindDirection is the opposite of another WindDirection.

        For this check, the sympo code is used. For example, WindDirections with sympo
        code 0 and 8 are opposite but WindDirections with sympo code 0 and 7 are not.
        """
        return (self.sympo_code - other.sympo_code) % 8 == 0

    def __add__(self, other: WindDirection) -> WindDirection:
        """Add 2 WindDirection."""
        return WindDirection(
            [
                self.lower_bound,
                self.upper_bound,
                other.lower_bound,
                other.upper_bound,
            ]
        )

    def __hash__(self):
        return hash(self.sympo_code)

    def __eq__(self, other: Optional[WindDirection]):
        return isinstance(other, WindDirection) and self.sympo_code == other.sympo_code

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(interval=[{self._lower_bound}, "
            f"{self._upper_bound}], size={self._size})"
        )


class WindDirectionPeriod(BaseWindPeriod[WindDirection]):
    """WindDirectionPeriod class."""

    @property
    def sympo_code(self) -> int:
        return self._wind_element.sympo_code

    @property
    def direction(self) -> str:
        return SympoCodeDirection.get_direction_from_sympo_code(self.sympo_code)

    def update(
        self,
        other: WindDirectionPeriod,
        **kwargs,
    ) -> bool:
        """Try to update the current WindDirectionPeriod.

        If the size of the resulting WindDirection is <= size_max, then it returns
        True, else False.
        """
        if super().update(other, **kwargs) is False:
            return False

        # Get size_max key argument
        size_max: float = kwargs["size_max"]

        # Get WindDirection
        wind_direction: WindDirection = self.wind_element + other.wind_element

        if wind_direction.check_size(size_max):
            self._period.end_time = other.end_time
            self._wind_element = wind_direction
            return True
        return False

    def has_same_direction_than(self, other: WindDirectionPeriod) -> bool:
        """Check if 2 WindDirectionPeriod has the same direction."""
        return self.wind_element == other.wind_element

    def has_opposite_direction_to(self, other: WindDirectionPeriod) -> bool:
        """Check if 2 WindDirectionPeriod has opposite directions."""
        return self.wind_element.is_opposite_to(other.wind_element)

    def __repr__(self):
        s = (
            f"{self.__class__.__name__}(begin_time={self.begin_time}, "
            f"end_time={self.end_time}, duration={self.duration}, "
            f"wind_direction={self._wind_element}, sympo_code={self.sympo_code}, "
            f"direction='{self.direction}')"
        )
        return s

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the WindDirectionPeriod."""
        summary: dict = super().summarize(reference_datetime)
        summary[self.WD] = self.direction

        return summary


class VariableWindDirection:
    """VariableWindDirection class."""

    DIRECTION: str = "direction variable"

    @property
    def direction(self) -> str:
        return self.DIRECTION


class VariableWindDirectionPeriod(BaseWindPeriod[VariableWindDirection]):
    """VariableWindDirectionPeriod class."""

    def __init__(self, begin_time: Datetime, end_time: Datetime):
        super().__init__(begin_time, end_time, VariableWindDirection())

    def __add__(
        self, other: VariableWindDirectionPeriod
    ) -> VariableWindDirectionPeriod:
        """Add 2 VariableWindDirectionPeriod."""
        return self

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the VariableWindDirectionPeriod."""
        summary: dict = super().summarize(reference_datetime)
        summary[self.WD] = self.wind_element.direction

        return summary
