static void
w_object(PyObject *v, WFILE *p)
{
    char flag = '\0';

    if (p->error != WFERR_OK)
    { // 错误状态直接退
        return;
    }

    p->depth++;
    // 确保每次进入复杂object都增加深度
    if (p->depth > MAX_MARSHAL_STACK_DEPTH)
    { // 深度过高不再处理
        p->error = WFERR_NESTEDTOODEEP;
    }
    else if (v == NULL)
    { // 检测特殊值
        w_byte(TYPE_NULL, p);
    }
    else if (v == Py_None)
    {
        w_byte(TYPE_NONE, p);
    }
    else if (v == PyExc_StopIteration)
    {
        w_byte(TYPE_STOPITER, p);
    }
    else if (v == Py_Ellipsis)
    {
        w_byte(TYPE_ELLIPSIS, p);
    }
    else if (v == Py_False)
    {
        w_byte(TYPE_FALSE, p);
    }
    else if (v == Py_True)
    {
        w_byte(TYPE_TRUE, p);
    }
    else if (!w_ref(v, &flag, p))
        // 检查对象是否被转化过，同时打标记
        w_complex_object(v, flag, p);

    p->depth--;
}

static void
w_complex_object(PyObject *v, char flag, WFILE *p)
{
    Py_ssize_t i, n;

    if (PyLong_CheckExact(v))
    { // 检测是否是长整型
        int overflow;
        long x = PyLong_AsLongAndOverflow(v, &overflow);
        // 将v转换到长整型并检测是否溢出
        if (overflow)
        { // 溢出交给其他方式写入
            w_PyLong((PyLongObject *)v, flag, p);
        }
        else
        {
#if SIZEOF_LONG > 4
            // 判断当前平台上 C 的 long 类型是否占超过 4 个字节
            long y = Py_ARITHMETIC_RIGHT_SHIFT(long, x, 31);
            // x算术右移31位
            if (y && y != -1)
            { // x无法放入32位
                /* Too large for TYPE_INT */
                w_PyLong((PyLongObject *)v, flag, p);
            }
            else
#endif
            { // 先写类型符号后写整数值
                W_TYPE(TYPE_INT, p);
                w_long(x, p);
            }
        }
    }
    else if (PyFloat_CheckExact(v))
    { // 检测float类型
        if (p->version > 1)
        { // 初代marshal和后续marshal写入类型不同
            W_TYPE(TYPE_BINARY_FLOAT, p);
            w_float_bin(PyFloat_AS_DOUBLE(v), p);
        }
        else
        {
            W_TYPE(TYPE_FLOAT, p);
            w_float_str(PyFloat_AS_DOUBLE(v), p);
        }
    }
    else if (PyComplex_CheckExact(v))
    { // 检测complex类型
        if (p->version > 1)
        { // 初代marshal和后续marshal使用类型不同
            W_TYPE(TYPE_BINARY_COMPLEX, p);
            w_float_bin(PyComplex_RealAsDouble(v), p);
            w_float_bin(PyComplex_ImagAsDouble(v), p);
        }
        else
        {
            W_TYPE(TYPE_COMPLEX, p);
            w_float_str(PyComplex_RealAsDouble(v), p);
            w_float_str(PyComplex_ImagAsDouble(v), p);
        }
    }
    else if (PyBytes_CheckExact(v))
    { // 字节流直接写
        W_TYPE(TYPE_STRING, p);
        w_pstring(PyBytes_AS_STRING(v), PyBytes_GET_SIZE(v), p);
    }
    else if (PyUnicode_CheckExact(v))
    { // 检测字符串类型
        if (p->version >= 4 && PyUnicode_IS_ASCII(v))
        { // marshal4以上有ascii的特殊处理
            int is_short = PyUnicode_GET_LENGTH(v) < 256;
            if (is_short)
            { // 长度小于256
                if (PyUnicode_CHECK_INTERNED(v))
                    // 驻留字符串
                    W_TYPE(TYPE_SHORT_ASCII_INTERNED, p);
                else
                    W_TYPE(TYPE_SHORT_ASCII, p);
                w_short_pstring(PyUnicode_1BYTE_DATA(v),
                                PyUnicode_GET_LENGTH(v), p);
            }
            else
            {
                if (PyUnicode_CHECK_INTERNED(v))
                    W_TYPE(TYPE_ASCII_INTERNED, p);
                else
                    W_TYPE(TYPE_ASCII, p);
                w_pstring(PyUnicode_1BYTE_DATA(v),
                          PyUnicode_GET_LENGTH(v), p);
            }
        }
        else
        {
            PyObject *utf8;
            utf8 = PyUnicode_AsEncodedString(v, "utf8", "surrogatepass");
            // v转化为utf-8编码字节流
            if (utf8 == NULL)
            { // 编码失败直接退
                p->depth--;
                p->error = WFERR_UNMARSHALLABLE;
                return;
            }
            if (p->version >= 3 && PyUnicode_CHECK_INTERNED(v))
                // marshal3以上检查驻留字符串
                W_TYPE(TYPE_INTERNED, p);
            else
                W_TYPE(TYPE_UNICODE, p);
            w_pstring(PyBytes_AS_STRING(utf8), PyBytes_GET_SIZE(utf8), p);
            Py_DECREF(utf8);
        }
    }
    else if (PyTuple_CheckExact(v))
    { // 检测元组类型
        n = PyTuple_GET_SIZE(v);
        if (p->version >= 4 && n < 256)
        { // 4版本以上检测小元组
            W_TYPE(TYPE_SMALL_TUPLE, p);
            w_byte((unsigned char)n, p);
        }
        else
        {
            W_TYPE(TYPE_TUPLE, p);
            W_SIZE(n, p);
        }
        for (i = 0; i < n; i++)
        { // 逐个写入元组元素
            w_object(PyTuple_GET_ITEM(v, i), p);
        }
    }
    else if (PyList_CheckExact(v))
    { // 检测列表类型
        W_TYPE(TYPE_LIST, p);
        n = PyList_GET_SIZE(v);
        W_SIZE(n, p);
        for (i = 0; i < n; i++)
        { // 逐个写入列表元素
            w_object(PyList_GET_ITEM(v, i), p);
        }
    }
    else if (PyDict_CheckExact(v))
    { // 检测字典类型
        Py_ssize_t pos;
        PyObject *key, *value;
        W_TYPE(TYPE_DICT, p);
        /* 字典由NULL结束 */
        pos = 0;
        while (PyDict_Next(v, &pos, &key, &value))
        { // 逐个写入键和值
            w_object(key, p);
            w_object(value, p);
        } // 写结束符
        w_object((PyObject *)NULL, p);
    }
    else if (PyAnySet_CheckExact(v))
    { // 检测set或frozenset
        PyObject *value;
        Py_ssize_t pos = 0;
        Py_hash_t hash;

        if (PyFrozenSet_CheckExact(v))
            // 检测frozenset
            W_TYPE(TYPE_FROZENSET, p);
        else
            W_TYPE(TYPE_SET, p);
        n = PySet_GET_SIZE(v);
        W_SIZE(n, p);
        // 写入set内元素个数
        // 为了支持可复制的构建，集合和冷冻集合需要
        // 以一致的顺序序列化它们的元素，即使它们已被哈希随机化打乱
        // 为了确保这一点，我们使用与sorted（v，key=marshall.dumps）等效的顺序：
        PyObject *pairs = PyList_New(n);
        // 创建列表存储集合元素
        if (pairs == NULL)
        { // 检测构建失败
            p->error = WFERR_NOMEMORY;
            return;
        }
        Py_ssize_t i = 0;
        Py_BEGIN_CRITICAL_SECTION(v);
        // 防止值被回收
        while (_PySet_NextEntryRef(v, &pos, &value, &hash))
        { // 遍历集合元素
            PyObject *dump = _PyMarshal_WriteObjectToString(value,
                                                            p->version, p->allow_code);
            if (dump == NULL)
            { // 检测不可marshal的元素
                p->error = WFERR_UNMARSHALLABLE;
                Py_DECREF(value);
                break;
            }
            PyObject *pair = PyTuple_Pack(2, dump, value);
            // 将每个元素转化为字节串后与原值创建元组
            Py_DECREF(dump);
            Py_DECREF(value);
            if (pair == NULL)
            { // 检测内存
                p->error = WFERR_NOMEMORY;
                break;
            }
            PyList_SET_ITEM(pairs, i++, pair);
            // 元组存入pairs
        }
        Py_END_CRITICAL_SECTION();
        if (p->error == WFERR_UNMARSHALLABLE || p->error == WFERR_NOMEMORY)
        { // 检测是否出错
            Py_DECREF(pairs);
            return;
        }
        assert(i == n);
        // 确认所有元素都已字节化完毕且存入pairs
        if (PyList_Sort(pairs))
        { // 对pairs根据字节化后的值进行排序，检测内存
            p->error = WFERR_NOMEMORY;
            Py_DECREF(pairs);
            return;
        }
        for (Py_ssize_t i = 0; i < n; i++)
        {
            PyObject *pair = PyList_GET_ITEM(pairs, i);
            value = PyTuple_GET_ITEM(pair, 1);
            w_object(value, p);
        } // 根据排序后顺序写入
        Py_DECREF(pairs);
    }
    else if (PyCode_Check(v))
    {
        if (!p->allow_code)
        { // 检测是否允许传入代码
            p->error = WFERR_CODE_NOT_ALLOWED;
            return;
        }
        PyCodeObject *co = (PyCodeObject *)v;
        PyObject *co_code = _PyCode_GetCode(co);
        // 获取代码字节化数据
        if (co_code == NULL)
        { // 检测
            p->error = WFERR_NOMEMORY;
            return;
        }
        W_TYPE(TYPE_CODE, p);
        w_long(co->co_argcount, p);
        // 写入参数数量
        w_long(co->co_posonlyargcount, p);
        // 写入位置参数数量
        w_long(co->co_kwonlyargcount, p);
        // 写入关键词参数数量
        w_long(co->co_stacksize, p);
        // 写入栈深度
        w_long(co->co_flags, p);
        // 写入代码特性标识符
        w_object(co_code, p);
        // 写入代码字节化数据
        w_object(co->co_consts, p);
        // 写入代码常量元组
        w_object(co->co_names, p);
        // 写入代码各种名称元组(变量，函数)
        w_object(co->co_localsplusnames, p);
        // 写入代码局部变量名元组
        w_object(co->co_localspluskinds, p);
        // 写入对应的变量种类
        w_object(co->co_filename, p);
        // 写入代码源文件路径
        w_object(co->co_name, p);
        // 写入代码名称
        w_object(co->co_qualname, p);
        // 写入完全限定名称如A(clase).f(method)
        w_long(co->co_firstlineno, p);
        // 写入代码起始行号
        w_object(co->co_linetable, p);
        // 写入行号映射表
        w_object(co->co_exceptiontable, p);
        // 写入异常处理表
        Py_DECREF(co_code);
    }
    else if (PyObject_CheckBuffer(v))
    { // 检查是否支持缓冲区协议
        /* 像一个字节object一样写入未知类字节object */
        Py_buffer view;
        if (PyObject_GetBuffer(v, &view, PyBUF_SIMPLE) != 0)
        { // 尝试获取字符串并检测错误
            w_byte(TYPE_UNKNOWN, p);
            p->depth--;
            p->error = WFERR_UNMARSHALLABLE;
            return;
        }
        W_TYPE(TYPE_STRING, p);
        w_pstring(view.buf, view.len, p);
        PyBuffer_Release(&view);
    }
    else if (PySlice_Check(v))
    {
        if (p->version < 5)
        { // marshal5以上才支持slice对象
            w_byte(TYPE_UNKNOWN, p);
            p->error = WFERR_UNMARSHALLABLE;
            return;
        }
        PySliceObject *slice = (PySliceObject *)v;
        W_TYPE(TYPE_SLICE, p);
        w_object(slice->start, p);
        w_object(slice->stop, p);
        w_object(slice->step, p);
        // 依次写入起始点,终止点(切片不包含),步长
    }
    else
    { // 未知类型直接退
        W_TYPE(TYPE_UNKNOWN, p);
        p->error = WFERR_UNMARSHALLABLE;
    }
}

static PyObject *
r_object(RFILE *p)
{
    /* NULL is a valid return value, it does not necessarily means that
       an exception is set. */
    PyObject *v, *v2;
    Py_ssize_t idx = 0;
    long i, n;
    int type, code = r_byte(p); // 读取第一个字符(根据dump可知这里是类型字符)
    int flag, is_interned = 0;
    PyObject *retval = NULL; // 存储读取结果

    if (code == EOF)
    { // 检测读取是否正常
        if (PyErr_ExceptionMatches(PyExc_EOFError))
        {
            PyErr_SetString(PyExc_EOFError,
                            "EOF read where object expected");
        }
        return NULL;
    }

    p->depth++; // 正式读取前先增加深度防止超栈

    if (p->depth > MAX_MARSHAL_STACK_DEPTH)
    { // 过深直接退
        p->depth--;
        PyErr_SetString(PyExc_ValueError, "recursion limit exceeded");
        return NULL;
    }

    flag = code & FLAG_REF;
    type = code & ~FLAG_REF;
    // 从之前读取的第一个字符获取类型和标记

#define R_REF(O)                   \
    do                             \
    {                              \
        if (flag)                  \
            O = r_ref(O, flag, p); \
    } while (0) // 保存引用表的宏

    switch (type)
    { // 先处理特殊值

    case TYPE_NULL:
        break;

    case TYPE_NONE:
        retval = Py_None;
        break;

    case TYPE_STOPITER:
        retval = Py_NewRef(PyExc_StopIteration);
        break;

    case TYPE_ELLIPSIS:
        retval = Py_Ellipsis;
        break;

    case TYPE_FALSE:
        retval = Py_False;
        break;

    case TYPE_TRUE:
        retval = Py_True;
        break;

    case TYPE_INT:
        n = r_long(p);
        if (n == -1 && PyErr_Occurred())
        { // 判断是否读取错误
            break;
        }
        retval = PyLong_FromLong(n);
        R_REF(retval);
        break;

    case TYPE_INT64:
        retval = r_long64(p);
        R_REF(retval);
        break;

    case TYPE_LONG:
        retval = r_PyLong(p);
        R_REF(retval);
        break;

    case TYPE_FLOAT:
    {
        double x = r_float_str(p);
        if (x == -1.0 && PyErr_Occurred())
            break;
        // 同样的判断是否读取错误
        retval = PyFloat_FromDouble(x);
        R_REF(retval);
        break;
    }

    case TYPE_BINARY_FLOAT:
    {
        double x = r_float_bin(p);
        if (x == -1.0 && PyErr_Occurred())
            break;
        retval = PyFloat_FromDouble(x);
        R_REF(retval);
        break;
    }

    case TYPE_COMPLEX:
    {
        Py_complex c;
        c.real = r_float_str(p);
        if (c.real == -1.0 && PyErr_Occurred())
            break;
        c.imag = r_float_str(p);
        if (c.imag == -1.0 && PyErr_Occurred())
            break;
        retval = PyComplex_FromCComplex(c);
        R_REF(retval);
        break;
    }

    case TYPE_BINARY_COMPLEX:
    {
        Py_complex c;
        c.real = r_float_bin(p);
        if (c.real == -1.0 && PyErr_Occurred())
            break;
        c.imag = r_float_bin(p);
        if (c.imag == -1.0 && PyErr_Occurred())
            break;
        retval = PyComplex_FromCComplex(c);
        R_REF(retval);
        break;
    }

    case TYPE_STRING:
    {
        const char *ptr;
        n = r_long(p); // 字节流会先写入长度
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (bytes object size out of range)");
            }
            break;
        }
        v = PyBytes_FromStringAndSize((char *)NULL, n);
        if (v == NULL) // 检测内存错误
            break;
        ptr = r_string(n, p);
        if (ptr == NULL)
        { // 检测读取是否失败
            Py_DECREF(v);
            break;
        }
        memcpy(PyBytes_AS_STRING(v), ptr, n);
        // 将读入内容拷贝给v
        retval = v;
        R_REF(retval);
        break;
    }

    case TYPE_ASCII_INTERNED:
        is_interned = 1;
        _Py_FALLTHROUGH; // 标记故意穿透
    case TYPE_ASCII:
        n = r_long(p); // 读入第一位长度
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
            PyErr_SetString(PyExc_ValueError,
                            "bad marshal data (string size out of range)");
            }
            break;
        } // 短ascii和长ascii基本没区别
        goto _read_ascii;

    case TYPE_SHORT_ASCII_INTERNED:
        is_interned = 1;
        _Py_FALLTHROUGH;
    case TYPE_SHORT_ASCII:
        n = r_byte(p);
        if (n == EOF)
        {
            break;
        }
    _read_ascii:
    {
        const char *ptr;
        ptr = r_string(n, p);
        if (ptr == NULL)
            break;
        v = PyUnicode_FromKindAndData(PyUnicode_1BYTE_KIND, ptr, n);
        // 从原始字节流生成每字符 1 字节的字符串
        if (v == NULL)
            break;
        if (is_interned)
        {
            // Marshall旨在用代码序列化.pyc文件
            // 对象和代码相关字符串目前是不朽的。
            PyInterpreterState *interp = _PyInterpreterState_GET();
            _PyUnicode_InternImmortal(interp, &v);
        }
        retval = v;
        R_REF(retval);
        break;
    }

    case TYPE_INTERNED:
        is_interned = 1;
        _Py_FALLTHROUGH;
    case TYPE_UNICODE:
    {
        const char *buffer;

        n = r_long(p);
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (string size out of range)");
            }
            break;
        }
        if (n != 0)
        {
            buffer = r_string(n, p);
            if (buffer == NULL)
                break;
            v = PyUnicode_DecodeUTF8(buffer, n, "surrogatepass");
            // 使用UTF-8解码器
        }
        else
        {
            v = Py_GetConstant(Py_CONSTANT_EMPTY_STR);
        } // n=0新建一个空白字符串
        if (v == NULL)
            break;
        if (is_interned)
        {
            // marshal is meant to serialize .pyc files with code
            // objects, and code-related strings are currently immortal.
            PyInterpreterState *interp = _PyInterpreterState_GET();
            _PyUnicode_InternImmortal(interp, &v);
        }
        retval = v;
        R_REF(retval);
        break;
    }

    case TYPE_SMALL_TUPLE:
        // 依旧先读长度
        n = r_byte(p);
        if (n == EOF)
        {
            break;
        }
        goto _read_tuple;
    case TYPE_TUPLE:
        n = r_long(p);
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (tuple size out of range)");
            }
            break;
        }
    _read_tuple:
        v = PyTuple_New(n);
        R_REF(v);
        if (v == NULL)
            break;

        for (i = 0; i < n; i++)
        { // 依旧逐个读入
            v2 = r_object(p);
            if (v2 == NULL)
            {
                if (!PyErr_Occurred())
                    PyErr_SetString(PyExc_TypeError,
                                    "NULL object in marshal data for tuple");
                Py_SETREF(v, NULL);
                break;
            }
            // v2设置到v的第i个位置
            PyTuple_SET_ITEM(v, i, v2);
        }
        retval = v;
        break;

    case TYPE_LIST:
        n = r_long(p);
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (list size out of range)");
            }
            break;
        }
        v = PyList_New(n);
        R_REF(v);
        if (v == NULL)
            break;
        for (i = 0; i < n; i++)
        {
            v2 = r_object(p);
            if (v2 == NULL)
            {
                if (!PyErr_Occurred())
                    PyErr_SetString(PyExc_TypeError,
                                    "NULL object in marshal data for list");
                Py_SETREF(v, NULL);
                break;
            }
            PyList_SET_ITEM(v, i, v2);
        }
        retval = v;
        break;

    case TYPE_DICT:
        v = PyDict_New();
        R_REF(v);
        if (v == NULL)
            break;
        for (;;) // 无限循环
        {
            PyObject *key, *val;
            key = r_object(p);
            if (key == NULL) // 检测是否读完和是否出错
                break;
            val = r_object(p);
            if (val == NULL)
            {
                Py_DECREF(key);
                break;
            }
            if (PyDict_SetItem(v, key, val) < 0)
            {
                Py_DECREF(key);
                Py_DECREF(val);
                break;
            }
            Py_DECREF(key);
            Py_DECREF(val);
        }
        if (PyErr_Occurred())
        { // 删除v的ref
            Py_SETREF(v, NULL);
        }
        retval = v;
        break;

    case TYPE_SET:
    case TYPE_FROZENSET:
        n = r_long(p);
        if (n < 0 || n > SIZE32_MAX)
        {
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (set size out of range)");
            }
            break;
        }

        if (n == 0 && type == TYPE_FROZENSET)
        { // 空的frozenset直接新建
            /* call frozenset() to get the empty frozenset singleton */
            v = _PyObject_CallNoArgs((PyObject *)&PyFrozenSet_Type);
            if (v == NULL)
                break;
            R_REF(v);
            retval = v;
        }
        else
        {
            v = (type == TYPE_SET) ? PySet_New(NULL) : PyFrozenSet_New(NULL);
            if (type == TYPE_SET)
            {
                R_REF(v);
            }
            else
            {
                // 必须使用延迟注册冷冻集，因为它们必须以refcount为1初始化
                // 在ref中先占一个位置
                idx = r_ref_reserve(flag, p);
                if (idx < 0)
                    Py_CLEAR(v); /* 信号错误 */
            }
            if (v == NULL)
                break;

            for (i = 0; i < n; i++)
            { // 依旧逐个读入
                v2 = r_object(p);
                if (v2 == NULL)
                {
                    if (!PyErr_Occurred())
                        PyErr_SetString(PyExc_TypeError,
                                        "NULL object in marshal data for set");
                    Py_SETREF(v, NULL);
                    break;
                }
                if (PySet_Add(v, v2) == -1)
                {
                    Py_DECREF(v);
                    Py_DECREF(v2);
                    v = NULL;
                    break;
                }
                Py_DECREF(v2);
            }
            if (type != TYPE_SET)
                // 替换预留占位符
                v = r_ref_insert(v, idx, flag, p);
            retval = v;
        }
        break;

    case TYPE_CODE:
    {
        int argcount;
        int posonlyargcount;
        int kwonlyargcount;
        int stacksize;
        int flags;
        PyObject *code = NULL;
        PyObject *consts = NULL;
        PyObject *names = NULL;
        PyObject *localsplusnames = NULL;
        PyObject *localspluskinds = NULL;
        PyObject *filename = NULL;
        PyObject *name = NULL;
        PyObject *qualname = NULL;
        int firstlineno;
        PyObject *linetable = NULL;
        PyObject *exceptiontable = NULL;

        if (!p->allow_code)
        { // 设置allow_code为0
            PyErr_SetString(PyExc_ValueError,
                            "unmarshalling code objects is disallowed");
            break;
        }
        // ref占位符
        idx = r_ref_reserve(flag, p);
        if (idx < 0)
            break;

        v = NULL;

        /* XXX ignore long->int overflows for now */
        argcount = (int)r_long(p);
        if (argcount == -1 && PyErr_Occurred())
            goto code_error;
        posonlyargcount = (int)r_long(p);
        if (posonlyargcount == -1 && PyErr_Occurred())
        {
            goto code_error;
        }
        kwonlyargcount = (int)r_long(p);
        if (kwonlyargcount == -1 && PyErr_Occurred())
            goto code_error;
        stacksize = (int)r_long(p);
        if (stacksize == -1 && PyErr_Occurred())
            goto code_error;
        flags = (int)r_long(p);
        if (flags == -1 && PyErr_Occurred())
            goto code_error;
        code = r_object(p);
        if (code == NULL)
            goto code_error;
        consts = r_object(p);
        if (consts == NULL)
            goto code_error;
        names = r_object(p);
        if (names == NULL)
            goto code_error;
        localsplusnames = r_object(p);
        if (localsplusnames == NULL)
            goto code_error;
        localspluskinds = r_object(p);
        if (localspluskinds == NULL)
            goto code_error;
        filename = r_object(p);
        if (filename == NULL)
            goto code_error;
        name = r_object(p);
        if (name == NULL)
            goto code_error;
        qualname = r_object(p);
        if (qualname == NULL)
            goto code_error;
        firstlineno = (int)r_long(p);
        if (firstlineno == -1 && PyErr_Occurred())
            break;
        linetable = r_object(p);
        if (linetable == NULL)
            goto code_error;
        exceptiontable = r_object(p);
        if (exceptiontable == NULL)
            goto code_error;

        struct _PyCodeConstructor con = {
            .filename = filename,
            .name = name,
            .qualname = qualname,
            .flags = flags,

            .code = code,
            .firstlineno = firstlineno,
            .linetable = linetable,

            .consts = consts,
            .names = names,

            .localsplusnames = localsplusnames,
            .localspluskinds = localspluskinds,

            .argcount = argcount,
            .posonlyargcount = posonlyargcount,
            .kwonlyargcount = kwonlyargcount,

            .stacksize = stacksize,

            .exceptiontable = exceptiontable,
        };

        if (_PyCode_Validate(&con) < 0)
        { // 检查代码合法性
            goto code_error;
        }

        v = (PyObject *)_PyCode_New(&con);
        if (v == NULL)
        {
            goto code_error;
        }

        v = r_ref_insert(v, idx, flag, p);
        // 填占位符
    code_error:
        if (v == NULL && !PyErr_Occurred())
        {
            PyErr_SetString(PyExc_TypeError,
                            "NULL object in marshal data for code object");
        }
        Py_XDECREF(code);
        Py_XDECREF(consts);
        Py_XDECREF(names);
        Py_XDECREF(localsplusnames);
        Py_XDECREF(localspluskinds);
        Py_XDECREF(filename);
        Py_XDECREF(name);
        Py_XDECREF(qualname);
        Py_XDECREF(linetable);
        Py_XDECREF(exceptiontable);
    }
        retval = v;
        break;

    case TYPE_REF:
        n = r_long(p); // 获取索引
        if (n < 0 || n >= PyList_GET_SIZE(p->refs))
        { // 验证引用索引
            if (!PyErr_Occurred())
            {
                PyErr_SetString(PyExc_ValueError,
                                "bad marshal data (invalid reference)");
            }
            break;
        }
        v = PyList_GET_ITEM(p->refs, n);
        if (v == Py_None)
        {
            PyErr_SetString(PyExc_ValueError, "bad marshal data (invalid reference)");
            break;
        }
        retval = Py_NewRef(v);
        break;

    case TYPE_SLICE:
    {
        Py_ssize_t idx = r_ref_reserve(flag, p);
        if (idx < 0)
        {
            break;
        }
        // 逐个读取起始 结束 步长
        PyObject *stop = NULL;
        PyObject *step = NULL;
        PyObject *start = r_object(p);
        if (start == NULL)
        {
            goto cleanup;
        }
        stop = r_object(p);
        if (stop == NULL)
        {
            goto cleanup;
        }
        step = r_object(p);
        if (step == NULL)
        {
            goto cleanup;
        }
        retval = PySlice_New(start, stop, step);
        r_ref_insert(retval, idx, flag, p);
    cleanup:
        Py_XDECREF(start);
        Py_XDECREF(stop);
        Py_XDECREF(step);
        break;
    }

    default:
        /*虚假数据被写入，这并不理想。
            这将让你继续工作和恢复。 */
        PyErr_SetString(PyExc_ValueError, "bad marshal data (unknown type code)");
        break;
    }
    p->depth--;
    return retval;
}