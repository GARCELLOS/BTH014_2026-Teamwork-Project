import sys
import types


TEST_FILENAME = "<test>"


def _find_code_object(code_obj, code_name):
    """Recursively find a nested code object by co_name."""
    for const in code_obj.co_consts:
        if not isinstance(const, types.CodeType):
            continue

        if const.co_name == code_name:
            return const

        nested = _find_code_object(const, code_name)
        if nested is not None:
            return nested

    return None


def _get_code_object(source, code_name, mode="exec"):
    """Compile source and return the target code object."""
    module_code = compile(source, TEST_FILENAME, mode)
    code_obj = _find_code_object(module_code, code_name)

    if code_obj is None:
        raise ValueError(f"code object {code_name!r} not found")

    return code_obj


def get_code_cases():
    cases = []

    cases.append(
        (
            "EQ-code-099",
            "code: def f(): pass, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object("def f(): pass", "f"),
        )
    )

    cases.append(
        (
            "EQ-code-100",
            "code: def f(x): return x, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(x): return x",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-101",
            "code: def f(a, b=1): return a+b, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(a, b=1): return a+b",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-102",
            "code: def f(*args): return args, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(*args): return args",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-103",
            "code: def f(**kw): return kw, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(**kw): return kw",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-104",
            "code: def f(a, b=2, *args, c=3, **kw), "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(a, b=2, *args, c=3, **kw): pass",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-105",
            "code: def f(a, *, b, c=4), "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(a, *, b, c=4): pass",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-106",
            "code: closure inner(y): return x+y, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def outer(x):\n"
                "    def inner(y): return x+y\n"
                "    return inner",
                "inner",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-107",
            "code: generator yield i, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def gen(n):\n    for i in range(n): yield i",
                "gen",
            ),
        )
    )

    if sys.version_info >= (3, 5):
        cases.append(
            (
                "EQ-code-108",
                "code: async def foo(): return 1, "
                "SHA-256 consistent after 10 serializations",
                _get_code_object(
                    "async def foo(): return 1",
                    "foo",
                ),
            )
        )

    cases.append(
        (
            "EQ-code-109",
            "code: def f(a:int, b:str='ok') -> bool, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(a: int, b: str = 'ok') -> bool: return True",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-110",
            "code: lambda x, y=2: x*y, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "lambda x, y=2: x * y",
                "<lambda>",
                mode="eval",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-111",
            "code: if-else conditional, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "x = 1\nif x > 0:\n    y = 1\nelse:\n    y = -1",
                TEST_FILENAME,
                "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-112",
            "code: for loop sum, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "s = 0\nfor i in range(10):\n    s += i",
                TEST_FILENAME,
                "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-113",
            "code: complex control flow, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def f(x):\n"
                "    if x>0:\n"
                "        for i in range(x):\n"
                "            try:\n"
                "                _=10/i\n"
                "            except ZeroDivisionError:\n"
                "                pass\n"
                "    return x",
                "f",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-114",
            "code: eval 1+2, "
            "SHA-256 consistent after 10 serializations",
            compile("1 + 2", TEST_FILENAME, "eval"),
        )
    )

    cases.append(
        (
            "EQ-code-115",
            "code: multiline statements, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "x = 1\ny = x + 2",
                TEST_FILENAME,
                "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-116",
            "code: try/except block, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "try:\n"
                "    x = 1/0\n"
                "except ZeroDivisionError:\n"
                "    x = 0",
                TEST_FILENAME,
                "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-117",
            "code: class A with method, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "class A:\n    def method(self): return 1",
                TEST_FILENAME,
                "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-118",
            "code: unicode source x='中文😀', "
            "SHA-256 consistent after 10 serializations",
            compile("x = '中文😀'", TEST_FILENAME, "exec"),
        )
    )

    cases.append(
        (
            "EQ-code-119",
            "code: def empty(): pass, "
            "SHA-256 consistent after 10 serializations",
            _get_code_object(
                "def empty(): pass",
                "empty",
            ),
        )
    )

    code_consts = compile(
        "x = (None, True, 123, 3.14, 'abc')",
        TEST_FILENAME,
        "exec",
    )
    cases.append(
        (
            "EQ-code-120",
            "code: mixed constants tuple, "
            "SHA-256 consistent after 10 serializations",
            code_consts,
        )
    )

    return cases
