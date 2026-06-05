import sys


def get_code_cases():
    cases = []

    cases.append(
        (
            "CODE-01",
            "Code object - no args",
            compile("def f(): pass", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-02",
            "Code object - positional arg",
            compile("def f(x): return x", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-03",
            "Code object - default args",
            compile("def f(a, b=1): return a+b", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-04",
            "Code object - *args",
            compile("def f(*args): return args", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-05",
            "Code object - **kwargs",
            compile("def f(**kw): return kw", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-06",
            "Code object - all arg types",
            compile("def f(a, b=2, *args, c=3, **kw): pass", "<test>", "exec").co_consts[
                0
            ],
        )
    )
    cases.append(
        (
            "CODE-07",
            "Code object - keyword-only args",
            compile("def f(a, *, b, c=4): pass", "<test>", "exec").co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-08",
            "Code object - closure",
            compile(
                "def outer(x):\n    def inner(y): return x+y\n    return inner",
                "<test>",
                "exec",
            )
            .co_consts[0]
            .co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-09",
            "Code object - generator",
            compile(
                "def gen(n):\n    for i in range(n): yield i", "<test>", "exec"
            ).co_consts[0],
        )
    )

    if sys.version_info >= (3, 5):
        cases.append(
            (
                "CODE-10",
                "Code object - async function",
                compile("async def foo(): return 1", "<test>", "exec").co_consts[0],
            )
        )

    cases.append(
        (
            "CODE-11",
            "Code object - annotations",
            compile(
                "def f(a: int, b: str = 'ok') -> bool: return True", "<test>", "exec"
            ).co_consts[0],
        )
    )
    cases.append(
        (
            "CODE-12",
            "Code object - lambda",
            compile("lambda x, y=2: x * y", "<test>", "eval"),
        )
    )
    cases.append(
        (
            "CODE-13",
            "Code object - if-else conditional",
            compile(
                "x = 1\nif x > 0:\n    y = 1\nelse:\n    y = -1",
                "<test>",
                "exec",
            ),
        )
    )
    cases.append(
        (
            "CODE-14",
            "Code object - for loop",
            compile("s = 0\nfor i in range(10):\n    s += i", "<test>", "exec"),
        )
    )
    cases.append(
        (
            "CODE-15",
            "Code object - complex control flow",
            compile(
                "def f(x):\n    if x>0:\n        for i in range(x):\n            try:\n                _=10/i\n            except ZeroDivisionError:\n                pass\n    return x",
                "<test>",
                "exec",
            ).co_consts[0],
        )
    )
    cases.append(
        ("CODE-16", "Code object - eval expression", compile("1 + 2", "<test>", "eval"))
    )
    cases.append(
        (
            "CODE-17",
            "Code object - multiline statements",
            compile("x = 1\ny = x + 2", "<test>", "exec"),
        )
    )
    cases.append(
        (
            "CODE-18",
            "Code object - try/except block",
            compile(
                "try:\n    x = 1/0\nexcept ZeroDivisionError:\n    x = 0",
                "<test>",
                "exec",
            ),
        )
    )
    cases.append(
        (
            "CODE-19",
            "Code object - class definition",
            compile("class A:\n    def method(self): return 1", "<test>", "exec"),
        )
    )
    cases.append(
        (
            "CODE-20",
            "Code object - unicode source",
            compile("x = '中文😀'", "<test>", "exec"),
        )
    )
    cases.append(
        (
            "CODE-21",
            "Code object - empty body",
            compile("def empty(): pass", "<test>", "exec").co_consts[0],
        )
    )

    code_consts = compile("x = (None, True, 123, 3.14, 'abc')", "<test>", "exec")
    cases.append(("CODE-22", "Code object - mixed constants tuple", code_consts))

    return cases
