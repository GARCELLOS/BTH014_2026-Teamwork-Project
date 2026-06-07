import marshal
import unittest


class TestError(unittest.TestCase):
    """To test some cases that may raise error"""
    def test_loads_default(self):
        """Test exception"""
        value = b"/0x1894"
        with self.assertRaises(ValueError):
            marshal.loads(value)

    def test_dump_notallowcode(self):
        """Test not allow code exception"""
        value = compile("def func(x): return x", "test", "exec")
        with self.assertRaises(ValueError):
            marshal.dumps(value, allow_code=False)

    def test_dump_slice_marshal0(self):
        """Test slice exception in marshal0"""
        value = slice(1, 9, 2)
        with self.assertRaises(ValueError):
            marshal.dump(value, 0)


if __name__ == "__main__":
    unittest.main()
