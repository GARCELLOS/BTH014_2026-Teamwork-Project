import marshal
import unittest
import array
import os
# please run genrateFloat_Complex_UTF8_smalltuple_longint.py
# on both python3.14 and py2.3 before testing
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp", "record.pyc")


class TestDumpAndLoad(unittest.TestCase):
    """To test the dump and load result of almost all branch"""
    def test_dump_and_load_none(self):
        """Test none dump and load result"""
        value = None
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_stopiteration(self):
        """Test stopiteration dump and load result"""
        value = StopIteration
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_ellipsis(self):
        """Test ellipsis dump and load result"""
        value = Ellipsis
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_false(self):
        """Test Bool dump and load result"""
        value = False
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_true(self):
        """Test Bool dump and load result"""
        value = True
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_bytes(self):
        """Test bytes dump and load result"""
        value = b"hello"
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_int64(self):
        """Test int64 dump and load result"""
        value = 4294967295
        with open(os.path.join(os.path.join(script_dir, "temp"),
                               "python_2.3_marshal_0_longint.pyc"),
                  "rb") as file:
            data = marshal.load(file)
        self.assertEqual(value, data)

    def test_dump_and_load_int(self):
        """Test int dump and load result"""
        value = 214748364
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_long(self):
        """Test long dump and load result"""
        value = 4294967295
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_float(self):
        """Test old version float dump and load result"""
        value = 3.14
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 0)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_binary_float(self):
        """Test float dump and load result"""
        value = 3.14
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_complex(self):
        """Test old version complex dump and load result"""
        value = 3+4j
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 0)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_binary_complex(self):
        """Test complex dump and load result"""
        value = 3+4j
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_shortascii_interened(self):
        """Test interened shortascii dump and load result"""
        value = "True"
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_shortascii_uninterened(self):
        """Test uninterened shortascii dump and load result"""
        value = ("True"+"1")[:-1]
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_longascii_interened(self):
        """Test interened longascii dump and load result"""
        valueOriginal = "T"*256
        value = valueOriginal
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_longascii_uninterened(self):
        """Test uninterened longascii dump and load result"""
        valueOriginal = "T"*256
        value = (valueOriginal+"1")[:-1]
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_utf8_interened(self):
        """Test interened utf8 dump and load result"""
        valueOriginal = "Hello World".encode("utf-8")
        value = valueOriginal
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_utf8_uninterened(self):
        """Test uninterened utf8 dump and load result"""
        valueOriginal = "Hello World".encode("utf-8")
        value = (valueOriginal+"1".encode("utf-8"))[:-1]
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_utf8_empty(self):
        """Test empty utf8 dump and load result"""
        value = "".encode("utf-8")
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_ref(self):
        """Test ref dump and load result"""
        valueOriginal = [1, 2]
        value = [valueOriginal, valueOriginal]
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_smalltuple(self):
        """Test small tuple dump and load result"""
        value = (1, 5, 6, 7, 9)
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_largetuple(self):
        """Test large tuple dump and load result"""
        value = tuple(range(256))
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_list(self):
        """Test list dump and load result"""
        value = [100, 50, [95, [77]], 88, {1: "56"}, "774", True, None]
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_dict(self):
        """Test dict dump and load result"""
        value = {1: 590, "42": "59", True: 75,
                 None: [79, 554], False: {"hello": 596}}
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_set(self):
        """Test set dump and load result"""
        value = {100, 50, 88, "774", True, None}
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_frozenset(self):
        """Test frozenset dump and load result"""
        value = frozenset({100, 50, 88, "774", True, None})
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_frozenset_empty(self):
        """Test empty frozen dump and load result"""
        value = frozenset()
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_code(self):
        """Test code dump and load result"""
        value = compile("def func(x): return x", "test", "exec")
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_buffer(self):
        """Test buffer array dump and load result"""
        value = array.array("i", [1, 8, 9])
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_slice(self):
        """Test slice dump and load result"""
        value = slice(1, 9, 2)
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)


if __name__ == "__main__":
    unittest.main()
