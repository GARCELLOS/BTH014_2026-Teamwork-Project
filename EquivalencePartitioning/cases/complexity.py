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
        ("COMPLEXITY-01", "Simple input - integer 1", 1),
        ("COMPLEXITY-02", "Medium mixed list", [1, "a", None, 3.14]),
        ("COMPLEXITY-03", "Empty complex structure", [[], {}, ()]),
        ("COMPLEXITY-04", "Nested list - 10 levels", make_nested_list(10)),
        ("COMPLEXITY-05", "Nested list - 50 levels", make_nested_list(50)),
        ("COMPLEXITY-06", "Nested list - 100 levels", make_nested_list(100)),
        ("COMPLEXITY-07", "Nested tuple - 10 levels", make_nested_tuple(10)),
        ("COMPLEXITY-08", "Nested tuple - 50 levels", make_nested_tuple(50)),
        ("COMPLEXITY-09", "Nested tuple - 100 levels", make_nested_tuple(100)),
        ("COMPLEXITY-10", "Nested dict - 10 levels", make_nested_dict(10)),
        ("COMPLEXITY-11", "Nested dict - 50 levels", make_nested_dict(50)),
        ("COMPLEXITY-12", "Nested dict - 100 levels", make_nested_dict(100)),
        ("COMPLEXITY-13", "Large list - range(1000)", list(range(1000))),
        ("COMPLEXITY-14", "Large list - range(10000)", list(range(10000))),
        ("COMPLEXITY-15", "Large list - range(50000)", list(range(50000))),
        ("COMPLEXITY-16", "Large tuple - range(1000)", tuple(range(1000))),
        ("COMPLEXITY-17", "Large tuple - range(10000)", tuple(range(10000))),
        ("COMPLEXITY-18", "Large tuple - range(50000)", tuple(range(50000))),
        (
            "COMPLEXITY-19",
            "Large dict - 1000 items",
            {f"key_{i}": i for i in range(1000)},
        ),
        (
            "COMPLEXITY-20",
            "Large dict - 10000 items",
            {f"key_{i}": i for i in range(10000)},
        ),
        (
            "COMPLEXITY-21",
            "Large dict - 50000 items",
            {f"key_{i}": i for i in range(50000)},
        ),
        ("COMPLEXITY-22", "Large set - range(1000)", set(range(1000))),
        ("COMPLEXITY-23", "Large set - range(10000)", set(range(10000))),
        ("COMPLEXITY-24", "Large frozenset - range(10000)", frozenset(range(10000))),
        ("COMPLEXITY-25", "Long normal string", "a" * 100000),
        ("COMPLEXITY-26", "Long Unicode string", "中文😀" * 10000),
        (
            "COMPLEXITY-27",
            "Large bytes - bytes(range(256)) * 1000",
            bytes(range(256)) * 1000,
        ),
        ("COMPLEXITY-28", "Large bytes - 1MB zero bytes", b"\x00" * (1024 * 1024)),
        ("COMPLEXITY-29", "Repeated reference list", repeated_reference),
        (
            "COMPLEXITY-30",
            "Mixed complex structure - 100 items",
            make_mixed_structure(100),
        ),
        (
            "COMPLEXITY-31",
            "Mixed complex structure - 1000 items",
            make_mixed_structure(1000),
        ),
        (
            "COMPLEXITY-32",
            "Complex dict - list values",
            {f"key_{i}": list(range(20)) for i in range(1000)},
        ),
        (
            "COMPLEXITY-33",
            "Complex dict - tuple values",
            {f"key_{i}": tuple(range(20)) for i in range(1000)},
        ),
        (
            "COMPLEXITY-34",
            "Complex list - dict elements",
            [{"id": i, "value": f"text_{i}"} for i in range(5000)],
        ),
    ]
