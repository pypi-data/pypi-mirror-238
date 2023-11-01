from geojson import Feature, FeatureCollection
from shapely.geometry import shape as SHAshape

from mfire.mask.north_south_mask import (
    MAX_AREA,
    MIN_AREA,
    CardinalMasks,
    get_cardinal_masks,
)

GEO = SHAshape(
    {"type": "Polygon", "coordinates": [[[1, 1], [1, 41], [81, 41], [81, 1], [1, 1]]]}
)
REF_FEAT = Feature(
    geometry=SHAshape(
        {
            "coordinates": [
                [
                    [0.99, 41.0],
                    [0.990048, 41.00098],
                    [0.990192, 41.001951],
                    [0.990431, 41.002903],
                    [0.990761, 41.003827],
                    [0.991181, 41.004714],
                    [0.991685, 41.005556],
                    [0.99227, 41.006344],
                    [0.992929, 41.007071],
                    [0.993656, 41.00773],
                    [0.994444, 41.008315],
                    [0.995286, 41.008819],
                    [0.996173, 41.009239],
                    [0.997097, 41.009569],
                    [0.998049, 41.009808],
                    [0.99902, 41.009952],
                    [1.0, 41.01],
                    [81.0, 41.01],
                    [81.00098, 41.009952],
                    [81.001951, 41.009808],
                    [81.002903, 41.009569],
                    [81.003827, 41.009239],
                    [81.004714, 41.008819],
                    [81.005556, 41.008315],
                    [81.006344, 41.00773],
                    [81.007071, 41.007071],
                    [81.00773, 41.006344],
                    [81.008315, 41.005556],
                    [81.008819, 41.004714],
                    [81.009239, 41.003827],
                    [81.009569, 41.002903],
                    [81.009808, 41.001951],
                    [81.009952, 41.00098],
                    [81.01, 41.0],
                    [81.01, 21.0],
                    [81.009952, 20.99902],
                    [81.009808, 20.998049],
                    [81.009569, 20.997097],
                    [81.009239, 20.996173],
                    [81.008819, 20.995286],
                    [81.008315, 20.994444],
                    [81.00773, 20.993656],
                    [81.007071, 20.992929],
                    [81.006344, 20.99227],
                    [81.005556, 20.991685],
                    [81.004714, 20.991181],
                    [81.003827, 20.990761],
                    [81.002903, 20.990431],
                    [81.001951, 20.990192],
                    [81.00098, 20.990048],
                    [81.0, 20.99],
                    [1.0, 20.99],
                    [0.99902, 20.990048],
                    [0.998049, 20.990192],
                    [0.997097, 20.990431],
                    [0.996173, 20.990761],
                    [0.995286, 20.991181],
                    [0.994444, 20.991685],
                    [0.993656, 20.99227],
                    [0.992929, 20.992929],
                    [0.99227, 20.993656],
                    [0.991685, 20.994444],
                    [0.991181, 20.995286],
                    [0.990761, 20.996173],
                    [0.990431, 20.997097],
                    [0.990192, 20.998049],
                    [0.990048, 20.99902],
                    [0.99, 21.0],
                    [0.99, 41.0],
                ]
            ],
            "type": "Polygon",
        }
    ),
    id="parent_compass_Nord",
    properties={"name": "dans le Nord"},
)
REF_SMALL = Feature(
    geometry=SHAshape(
        {
            "coordinates": [
                [
                    [0.99, 41.0],
                    [0.990048, 41.00098],
                    [0.990192, 41.001951],
                    [0.990431, 41.002903],
                    [0.990761, 41.003827],
                    [0.991181, 41.004714],
                    [0.991685, 41.005556],
                    [0.99227, 41.006344],
                    [0.992929, 41.007071],
                    [0.993656, 41.00773],
                    [0.994444, 41.008315],
                    [0.995286, 41.008819],
                    [0.996173, 41.009239],
                    [0.997097, 41.009569],
                    [0.998049, 41.009808],
                    [0.99902, 41.009952],
                    [1.0, 41.01],
                    [81.0, 41.01],
                    [81.00098, 41.009952],
                    [81.001951, 41.009808],
                    [81.002903, 41.009569],
                    [81.003827, 41.009239],
                    [81.004714, 41.008819],
                    [81.005556, 41.008315],
                    [81.006344, 41.00773],
                    [81.007071, 41.007071],
                    [81.00773, 41.006344],
                    [81.008315, 41.005556],
                    [81.008819, 41.004714],
                    [81.009239, 41.003827],
                    [81.009569, 41.002903],
                    [81.009808, 41.001951],
                    [81.009952, 41.00098],
                    [81.01, 41.0],
                    [81.01, 27.0],
                    [81.009952, 26.99902],
                    [81.009808, 26.998049],
                    [81.009569, 26.997097],
                    [81.009239, 26.996173],
                    [81.008819, 26.995286],
                    [81.008315, 26.994444],
                    [81.00773, 26.993656],
                    [81.007071, 26.992929],
                    [81.006344, 26.99227],
                    [81.005556, 26.991685],
                    [81.004714, 26.991181],
                    [81.003827, 26.990761],
                    [81.002903, 26.990431],
                    [81.001951, 26.990192],
                    [81.00098, 26.990048],
                    [81.0, 26.99],
                    [1.0, 26.99],
                    [0.99902, 26.990048],
                    [0.998049, 26.990192],
                    [0.997097, 26.990431],
                    [0.996173, 26.990761],
                    [0.995286, 26.991181],
                    [0.994444, 26.991685],
                    [0.993656, 26.99227],
                    [0.992929, 26.992929],
                    [0.99227, 26.993656],
                    [0.991685, 26.994444],
                    [0.991181, 26.995286],
                    [0.990761, 26.996173],
                    [0.990431, 26.997097],
                    [0.990192, 26.998049],
                    [0.990048, 26.99902],
                    [0.99, 27.0],
                    [0.99, 41.0],
                ]
            ],
            "type": "Polygon",
        }
    ),
    id="parent_compass_SmallNord",
    properties={"name": "dans une petite partie Nord"},
)


class TestModule:
    def test_get_cardinal_masks(self):
        parent_id = "parent_compass"
        rsltcol = get_cardinal_masks(GEO, parent_id, ["Nord"])
        ref_col = FeatureCollection([REF_FEAT, REF_SMALL])
        assert ref_col == rsltcol
        pass


class TestCardinalMasks:
    def test_test_area(self):
        geo = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 41], [81, 41], [81, 1], [1, 1]]],
            }
        )
        cm = CardinalMasks(geo, "parent_compass")
        min_area = MIN_AREA
        max_area = MAX_AREA
        # one sub zone ok
        sub = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 20], [20, 20], [20, 1], [1, 1]]],
            }
        )
        rslt = cm.test_area(sub, min_area, max_area)
        assert rslt
        # the second sub zone too close of an existant subzone
        sub = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 20], [20, 20], [20, 1], [1, 1]]],
            }
        )
        cm.l_result = [sub]
        rslt = cm.test_area(sub, min_area, max_area)
        assert not rslt
        # sub zone too big compare to geo zone
        sub = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 41], [81, 41], [81, 1], [1, 1]]],
            }
        )
        rslt = cm.test_area(sub, min_area, max_area)
        assert not rslt
        # sub zone too small compare to geo zone
        sub = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]],
            }
        )
        rslt = cm.test_area(sub, min_area, max_area)
        assert not rslt

    def test_get_rect_mask(self):
        geo = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 41], [81, 41], [81, 1], [1, 1]]],
            }
        )
        cm = CardinalMasks(geo, "parent_compass")
        lon_scale = 0.5
        lat_scale = 0.5
        origin = (41, 21)
        rslt = cm.get_rect_mask(lon_scale, lat_scale, origin)
        refpoly = "POLYGON ((21 11, 21 31, 61 31, 61 11, 21 11))"
        assert refpoly == str(rslt)

    def test_get_central_squares(self):
        geo = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 41], [81, 41], [81, 1], [1, 1]]],
            }
        )
        cm = CardinalMasks(geo, "parent_compass")
        resultbig, resultsmall = cm.get_central_squares()
        big = str(resultbig)
        small = str(resultsmall)
        refbig = "POLYGON ((41 31, 61 21, 41 11, 21 21, 41 31))"
        refsmall = "POLYGON ((41 26, 51 21, 41 16, 31 21, 41 26))"
        assert refbig == big and refsmall == small

    def test_make_name(self):
        geo = SHAshape(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 4], [3, 4], [3, 1], [1, 1]]],
            }
        )
        cm = CardinalMasks(geo, "parent_compass")
        result = cm.make_name("Nord")
        assert result == "dans le Nord"
        result = cm.make_name("Ouest")
        assert result == "dans l'Ouest"
        result = cm.make_name("SmallSud")
        assert result == "dans une petite partie Sud"
        result = cm.make_name("SmallOuest")
        assert result == "dans une petite partie Ouest"

    def test_make_all_masks(self):
        cm = CardinalMasks(GEO, "parent_compass")
        cardinal_point = "Nord"
        cm.make_all_masks(cardinal_point)
        rslt = cm.l_feat
        feat = rslt.pop(0)
        assert feat == REF_FEAT
