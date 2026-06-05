"""构造复杂测试输入的辅助函数。"""


def make_nested_list(depth):
    value = 1
    for _ in range(depth):
        value = [value]
    return value


def make_nested_tuple(depth):
    value = 1
    for _ in range(depth):
        value = (value,)
    return value


def make_nested_dict(depth):
    value = 1
    for i in range(depth):
        value = {f"level_{i}": value}
    return value


def make_mixed_structure(size):
    return [
        {
            "id": i,
            "name": f"item_{i}",
            "active": i % 2 == 0,
            "score": i + 0.5,
            "data": [i, i + 1, i + 2],
            "extra": {
                "none": None,
                "bytes": bytes([i % 256]),
                "tuple": (i, str(i), False),
            },
        }
        for i in range(size)
    ]
