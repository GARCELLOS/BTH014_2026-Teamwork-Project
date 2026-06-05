import marshal
import unittest


class TestLoads(unittest.TestCase):
    """To cover load code that not cover by load and dump"""
    def test_loads_int(self):
        """Test int"""
        value = 214748364
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_long(self):
        """Test long"""
        value = 4294967295
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_float(self):
        """Test float"""
        value = 3.14
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_binary_float(self):
        """Test old version float"""
        value = 3.14
        data = marshal.dumps(value, 0)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_complex(self):
        """Test complex"""
        value = 3+4j
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_binary_complex(self):
        """Test old version complex"""
        value = 3+4j
        data = marshal.dumps(value, 0)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_shortascii_interened(self):
        """Test interened shortascii"""
        value = "True"
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_shortascii_uninterened(self):
        """Test uninterened shortascii"""
        value = ("True"+"1")[:-1]
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_longascii_interened(self):
        """Test interened longascii"""
        valueOriginal = "T"*256
        value = valueOriginal
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_longascii_uninterened(self):
        """Test uninterened longascii"""
        valueOriginal = "T"*256
        value = (valueOriginal+"1")[:-1]
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_utf8_interened(self):
        """Test interened utf8"""
        valueOriginal = "Hello World".encode("utf-8")
        value = valueOriginal
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_utf8_uninterened(self):
        """Test uninterened utf8"""
        valueOriginal = "Hello World".encode("utf-8")
        value = (valueOriginal+"1".encode("utf-8"))[:-1]
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_utf8_empty(self):
        """Test empty utf8"""
        value = "".encode("utf-8")
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_ref(self):
        """Test ref"""
        valueOriginal = [1, 2]
        value = [valueOriginal, valueOriginal]
        data = marshal.dumps(value, 5)
        result = marshal.loads(data)
        self.assertEqual(result, value)

    def test_loads_default(self):
        """Test exception"""
        value = b"/0x1894"
        with self.assertRaises(ValueError):
            marshal.loads(value)


if __name__ == "__main__":
    unittest.main()
