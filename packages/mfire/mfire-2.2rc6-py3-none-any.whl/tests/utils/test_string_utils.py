from mfire.utils.string_utils import concatenate_string, decapitalize


class TestStringUtilsFunctions:
    def test_decapitalize(self):
        assert decapitalize("LOwer") == "lOwer"

    def test_concatenate_string(self):
        assert concatenate_string(["test1"]) == "test1"
        assert concatenate_string(["test1"], last_ponctuation=".") == "test1."
        assert (
            concatenate_string(["test1", "test2", "test3"]) == "test1, test2 et "
            "test3"
        )
