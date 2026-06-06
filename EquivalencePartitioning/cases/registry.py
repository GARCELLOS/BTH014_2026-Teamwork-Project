from cases.basic import get_basic_type_cases
from cases.code import get_code_cases
from cases.complexity import get_complexity_cases
from cases.container import get_container_type_cases
from cases.structure import get_cycle_cases, get_nested_cases

CASE_GROUPS = {
    "basic": {
        "getter": get_basic_type_cases,
        "title": "basic type",
        "result_prefix": "basic_type",
    },
    "container": {
        "getter": get_container_type_cases,
        "title": "container type",
        "result_prefix": "container_type",
    },
    "complexity": {
        "getter": get_complexity_cases,
        "title": "complexity",
        "result_prefix": "complexity",
    },
    "code": {
        "getter": get_code_cases,
        "title": "code object",
        "result_prefix": "code",
    },
    "nested": {
        "getter": get_nested_cases,
        "title": "nested structure",
        "result_prefix": "nested",
    },
    "cycle": {
        "getter": get_cycle_cases,
        "title": "circular reference",
        "result_prefix": "cycle",
    },
}

CASE_GROUP_ORDER = (
    "basic", "container", "complexity", "code", "nested", "cycle",
)


def iter_case_groups():
    """按注册顺序遍历用例组。"""
    for key in CASE_GROUP_ORDER:
        yield key, CASE_GROUPS[key]


def count_cases():
    """返回各组用例数量与总数。"""
    per_group = {
        key: len(group["getter"]())
        for key, group in CASE_GROUPS.items()
    }
    return per_group, sum(per_group.values())


def collect_all_version_cases():
    cases = []
    for group_key, group in iter_case_groups():
        for test_id, name, value in group["getter"]():
            cases.append((group_key, test_id, name, value))
    return cases
