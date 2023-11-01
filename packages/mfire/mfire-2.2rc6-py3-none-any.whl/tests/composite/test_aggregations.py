from pathlib import Path

import pytest

from mfire.composite import Aggregation, GeoComposite
from mfire.composite.aggregations import AggregationKwargs
from mfire.data.aggregator import AggregationMethod


class TestAggregation:
    def test_aggregation_mean(self):
        # Without kwargs
        agg = Aggregation(method=AggregationMethod.MEAN, kwargs=None)
        assert isinstance(agg, Aggregation)
        assert agg.method == AggregationMethod.MEAN

        # With kwargs
        with pytest.raises(ValueError, match="erreur aggregation kwargs 2"):
            Aggregation(method=AggregationMethod.MEAN, kwargs=AggregationKwargs(dr=0.5))

    def test_missing_key(self):
        with pytest.raises(ValueError) as err:
            Aggregation(
                method=AggregationMethod.RDENSITY_CONDITIONAL,
                kwargs=AggregationKwargs(dr=0.5),
            )
        assert "Missing expected values ['central_mask_id']" in str(err.value)

        with pytest.raises(ValueError) as err:
            Aggregation(
                method=AggregationMethod.RDENSITY_WEIGHTED,
                kwargs=AggregationKwargs(dr=0.5),
            )
        assert (
            "Missing expected values ['central_mask_id', 'central_weight',"
            " 'outer_weight']" in str(err.value)
        )

    def test_unexpected_key(self):
        with pytest.raises(ValueError) as err:
            Aggregation(
                method=AggregationMethod.RDENSITY,
                kwargs=AggregationKwargs(
                    dr=0.5, central_mask_id=GeoComposite(file=Path())
                ),
            )
        assert "Unexpected values ['central_mask_id']" in str(err.value)

        with pytest.raises(ValueError) as err:
            Aggregation(
                method=AggregationMethod.RDENSITY_CONDITIONAL,
                kwargs=AggregationKwargs(
                    dr=0.5,
                    central_mask_id=GeoComposite(file=Path()),
                    central_weight=1,
                    outer_weight=1,
                ),
            )
        assert "Unexpected values ['central_weight', 'outer_weight']" in str(err.value)
