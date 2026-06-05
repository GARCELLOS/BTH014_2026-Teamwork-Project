import marshal
import unittest


class TestDumps(unittest.TestCase):
    """I found some branch in load float, complex, str, tuple type data
    may reach by marshal version and interened state
    """
    def test_dumps_float_marshal0and5(self):
        """Test float dumps result in marshal5 and 0"""
        value = 3.14
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dumps_complex_marshal0and5(self):
        """Test complex dumps result in marshal5 and 0"""
        value = 3+4j
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dumps_shortascii_interenedandnot(self):
        """Test interened shortascii and uninterened utf8 dumps result"""
        valueinterened = "True"
        valueuninterened = ("True"+"1")[:-1]
        datainterened = marshal.dumps(valueinterened, 5)
        dataUnterened = marshal.dumps(valueuninterened, 5)
        self.assertEqual(datainterened, dataUnterened)

    def test_dumps_longascii_interenedandnot(self):
        """Test interened longascii and uninterened utf8 dumps result"""
        value = "T"*256
        valueinterened = value
        valueuninterened = (value+"1")[:-1]
        datainterened = marshal.dumps(valueinterened, 5)
        dataUnterened = marshal.dumps(valueuninterened, 5)
        self.assertEqual(datainterened, dataUnterened)

    def test_dumps_utf8_interenedandnot(self):
        """Test interened utf8 and uninterened utf8 dumps result"""
        value = "Hello World".encode("utf-8")
        valueinterened = value
        valueuninterened = (value+"1".encode("utf-8"))[:-1]
        datainterened = marshal.dumps(valueinterened, 5)
        dataUnterened = marshal.dumps(valueuninterened, 5)
        self.assertEqual(datainterened, dataUnterened)

    def test_dumps_utf8_marshal0and5(self):
        """Test interened utf8 dumps result in marshal5 and 0"""
        value = "Hello World".encode("utf-8")
        valueinterened = value
        data0 = marshal.dumps(valueinterened, 0)
        data5 = marshal.dumps(valueinterened, 5)
        self.assertEqual(data0, data5)

    def test_dumps_smalltuple_marshal0and5(self):
        """Test small tuple dumps result in marshal5 and 0"""
        value = (1, 5, 6, 7, 9)
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)


if __name__ == "__main__":
    unittest.main()
