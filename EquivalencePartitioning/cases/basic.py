def get_basic_type_cases():
    cases = []

    cases.append(
        (
            "EQ-basic-001",
            "None: SHA-256 consistent after 10 serializations",
            None,
        )
    )

    cases.append(
        (
            "EQ-basic-002",
            "True: SHA-256 consistent after 10 serializations",
            True,
        )
    )

    cases.append(
        (
            "EQ-basic-003",
            "False: SHA-256 consistent after 10 serializations",
            False,
        )
    )

    cases.append(
        (
            "EQ-basic-004",
            "0: SHA-256 consistent after 10 serializations",
            0,
        )
    )

    cases.append(
        (
            "EQ-basic-005",
            "1: SHA-256 consistent after 10 serializations",
            1,
        )
    )

    cases.append(
        (
            "EQ-basic-006",
            "-1: SHA-256 consistent after 10 serializations",
            -1,
        )
    )

    cases.append(
        (
            "EQ-basic-007",
            "2**31: SHA-256 consistent after 10 serializations",
            2**31,
        )
    )

    cases.append(
        (
            "EQ-basic-008",
            "2**63: SHA-256 consistent after 10 serializations",
            2**63,
        )
    )

    cases.append(
        (
            "EQ-basic-009",
            "-2**63: SHA-256 consistent after 10 serializations",
            -(2**63),
        )
    )

    cases.append(
        (
            "EQ-basic-010",
            "2**100: SHA-256 consistent after 10 serializations",
            2**100,
        )
    )

    cases.append(
        (
            "EQ-basic-011",
            "-2**100: SHA-256 consistent after 10 serializations",
            -(2**100),
        )
    )

    cases.append(
        (
            "EQ-basic-012",
            '"hello": SHA-256 consistent after 10 serializations',
            "hello",
        )
    )

    cases.append(
        (
            "EQ-basic-013",
            '"" (empty): SHA-256 consistent after 10 serializations',
            "",
        )
    )

    cases.append(
        (
            "EQ-basic-014",
            '"a"*10000: SHA-256 consistent after 10 serializations',
            "a" * 10000,
        )
    )

    cases.append(
        (
            "EQ-basic-015",
            '"中文😀": SHA-256 consistent after 10 serializations',
            "中文😀",
        )
    )

    cases.append(
        (
            "EQ-basic-016",
            '"中文😀"*1000: SHA-256 consistent after 10 serializations',
            "中文😀" * 1000,
        )
    )

    cases.append(
        (
            "EQ-basic-017",
            "special-chars str: SHA-256 consistent after 10 serializations",
            '\n\t\r\\\'"',
        )
    )

    cases.append(
        (
            "EQ-basic-018",
            'b"abc": SHA-256 consistent after 10 serializations',
            b"abc",
        )
    )

    cases.append(
        (
            "EQ-basic-019",
            "bytes(range(256)): SHA-256 consistent after 10 serializations",
            bytes(range(256)),
        )
    )

    cases.append(
        (
            "EQ-basic-020",
            'b"": SHA-256 consistent after 10 serializations',
            b"",
        )
    )

    cases.append(
        (
            "EQ-basic-021",
            "1MB zero-bytes: SHA-256 consistent after 10 serializations",
            b"\x00" * (1024 * 1024),
        )
    )

    cases.append(
        (
            "EQ-basic-022",
            "0.0: SHA-256 consistent after 10 serializations",
            0.0,
        )
    )

    cases.append(
        (
            "EQ-basic-023",
            "3.14: SHA-256 consistent after 10 serializations",
            3.14,
        )
    )

    cases.append(
        (
            "EQ-basic-024",
            "-3.14: SHA-256 consistent after 10 serializations",
            -3.14,
        )
    )

    cases.append(
        (
            "EQ-basic-025",
            "1e-100: SHA-256 consistent after 10 serializations",
            1e-100,
        )
    )

    cases.append(
        (
            "EQ-basic-026",
            "1e100: SHA-256 consistent after 10 serializations",
            1e100,
        )
    )

    cases.append(
        (
            "EQ-basic-027",
            "1+2j: SHA-256 consistent after 10 serializations",
            1 + 2j,
        )
    )

    cases.append(
        (
            "EQ-basic-028",
            "0j: SHA-256 consistent after 10 serializations",
            0j,
        )
    )

    cases.append(
        (
            "EQ-basic-029",
            'bytearray(b"abc"): SHA-256 consistent after 10 serializations',
            bytearray(b"abc"),
        )
    )

    cases.append(
        (
            "EQ-basic-030",
            "bytearray(range(256)): "
            "SHA-256 consistent after 10 serializations",
            bytearray(range(256)),
        )
    )

    cases.append(
        (
            "EQ-basic-031",
            "bytearray(): SHA-256 consistent after 10 serializations",
            bytearray(),
        )
    )

    cases.append(
        (
            "EQ-basic-032",
            "Ellipsis: SHA-256 consistent after 10 serializations",
            Ellipsis,
        )
    )

    cases.append(
        (
            "EQ-basic-033",
            "StopIteration: SHA-256 consistent after 10 serializations",
            StopIteration,
        )
    )

    return cases
