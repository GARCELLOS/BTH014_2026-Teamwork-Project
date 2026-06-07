PyObject *
PyMarshal_ReadObjectFromString(const char *str, Py_ssize_t len)
{
    RFILE rf;
    PyObject *result;
    rf.allow_code = 1;
    rf.fp = NULL;
    rf.readable = NULL;
    rf.ptr = str;
    rf.end = str + len;
    rf.buf = NULL;
    rf.depth = 0;
    rf.refs = PyList_New(0);
    if (rf.refs == NULL)
        return NULL;
    result = read_object(&rf);
    Py_DECREF(rf.refs);
    if (rf.buf != NULL)
        PyMem_Free(rf.buf);
    return result;
}

static PyObject *
_PyMarshal_WriteObjectToString(PyObject *x, int version, int allow_code)
{
    WFILE wf;

    if (PySys_Audit("marshal.dumps", "Oi", x, version) < 0)
    {
        return NULL;
    }
    memset(&wf, 0, sizeof(wf));
    wf.str = PyBytes_FromStringAndSize((char *)NULL, 50);
    if (wf.str == NULL)
        return NULL;
    wf.ptr = wf.buf = PyBytes_AS_STRING(wf.str);
    wf.end = wf.ptr + PyBytes_GET_SIZE(wf.str);
    wf.error = WFERR_OK;
    wf.version = version;
    wf.allow_code = allow_code;
    if (w_init_refs(&wf, version))
    {
        Py_DECREF(wf.str);
        return NULL;
    }
    w_object(x, &wf);
    w_clear_refs(&wf);
    if (wf.str != NULL)
    {
        const char *base = PyBytes_AS_STRING(wf.str);
        if (_PyBytes_Resize(&wf.str, (Py_ssize_t)(wf.ptr - base)) < 0)
            return NULL;
    }
    if (wf.error != WFERR_OK)
    {
        Py_XDECREF(wf.str);
        switch (wf.error)
        {
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

PyObject *
PyMarshal_WriteObjectToString(PyObject *x, int version)
{
    return _PyMarshal_WriteObjectToString(x, version, 1);
}

long PyMarshal_ReadLongFromFile(FILE *fp)
{
    RFILE rf;
    long res;
    rf.fp = fp;
    rf.readable = NULL;
    rf.ptr = rf.end = NULL;
    rf.buf = NULL;
    res = r_long(&rf);
    if (rf.buf != NULL)
        PyMem_Free(rf.buf);
    return res;
}

int PyMarshal_ReadShortFromFile(FILE *fp)
{
    RFILE rf;
    int res;
    assert(fp);
    rf.readable = NULL;
    rf.fp = fp;
    rf.end = rf.ptr = NULL;
    rf.buf = NULL;
    res = r_short(&rf);
    if (rf.buf != NULL)
        PyMem_Free(rf.buf);
    return res;
}

PyObject *
PyMarshal_ReadObjectFromFile(FILE *fp)
{
    RFILE rf;
    PyObject *result;
    rf.allow_code = 1;
    rf.fp = fp;
    rf.readable = NULL;
    rf.depth = 0;
    rf.ptr = rf.end = NULL;
    rf.buf = NULL;
    rf.refs = PyList_New(0);
    if (rf.refs == NULL)
        return NULL;
    result = read_object(&rf);
    Py_DECREF(rf.refs);
    if (rf.buf != NULL)
        PyMem_Free(rf.buf);
    return result;
}

/* If we can get the size of the file up-front, and it's reasonably small,
 * read it in one gulp and delegate to ...FromString() instead.  Much quicker
 * than reading a byte at a time from file; speeds .pyc imports.
 * CAUTION:  since this may read the entire remainder of the file, don't
 * call it unless you know you're done with the file.
 */
PyObject *
PyMarshal_ReadLastObjectFromFile(FILE *fp)
{
/* REASONABLE_FILE_LIMIT is by defn something big enough for Tkinter.pyc. */
#define REASONABLE_FILE_LIMIT (1L << 18)
    off_t filesize;
    filesize = getfilesize(fp);
    if (filesize > 0 && filesize <= REASONABLE_FILE_LIMIT)
    {
        char *pBuf = (char *)PyMem_Malloc(filesize);
        if (pBuf != NULL)
        {
            size_t n = fread(pBuf, 1, (size_t)filesize, fp);
            PyObject *v = PyMarshal_ReadObjectFromString(pBuf, n);
            PyMem_Free(pBuf);
            return v;
        }
    }
    /* We don't have fstat, or we do but the file is larger than
     * REASONABLE_FILE_LIMIT or malloc failed -- read a byte at a time.
     */
    return PyMarshal_ReadObjectFromFile(fp);

#undef REASONABLE_FILE_LIMIT
}

/* version currently has no effect for writing ints. */
/* Note that while the documentation states that this function
 * can error, currently it never does. Setting an exception in
 * this function should be regarded as an API-breaking change.
 */
void PyMarshal_WriteLongToFile(long x, FILE *fp, int version)
{
    char buf[4];
    WFILE wf;
    memset(&wf, 0, sizeof(wf));
    wf.fp = fp;
    wf.ptr = wf.buf = buf;
    wf.end = wf.ptr + sizeof(buf);
    wf.error = WFERR_OK;
    wf.version = version;
    w_long(x, &wf);
    w_flush(&wf);
}

void PyMarshal_WriteObjectToFile(PyObject *x, FILE *fp, int version)
{
    char buf[BUFSIZ];
    WFILE wf;
    if (PySys_Audit("marshal.dumps", "Oi", x, version) < 0)
    {
        return; /* caller must check PyErr_Occurred() */
    }
    memset(&wf, 0, sizeof(wf));
    wf.fp = fp;
    wf.ptr = wf.buf = buf;
    wf.end = wf.ptr + sizeof(buf);
    wf.error = WFERR_OK;
    wf.version = version;
    wf.allow_code = 1;
    if (w_init_refs(&wf, version))
    {
        return; /* caller must check PyErr_Occurred() */
    }
    w_object(x, &wf);
    w_clear_refs(&wf);
    w_flush(&wf);
}