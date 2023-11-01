from mfire.utils.unit_converter import fromWWMFToW1


class TestConversion:
    def test_simple(self):
        assert set(fromWWMFToW1(98)) == {29}
        assert set(fromWWMFToW1(61)) == {13}

    def test_list(self):
        assert set(fromWWMFToW1([98, 99])) == {25, 29}
        assert set(fromWWMFToW1([40, 53, 61, 99])) == {9, 11, 13, 25}
