def get_container_type_cases():
    cases = []

    cases.append(
        (
            "EQ-container-034",
            "[]: SHA-256 consistent after 10 serializations",
            [],
        )
    )

    cases.append(
        (
            "EQ-container-035",
            "(): SHA-256 consistent after 10 serializations",
            (),
        )
    )

    cases.append(
        (
            "EQ-container-036",
            "{}: SHA-256 consistent after 10 serializations",
            {},
        )
    )

    cases.append(
        (
            "EQ-container-037",
            "set(): SHA-256 consistent after 10 serializations",
            set(),
        )
    )

    cases.append(
        (
            "EQ-container-038",
            "frozenset(): SHA-256 consistent after 10 serializations",
            frozenset(),
        )
    )

    cases.append(
        (
            "EQ-container-039",
            "[1, 2, 3]: SHA-256 consistent after 10 serializations",
            [1, 2, 3],
        )
    )

    cases.append(
        (
            "EQ-container-040",
            "(1, 2, 3): SHA-256 consistent after 10 serializations",
            (1, 2, 3),
        )
    )

    cases.append(
        (
            "EQ-container-041",
            "{'a': 1, 'b': 2}: SHA-256 consistent after 10 serializations",
            {'a': 1, 'b': 2},
        )
    )

    cases.append(
        (
            "EQ-container-042",
            "{1, 2, 3}: SHA-256 consistent after 10 serializations",
            {1, 2, 3},
        )
    )

    cases.append(
        (
            "EQ-container-043",
            "frozenset({1, 2, 3}): SHA-256 consistent after 10 serializations",
            frozenset({1, 2, 3}),
        )
    )

    cases.append(
        (
            "EQ-container-044",
            "[1, 'a', None, True, 3.14, b'abc']:"
            "SHA-256 consistent after 10 serializations",
            [1, 'a', None, True, 3.14, b'abc'],
        )
    )

    cases.append(
        (
            "EQ-container-045",
            "(1, 'a', None, True, 3.14, b'abc'):"
            "SHA-256 consistent after 10 serializations",
            (1, 'a', None, True, 3.14, b'abc'),
        )
    )

    cases.append(
        (
            "EQ-container-046",
            "{'int': 1, 'str': 'a', 'none': None, 'bool': True}:"
            "SHA-256 consistent after 10 serializations",
            {'int': 1, 'str': 'a', 'none': None, 'bool': True},
        )
    )

    cases.append(
        (
            "EQ-container-047",
            "[{a:1}, {b:2}, {c:3}]: "
            "SHA-256 consistent after 10 serializations",
            [{"a": 1}, {"b": 2}, {"c": 3}],
        )
    )

    cases.append(
        (
            "EQ-container-048",
            "{numbers: [1,2,3], letters: [a,b,c]}:"
            "SHA-256 consistent after 10 serializations",
            {"numbers": [1, 2, 3], "letters": ["a", "b", "c"]},
        )
    )

    cases.append(
        (
            "EQ-container-049",
            "[(1,2), (3,4), (5,6)]: "
            "SHA-256 consistent after 10 serializations",
            [(1, 2), (3, 4), (5, 6)],
        )
    )

    cases.append(
        (
            "EQ-container-050",
            "([1,2], [3,4], [5,6]): "
            "SHA-256 consistent after 10 serializations",
            ([1, 2], [3, 4], [5, 6]),
        )
    )

    cases.append(
        (
            "EQ-container-051",
            "{point: (10,20), color: (255,255,255)}:"
            "SHA-256 consistent after 10 serializations",
            {"point": (10, 20), "color": (255, 255, 255)},
        )
    )

    cases.append(
        (
            "EQ-container-052",
            "{'values': {1, 2, 3}}: "
            "SHA-256 consistent after 10 serializations",
            {"values": {1, 2, 3}},
        )
    )

    cases.append(
        (
            "EQ-container-053",
            "[{1,2}, {3,4}, {5,6}]: "
            "SHA-256 consistent after 10 serializations",
            [{1, 2}, {3, 4}, {5, 6}],
        )
    )

    cases.append(
        (
            "EQ-container-054",
            "[{items: [1,2,3]}, {items: [4,5,6]}]:"
            "SHA-256 consistent after 10 serializations",
            [{"items": [1, 2, 3]}, {"items": [4, 5, 6]}],
        )
    )

    cases.append(
        (
            "EQ-container-055",
            "{user: {id:1, roles:(admin,tester)}}:"
            "SHA-256 consistent after 10 serializations",
            {"user": {"id": 1, "roles": ("admin", "tester")}},
        )
    )

    cases.append(
        (
            "EQ-container-056",
            "[1,1,1,a,a,None,None]: "
            "SHA-256 consistent after 10 serializations",
            [1, 1, 1, "a", "a", None, None],
        )
    )

    cases.append(
        (
            "EQ-container-057",
            "{1:one, 2:two, 3:three}:"
            "SHA-256 consistent after 10 serializations",
            {1: "one", 2: "two", 3: "three"},
        )
    )

    cases.append(
        (
            "EQ-container-058",
            "{a:1, 2:b, (3,4):tuple_key}:"
            "SHA-256 consistent after 10 serializations",
            {"a": 1, 2: "b", (3, 4): "tuple_key"},
        )
    )

    cases.append(
        (
            "EQ-container-059",
            "slice(1, 10, 2): SHA-256 consistent after 10 serializations",
            slice(1, 10, 2),
        )
    )

    cases.append(
        (
            "EQ-container-060",
            "slice(None, 10, None): "
            "SHA-256 consistent after 10 serializations",
            slice(None, 10, None),
        )
    )

    cases.append(
        (
            "EQ-container-061",
            "slice(None, None, -1): "
            "SHA-256 consistent after 10 serializations",
            slice(None, None, -1),
        )
    )

    cases.append(
        (
            "EQ-container-062",
            "[slice(1,5), slice(None,None,-1)]:"
            "SHA-256 consistent after 10 serializations",
            [slice(1, 5), slice(None, None, -1)],
        )
    )

    cases.append(
        (
            "EQ-container-063",
            "(slice(0,10), slice(None,None,-1)):"
            "SHA-256 consistent after 10 serializations",
            (slice(0, 10), slice(None, None, -1)),
        )
    )

    cases.append(
        (
            "EQ-container-064",
            "{range: slice(1,10,2)}:"
            "SHA-256 consistent after 10 serializations",
            {"range": slice(1, 10, 2)},
        )
    )

    return cases
