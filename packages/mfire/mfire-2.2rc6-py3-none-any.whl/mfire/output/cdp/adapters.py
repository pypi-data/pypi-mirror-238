"""
This module manages everything concerning the adaptation
of the outputs for the cdp

"""
from abc import abstractmethod

from pydantic import Field

from mfire.composite.components import RiskComponentComposite, TextComponentComposite
from mfire.output.base import BaseOutputAdapter
from mfire.output.cdp.components import (
    CDPAlea,
    CDPComponents,
    CDPText,
)
from mfire.output.cdp.productions import CDPProduction
from mfire.utils.date import Datetime


class BaseCDPAdapter(BaseOutputAdapter):
    """This class returns the production type information
    to be provided for the cdp

    Args:
        BaseModel : BaseOutputAdapter

    Returns:
        BaseModel : CDPProduction
    """

    output_type: str = Field("CDP", const=True)

    @property
    @abstractmethod
    def adapted_components(self) -> CDPComponents:
        pass

    def compute(self) -> CDPProduction:
        return CDPProduction(
            ProductionId=self.component.production_id,
            ProductionName=self.component.production_name,
            CustomerId=self.component.customer,
            CustomerName=self.component.customer_name,
            DateBulletin=self.component.production_datetime,
            DateProduction=Datetime.utcnow(),
            DateConfiguration=self.component.configuration_datetime,
            Components=self.adapted_components,
        )


class CDPRiskAdapter(BaseCDPAdapter):
    """This class returns information related to risk components

    Args:
        baseModel : BaseCDPAdapter

    Returns:
        baseModel : objet CDPComponents
    """

    component: RiskComponentComposite

    @property
    def adapted_components(self) -> CDPComponents:
        return CDPComponents(
            Aleas=[
                CDPAlea.from_composite(
                    component=self.component,
                    geo_id=geo_id,
                    text=self.texts[geo_id],
                )
                for geo_id in self.texts
            ]
        )


class CDPTextAdapter(BaseCDPAdapter):
    component: TextComponentComposite

    @property
    def adapted_components(self) -> CDPComponents:
        return CDPComponents(
            Text=[
                CDPText.from_composite(
                    component=self.component,
                    geo_id=geo_id,
                    text=self.texts[geo_id],
                )
                for geo_id in self.texts
            ]
        )
