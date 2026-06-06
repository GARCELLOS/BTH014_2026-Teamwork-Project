def get_container_type_cases():
    return [
        ("EQ-container-034", "Empty list", []),
        ("EQ-container-035", "Empty tuple", ()),
        ("EQ-container-036", "Empty dict", {}),
        ("EQ-container-037", "Empty set", set()),
        ("EQ-container-038", "Empty frozenset", frozenset()),
        ("EQ-container-039", "Simple list - [1, 2, 3]", [1, 2, 3]),
        (
            "EQ-container-040",
            "Simple tuple - (1, 2, 3)",
            (1, 2, 3),
        ),
        (
            "EQ-container-041",
            "Simple dict - {'a': 1, 'b': 2}",
            {"a": 1, "b": 2},
        ),
        (
            "EQ-container-042",
            "Simple set - {1, 2, 3}",
            {1, 2, 3},
        ),
        (
            "EQ-container-043",
            "Simple frozenset - {1, 2, 3}",
            frozenset({1, 2, 3}),
        ),
        (
            "EQ-container-044",
            "Mixed list",
            [1, "a", None, True, 3.14, b"abc"],
        ),
        (
            "EQ-container-045",
            "Mixed tuple",
            (1, "a", None, True, 3.14, b"abc"),
        ),
        (
            "EQ-container-046",
            "Mixed dict",
            {"int": 1, "str": "a", "none": None, "bool": True},
        ),
        (
            "EQ-container-047",
            "List containing dict",
            [{"a": 1}, {"b": 2}, {"c": 3}],
        ),
        (
            "EQ-container-048",
            "Dict containing list",
            {"numbers": [1, 2, 3], "letters": ["a", "b", "c"]},
        ),
        (
            "EQ-container-049",
            "List containing tuple",
            [(1, 2), (3, 4), (5, 6)],
        ),
        (
            "EQ-container-050",
            "Tuple containing list",
            ([1, 2], [3, 4], [5, 6]),
        ),
        (
            "EQ-container-051",
            "Dict containing tuple",
            {"point": (10, 20), "color": (255, 255, 255)},
        ),
        (
            "EQ-container-052",
            "Dict containing set",
            {"values": {1, 2, 3}},
        ),
        (
            "EQ-container-053",
            "List containing set",
            [{1, 2}, {3, 4}, {5, 6}],
        ),
        (
            "EQ-container-054",
            "Nested list and dict",
            [{"items": [1, 2, 3]}, {"items": [4, 5, 6]}],
        ),
        (
            "EQ-container-055",
            "Nested dict and tuple",
            {"user": {"id": 1, "roles": ("admin", "tester")}},
        ),
        (
            "EQ-container-056",
            "Repeated values in list",
            [1, 1, 1, "a", "a", None, None],
        ),
        (
            "EQ-container-057",
            "Dict with integer keys",
            {1: "one", 2: "two", 3: "three"},
        ),
        (
            "EQ-container-058",
            "Dict with mixed keys",
            {"a": 1, 2: "b", (3, 4): "tuple_key"},
        ),
        (
            "EQ-container-059",
            "Slice - slice(1, 10, 2)",
            slice(1, 10, 2),
        ),
        (
            "EQ-container-060",
            "Slice - slice(None, 10, None)",
            slice(None, 10, None),
        ),
        (
            "EQ-container-061",
            "Slice - slice(None, None, -1)",
            slice(None, None, -1),
        ),
        (
            "EQ-container-062",
            "List containing slice",
            [slice(1, 5), slice(None, None, -1)],
        ),
        (
            "EQ-container-063",
            "Tuple containing slice",
            (slice(0, 10), slice(None, None, -1)),
        ),
        (
            "EQ-container-064",
            "Dict containing slice value",
            {"range": slice(1, 10, 2)},
        ),
    ]
