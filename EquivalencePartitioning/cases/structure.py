"""嵌套结构与循环引用用例。"""

from cases.builders import make_nested_list


def get_nested_cases():
    cases = []

    cases.append(
        ("EQ-nested-121", "Simple nested list", [[1, 2], [3, 4]]),
    )
    cases.append(
        (
            "EQ-nested-122",
            "Nested dict",
            {"a": {"b": {"c": 1}}},
        ),
    )
    cases.append(
        (
            "EQ-nested-123",
            "Mixed nested list/dict/tuple/None",
            [{"a": [1, 2, 3]}, ("x", None)],
        )
    )
    cases.append(
        (
            "EQ-nested-124",
            "Nested with float special values",
            {"value": [1.0, float("inf"), float("nan")]},
        )
    )
    cases.append(
        ("EQ-nested-125", "Deep nested list depth 5", [[[[[1]]]]]),
    )
    cases.append(
        (
            "EQ-nested-126",
            "List containing tuple",
            [1, (2, 3), 4],
        ),
    )
    cases.append(
        (
            "EQ-nested-127",
            "Tuple containing list",
            (1, [2, 3], 4),
        ),
    )
    cases.append(
        (
            "EQ-nested-128",
            "Dict containing list and tuple",
            {"list": [1, 2], "tuple": (3, 4)},
        )
    )
    cases.append(
        (
            "EQ-nested-129",
            "Dict containing set",
            {"s": {1, 2, 3}},
        ),
    )
    cases.append(
        (
            "EQ-nested-130",
            "List containing frozenset",
            [frozenset([1, 2, 3])],
        ),
    )
    cases.append(
        (
            "EQ-nested-131",
            "Empty nested containers",
            [[], {}, (), set()],
        ),
    )
    cases.append(
        (
            "EQ-nested-132",
            "Complex mixed nested structure",
            {"a": [1, {"b": (None, True, 3.14)}]},
        )
    )
    cases.append(
        (
            "EQ-nested-133",
            "Deep nested list depth 500 (within limit)",
            make_nested_list(500),
        )
    )
    cases.append(
        (
            "EQ-nested-134",
            "Deep nested list depth 1999 (near limit)",
            make_nested_list(1999),
        )
    )
    cases.append(
        (
            "EQ-nested-135",
            "Deep nested list depth 2001 "
            "(exceed limit, expect RecursionError)",
            make_nested_list(2001),
        )
    )
    cases.append(
        (
            "EQ-nested-136",
            "Large list 100000 elements",
            [0] * 100000,
        ),
    )
    cases.append(
        (
            "EQ-nested-137",
            "Large dict 100000 integer keys",
            {i: i for i in range(100000)},
        ),
    )
    cases.append(
        (
            "EQ-nested-138",
            "Large set 100000 integers",
            set(range(100000)),
        ),
    )
    cases.append(
        (
            "EQ-nested-139",
            "Large tuple 100000 integers",
            tuple(range(100000)),
        ),
    )

    shared = [1, 2, 3]
    cases.append(
        (
            "EQ-nested-140",
            "Shared reference list (same object repeated)",
            [shared, shared, shared],
        )
    )
    shared_dict = {"a": 1}
    cases.append(
        (
            "EQ-nested-141",
            "Shared reference dict",
            {"first": shared_dict, "second": shared_dict},
        )
    )

    huge_str = "x" * (1024 * 1024)
    cases.append(
        (
            "EQ-nested-142",
            "Nested list containing huge string",
            [huge_str, [huge_str]],
        ),
    )
    huge_bytes = b"y" * (1024 * 1024)
    cases.append(
        (
            "EQ-nested-143",
            "Nested list containing huge bytes",
            [huge_bytes, [huge_bytes]],
        ),
    )
    cases.append(
        (
            "EQ-nested-144",
            "Frozenset order independence",
            [frozenset([1, 2, 3]), frozenset([3, 2, 1])],
        )
    )

    return cases


def _make_cycle_list(depth):
    nodes = [None] * depth
    for i in range(depth):
        nodes[i] = []
    for i in range(depth):
        nodes[i].append(nodes[(i + 1) % depth])
    return nodes[0]


def get_cycle_cases():
    cases = []

    self_list = []
    self_list.append(self_list)
    cases.append(
        ("EQ-cycle-145", "Self-referential list", self_list),
    )

    self_dict = {}
    self_dict["self"] = self_dict
    cases.append(
        ("EQ-cycle-146", "Self-referential dict", self_dict),
    )

    a = []
    b = [a]
    a.append(b)
    cases.append(
        (
            "EQ-cycle-147",
            "Indirect circular reference (list->list)",
            a,
        ),
    )

    ld = []
    d = {"ref": ld}
    ld.append(d)
    cases.append(
        (
            "EQ-cycle-148",
            "List and dict mutual reference",
            ld,
        ),
    )

    d2 = {}
    a2 = [d2]
    d2["list"] = a2
    cases.append(
        (
            "EQ-cycle-149",
            "Dict and list mutual reference (reverse)",
            d2,
        ),
    )

    a3 = []
    b3 = [1, 2, a3]
    a3.append(b3)
    cases.append(
        ("EQ-cycle-150", "Nested list with cycle", a3),
    )

    x = [1, 2]
    a4 = [x, x]
    cases.append(
        (
            "EQ-cycle-151",
            "Repeated reference without cycle",
            a4,
        ),
    )

    a5 = []
    b5 = [a5]
    c5 = [b5]
    a5.append(c5)
    cases.append(
        (
            "EQ-cycle-152",
            "Deep indirect cycle (3 levels)",
            a5,
        ),
    )

    cases.append(
        (
            "EQ-cycle-153",
            "Deep cycle length 10",
            _make_cycle_list(10),
        ),
    )

    shared_node = []
    cycle_a = [shared_node]
    cycle_b = [shared_node]
    shared_node.append(cycle_a)
    shared_node.append(cycle_b)
    cases.append(
        (
            "EQ-cycle-154",
            "Multiple cycles sharing a node",
            shared_node,
        ),
    )

    nan_cycle = []
    inf_cycle = []
    nan_cycle.append(inf_cycle)
    inf_cycle.append(nan_cycle)
    nan_cycle.insert(0, float("nan"))
    inf_cycle.insert(0, float("inf"))
    cases.append(
        (
            "EQ-cycle-155",
            "Cycle with NaN and Inf",
            nan_cycle,
        ),
    )

    big_cycle = []
    big_str = "big" * 100000
    for _ in range(3):
        node = [big_str]
        big_cycle.append(node)
    big_cycle[-1].append(big_cycle[0])
    cases.append(
        (
            "EQ-cycle-156",
            "Cycle with large string payload",
            big_cycle[0],
        ),
    )

    tup = (1,)
    lst_for_tup: list = [tup]
    tup = (lst_for_tup,)
    lst_for_tup.append(tup)
    cases.append(
        (
            "EQ-cycle-157",
            "Self-referential tuple (indirect)",
            tup,
        ),
    )

    repeat_cycle = []
    repeat_cycle.append(repeat_cycle)
    cases.append(
        (
            "EQ-cycle-158",
            "Repeated dumps of same cycle object",
            repeat_cycle,
        ),
    )

    return cases
