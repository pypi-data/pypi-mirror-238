import pytest

from mfire.composite import AltitudeComposite
from mfire.settings import ALT_MAX, ALT_MIN


class TestAltitudeComposite:
    def test_default_init(self, test_file):
        with pytest.raises(FileNotFoundError, match="No such file ."):
            AltitudeComposite(filename="")

        alt = AltitudeComposite(filename=test_file.name)
        assert alt.alt_min == ALT_MIN
        assert alt.alt_max == ALT_MAX
