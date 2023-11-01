from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from mfire.composite import LocalisationConfig, WeatherComposite
from tests.composite.factories import GeoCompositeFactory, WeatherCompositeFactory
from tests.functions_test import assert_identically_close


class TestWeatherComposite:
    def test_wrong_field(self):
        with pytest.raises(
            ValueError,
            match="Wrong field: [], expected ['wwmf', 'precip', 'rain', 'snow', 'lpn']",
        ):
            WeatherComposite(
                id="weather", params={}, units={}, localisation=LocalisationConfig()
            )

    def test_check_condition(self):
        weather_compo = WeatherComposite(
            id="tempe",
            params={
                "tempe": {
                    "file": Path(""),
                    "selection": None,
                    "grid_name": "",
                    "name": "",
                }
            },
            units={},
            localisation=LocalisationConfig(),
        )
        assert weather_compo.check_condition is False

    def test_altitudes(self):
        weather_compo = WeatherComposite(
            id="tempe",
            params={
                "tempe": {
                    "file": Path(""),
                    "selection": None,
                    "grid_name": "franxl1s100",
                    "name": "",
                }
            },
            units={},
            localisation=LocalisationConfig(),
        )

        assert weather_compo.altitudes("weather") is None

        alt = weather_compo.altitudes("tempe")
        assert isinstance(alt, xr.DataArray)
        assert alt.name == "franxl1s100"

    @pytest.mark.parametrize("test_file_path", [{"extension": "nc"}], indirect=True)
    def test_geos_descriptive(self, test_file_path):
        lon, lat = [31], [40]
        ids = ["id_axis", "id_1", "id_2", "id_axis_altitude", "id_axis_compass"]
        ds = xr.Dataset(
            {
                "A": (
                    ["longitude", "latitude", "id"],
                    [[[True, True, False, True, False]]],
                ),
            },
            coords={
                "id": ids,
                "longitude": lon,
                "latitude": lat,
                "areaType": (
                    ["id"],
                    ["areaTypeAxis", "areaType1", "areaType2", "Altitude", "compass"],
                ),
            },
        )
        ds.to_netcdf(test_file_path)

        geos = GeoCompositeFactory(file=test_file_path, grid_name="A")
        weather_compo = WeatherCompositeFactory(geos=geos, geo_id="id_axis")
        weather_compo.localisation.geos_descriptive = ["id_1", "id_2"]
        weather_compo.localisation.compass_split = True
        weather_compo.localisation.altitude_split = True
        assert_identically_close(
            weather_compo.geos_descriptive,
            xr.DataArray(
                [[[1.0, np.nan, 1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2", "id_axis_altitude", "id_axis_compass"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaType": (
                        ["id"],
                        ["areaType1", "areaType2", "Altitude", "compass"],
                    ),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )

        weather_compo.localisation.compass_split = False
        weather_compo.localisation.altitude_split = False
        assert_identically_close(
            weather_compo.geos_descriptive,
            xr.DataArray(
                [[[1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaType": (["id"], ["areaType1", "areaType2"]),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )
