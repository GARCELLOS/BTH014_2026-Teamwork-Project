import unittest
import os
# please run generate_int.py on both linux and windows platform before testing
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp")


class TestLinuxAndWindows(unittest.TestCase):
    """I found some branch in load int type data
    may reach by linux and windows system
    """
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
