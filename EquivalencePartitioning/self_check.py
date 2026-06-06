"""提交前自检：编译、注册表、判定逻辑、过滤与汇总。"""

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EXPECTED_CASE_COUNTS = {
    "basic": 33,
    "container": 31,
    "complexity": 34,
    "code": 22,
    "nested": 24,
    "cycle": 14,
}
TOTAL_CASES = 158
GROUP_METADATA_KEYS = {"getter", "title", "result_prefix"}


def check_compile():
    import py_compile

    paths = [
        ROOT / "config.py",
        ROOT / "run_marshal_tests.py",
        ROOT / "self_check.py",
    ]
    paths.extend((ROOT / "cases").glob("*.py"))
    paths.extend((ROOT / "core").glob("*.py"))
    for path in paths:
        py_compile.compile(str(path), doraise=True)
    print(f"OK compile: {len(paths)} files")


def check_required_layout():
    from config import REQUIRED_PROJECT_DIRS, REQUIRED_PROJECT_FILES

    for name in REQUIRED_PROJECT_FILES:
        assert (ROOT / name).is_file(), f"missing required file: {name}"
    for name in REQUIRED_PROJECT_DIRS:
        assert (ROOT / name).is_dir(), f"missing required dir: {name}"

    expected = {
        "__init__.py", "registry.py", "basic.py", "container.py",
        "complexity.py", "code.py", "structure.py", "builders.py",
    }
    actual = {p.name for p in (ROOT / "cases").glob("*.py")}
    missing = expected - actual
    extra = actual - expected
    assert not missing, f"missing cases files: {missing}"
    assert not extra, f"unexpected cases files: {extra}"
    print("OK project layout")


def check_registry():
    from cases import (
        CASE_GROUP_ORDER, CASE_GROUPS,
        collect_all_version_cases, count_cases,
    )
    from config import HEAVY_CASE_GROUPS

    # 结构完整性
    assert tuple(CASE_GROUPS.keys()) == CASE_GROUP_ORDER
    assert len(CASE_GROUP_ORDER) == 6

    # 每个组的元数据只包含预期字段（不允许残留 finish_message 等）
    for key in CASE_GROUP_ORDER:
        group = CASE_GROUPS[key]
        actual_keys = set(group.keys())
        assert actual_keys == GROUP_METADATA_KEYS, (
            f"{key}: unexpected metadata keys "
            f"(got {actual_keys - GROUP_METADATA_KEYS}, "
            f"missing {GROUP_METADATA_KEYS - actual_keys})"
        )
        assert callable(group["getter"]), f"{key}: getter is not callable"
        assert (
            isinstance(group["title"], str) and group["title"]
        ), f"{key}: invalid title"
        assert (
            isinstance(group["result_prefix"], str)
            and group["result_prefix"]
        ), f"{key}: invalid result_prefix"

    # 用例数量精确校验
    per_group, total = count_cases()
    assert per_group == EXPECTED_CASE_COUNTS, (
        f"case counts mismatch:\n"
        f"  got {per_group}\n"
        f"  expected {EXPECTED_CASE_COUNTS}"
    )
    assert total == TOTAL_CASES

    # 全量收集
    all_cases = collect_all_version_cases()
    assert len(all_cases) == total == sum(per_group.values())

    # ID 唯一性 & 格式校验
    ids = []
    for group_key, test_id, name, _value in all_cases:
        ids.append(test_id)
        assert test_id.startswith(f"EQ-{group_key}-"), (
            f"{test_id}: expected prefix EQ-{group_key}-"
        )
        assert test_id[-3:].isdigit(), (
            f"{test_id}: expected 3-digit numeric suffix"
        )
        assert name, f"{test_id}: empty test_name"

    assert len(ids) == len(set(ids)), (
        f"duplicate test_ids: {len(ids)} total, {len(set(ids))} unique"
    )

    # 重量级组存在性
    for g in HEAVY_CASE_GROUPS:
        assert g in CASE_GROUPS, f"unknown heavy group: {g}"

    # 每组非空 & 每个 case 字段非空
    for key, group in CASE_GROUPS.items():
        cases = group["getter"]()
        assert cases, f"empty case group: {key}"
        for tid, tname, _tval in cases:
            assert tid and tname, f"{key}: empty id or name"

    # finish_message 推导逻辑验证
    for key in CASE_GROUP_ORDER:
        title = CASE_GROUPS[key]["title"]
        msg = f"{title.capitalize()} marshal tests finished."
        assert msg[0].isupper(), (
            f"{key}: derived finish_message not capitalized"
        )

    print(f"OK registry: {total} cases in {len(CASE_GROUPS)} groups")
    for key in CASE_GROUP_ORDER:
        print(f"     {key}: {per_group[key]}")


def check_builders():
    from cases.builders import (
        make_nested,
        make_nested_list,
        make_nested_tuple,
        make_nested_dict,
    )

    # 核心函数
    assert make_nested(list, 3) == [[[1]]]
    assert make_nested(tuple, 2) == ((1,),)
    assert make_nested(dict, 2) == {"level_1": {"level_0": 1}}
    assert make_nested(list, 0) == 1
    assert make_nested(dict, 0) == 1

    # 不支持的类型
    try:
        make_nested(set, 1)
        raise AssertionError("should have raised TypeError")
    except TypeError:
        pass

    # 包装别名与原函数等价
    assert make_nested_list(3) == make_nested(list, 3)
    assert make_nested_tuple(2) == make_nested(tuple, 2)
    assert make_nested_dict(2) == make_nested(dict, 2)

    print("OK builders")


def check_executor():
    from core.executor import (
        judge_final_result, _status_from_final_result, run_one_case,
    )

    # --- judge_final_result: 无预计算列表（兼容路径） ---
    all_success = [
        {
            "status": "SUCCESS", "sha256": "a", "size": 1,
            "exception_type": "", "exception_message": "",
        },
        {
            "status": "SUCCESS", "sha256": "a", "size": 1,
            "exception_type": "", "exception_message": "",
        },
    ]
    assert judge_final_result(all_success) == "STABLE_SUCCESS"

    # --- judge_final_result: 传入预计算列表（优化路径） ---
    successes = [a for a in all_success if a["status"] == "SUCCESS"]
    failures = [a for a in all_success if a["status"] == "EXCEPTION"]
    assert judge_final_result(
        all_success, successes, failures,
    ) == "STABLE_SUCCESS"

    # UNSTABLE_HASH
    mixed_hash = [
        {
            "status": "SUCCESS", "sha256": "a", "size": 1,
            "exception_type": "", "exception_message": "",
        },
        {
            "status": "SUCCESS", "sha256": "b", "size": 1,
            "exception_type": "", "exception_message": "",
        },
    ]
    assert judge_final_result(mixed_hash) == "UNSTABLE_HASH"

    # STABLE_EXCEPTION
    all_exc = [
        {
            "status": "EXCEPTION", "sha256": "", "size": "",
            "exception_type": "ValueError", "exception_message": "e1",
        },
        {
            "status": "EXCEPTION", "sha256": "", "size": "",
            "exception_type": "ValueError", "exception_message": "e2",
        },
    ]
    assert judge_final_result(all_exc) == "STABLE_EXCEPTION"

    # UNSTABLE_EXCEPTION
    mixed_exc = [
        {
            "status": "EXCEPTION", "sha256": "", "size": "",
            "exception_type": "ValueError", "exception_message": "",
        },
        {
            "status": "EXCEPTION", "sha256": "", "size": "",
            "exception_type": "TypeError", "exception_message": "",
        },
    ]
    assert judge_final_result(mixed_exc) == "UNSTABLE_EXCEPTION"

    # UNSTABLE_MIXED
    mixed = [
        {
            "status": "SUCCESS", "sha256": "a", "size": 1,
            "exception_type": "", "exception_message": "",
        },
        {
            "status": "EXCEPTION", "sha256": "", "size": "",
            "exception_type": "ValueError", "exception_message": "",
        },
    ]
    assert judge_final_result(mixed) == "UNSTABLE_MIXED"

    # --- _status_from_final_result 全覆盖 ---
    assert _status_from_final_result("STABLE_SUCCESS") == "SUCCESS"
    assert _status_from_final_result("STABLE_EXCEPTION") == "EXCEPTION"
    assert _status_from_final_result("UNSTABLE_HASH") == "UNSTABLE"
    assert _status_from_final_result("UNSTABLE_EXCEPTION") == "UNSTABLE"
    assert _status_from_final_result("UNSTABLE_MIXED") == "UNSTABLE"

    # --- run_one_case mock 路径 ---
    with patch(
        "core.executor._single_attempt", side_effect=mixed_hash,
    ):
        row = run_one_case("T", "t", 0, repeat_count=2)
    assert row["final_result"] == "UNSTABLE_HASH"
    assert row["status"] == "UNSTABLE"
    assert row["success_runs"] == 2
    assert row["exception_runs"] == 0

    print("OK executor")


def check_filter_and_repeat():
    from config import (
        HEAVY_CASE_GROUPS, RunOptions,
        filter_cases, resolve_repeat_count,
    )

    cases = [("A-01", "has slice", 1), ("B-02", "plain", 2)]

    # 文本过滤
    opts = RunOptions(filter_text="slice")
    filtered = filter_cases(cases, opts)
    assert len(filtered) == 1 and filtered[0][0] == "A-01"

    # --only 过滤（大小写不敏感，CLI 通过 from_args 已做 upper）
    opts2 = RunOptions(only_ids={"A-01"})
    assert len(filter_cases(cases, opts2)) == 1

    # 无过滤
    assert len(filter_cases(cases, RunOptions())) == 2

    # both filters active, no match
    opts3 = RunOptions(only_ids={"b-02"}, filter_text="slice")
    assert len(filter_cases(cases, opts3)) == 0

    # 4-tuple cases (version mode)
    cases4 = [
        ("basic", "A-01", "test a", 1),
        ("container", "B-02", "test b", 2),
    ]
    opts4 = RunOptions(filter_text="test a")
    assert len(filter_cases(cases4, opts4)) == 1

    # repeat 解析
    assert resolve_repeat_count("complexity", RunOptions(quick=True)) == 1
    assert resolve_repeat_count("basic", RunOptions(quick=True)) == 1
    heavy_default = resolve_repeat_count(
        "complexity", RunOptions(),
    )
    assert resolve_repeat_count("nested", RunOptions()) == heavy_default
    assert resolve_repeat_count("basic", RunOptions()) >= 1
    assert resolve_repeat_count("cycle", RunOptions(repeat_count=5)) == 5
    assert (
        resolve_repeat_count("complexity", RunOptions(repeat_count=3))
        == 3
    )

    assert HEAVY_CASE_GROUPS == frozenset(
        {"complexity", "nested", "cycle"},
    )

    print("OK filter and repeat")


def main():
    check_compile()
    check_required_layout()
    check_registry()
    check_builders()
    check_executor()
    check_filter_and_repeat()
    print("-" * 40)
    print("All self-checks passed.")


if __name__ == "__main__":
    main()
