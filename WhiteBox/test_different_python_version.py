import unittest
import os
# please run genrateFloat_Complex_UTF8_smalltuple
# on both python3.14 and py2.3 before testing
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp")


class TestDump(unittest.TestCase):
    """This is a retest of some test cases that
    change marshal version in dumps
    achieve different branch
    by use different python version
    """
    def test_dump_float(self):
        """Test float dump result in marshal5 and 0
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

    def test_dump_complex(self):
        """Test complex dump result in marshal5 and 0
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

    def test_dump_utf8_interened(self):
        """Test Intererened UTF dump result in marshal5 and 0
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

    def test_dump_smalltuple(self):
        """Test Intererened UTF dump result in marshal5 and 0
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


if __name__ == "__main__":
    unittest.main()
