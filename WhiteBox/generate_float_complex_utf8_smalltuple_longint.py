import marshal
import platform
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
tempfile_dir = os.path.join(script_dir, "temp")
python_version = ".".join(platform.python_version().split('.')[:2])
if python_version == "2.3":
    marshal_version = "0"
else:
    marshal_version = str(marshal.version)
env_name = os.path.join(tempfile_dir, "python_" + python_version +
                        "_marshal_"+marshal_version)

value = 3.14
file_name = env_name+"_Float.pyc"
file = open(file_name, "wb")
marshal.dump(value, file)
file.close()

value = 3+4j
file_name = env_name+"_Complex.pyc"
file = open(file_name, "wb")
marshal.dump(value, file)
file.close()

valueOriginal = "Hello World".encode("utf-8")
value = valueOriginal
file_name = env_name+"_UTF8_Interened.pyc"
file = open(file_name, "wb")
marshal.dump(value, file)
file.close()

value = (1, 5, 6, 7, 9)
file_name = env_name+"_smalltuple.pyc"
file = open(file_name, "wb")
marshal.dump(value, file)
file.close()

value = 4294967295
file_name = env_name+"_longint.pyc"
file = open(file_name, "wb")
marshal.dump(value, file)
file.close()
