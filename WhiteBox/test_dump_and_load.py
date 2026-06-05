import marshal
import unittest
import array
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp", "record.pyc")


class TestDumpAndLoad(unittest.TestCase):
    """Cover data type that only have one branch in both load and dump"""
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
        """Test none dump and load result"""
        value = False
        with open(tempfile_dir, "wb") as file:
            marshal.dump(value, file, 5)
        with open(tempfile_dir, "rb") as file:
            data = marshal.load(file)
        self.assertEqual(data, value)

    def test_dump_and_load_true(self):
        """Test true dump and load result"""
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
        """Test frozen dump and load result"""
        value = frozenset({100, 50, 88, "774", True, None})
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

    def test_dump_notallowcode(self):
        """Test not allow code exception"""
        value = compile("def func(x): return x", "test", "exec")
        with self.assertRaises(ValueError):
            with open(tempfile_dir, "rb") as file:
                marshal.dump(value, file, allow_code=False)

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

    def test_dump_slice_marshal0(self):
        """Test slice exception in marshal0"""
        value = slice(1, 9, 2)
        with self.assertRaises(ValueError):
            with open(tempfile_dir, "wb") as file:
                marshal.dump(value, file, 0)


if __name__ == "__main__":
    unittest.main()
