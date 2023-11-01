import pytest

from mfire.utils.formatter import TagFormatter, match_text


class TestFormatterFunctions:
    @pytest.mark.parametrize(
        "text1,text2,expected",
        [
            ("Les vents seront forts", "Les vents seront " "marqués", True),
            ("Les vents seront faibles", "Les vents seront " "marqués", False),
        ],
    )
    def test_match_text(self, text1, text2, expected):
        assert match_text(text1, text2) == expected


class TestTagFormatter:
    @pytest.mark.parametrize(
        "text,tags,expected",
        [
            ("Datetime: [key:ymdhm]", {}, "Datetime: [key:ymdhm]"),
            ("Datetime: [key:ymd]", {"key": 1618617600}, "Datetime: 20210417"),
            (
                "Datetime: [key:ymdhm]",
                {"key": "20230301T0600"},
                "Datetime: 202303010600",
            ),
            (
                "Datetime: [key:vortex]",
                {"key": "20230301T0600"},
                "Datetime: 20230301T060000",
            ),
        ],
    )
    def test_format_tags(self, text, tags, expected):
        tag_formatter = TagFormatter()
        assert tag_formatter.format_tags(text, tags=tags) == expected
