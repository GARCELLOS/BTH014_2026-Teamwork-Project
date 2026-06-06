from cases.builders import (
    make_mixed_structure,
    make_nested_dict,
    make_nested_list,
    make_nested_tuple,
)


def get_complexity_cases():
    shared_list = [1, 2, 3]
    repeated_reference = [shared_list, shared_list, shared_list]

    return [
        ("EQ-complexity-065", "Simple input - integer 1", 1),
        ("EQ-complexity-066", "Medium mixed list", [1, "a", None, 3.14]),
        ("EQ-complexity-067", "Empty complex structure", [[], {}, ()]),
        ("EQ-complexity-068", "Nested list - 10 levels", make_nested_list(10)),
        ("EQ-complexity-069", "Nested list - 50 levels", make_nested_list(50)),
        (
            "EQ-complexity-070",
            "Nested list - 100 levels",
            make_nested_list(100),
        ),
        (
            "EQ-complexity-071",
            "Nested tuple - 10 levels",
            make_nested_tuple(10),
        ),
        (
            "EQ-complexity-072",
            "Nested tuple - 50 levels",
            make_nested_tuple(50),
        ),
        (
            "EQ-complexity-073",
            "Nested tuple - 100 levels",
            make_nested_tuple(100),
        ),
        (
            "EQ-complexity-074",
            "Nested dict - 10 levels",
            make_nested_dict(10),
        ),
        (
            "EQ-complexity-075",
            "Nested dict - 50 levels",
            make_nested_dict(50),
        ),
        (
            "EQ-complexity-076",
            "Nested dict - 100 levels",
            make_nested_dict(100),
        ),
        (
            "EQ-complexity-077",
            "Large list - range(1000)",
            list(range(1000)),
        ),
        (
            "EQ-complexity-078",
            "Large list - range(10000)",
            list(range(10000)),
        ),
        (
            "EQ-complexity-079",
            "Large list - range(50000)",
            list(range(50000)),
        ),
        (
            "EQ-complexity-080",
            "Large tuple - range(1000)",
            tuple(range(1000)),
        ),
        (
            "EQ-complexity-081",
            "Large tuple - range(10000)",
            tuple(range(10000)),
        ),
        (
            "EQ-complexity-082",
            "Large tuple - range(50000)",
            tuple(range(50000)),
        ),
        (
            "EQ-complexity-083",
            "Large dict - 1000 items",
            {f"key_{i}": i for i in range(1000)},
        ),
        (
            "EQ-complexity-084",
            "Large dict - 10000 items",
            {f"key_{i}": i for i in range(10000)},
        ),
        (
            "EQ-complexity-085",
            "Large dict - 50000 items",
            {f"key_{i}": i for i in range(50000)},
        ),
        ("EQ-complexity-086", "Large set - range(1000)", set(range(1000))),
        ("EQ-complexity-087", "Large set - range(10000)", set(range(10000))),
        (
            "EQ-complexity-088",
            "Large frozenset - range(10000)",
            frozenset(range(10000)),
        ),
        (
            "EQ-complexity-089",
            "Long normal string",
            "a" * 100000,
        ),
        (
            "EQ-complexity-090",
            "Long Unicode string",
            "中文😀" * 10000,
        ),
        (
            "EQ-complexity-091",
            "Large bytes - bytes(range(256)) * 1000",
            bytes(range(256)) * 1000,
        ),
        (
            "EQ-complexity-092",
            "Large bytes - 1MB zero bytes",
            b"\x00" * (1024 * 1024),
        ),
        ("EQ-complexity-093", "Repeated reference list", repeated_reference),
        (
            "EQ-complexity-094",
            "Mixed complex structure - 100 items",
            make_mixed_structure(100),
        ),
        (
            "EQ-complexity-095",
            "Mixed complex structure - 1000 items",
            make_mixed_structure(1000),
        ),
        (
            "EQ-complexity-096",
            "Complex dict - list values",
            {f"key_{i}": list(range(20)) for i in range(1000)},
        ),
        (
            "EQ-complexity-097",
            "Complex dict - tuple values",
            {f"key_{i}": tuple(range(20)) for i in range(1000)},
        ),
        (
            "EQ-complexity-098",
            "Complex list - dict elements",
            [{"id": i, "value": f"text_{i}"} for i in range(5000)],
        ),
    ]
