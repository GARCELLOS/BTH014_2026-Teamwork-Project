"""构造复杂测试输入的辅助函数。"""


def make_nested(container_type, depth):
    """Build a deeply nested container of the given type.

    Args:
        container_type: list, tuple, or dict.
        depth: Nesting depth (>= 0).

    Returns:
        A nested structure of the requested depth.
    """
    value = 1
    if container_type is list:
        for _ in range(depth):
            value = [value]
    elif container_type is tuple:
        for _ in range(depth):
            value = (value,)
    elif container_type is dict:
        for i in range(depth):
            value = {f"level_{i}": value}
    else:
        raise TypeError(f"Unsupported container type: {container_type}")
    return value


def make_nested_list(depth):
    return make_nested(list, depth)


def make_nested_tuple(depth):
    return make_nested(tuple, depth)


def make_nested_dict(depth):
    return make_nested(dict, depth)


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
