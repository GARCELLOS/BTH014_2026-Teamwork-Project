import marshal
import unittest
import os
# please run genrateFloat_Complex_UTF8_smalltuple_longint.py
# on both python3.14 and py2.3 before testing and
# generate_int.py on both linux and windows platform
# before running
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp")


class TestLinuxAndWindows(unittest.TestCase):
    """To test dump or dumps result in different branch"""
    def test_dumps_float_marshal0and5(self):
        """Test float dumps result in marshal5 and 0"""
        value = 3.14
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dump_float_python(self):
        """Test float dump result in marshal5 and 0
        but change it by changing python version
        value = 3.14
        """
        with open(os.path.join(tempfile_dir,
                               "python_3.14_marshal_5_Float.pyc"),
                  "rb") as file:
            data5 = file.read()
        with open(os.path.join(tempfile_dir,
                               "python_2.3_marshal_0_Float.pyc"),
                  "rb") as file:
            data0 = file.read()
        self.assertEqual(data5, data0)

    def test_dumps_complex_marshal0and5(self):
        """Test complex dumps result in marshal5 and 0"""
        value = 3+4j
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dump_complex_python(self):
        """Test complex dump result in marshal5 and 0
        but change it by changing python version
        value = 3+4j
        """
        with open(os.path.join(tempfile_dir,
                               "python_3.14_marshal_5_Complex.pyc"),
                  "rb") as file:
            data5 = file.read()
        with open(os.path.join(tempfile_dir,
                               "python_2.3_marshal_0_Complex.pyc"),
                  "rb") as file:
            data0 = file.read()
        self.assertEqual(data5, data0)

    def test_dumps_utf8_interened_marshal0and5(self):
        """Test interened utf8 dumps result in marshal5 and 0"""
        value = "Hello World".encode("utf-8")
        valueinterened = value
        data0 = marshal.dumps(valueinterened, 0)
        data5 = marshal.dumps(valueinterened, 5)
        self.assertEqual(data0, data5)

    def test_dump_utf8_interened_python(self):
        """Test Intererened UTF dump result in marshal5 and 0
        but change it by changing python version
        value = "Hello World".encode("utf-8")
        """
        with open(os.path.join(tempfile_dir,
                               "python_3.14_marshal_5_UTF8_Interened.pyc"),
                  "rb") as file:
            data5 = file.read()
        with open(os.path.join(tempfile_dir,
                               "python_2.3_marshal_0_UTF8_Interened.pyc"),
                  "rb") as file:
            data0 = file.read()
        self.assertEqual(data5, data0)

    def test_dumps_ascii_marshal0and5(self):
        """Test ascii dumps result in marshal5 and 0"""
        value = "Hello World"
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dumps_ascii_interned_marshal0and3(self):
        """Test interned ascii dumps result in marshal3 and 0"""
        value = "Hello World"
        data0 = marshal.dumps(value, 0)
        data3 = marshal.dumps(value, 3)
        self.assertEqual(data0, data3)

    def test_dumps_smalltuple_marshal0and5(self):
        """Test small tuple dumps result in marshal5 and 0"""
        value = (1, 5, 6, 7, 9)
        data0 = marshal.dumps(value, 0)
        data5 = marshal.dumps(value, 5)
        self.assertEqual(data0, data5)

    def test_dump_smalltuple_python(self):
        """Test Intererened UTF dump result in marshal5 and 0
        but change it by changing python version
        value = (1, 5, 6, 7, 9)
        """
        with open(os.path.join(tempfile_dir,
                               "python_3.14_marshal_5_smalltuple.pyc"),
                  "rb") as file:
            data5 = file.read()
        with open(os.path.join(tempfile_dir,
                               "python_2.3_marshal_0_smalltuple.pyc"),
                  "rb") as file:
            data0 = file.read()
        self.assertEqual(data5, data0)

    def test_dump_longint_python(self):
        """Test long int in marshal5 and marshal0
        but change it by changing python version
        value = 4294967295
        """
        with open(os.path.join(tempfile_dir,
                               "python_3.14_marshal_5_longint.pyc"),
                  "rb") as file:
            data5 = file.read()
        with open(os.path.join(tempfile_dir,
                               "python_2.3_marshal_0_longint.pyc"),
                  "rb") as file:
            data0 = file.read()
        self.assertEqual(data5, data0)

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

    def test_dump_shortint(self):
        """Test short int in Linux and Windows system
        value = 214748364
        """
        with open(os.path.join(tempfile_dir,
                               "Windows_shortint.pyc"),
                  "rb") as file:
            dataWindows = file.read()
        with open(os.path.join(tempfile_dir,
                               "Linux_shortint.pyc"),
                  "rb") as file:
            dataLinux = file.read()
        self.assertEqual(dataWindows, dataLinux)

    def test_dump_longint(self):
        """Test long int in Linux and Windows system
        value = 4294967295
        """
        with open(os.path.join(tempfile_dir,
                               "Windows_longint.pyc"),
                  "rb") as file:
            dataWindows = file.read()
        with open(os.path.join(tempfile_dir,
                               "Linux_longint.pyc"),
                  "rb") as file:
            dataLinux = file.read()
        self.assertEqual(dataWindows, dataLinux)


if __name__ == "__main__":
    unittest.main()
