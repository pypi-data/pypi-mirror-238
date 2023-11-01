import xarray as xr
from numpy import nan

from mfire.mask.altitude_mask import generate_mask_by_altitude


class TestModule:
    def test_generate_mask_by_altitude(self):
        valeurs = [[9999, 100, 220], [450, 550, 650], [1750, 3130, 4000]]
        altitude = xr.DataArray(
            data=valeurs,
            coords={"latitude": [44, 45, 46], "longitude": [0, 1, 2]},
            dims=["latitude", "longitude"],
            name="grille",
        )
        area_id = "id1"
        # empty domain
        valeurs = [[[nan, nan, nan], [nan, nan, nan], [nan, nan, nan]]]
        domain = xr.DataArray(
            data=valeurs,
            coords={
                "latitude_grille": [44, 45, 46],
                "longitude_grille": [0, 1, 2],
                "id": ["id1"],
            },
            dims=["id", "latitude_grille", "longitude_grille"],
            name="grille",
        )
        result = generate_mask_by_altitude(domain, altitude, area_id)
        assert result is None
        # domain within altitude
        valeurs = [[[nan, 1, 1], [1, 1, 1], [1, 1, 1]]]
        domain = xr.DataArray(
            data=valeurs,
            coords={
                "latitude_grille": [44, 45, 46],
                "longitude_grille": [0, 1, 2],
                "id": ["id1"],
            },
            dims=["id", "latitude_grille", "longitude_grille"],
            name="grille",
        )
        result = generate_mask_by_altitude(domain, altitude, area_id)
        # print("to_dict\n",result.to_dict())
        ref_dict = {
            "coords": {
                "id": {
                    "dims": ("id",),
                    "attrs": {},
                    "data": [
                        "id1_inf_200",
                        "id1_inf_300",
                        "id1_inf_400",
                        "id1_inf_500",
                        "id1_sup_1000",
                        "id1_sup_1200",
                        "id1_sup_1400",
                        "id1_sup_1600",
                        "id1_sup_1800",
                        "id1_sup_2000",
                        "id1_sup_2300",
                        "id1_sup_2600",
                        "id1_sup_2900",
                        "id1_sup_300",
                        "id1_sup_3200",
                        "id1_sup_3500",
                        "id1_sup_400",
                        "id1_sup_500",
                        "id1_sup_600",
                        "id1_sup_700",
                        "id1_sup_800",
                        "id1_sup_900",
                    ],
                },
                "latitude_grille": {
                    "dims": ("latitude_grille",),
                    "attrs": {},
                    "data": [44, 45, 46],
                },
                "longitude_grille": {
                    "dims": ("longitude_grille",),
                    "attrs": {},
                    "data": [0, 1, 2],
                },
            },
            "attrs": {},
            "dims": {"id": 22, "latitude_grille": 3, "longitude_grille": 3},
            "data_vars": {
                "areaName": {
                    "dims": ("id",),
                    "attrs": {},
                    "data": [
                        "en dessous de 200 m",
                        "en dessous de 300 m",
                        "en dessous de 400 m",
                        "en dessous de 500 m",
                        "au-dessus de 1000 m",
                        "au-dessus de 1200 m",
                        "au-dessus de 1400 m",
                        "au-dessus de 1600 m",
                        "au-dessus de 1800 m",
                        "au-dessus de 2000 m",
                        "au-dessus de 2300 m",
                        "au-dessus de 2600 m",
                        "au-dessus de 2900 m",
                        "au-dessus de 300 m",
                        "au-dessus de 3200 m",
                        "au-dessus de 3500 m",
                        "au-dessus de 400 m",
                        "au-dessus de 500 m",
                        "au-dessus de 600 m",
                        "au-dessus de 700 m",
                        "au-dessus de 800 m",
                        "au-dessus de 900 m",
                    ],
                },
                "areaType": {
                    "dims": ("id",),
                    "attrs": {},
                    "data": [
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                        "Altitude",
                    ],
                },
                "grille": {
                    "dims": ("id", "latitude_grille", "longitude_grille"),
                    "attrs": {},
                    "data": [
                        [[nan, 1.0, nan], [nan, nan, nan], [nan, nan, nan]],
                        [[nan, 1.0, 1.0], [nan, nan, nan], [nan, nan, nan]],
                        [[nan, 1.0, 1.0], [nan, nan, nan], [nan, nan, nan]],
                        [[nan, 1.0, 1.0], [1.0, nan, nan], [nan, nan, nan]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, 1.0, 1.0]],
                        [[nan, nan, nan], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, nan, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [nan, nan, 1.0]],
                        [[nan, nan, nan], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, 1.0, 1.0], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, 1.0], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                        [[nan, nan, nan], [nan, nan, nan], [1.0, 1.0, 1.0]],
                    ],
                },
            },
        }
        ref_ds = xr.Dataset.from_dict(ref_dict)
        xr.testing.assert_equal(result, ref_ds)
