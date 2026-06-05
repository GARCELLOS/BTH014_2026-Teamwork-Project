from cases.basic import get_basic_type_cases
from cases.code import get_code_cases
from cases.complexity import get_complexity_cases
from cases.container import get_container_type_cases
from cases.structure import get_cycle_cases, get_nested_cases


def _group(getter, key, title, result_prefix, finish_message):
    return key, {
        "getter": getter,
        "title": title,
        "result_prefix": result_prefix,
        "finish_message": finish_message,
    }


_CASE_SPECS = [
    _group(
        get_basic_type_cases,
        "basic",
        "basic type",
        "basic_type",
        "Basic type marshal tests finished.",
    ),
    _group(
        get_container_type_cases,
        "container",
        "container type",
        "container_type",
        "Container type marshal tests finished.",
    ),
    _group(
        get_complexity_cases,
        "complexity",
        "complexity",
        "complexity",
        "Complexity marshal tests finished.",
    ),
    _group(
        get_code_cases,
        "code",
        "code object",
        "code",
        "Code object marshal tests finished.",
    ),
    _group(
        get_nested_cases,
        "nested",
        "nested structure",
        "nested",
        "Nested structure marshal tests finished.",
    ),
    _group(
        get_cycle_cases,
        "cycle",
        "circular reference",
        "cycle",
        "Circular reference marshal tests finished.",
    ),
]

CASE_GROUPS = dict(_CASE_SPECS)
CASE_GROUP_ORDER = tuple(key for key, _ in _CASE_SPECS)


def iter_case_groups():
    """按注册顺序遍历用例组。"""
    for key in CASE_GROUP_ORDER:
        yield key, CASE_GROUPS[key]


def count_cases():
    """返回各组用例数量与总数。"""
    per_group = {key: len(group["getter"]()) for key, group in CASE_GROUPS.items()}
    return per_group, sum(per_group.values())


def collect_all_version_cases():
    cases = []
    for group_key, group in iter_case_groups():
        for test_id, name, value in group["getter"]():
            cases.append((group_key, test_id, name, value))
    return cases
