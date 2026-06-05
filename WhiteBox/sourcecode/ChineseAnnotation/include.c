/*将Python对象写入文件并读回。
这主要用于编写和读取编译的Python代码，
尽管支持在代码对象中不常见的dicts、list、set和frozensets。
此协议的版本3正确支持循环链接和共享*/

#include "Python.h"
#include "pycore_call.h"          // _PyObject_CallNoArgs()
#include "pycore_code.h"          // _PyCode_New()
#include "pycore_hashtable.h"     // _Py_hashtable_t
#include "pycore_long.h"          // _PyLong_IsZero()
#include "pycore_object.h"        // _PyObject_IsUniquelyReferenced
#include "pycore_pystate.h"       // _PyInterpreterState_GET()
#include "pycore_setobject.h"     // _PySet_NextEntryRef()
#include "pycore_unicodeobject.h" // _PyUnicode_InternImmortal()

#include "marshal.h" // Py_MARSHAL_VERSION

#ifdef __APPLE__ //
#include "TargetConditionals.h"
#endif /* __APPLE__ */

/*[clinic input]
module marshal
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=c982b7930dee17db]*/

#include "clinic/marshal.c.h"