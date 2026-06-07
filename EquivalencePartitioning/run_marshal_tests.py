"""
marshal 序列化稳定性测试 — 唯一入口
"""

import argparse
import sys

# 确保 Windows 下中文路径能正确显示
try:
    sys.stdout.reconfigure(  # pyright: ignore[reportAttributeAccessIssue]
        encoding="utf-8",
    )
except Exception:
    pass

from cases import CASE_GROUP_ORDER, CASE_GROUPS
from config import HEAVY_CASE_GROUPS, VERSION_TARGETS, RunOptions
from core.compare_versions import run_version_compare
from core.group_runner import run_registered_group
from core.version_runner import (
    check_required_files,
    run_current_python,
    run_selected_target_pythons,
)


def _build_epilog(heavy_repeat: int) -> str:
    groups = ", ".join(CASE_GROUP_ORDER)
    return f"""
提示:
  --all          跨 Python 3.10–3.14 版本对比（结果在 results/python_versions/）
  --all-groups   依次运行全部用例组: {groups}
  --quick        每用例只跑 1 次（调试用）
  重量级组 ({", ".join(sorted(HEAVY_CASE_GROUPS))}) 默认 repeat={heavy_repeat}
  --compare      根据已有版本结果生成 cross_version_pivot_*.csv
""".strip()


def build_parser():
    from config import HEAVY_CASE_DEFAULT_REPEAT

    parser = argparse.ArgumentParser(
        description="marshal 序列化稳定性测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_build_epilog(HEAVY_CASE_DEFAULT_REPEAT),
    )
    parser.add_argument(
        "group",
        nargs="?",
        choices=list(CASE_GROUPS.keys()),
        help="运行单个用例组",
    )
    parser.add_argument(
        "--all-groups",
        action="store_true",
        help=f"运行全部 {len(CASE_GROUP_ORDER)} 个用例组（不是跨 Python 版本）",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=None,
        metavar="N",
        help="每用例重复次数（默认 10；重量级组默认见配置）",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="快速模式：等价于 --repeat 1",
    )
    parser.add_argument(
        "--only",
        metavar="IDS",
        help="只跑指定用例，逗号分隔，如 EQ-basic-001,EQ-container-034",
    )
    parser.add_argument(
        "--filter",
        metavar="TEXT",
        help="只跑 test_id 或 test_name 包含该文本的用例（如 slice）",
    )
    parser.add_argument("--current", action="store_true", help="当前解释器跑全部用例")
    parser.add_argument("--single", action="store_true", help="同 --current")
    parser.add_argument(
        "--all",
        action="store_true",
        help="uv 切换 3.10–3.14 跑版本对比（不是 --all-groups）",
    )
    parser.add_argument(
        "--target",
        nargs="+",
        metavar="VER",
        help="指定 Python 版本",
    )
    parser.add_argument("--version-label", default="CURRENT", help="结果中的版本标签")
    parser.add_argument(
        "--compare",
        action="store_true",
        help="根据 results/python_versions/ 生成跨版本 pivot CSV",
    )
    parser.add_argument(
        "--compare-after",
        action="store_true",
        help="--all / --target 完成后自动生成 pivot",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    options = RunOptions.from_args(args)

    if args.quick and args.repeat is not None and args.repeat != 1:
        parser.error("--quick 与 --repeat 不能同时指定不同次数")

    if args.repeat is not None and args.repeat < 1:
        parser.error("--repeat 必须 >= 1")

    if args.compare:
        check_required_files()
        run_version_compare()
        return

    version_mode = args.current or args.single or args.all or args.target

    if version_mode and args.group:
        parser.error("不能同时指定用例组（如 basic）与 --current / --all / --target")

    if args.all:
        print(
            "提示: --all = 跨 Python 版本对比；跑全部用例组请用 --all-groups。\n",
            flush=True,
        )

    if version_mode:
        check_required_files()
        if args.current or args.single:
            run_current_python(args.version_label, options=options)
            return
        if args.target:
            run_selected_target_pythons(args.target, options=options)
            return
        if args.all:
            run_selected_target_pythons(
                list(VERSION_TARGETS.keys()),
                options=options,
            )
            return
        parser.error("版本模式请指定 --current、--target 或 --all")

    if args.all_groups:
        for group_key in CASE_GROUP_ORDER:
            run_registered_group(group_key, options=options)
        return

    if args.group:
        run_registered_group(args.group, options=options)
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
