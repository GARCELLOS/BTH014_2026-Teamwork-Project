/* 定义最大深度防止marshal过于深和危及编译器，
 * 当object栈到达最大深度时报错而不是继续
 * Windows调试版本减低该值
 *
 * BUG: https://bugs.python.org/issue33720
 * 在Windows PGO版本中，r_object函数过度分配其堆栈可能会导致堆栈溢出
 * 我们降低了所有窗口的最大深度释放以防止这种情况
 * #if defined(MS_WINDOWS) && defined(_DEBUG)
 */

#if defined(MS_WINDOWS)
#define MAX_MARSHAL_STACK_DEPTH 1000
#elif defined(__wasi__)
#define MAX_MARSHAL_STACK_DEPTH 1500
// TARGET_OS_IPHONE涵盖任何非macOS苹果平台。
// 它不会在较旧的macOS SDK上定义
#elif defined(__APPLE__) && defined(TARGET_OS_IPHONE) && TARGET_OS_IPHONE
#define MAX_MARSHAL_STACK_DEPTH 1500
#else
#define MAX_MARSHAL_STACK_DEPTH 2000
#endif

/* Supported types */
#define TYPE_NULL '0'
#define TYPE_NONE 'N'
#define TYPE_FALSE 'F'
#define TYPE_TRUE 'T'
#define TYPE_STOPITER 'S'
#define TYPE_ELLIPSIS '.'
#define TYPE_BINARY_FLOAT 'g'   // Version 0 uses TYPE_FLOAT instead.
#define TYPE_BINARY_COMPLEX 'y' // Version 0 uses TYPE_COMPLEX instead.
#define TYPE_LONG 'l'           // See also TYPE_INT.
#define TYPE_STRING 's'         // Bytes. (Name comes from Python 2.)
#define TYPE_TUPLE '('          // See also TYPE_SMALL_TUPLE.
#define TYPE_LIST '['
#define TYPE_DICT '{'
#define TYPE_CODE 'c'
#define TYPE_UNICODE 'u'
#define TYPE_UNKNOWN '?'
// added in version 2:
#define TYPE_SET '<'
#define TYPE_FROZENSET '>'
// added in version 5:
#define TYPE_SLICE ':'
// Remember to update the version and documentation when adding new types.

/* Special cases for unicode strings (added in version 4) */
#define TYPE_INTERNED 't' // Version 1+
#define TYPE_ASCII 'a'
#define TYPE_ASCII_INTERNED 'A'
#define TYPE_SHORT_ASCII 'z'
#define TYPE_SHORT_ASCII_INTERNED 'Z'

/* Special cases for small objects */
#define TYPE_INT 'i'         // All versions. 32-bit encoding.
#define TYPE_SMALL_TUPLE ')' // Version 4+

/* Supported for backwards compatibility */
#define TYPE_COMPLEX 'x' // Generated for version 0 only.
#define TYPE_FLOAT 'f'   // Generated for version 0 only.
#define TYPE_INT64 'I'   // Not generated any more.

/* References (added in version 3) */
#define TYPE_REF 'r'
#define FLAG_REF '\x80' /* with a type, add obj to index */

// Error codes:
#define WFERR_OK 0
#define WFERR_UNMARSHALLABLE 1
#define WFERR_NESTEDTOODEEP 2
#define WFERR_NOMEMORY 3
#define WFERR_CODE_NOT_ALLOWED 4

typedef struct
{
    FILE *fp;
    int error; /* see WFERR_* values */
    int depth;
    PyObject *str;
    char *ptr;
    const char *end;
    char *buf;
    _Py_hashtable_t *hashtable;
    int version;
    int allow_code;
} WFILE;

#define w_byte(c, p)                                   \
    do                                                 \
    {                                                  \
        if ((p)->ptr != (p)->end || w_reserve((p), 1)) \
            *(p)->ptr++ = (c);                         \
    } while (0)

// 此处有一段静态函数

#define SIZE32_MAX 0x7FFFFFFF

#if SIZEOF_SIZE_T > 4
#define W_SIZE(n, p)                           \
    do                                         \
    {                                          \
        if ((n) > SIZE32_MAX)                  \
        {                                      \
            (p)->depth--;                      \
            (p)->error = WFERR_UNMARSHALLABLE; \
            return;                            \
        }                                      \
        w_long((long)(n), p);                  \
    } while (0)
#else
#define W_SIZE w_long
#endif

// 此处有一段静态函数

/* We assume that Python ints are stored internally in base some power of
   2**15; for the sake of portability we'll always read and write them in base
   exactly 2**15. */

#define PyLong_MARSHAL_SHIFT 15
#define PyLong_MARSHAL_BASE ((short)1 << PyLong_MARSHAL_SHIFT)
#define PyLong_MARSHAL_MASK (PyLong_MARSHAL_BASE - 1)

#define W_TYPE(t, p)             \
    do                           \
    {                            \
        w_byte((t) | flag, (p)); \
    } while (0)

// 此处有一段函数

typedef struct
{
    FILE *fp;
    int depth;
    PyObject *readable; /* Stream-like object being read from */
    const char *ptr;
    const char *end;
    char *buf;
    Py_ssize_t buf_size;
    PyObject *refs; /* a list */
    int allow_code;
} RFILE;

// 此处有一段静态函数
