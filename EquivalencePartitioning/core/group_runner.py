"""单组测试运行、控制台输出与结果汇总。"""

import marshal
import platform
from collections import Counter

from cases import CASE_GROUPS
from config import RunOptions, filter_cases, resolve_repeat_count
from core.executor import run_one_case
from core.exporter import save_results


def print_result_summary(results, title="Summary"):
    if not results:
        print(f"{title}: (no cases run)")
        return
    final_counts = Counter(r.get("final_result", "") for r in results)
    status_counts = Counter(r.get("status", "") for r in results)
    unstable = sum(
        final_counts[k]
        for k in ("UNSTABLE_HASH", "UNSTABLE_EXCEPTION", "UNSTABLE_MIXED")
    )
    print("-" * 80)
    print(title)
    print(f"  Total cases run: {len(results)}")
    print(f"  STABLE_SUCCESS:  {final_counts.get('STABLE_SUCCESS', 0)}")
    print(f"  STABLE_EXCEPTION:{final_counts.get('STABLE_EXCEPTION', 0)}")
    print(f"  UNSTABLE:        {unstable}")
    print(
        f"  status -> SUCCESS: {status_counts.get('SUCCESS', 0)}, "
        f"EXCEPTION: {status_counts.get('EXCEPTION', 0)}, "
        f"UNSTABLE: {status_counts.get('UNSTABLE', 0)}"
    )


def print_case_result(result, *, show_group=False):
    prefix = f"{result['case_group']} | " if show_group else ""
    print(
        f"{prefix}"
        f"{result['test_id']} | "
        f"{result['test_name']} | "
        f"{result['status']} | "
        f"final={result['final_result']} | "
        f"size={result['size']} | "
        f"sha256={result['sha256']}"
    )


def run_and_save_group(
    cases,
    title,
    result_prefix,
    group_key=None,
    options: RunOptions | None = None,
):
    options = options or RunOptions()
    cases = filter_cases(cases, options)
    repeat_count = resolve_repeat_count(group_key, options)

    if not cases:
        print(f"No cases matched filter for: {title}")
        return []

    print(f"Running {title} marshal tests...")
    print(f"Python version: {platform.python_version()}")
    print(f"marshal.version: {marshal.version}")
    print(f"Repeat count per case: {repeat_count}")
    print(f"Total cases: {len(cases)}")
    print("-" * 80)

    results = []
    for test_id, name, value in cases:
        result = run_one_case(test_id, name, value, repeat_count=repeat_count)
        results.append(result)
        print_case_result(result)

    save_results(results, result_prefix)
    print("-" * 80)
    print(f"{title.capitalize()} marshal tests finished.")
    print_result_summary(results, title=f"Summary ({title})")
    return results


def run_registered_group(group_key, options: RunOptions | None = None):
    if group_key not in CASE_GROUPS:
        known = ", ".join(sorted(CASE_GROUPS))
        raise KeyError(
            f"Unknown case group '{group_key}'. Known groups: {known}"
        )
    group = CASE_GROUPS[group_key]
    return run_and_save_group(
        cases=group["getter"](),
        title=group["title"],
        result_prefix=group["result_prefix"],
        group_key=group_key,
        options=options,
    )
