"""嵌套结构与循环引用用例。"""

from cases.builders import make_nested_list


def get_nested_cases():
    cases = []

    cases.append(("NEST-01", "Simple nested list", [[1, 2], [3, 4]]))
    cases.append(("NEST-02", "Nested dict", {"a": {"b": {"c": 1}}}))
    cases.append(
        (
            "NEST-03",
            "Mixed nested list/dict/tuple/None",
            [{"a": [1, 2, 3]}, ("x", None)],
        )
    )
    cases.append(
        (
            "NEST-04",
            "Nested with float special values",
            {"value": [1.0, float("inf"), float("nan")]},
        )
    )
    cases.append(("NEST-05", "Deep nested list depth 5", [[[[[1]]]]]))
    cases.append(("NEST-06", "List containing tuple", [1, (2, 3), 4]))
    cases.append(("NEST-07", "Tuple containing list", (1, [2, 3], 4)))
    cases.append(
        (
            "NEST-08",
            "Dict containing list and tuple",
            {"list": [1, 2], "tuple": (3, 4)},
        )
    )
    cases.append(("NEST-09", "Dict containing set", {"s": {1, 2, 3}}))
    cases.append(
        ("NEST-10", "List containing frozenset", [frozenset([1, 2, 3])])
    )
    cases.append(("NEST-11", "Empty nested containers", [[], {}, (), set()]))
    cases.append(
        (
            "NEST-12",
            "Complex mixed nested structure",
            {"a": [1, {"b": (None, True, 3.14)}]},
        )
    )
    cases.append(
        (
            "NEST-13",
            "Deep nested list depth 500 (within limit)",
            make_nested_list(500),
        )
    )
    cases.append(
        (
            "NEST-14",
            "Deep nested list depth 1999 (near limit)",
            make_nested_list(1999),
        )
    )
    cases.append(
        (
            "NEST-15",
            "Deep nested list depth 2001 (exceed limit, expect RecursionError)",
            make_nested_list(2001),
        )
    )
    cases.append(("NEST-16", "Large list 100000 elements", [0] * 100000))
    cases.append(
        ("NEST-17", "Large dict 100000 integer keys", {i: i for i in range(100000)})
    )
    cases.append(("NEST-18", "Large set 100000 integers", set(range(100000))))
    cases.append(("NEST-19", "Large tuple 100000 integers", tuple(range(100000))))

    shared = [1, 2, 3]
    cases.append(
        (
            "NEST-20",
            "Shared reference list (same object repeated)",
            [shared, shared, shared],
        )
    )
    shared_dict = {"a": 1}
    cases.append(
        (
            "NEST-21",
            "Shared reference dict",
            {"first": shared_dict, "second": shared_dict},
        )
    )

    huge_str = "x" * (1024 * 1024)
    cases.append(
        ("NEST-22", "Nested list containing huge string", [huge_str, [huge_str]])
    )
    huge_bytes = b"y" * (1024 * 1024)
    cases.append(
        ("NEST-23", "Nested list containing huge bytes", [huge_bytes, [huge_bytes]])
    )
    cases.append(
        (
            "NEST-24",
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
    cases.append(("CYCLE-01", "Self-referential list", self_list))

    self_dict = {}
    self_dict["self"] = self_dict
    cases.append(("CYCLE-02", "Self-referential dict", self_dict))

    a = []
    b = [a]
    a.append(b)
    cases.append(("CYCLE-03", "Indirect circular reference (list->list)", a))

    ld = []
    d = {"ref": ld}
    ld.append(d)
    cases.append(("CYCLE-04", "List and dict mutual reference", ld))

    d2 = {}
    a2 = [d2]
    d2["list"] = a2
    cases.append(("CYCLE-05", "Dict and list mutual reference (reverse)", d2))

    a3 = []
    b3 = [1, 2, a3]
    a3.append(b3)
    cases.append(("CYCLE-06", "Nested list with cycle", a3))

    x = [1, 2]
    a4 = [x, x]
    cases.append(("CYCLE-07", "Repeated reference without cycle", a4))

    a5 = []
    b5 = [a5]
    c5 = [b5]
    a5.append(c5)
    cases.append(("CYCLE-08", "Deep indirect cycle (3 levels)", a5))

    cases.append(("CYCLE-09", "Deep cycle length 10", _make_cycle_list(10)))

    shared_node = []
    cycle_a = [shared_node]
    cycle_b = [shared_node]
    shared_node.append(cycle_a)
    shared_node.append(cycle_b)
    cases.append(("CYCLE-10", "Multiple cycles sharing a node", shared_node))

    nan_cycle = []
    inf_cycle = []
    nan_cycle.append(inf_cycle)
    inf_cycle.append(nan_cycle)
    nan_cycle.insert(0, float("nan"))
    inf_cycle.insert(0, float("inf"))
    cases.append(("CYCLE-11", "Cycle with NaN and Inf", nan_cycle))

    big_cycle = []
    big_str = "big" * 100000
    for _ in range(3):
        node = [big_str]
        big_cycle.append(node)
    big_cycle[-1].append(big_cycle[0])
    cases.append(("CYCLE-12", "Cycle with large string payload", big_cycle[0]))

    tup = (1,)
    lst_for_tup = [tup]
    tup = (lst_for_tup,)
    lst_for_tup.append(tup)
    cases.append(("CYCLE-13", "Self-referential tuple (indirect)", tup))

    repeat_cycle = []
    repeat_cycle.append(repeat_cycle)
    cases.append(("CYCLE-14", "Repeated dumps of same cycle object", repeat_cycle))

    return cases
