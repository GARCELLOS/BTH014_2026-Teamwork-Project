import marshal
import platform
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp")

value = 4294967295
file_name = os.path.join(tempfile_dir, platform.uname()[0]+"_longint.pyc")
with open(file_name, "wb") as file:
    marshal.dump(value, file, 5)
value = 214748364
file_name = os.path.join(tempfile_dir, platform.uname()[0]+"_shortint.pyc")
with open(file_name, "wb") as file:
    marshal.dump(value, file, 5)
