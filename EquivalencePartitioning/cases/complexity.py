from cases.builders import (
    make_mixed_structure,
    make_nested_dict,
    make_nested_list,
    make_nested_tuple,
)


def get_complexity_cases():
    cases = []

    shared_list = [1, 2, 3]
    repeated_reference = [shared_list, shared_list, shared_list]

    cases.append(
        (
            "EQ-complexity-065",
            "1: SHA-256 consistent after 1 serialization",
            1,
        )
    )

    cases.append(
        (
            "EQ-complexity-066",
            "[1, 'a', None, 3.14]: SHA-256 consistent after 1 serialization",
            [1, "a", None, 3.14],
        )
    )

    cases.append(
        (
            "EQ-complexity-067",
            "[[], {}, ()]: SHA-256 consistent after 1 serialization",
            [[], {}, ()],
        )
    )

    cases.append(
        (
            "EQ-complexity-068",
            "nested list depth 10: SHA-256 consistent after 1 serialization",
            make_nested_list(10),
        )
    )

    cases.append(
        (
            "EQ-complexity-069",
            "nested list depth 50: SHA-256 consistent after 1 serialization",
            make_nested_list(50),
        )
    )

    cases.append(
        (
            "EQ-complexity-070",
            "nested list depth 100: SHA-256 consistent after 1 serialization",
            make_nested_list(100),
        )
    )

    cases.append(
        (
            "EQ-complexity-071",
            "nested tuple depth 10: SHA-256 consistent after 1 serialization",
            make_nested_tuple(10),
        )
    )

    cases.append(
        (
            "EQ-complexity-072",
            "nested tuple depth 50: SHA-256 consistent after 1 serialization",
            make_nested_tuple(50),
        )
    )

    cases.append(
        (
            "EQ-complexity-073",
            "nested tuple depth 100:"
            "SHA-256 consistent after 1 serialization",
            make_nested_tuple(100),
        )
    )

    cases.append(
        (
            "EQ-complexity-074",
            "nested dict depth 10: SHA-256 consistent after 1 serialization",
            make_nested_dict(10),
        )
    )

    cases.append(
        (
            "EQ-complexity-075",
            "nested dict depth 50: SHA-256 consistent after 1 serialization",
            make_nested_dict(50),
        )
    )

    cases.append(
        (
            "EQ-complexity-076",
            "nested dict depth 100: SHA-256 consistent after 1 serialization",
            make_nested_dict(100),
        )
    )

    cases.append(
        (
            "EQ-complexity-077",
            "list(range(1000)): SHA-256 consistent after 1 serialization",
            list(range(1000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-078",
            "list(range(10000)): SHA-256 consistent after 1 serialization",
            list(range(10000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-079",
            "list(range(50000)): SHA-256 consistent after 1 serialization",
            list(range(50000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-080",
            "tuple(range(1000)): SHA-256 consistent after 1 serialization",
            tuple(range(1000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-081",
            "tuple(range(10000)): SHA-256 consistent after 1 serialization",
            tuple(range(10000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-082",
            "tuple(range(50000)): SHA-256 consistent after 1 serialization",
            tuple(range(50000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-083",
            "dict 1000 str-keyed items:"
            "SHA-256 consistent after 1 serialization",
            {f"key_{i}": i for i in range(1000)},
        )
    )

    cases.append(
        (
            "EQ-complexity-084",
            "dict 10000 str-keyed items:"
            "SHA-256 consistent after 1 serialization",
            {f"key_{i}": i for i in range(10000)},
        )
    )

    cases.append(
        (
            "EQ-complexity-085",
            "dict 50000 str-keyed items:"
            "SHA-256 consistent after 1 serialization",
            {f"key_{i}": i for i in range(50000)},
        )
    )

    cases.append(
        (
            "EQ-complexity-086",
            "set(range(1000)): SHA-256 consistent after 1 serialization",
            set(range(1000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-087",
            "set(range(10000)): SHA-256 consistent after 1 serialization",
            set(range(10000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-088",
            "frozenset(range(10000)):"
            "SHA-256 consistent after 1 serialization",
            frozenset(range(10000)),
        )
    )

    cases.append(
        (
            "EQ-complexity-089",
            '"a"*100000: SHA-256 consistent after 1 serialization',
            "a" * 100000,
        )
    )

    cases.append(
        (
            "EQ-complexity-090",
            '"中文😀"*10000: SHA-256 consistent after 1 serialization',
            "中文😀" * 10000,
        )
    )

    cases.append(
        (
            "EQ-complexity-091",
            "bytes(range(256))*1000:"
            "SHA-256 consistent after 1 serialization",
            bytes(range(256)) * 1000,
        )
    )

    cases.append(
        (
            "EQ-complexity-092",
            "1MB zero-bytes: SHA-256 consistent after 1 serialization",
            b"\x00" * (1024 * 1024),
        )
    )

    cases.append(
        (
            "EQ-complexity-093",
            "shared list repeated 3x:"
            "SHA-256 consistent after 1 serialization",
            repeated_reference,
        )
    )

    cases.append(
        (
            "EQ-complexity-094",
            "mixed structure 100 items:"
            "SHA-256 consistent after 1 serialization",
            make_mixed_structure(100),
        )
    )

    cases.append(
        (
            "EQ-complexity-095",
            "mixed structure 1000 items:"
            "SHA-256 consistent after 1 serialization",
            make_mixed_structure(1000),
        )
    )

    cases.append(
        (
            "EQ-complexity-096",
            "dict 1000 list-valued items:"
            "SHA-256 consistent after 1 serialization",
            {f"key_{i}": list(range(20)) for i in range(1000)},
        )
    )

    cases.append(
        (
            "EQ-complexity-097",
            "dict 1000 tuple-valued items:"
            "SHA-256 consistent after 1 serialization",
            {f"key_{i}": tuple(range(20)) for i in range(1000)},
        )
    )

    cases.append(
        (
            "EQ-complexity-098",
            "list 5000 dict elements:"
            "SHA-256 consistent after 1 serialization",
            [{"id": i, "value": f"text_{i}"} for i in range(5000)],
        )
    )

    return cases
