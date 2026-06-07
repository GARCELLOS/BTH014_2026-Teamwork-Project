import sys


def get_code_cases():
    cases = []

    cases.append(
        (
            "EQ-code-099",
            "code: def f(): pass, "
            "SHA-256 consistent after 10 serializations",
            compile("def f(): pass", "<test>", "exec").co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-100",
            "code: def f(x): return x, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(x): return x", "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-101",
            "code: def f(a, b=1): return a+b, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(a, b=1): return a+b", "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-102",
            "code: def f(*args): return args, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(*args): return args", "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-103",
            "code: def f(**kw): return kw, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(**kw): return kw", "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-104",
            "code: def f(a, b=2, *args, c=3, **kw), "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(a, b=2, *args, c=3, **kw): pass",
                "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-105",
            "code: def f(a, *, b, c=4), "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(a, *, b, c=4): pass", "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-106",
            "code: closure inner(y): return x+y, "
            "SHA-256 consistent after 10 serializations",
            compile(
                (
                    "def outer(x):\n"
                    "    def inner(y): return x+y\n"
                    "    return inner"
                ),
                "<test>",
                "exec",
            )
            .co_consts[0]
            .co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-107",
            "code: generator yield i, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def gen(n):\n    for i in range(n): yield i",
                "<test>", "exec",
            ).co_consts[0],
        )
    )

    if sys.version_info >= (3, 5):
        cases.append(
            (
                "EQ-code-108",
                "code: async def foo(): return 1, "
                "SHA-256 consistent after 10 serializations",
                compile(
                    "async def foo(): return 1", "<test>", "exec",
                ).co_consts[0],
            )
        )

    cases.append(
        (
            "EQ-code-109",
            "code: def f(a:int, b:str='ok') -> bool, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def f(a: int, b: str = 'ok') -> bool: return True",
                "<test>", "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-110",
            "code: lambda x, y=2: x*y, "
            "SHA-256 consistent after 10 serializations",
            compile("lambda x, y=2: x * y", "<test>", "eval"),
        )
    )

    cases.append(
        (
            "EQ-code-111",
            "code: if-else conditional, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "x = 1\nif x > 0:\n    y = 1\nelse:\n    y = -1",
                "<test>",
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
                "<test>", "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-113",
            "code: complex control flow, "
            "SHA-256 consistent after 10 serializations",
            compile(
                (
                    "def f(x):\n"
                    "    if x>0:\n"
                    "        for i in range(x):\n"
                    "            try:\n"
                    "                _=10/i\n"
                    "            except ZeroDivisionError:\n"
                    "                pass\n"
                    "    return x"
                ),
                "<test>",
                "exec",
            ).co_consts[0],
        )
    )

    cases.append(
        (
            "EQ-code-114",
            "code: eval 1+2, "
            "SHA-256 consistent after 10 serializations",
            compile("1 + 2", "<test>", "eval"),
        )
    )

    cases.append(
        (
            "EQ-code-115",
            "code: multiline statements, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "x = 1\ny = x + 2", "<test>", "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-116",
            "code: try/except block, "
            "SHA-256 consistent after 10 serializations",
            compile(
                (
                    "try:\n"
                    "    x = 1/0\n"
                    "except ZeroDivisionError:\n"
                    "    x = 0"
                ),
                "<test>",
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
                "<test>", "exec",
            ),
        )
    )

    cases.append(
        (
            "EQ-code-118",
            "code: unicode source x='中文😀', "
            "SHA-256 consistent after 10 serializations",
            compile("x = '中文😀'", "<test>", "exec"),
        )
    )

    cases.append(
        (
            "EQ-code-119",
            "code: def empty(): pass, "
            "SHA-256 consistent after 10 serializations",
            compile(
                "def empty(): pass", "<test>", "exec",
            ).co_consts[0],
        )
    )

    code_consts = compile(
        "x = (None, True, 123, 3.14, 'abc')", "<test>", "exec",
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
