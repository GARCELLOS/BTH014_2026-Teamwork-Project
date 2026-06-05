"""
项目配置与运行选项。

环境变量：
  MARSHAL_TEST_REPEAT      默认重复次数（默认 10）
  MARSHAL_HEAVY_REPEAT     重量级用例组默认重复（默认 1）
  MARSHAL_COMPLEXITY_REPEAT  同 MARSHAL_HEAVY_REPEAT（兼容旧名）
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
VERSION_RESULTS_DIR = RESULTS_DIR / "python_versions"

VERSION_TARGETS = {
    "3.10": "PY-01",
    "3.11": "PY-02",
    "3.12": "PY-03",
    "3.13": "PY-04",
    "3.14": "PY-05",
}

REQUIRED_PROJECT_FILES = ["config.py", "run_marshal_tests.py"]
REQUIRED_PROJECT_DIRS = ["cases", "core"]


def _read_int_env(name: str, default: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        return default
    return value if value >= 1 else default


DEFAULT_REPEAT_COUNT = _read_int_env("MARSHAL_TEST_REPEAT", 10)


def _read_heavy_repeat_default() -> int:
    if os.environ.get("MARSHAL_HEAVY_REPEAT") is not None:
        return _read_int_env("MARSHAL_HEAVY_REPEAT", 1)
    return _read_int_env("MARSHAL_COMPLEXITY_REPEAT", 1)


HEAVY_CASE_DEFAULT_REPEAT = _read_heavy_repeat_default()
HEAVY_CASE_GROUPS = frozenset({"complexity", "nested", "cycle"})


@dataclass
class RunOptions:
    repeat_count: int | None = None
    quick: bool = False
    only_ids: set[str] = field(default_factory=set)
    filter_text: str | None = None
    compare_after: bool = False

    @classmethod
    def from_args(cls, args):
        only_ids = set()
        if getattr(args, "only", None):
            for part in args.only.split(","):
                part = part.strip().upper()
                if part:
                    only_ids.add(part)
        return cls(
            repeat_count=args.repeat,
            quick=getattr(args, "quick", False),
            only_ids=only_ids,
            filter_text=getattr(args, "filter", None),
            compare_after=getattr(args, "compare_after", False),
        )


def resolve_repeat_count(group_key: str | None, options: RunOptions) -> int:
    if options.quick:
        return 1
    if options.repeat_count is not None:
        return options.repeat_count
    if group_key in HEAVY_CASE_GROUPS:
        return HEAVY_CASE_DEFAULT_REPEAT
    return DEFAULT_REPEAT_COUNT


def filter_cases(cases, options: RunOptions):
    if not options.only_ids and not options.filter_text:
        return cases
    filtered = []
    for item in cases:
        if len(item) == 3:
            test_id, name, _value = item
        else:
            _, test_id, name, _value = item
        if options.only_ids and test_id.upper() not in options.only_ids:
            continue
        if options.filter_text:
            haystack = f"{test_id} {name}".lower()
            if options.filter_text.lower() not in haystack:
                continue
        filtered.append(item)
    return filtered
