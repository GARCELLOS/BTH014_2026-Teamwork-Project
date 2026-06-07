static PyObject *
marshal_dump(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{ // 传入值分别为   模块本身     所有python传入值数组     位置参数的数量     关键词参数的名称元组
    PyObject *return_value = NULL;
#if defined(Py_BUILD_CORE) && !defined(Py_BUILD_CORE_MODULE)
// 编译核心解释器器且不编译内置模块时
#define NUM_KEYWORDS 1
    // 定义当前函数支持的关键词参数数量
    static struct
    {
        PyGC_Head _this_is_not_used;
        PyObject_VAR_HEAD
            Py_hash_t ob_hash;
        PyObject *ob_item[NUM_KEYWORDS];
    } _kwtuple = {
        .ob_base = PyVarObject_HEAD_INIT(&PyTuple_Type, NUM_KEYWORDS)
                       .ob_hash = -1,
        .ob_item = {
            &_Py_ID(allow_code),
        },
    };
    // 创建静态伪元组(”allow_code“,)
#undef NUM_KEYWORDS
#define KWTUPLE (&_kwtuple.ob_base.ob_base)
// 定义伪元组供后续使用
#else // !Py_BUILD_CORE
#define KWTUPLE NULL
// 其他模块包含marshal.c.h时才会进入，基本不触发
#endif // !Py_BUILD_CORE

    static const char *const _keywords[] = {"", "", "", "allow_code", NULL};
    // 对应于dump(value, file, version=version, allow_code=True)
    // 前三个都是位置参数只有allow_code是关键词参数
    static _PyArg_Parser _parser = {
        .keywords = _keywords,
        .fname = "dump",
        .kwtuple = KWTUPLE, // 元组用于快速查找allow_code
    }; // 用于匹配获取参数
#undef KWTUPLE
    PyObject *argsbuf[4];
    // 仅用于缓冲
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 2;
    // 计算可选参数数量，必须参数为value和file
    PyObject *value;
    PyObject *file;
    int version = Py_MARSHAL_VERSION;
    int allow_code = 1;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser,
                                 /*minpos*/ 2, /*maxpos*/ 3, /*minkw*/ 0, /*varpos*/ 0, argsbuf);
    // 位置参数最少两个最多三个，关键词参数最少一个，不允许额外参数
    if (!args) // 无参数直接退
    {
        goto exit;
    }
    value = args[0];
    file = args[1];
    if (nargs < 3) // 没有可选参数
    {
        goto skip_optional_posonly;
    }
    noptargs--; // 处理第一个可选参数：version
    version = PyLong_AsInt(args[2]);
    if (version == -1 && PyErr_Occurred())
    {
        goto exit;
    }
skip_optional_posonly:
    if (!noptargs) // 没有剩下的可选参数直接执行
    {
        goto skip_optional_kwonly;
    }
    // 处理第二个可选参数：allow_code
    allow_code = PyObject_IsTrue(args[3]);
    if (allow_code < 0)
    {
        goto exit;
    }
skip_optional_kwonly:
    return_value = marshal_dump_impl(module, value, file, version, allow_code);

exit:
    return return_value;
}

static PyObject *
marshal_dump_impl(PyObject *module, PyObject *value, PyObject *file,
                  int version, int allow_code)
/*[clinic end generated code: output=429e5fd61c2196b9 input=041f7f6669b0aafb]*/
{
    /* XXX Quick hack -- need to do this differently */
    PyObject *s;
    PyObject *res;

    s = _PyMarshal_WriteObjectToString(value, version, allow_code);
    // 将value转换为字节串
    if (s == NULL)
        return NULL;
    res = PyObject_CallMethodOneArg(file, &_Py_ID(write), s);
    // 调用write写入文件
    Py_DECREF(s);
    // 回收内存
    return res;
}

static PyObject *
_PyMarshal_WriteObjectToString(PyObject *x, int version, int allow_code)
{
    WFILE wf;

    if (PySys_Audit("marshal.dumps", "Oi", x, version) < 0)
    // 安全检查
    {
        return NULL;
    }
    memset(&wf, 0, sizeof(wf));
    // 初始化wf
    wf.str = PyBytes_FromStringAndSize((char *)NULL, 50);
    // 分配50字节内存
    if (wf.str == NULL)
        // 检测内存失败
        return NULL;
    wf.ptr = wf.buf = PyBytes_AS_STRING(wf.str);
    // 初始化指针
    wf.end = wf.ptr + PyBytes_GET_SIZE(wf.str);
    // 初始化结束指针
    wf.error = WFERR_OK;
    // 初始化错误状态为OK
    wf.version = version;
    wf.allow_code = allow_code;
    if (w_init_refs(&wf, version))
    { // 版本大于3时初始化用于记录对象的哈希表，检测是否内存不足
        Py_DECREF(wf.str);
        return NULL;
    }
    w_object(x, &wf);
    // 将值转换为字节串
    w_clear_refs(&wf);
    // 清除哈希表
    if (wf.str != NULL)
    { // 检测序列化是否出错
        const char *base = PyBytes_AS_STRING(wf.str);
        // 获取str起始位置
        if (_PyBytes_Resize(&wf.str, (Py_ssize_t)(wf.ptr - base)) < 0)
            // 重新分配内存，检测是否分配失败
            return NULL;
    }
    if (wf.error != WFERR_OK)
    { // 根据错误报错
        Py_XDECREF(wf.str);
        // 清理内存
        switch (wf.error)
        { // 根据报错提示
        case WFERR_NOMEMORY:
            PyErr_NoMemory();
            break;
        case WFERR_NESTEDTOODEEP:
            PyErr_SetString(PyExc_ValueError,
                            "object too deeply nested to marshal");
            break;
        case WFERR_CODE_NOT_ALLOWED:
            PyErr_SetString(PyExc_ValueError,
                            "marshalling code objects is disallowed");
            break;
        default:
        case WFERR_UNMARSHALLABLE:
            PyErr_SetString(PyExc_ValueError,
                            "unmarshallable object");
            break;
        }
        return NULL;
    }
    return wf.str;
}

static PyObject *
marshal_load(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
#if defined(Py_BUILD_CORE) && !defined(Py_BUILD_CORE_MODULE)

#define NUM_KEYWORDS 1
    static struct
    {
        PyGC_Head _this_is_not_used;
        PyObject_VAR_HEAD
            Py_hash_t ob_hash;
        PyObject *ob_item[NUM_KEYWORDS];
    } _kwtuple = {
        .ob_base = PyVarObject_HEAD_INIT(&PyTuple_Type, NUM_KEYWORDS)
                       .ob_hash = -1,
        .ob_item = {
            &_Py_ID(allow_code),
        },
    };
#undef NUM_KEYWORDS
#define KWTUPLE (&_kwtuple.ob_base.ob_base)

#else // !Py_BUILD_CORE
#define KWTUPLE NULL
#endif // !Py_BUILD_CORE

    static const char *const _keywords[] = {"", "allow_code", NULL};
    static _PyArg_Parser _parser = {
        .keywords = _keywords,
        .fname = "load",
        .kwtuple = KWTUPLE,
    };
#undef KWTUPLE
    PyObject *argsbuf[2];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    PyObject *file;
    int allow_code = 1;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser,
                                 /*minpos*/ 1, /*maxpos*/ 1, /*minkw*/ 0, /*varpos*/ 0, argsbuf);
    if (!args)
    {
        goto exit;
    }
    file = args[0];
    if (!noptargs)
    {
        goto skip_optional_kwonly;
    }
    allow_code = PyObject_IsTrue(args[1]);
    if (allow_code < 0)
    {
        goto exit;
    }
skip_optional_kwonly:
    return_value = marshal_load_impl(module, file, allow_code);

exit:
    return return_value;
}

static PyObject *
marshal_load_impl(PyObject *module, PyObject *file, int allow_code)
/*[clinic end generated code: output=0c1aaf3546ae3ed3 input=2dca7b570653b82f]*/
{
    PyObject *data, *result;
    RFILE rf;

    /*
     * Make a call to the read method, but read zero bytes.
     * This is to ensure that the object passed in at least
     * has a read method which returns bytes.
     * This can be removed if we guarantee good error handling
     * for r_string()
     */
    data = _PyObject_CallMethod(file, &_Py_ID(read), "i", 0);
    // 检测文件是否支持读取
    if (data == NULL)
        return NULL;
    if (!PyBytes_Check(data))
    { // 确认读入bytes对象
        PyErr_Format(PyExc_TypeError,
                     "file.read() returned not bytes but %.100s",
                     Py_TYPE(data)->tp_name);
        result = NULL;
    }
    else
    {
        rf.allow_code = allow_code;
        rf.depth = 0;
        rf.fp = NULL;
        rf.readable = file;     // 读取的流式对象
        rf.ptr = rf.end = NULL; // 从文件中读入，不需要指针
        rf.buf = NULL;          // 可能需要缓冲
        if ((rf.refs = PyList_New(0)) != NULL)
        { // rf.refs就是python列表，此处为检查refs初始化是否成功
            result = read_object(&rf);
            Py_DECREF(rf.refs);
            if (rf.buf != NULL)
                PyMem_Free(rf.buf);
        }
        else
            result = NULL;
    }
    Py_DECREF(data);
    return result;
}

static PyObject *
marshal_loads_impl(PyObject *module, Py_buffer *bytes, int allow_code)
/*[clinic end generated code: output=62c0c538d3edc31f input=14de68965b45aaa7]*/
{
    RFILE rf;
    char *s = bytes->buf;
    Py_ssize_t n = bytes->len;
    PyObject *result;
    rf.allow_code = allow_code;
    rf.fp = NULL;
    rf.readable = NULL; // 从bytes对象中读入，不需要文件
    rf.ptr = s;
    rf.end = s + n;
    rf.depth = 0;
    if ((rf.refs = PyList_New(0)) == NULL)
        // 同样的检测refs初始化
        return NULL;
    result = read_object(&rf);
    Py_DECREF(rf.refs);
    return result;
}

static PyObject *
read_object(RFILE *p)
{
    PyObject *v;
    if (PyErr_Occurred())
    { // 检查是否已经有错误在线程中
        fprintf(stderr, "XXX readobject called with exception set\n");
        return NULL;
    }
    if (p->ptr && p->end)
    { // 定义了指针表明在使用loads方法
        if (PySys_Audit("marshal.loads", "y#", p->ptr, (Py_ssize_t)(p->end - p->ptr)) < 0)
        {
            return NULL;
        }
    }
    else if (p->fp || p->readable)
    { // 定义了文件表明在使用load
        if (PySys_Audit("marshal.load", NULL) < 0)
        {
            return NULL;
        }
    }
    v = r_object(p);
    if (v == NULL && !PyErr_Occurred())
        // 检查结果
        PyErr_SetString(PyExc_TypeError, "NULL object in marshal data for object");
    return v;
}