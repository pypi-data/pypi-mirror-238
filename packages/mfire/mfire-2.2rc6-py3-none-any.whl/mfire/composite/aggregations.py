"""
    Module d'interprétation de la configuration des geos
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from mfire.composite.geos import GeoComposite
from mfire.data.aggregator import AggregationMethod


class AggregationType(str, Enum):
    """Création d'une classe d'énumération contenant les differents
    types d'aggregation
    """

    UP_STREAM = "upStream"
    DOWN_STREAM = "downStream"


class AggregationKwargs(BaseModel):
    """Création d'un objet Kwards contenant la configuration des méthodes d'aggrégation

    Args:
        BaseModel : Kwargs
    """

    dr: float
    # deprecated
    central_weight: Optional[int]
    # deprecated
    outer_weight: Optional[int]
    central_mask_id: Optional[GeoComposite]


class Aggregation(BaseModel):
    """Création d'un objet Agrégation contenant la configuration des méthodes d'agrégations
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Aggregation
    """

    kwargs: Optional[AggregationKwargs]
    method: AggregationMethod

    @validator("method")
    def check_method_kwargs(cls, method, values):
        if method == AggregationMethod.MEAN:
            if values["kwargs"] is not None:
                raise ValueError("erreur aggregation kwargs 2")
        else:
            dic_kwargs = values["kwargs"].dict()

            missing_keys = {
                AggregationMethod.RDENSITY: [],
                AggregationMethod.RDENSITY_CONDITIONAL: [
                    "central_mask_id",
                ],
                AggregationMethod.RDENSITY_WEIGHTED: [
                    "central_mask_id",
                    "central_weight",
                    "outer_weight",
                ],
            }
            unexpected_keys = {
                AggregationMethod.RDENSITY: [
                    "central_weight",
                    "outer_weight",
                    "central_mask_id",
                ],
                AggregationMethod.RDENSITY_CONDITIONAL: [
                    "central_weight",
                    "outer_weight",
                ],
                AggregationMethod.RDENSITY_WEIGHTED: [],
            }

            missing = [key for key in missing_keys[method] if dic_kwargs[key] is None]
            if missing:
                raise ValueError(f"Missing expected values {missing}")

            unexpected = [
                key for key in unexpected_keys[method] if dic_kwargs[key] is not None
            ]
            if unexpected:
                raise ValueError(f"Unexpected values {unexpected}")

        return method
