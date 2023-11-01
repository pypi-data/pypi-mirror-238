from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from jinja2 import Template

from mfire.settings import get_logger
from mfire.settings.text.synthesis.const import DEFAULT_TEMPLATE
from mfire.text.wind.base.reducers import BaseReducer
from mfire.text.wind.base.selectors import BaseSelector
from mfire.utils.jinja_template import JinjaTemplateCreator

# Logging
LOGGER = get_logger(name="base_builder.mod", bind="base_builder")


def add_extra_content_to_summary(summary: dict, extra_content: Any):
    """Add an extra content in a dict summary."""
    summary[BaseParamBuilder.EXTRA_KEY] = extra_content


class BaseBuilder(ABC):
    """BaseBuilder class."""

    @abstractmethod
    def compute(
        self, summary: dict, with_extra: bool = False
    ) -> tuple[str, Optional[str]]:
        pass


class BaseParamBuilder(BaseBuilder):
    """BaseParamBuilder class.

    This class allows to build a synthesis text from a dict summary for a particular
    parameter (for example the temperature, the wind or the gust).
    """

    PARAM_NAME: str
    EXTRA_KEY: str = "extra"
    DEFAULT_OUTPUT: str = "RAS"  # Nothing to report
    DEFAULT_TEMPLATE_KEY: str = DEFAULT_TEMPLATE
    SELECTOR_KEY: str = BaseSelector.KEY
    TEMPLATES_DICT: dict

    @classmethod
    def default_template(cls):
        """TODO: Find a good default template !!"""
        return cls.TEMPLATES_DICT[cls.DEFAULT_TEMPLATE_KEY]

    def _get_template_key_from_selector(self, summary: dict) -> Optional[str]:
        """Get the template key from the selector key."""
        try:
            return summary.get(self.SELECTOR_KEY)
        except KeyError:
            LOGGER.error(
                f"Selector '{self.SELECTOR_KEY}' not found for "
                f"param '{self.PARAM_NAME}' !"
            )
            return None

    def _get_template_str(self, template_key: Optional[str]) -> str:
        """Get the template string from the template key."""
        try:
            return self.TEMPLATES_DICT[template_key]
        except KeyError:
            LOGGER.error(
                f"Template '{template_key}' not found for param '{self.PARAM_NAME}' !"
            )
            return self.default_template()

    def _get_jinja_template(self, summary: dict) -> Template:
        """Get the jinja Template object from the summary by using the selector key."""
        template_key: Optional[str] = self._get_template_key_from_selector(summary)

        template_str: str
        if template_key is None:
            template_str = self.default_template()
        else:
            template_str: str = self._get_template_str(template_key)

        return JinjaTemplateCreator().run(template_str)

    def compute(
        self, summary: dict, with_extra: bool = False
    ) -> tuple[str, Optional[str]]:
        """Compute the synthesis text from a dict summary."""
        template: Template = self._get_jinja_template(summary)
        text: str = template.render(summary)

        # Get extra content in the text
        extra_content: Any = None
        if with_extra is True:
            if self.EXTRA_KEY not in summary.keys():
                LOGGER.warning(f"'{self.EXTRA_KEY}' EXTRA_KEY not found in summary")
            else:
                extra_content: Any = summary.get(self.EXTRA_KEY)
                if extra_content:
                    extra_content = f"[{self.PARAM_NAME}: {extra_content}]"

        return text if text else self.DEFAULT_OUTPUT, extra_content


class BaseMultiParamsBuilder(BaseBuilder):
    """BaseMultiParamsBuilder class.

    This class allows to build a synthesis text from a dict summary for many
    parameters (for example for wind and gust). The generated text is the concatenation
    of all the param synthesis. The concatenation order is related to the order in the
    PARAM_BUILDER_CLASSES attribute list.
    """

    DEFAULT_OUTPUT: Optional[str] = None  # Set during the initialization
    DEFAULT_TEMPLATE_KEY: Optional[str] = None  # Set during the initialization
    PARAMS_SUMMARY_PATH: str = BaseReducer.PARAM_SUMMARIES_KEY
    PARAM_BUILDER_CLASSES: list[BaseParamBuilder] = []

    def __init__(self) -> None:
        """Initialize a BaseMultiParamsBuilder instance."""
        self.use_default_template: bool = False
        self.extra_content_list: list = []
        self.texts_list: list = []

        if self._update_builder_classes_attrs() is False:
            self.use_default_template = True

    def _add_text(self, text: str) -> None:
        """Add a text int the texts_list attribute."""
        if not text or text == self.DEFAULT_OUTPUT:
            return
        self.texts_list.append(text)

    def _reset_texts_list(self) -> None:
        """Reset the texts_list attribute."""
        self.texts_list = []

    def _reset_extra_content_list(self) -> None:
        """Reset the extra_content_list attribute."""
        self.extra_content_list = []

    def _reset(self) -> None:
        """Reset the BaseMultiParamsBuilder instance."""
        self.use_default_template = False
        self._reset_texts_list()
        self._reset_extra_content_list()

    def _set_default_template(self) -> None:
        """Set the default template in the texts_list attribute."""
        self._reset_texts_list()
        self._add_text(self.PARAM_BUILDER_CLASSES[0].default_template())

    def _add_extra_content(self, extra_content: Optional[str]):
        """Add extra content in the extra_content_list attribute."""
        if extra_content is None:
            return
        self.extra_content_list.append(extra_content)

    def _get_param_summary(self, summary: dict, param_name: str) -> Optional[dict]:
        """Get the summary of a parameter from its name in a bigger dict summary."""
        try:
            return summary[self.PARAMS_SUMMARY_PATH][param_name]
        except KeyError:
            LOGGER.error(f"Param summary of '{param_name}' not found !")
            return None

    def _preprocessing(self, summary: dict):
        """Preprocess."""
        pass

    def _update_builder_classes_attrs(self) -> bool:
        """Get DEFAULT_OUTPUT and DEFAULT_TEMPLATE_KEY from PARAM_BUILDER_CLASSES."""
        for builder_class in self.PARAM_BUILDER_CLASSES:
            # Set DEFAULT_OUTPUT
            if not self.DEFAULT_OUTPUT:
                self.DEFAULT_OUTPUT = builder_class.DEFAULT_OUTPUT
            elif self.DEFAULT_OUTPUT != builder_class.DEFAULT_OUTPUT:
                LOGGER.error(
                    f"{builder_class.__class__.__name__}.DEFAULT_OUTPUT is variable: "
                    f"'{self.DEFAULT_OUTPUT}' != {builder_class.DEFAULT_OUTPUT}' !"
                )
                return False

            # Set DEFAULT_TEMPLATE_KEY
            if not self.DEFAULT_TEMPLATE_KEY:
                self.DEFAULT_TEMPLATE_KEY = builder_class.DEFAULT_TEMPLATE_KEY
            elif self.DEFAULT_TEMPLATE_KEY != builder_class.DEFAULT_TEMPLATE_KEY:
                LOGGER.error(
                    f"{builder_class.__class__.__name__}.DEFAULT_TEMPLATE_KEY is "
                    f"variable: '{self.DEFAULT_TEMPLATE_KEY}' != "
                    f"{builder_class.DEFAULT_TEMPLATE_KEY}' !"
                )
                return False
        return True

    def _build_synthesis_elements(self) -> tuple[str, Optional[str]]:
        """Build synthesis elements from texts_list and extra_content_list."""
        text: Optional[str] = (
            " ".join(self.texts_list) if self.texts_list else self.DEFAULT_OUTPUT
        )
        extra_content: str = (
            " ".join(self.extra_content_list) if self.extra_content_list else None
        )
        return text, extra_content

    def _build_default_synthesis_elements(self) -> tuple[str, Optional[str]]:
        """Build synthesis elements with default template and extra_content_list."""
        self._set_default_template()
        return self._build_synthesis_elements()

    def compute(
        self, summary: dict, with_extra: bool = False
    ) -> tuple[str, Optional[str]]:
        """Compute the synthesis elements from a dict summary."""
        # Reset
        self._reset()

        # Preprocess summary
        self._preprocessing(summary)

        if self.use_default_template is True:
            return self._build_default_synthesis_elements()

        # Build synthesis text from summary
        for builder_class in self.PARAM_BUILDER_CLASSES:

            # Get parameter summary
            param_summary: Optional[dict] = self._get_param_summary(
                summary, builder_class.PARAM_NAME
            )
            if param_summary is None:
                return self._build_default_synthesis_elements()

            builder = builder_class()
            text, extra_content = builder.compute(
                summary[self.PARAMS_SUMMARY_PATH][builder_class.PARAM_NAME], with_extra
            )

            # If text is the default template, then return default synthesis
            if text == builder.default_template():
                return self._build_default_synthesis_elements()

            self._add_text(text)
            self._add_extra_content(extra_content)

        return self._build_synthesis_elements()
