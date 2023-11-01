import pytest

from mfire.utils import dict_diff
from mfire.utils.dict_utils import KeyBasedDefaultDict


class TestDictUtilsFunctions:
    @pytest.mark.parametrize(
        "left,right,kwargs,expected",
        [
            (set(), list(), {}, False),  # not same type
            (set("a"), set("b"), {}, False),
            (set("a"), set("a"), {}, True),
            ("string {param1}", "string {param2}", {}, False),
            (
                "string {param1}",
                "string {param2}",
                {"param1": "string1", "param2": "string2"},
                False,
            ),
            (
                "string {param1}",
                "string {param2}",
                {"param1": "string1", "param2": "string1"},
                True,
            ),
        ],
    )
    def test_dict_diff(self, left, right, kwargs, expected):
        assert dict_diff(left, right, **kwargs) == expected


class TestKeyBasedDefaultDict:
    def test_init(self):
        key_based_default_dict = KeyBasedDefaultDict(lambda x: {"key": x})
        assert key_based_default_dict["test"]["key"] == "test"

    def test_no_default_factory(self):
        key_based_default_dict = KeyBasedDefaultDict()
        with pytest.raises(KeyError, match="key"):
            _ = key_based_default_dict["key"]
