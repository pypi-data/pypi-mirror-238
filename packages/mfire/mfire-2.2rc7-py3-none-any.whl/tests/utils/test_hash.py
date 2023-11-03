from mfire.utils import MD5


class TestMD5:
    def test_obj_with_string(self):
        md5 = MD5("test")
        assert md5.obj == b"test"

    def test_obj_with_file(self, test_file):
        test_file.write("test")
        test_file.close()
        md5 = MD5(test_file.name)
        assert md5.obj == b"test"

    def test_hash(self, test_file):
        test_file.write("test")
        test_file.close()
        md5 = MD5(test_file.name)
        assert md5.hash == "098f6bcd"
