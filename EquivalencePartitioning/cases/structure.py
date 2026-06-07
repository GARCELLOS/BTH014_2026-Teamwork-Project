"""嵌套结构与循环引用用例。"""

from cases.builders import make_nested_list


def get_nested_cases():
    cases = []

    shared = [1, 2, 3]
    shared_dict = {"a": 1}
    huge_str = "x" * (1024 * 1024)
    huge_bytes = b"y" * (1024 * 1024)

    cases.append(
        (
            "EQ-nested-121",
            "[[1,2], [3,4]]: "
            "SHA-256 consistent after 1 serialization",
            [[1, 2], [3, 4]],
        )
    )

    cases.append(
        (
            "EQ-nested-122",
            "{a: {b: {c: 1}}}: "
            "SHA-256 consistent after 1 serialization",
            {"a": {"b": {"c": 1}}},
        )
    )

    cases.append(
        (
            "EQ-nested-123",
            "[{a: [1,2,3]}, (x, None)]: "
            "SHA-256 consistent after 1 serialization",
            [{"a": [1, 2, 3]}, ("x", None)],
        )
    )

    cases.append(
        (
            "EQ-nested-124",
            "{value: [1.0, inf, nan]}: "
            "SHA-256 consistent after 1 serialization",
            {"value": [1.0, float("inf"), float("nan")]},
        )
    )

    cases.append(
        (
            "EQ-nested-125",
            "nested list depth 5: "
            "SHA-256 consistent after 1 serialization",
            [[[[[1]]]]],
        )
    )

    cases.append(
        (
            "EQ-nested-126",
            "[1, (2,3), 4]: "
            "SHA-256 consistent after 1 serialization",
            [1, (2, 3), 4],
        )
    )

    cases.append(
        (
            "EQ-nested-127",
            "(1, [2,3], 4): "
            "SHA-256 consistent after 1 serialization",
            (1, [2, 3], 4),
        )
    )

    cases.append(
        (
            "EQ-nested-128",
            "{list: [1,2], tuple: (3,4)}: "
            "SHA-256 consistent after 1 serialization",
            {"list": [1, 2], "tuple": (3, 4)},
        )
    )

    cases.append(
        (
            "EQ-nested-129",
            "{s: {1,2,3}}: "
            "SHA-256 consistent after 1 serialization",
            {"s": {1, 2, 3}},
        )
    )

    cases.append(
        (
            "EQ-nested-130",
            "[frozenset({1,2,3})]: "
            "SHA-256 consistent after 1 serialization",
            [frozenset([1, 2, 3])],
        )
    )

    cases.append(
        (
            "EQ-nested-131",
            "[[], {}, (), set()]: "
            "SHA-256 consistent after 1 serialization",
            [[], {}, (), set()],
        )
    )

    cases.append(
        (
            "EQ-nested-132",
            "{a: [1, {b: (None,True,3.14)}]}: "
            "SHA-256 consistent after 1 serialization",
            {"a": [1, {"b": (None, True, 3.14)}]},
        )
    )

    cases.append(
        (
            "EQ-nested-133",
            "nested list depth 500: "
            "SHA-256 consistent after 1 serialization",
            make_nested_list(500),
        )
    )

    cases.append(
        (
            "EQ-nested-134",
            "nested list depth 1999: "
            "SHA-256 consistent after 1 serialization",
            make_nested_list(1999),
        )
    )

    cases.append(
        (
            "EQ-nested-135",
            "nested list depth 2001 (expect RecursionError): "
            "SHA-256 consistent after 1 serialization",
            make_nested_list(2001),
        )
    )

    cases.append(
        (
            "EQ-nested-136",
            "list 100000 elements: "
            "SHA-256 consistent after 1 serialization",
            [0] * 100000,
        )
    )

    cases.append(
        (
            "EQ-nested-137",
            "dict 100000 int keys: "
            "SHA-256 consistent after 1 serialization",
            {i: i for i in range(100000)},
        )
    )

    cases.append(
        (
            "EQ-nested-138",
            "set 100000 ints: "
            "SHA-256 consistent after 1 serialization",
            set(range(100000)),
        )
    )

    cases.append(
        (
            "EQ-nested-139",
            "tuple 100000 ints: "
            "SHA-256 consistent after 1 serialization",
            tuple(range(100000)),
        )
    )

    cases.append(
        (
            "EQ-nested-140",
            "shared list repeated 3x: "
            "SHA-256 consistent after 1 serialization",
            [shared, shared, shared],
        )
    )

    cases.append(
        (
            "EQ-nested-141",
            "shared dict in two keys: "
            "SHA-256 consistent after 1 serialization",
            {"first": shared_dict, "second": shared_dict},
        )
    )

    cases.append(
        (
            "EQ-nested-142",
            "nested list with 1MB str: "
            "SHA-256 consistent after 1 serialization",
            [huge_str, [huge_str]],
        )
    )

    cases.append(
        (
            "EQ-nested-143",
            "nested list with 1MB bytes: "
            "SHA-256 consistent after 1 serialization",
            [huge_bytes, [huge_bytes]],
        )
    )

    cases.append(
        (
            "EQ-nested-144",
            "[frozenset({1,2,3}), frozenset({3,2,1})]: "
            "SHA-256 consistent after 1 serialization",
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
        (
            "EQ-cycle-145",
            "self-ref list: "
            "SHA-256 consistent after 1 serialization",
            self_list,
        )
    )

    self_dict = {}
    self_dict["self"] = self_dict
    cases.append(
        (
            "EQ-cycle-146",
            "self-ref dict: "
            "SHA-256 consistent after 1 serialization",
            self_dict,
        )
    )

    a = []
    b = [a]
    a.append(b)
    cases.append(
        (
            "EQ-cycle-147",
            "indirect cycle list->list: "
            "SHA-256 consistent after 1 serialization",
            a,
        )
    )

    ld = []
    d = {"ref": ld}
    ld.append(d)
    cases.append(
        (
            "EQ-cycle-148",
            "mutual ref list<->dict: "
            "SHA-256 consistent after 1 serialization",
            ld,
        )
    )

    d2 = {}
    a2 = [d2]
    d2["list"] = a2
    cases.append(
        (
            "EQ-cycle-149",
            "mutual ref dict<->list: "
            "SHA-256 consistent after 1 serialization",
            d2,
        )
    )

    a3 = []
    b3 = [1, 2, a3]
    a3.append(b3)
    cases.append(
        (
            "EQ-cycle-150",
            "nested list with cycle: "
            "SHA-256 consistent after 1 serialization",
            a3,
        )
    )

    x = [1, 2]
    a4 = [x, x]
    cases.append(
        (
            "EQ-cycle-151",
            "repeated ref no cycle: "
            "SHA-256 consistent after 1 serialization",
            a4,
        )
    )

    a5 = []
    b5 = [a5]
    c5 = [b5]
    a5.append(c5)
    cases.append(
        (
            "EQ-cycle-152",
            "indirect cycle 3 levels: "
            "SHA-256 consistent after 1 serialization",
            a5,
        )
    )

    cases.append(
        (
            "EQ-cycle-153",
            "cycle length 10: "
            "SHA-256 consistent after 1 serialization",
            _make_cycle_list(10),
        )
    )

    shared_node = []
    cycle_a = [shared_node]
    cycle_b = [shared_node]
    shared_node.append(cycle_a)
    shared_node.append(cycle_b)
    cases.append(
        (
            "EQ-cycle-154",
            "multiple cycles sharing node: "
            "SHA-256 consistent after 1 serialization",
            shared_node,
        )
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
            "cycle with NaN and Inf: "
            "SHA-256 consistent after 1 serialization",
            nan_cycle,
        )
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
            "cycle with large str payload: "
            "SHA-256 consistent after 1 serialization",
            big_cycle[0],
        )
    )

    tup = (1,)
    lst_for_tup: list = [tup]
    tup = (lst_for_tup,)
    lst_for_tup.append(tup)
    cases.append(
        (
            "EQ-cycle-157",
            "self-ref tuple indirect: "
            "SHA-256 consistent after 1 serialization",
            tup,
        )
    )

    repeat_cycle = []
    repeat_cycle.append(repeat_cycle)
    cases.append(
        (
            "EQ-cycle-158",
            "repeated dumps same cycle: "
            "SHA-256 consistent after 1 serialization",
            repeat_cycle,
        )
    )

    return cases
