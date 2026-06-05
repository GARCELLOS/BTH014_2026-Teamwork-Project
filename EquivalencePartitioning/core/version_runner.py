"""跨 Python 版本 marshal 测试。"""

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import os

from cases import collect_all_version_cases
from config import (
    BASE_DIR,
    REQUIRED_PROJECT_DIRS,
    REQUIRED_PROJECT_FILES,
    VERSION_RESULTS_DIR,
    VERSION_TARGETS,
    RunOptions,
    filter_cases,
    resolve_repeat_count,
)
from core.compare_versions import run_version_compare
from core.executor import run_one_case
from core.exporter import (
    ensure_version_dirs,
    list_version_result_files,
    save_current_version_results,
    save_summary,
)
from core.group_runner import print_case_result, print_result_summary


def check_required_files():
    missing = [
        *(n for n in REQUIRED_PROJECT_FILES if not (BASE_DIR / n).exists()),
        *(n for n in REQUIRED_PROJECT_DIRS if not (BASE_DIR / n).is_dir()),
    ]
    if missing:
        print("缺少必要文件或目录：")
        for name in missing:
            print(f"  - {name}")
        sys.exit(1)
def _utf8_env():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def _run_subprocess(cmd, *, cwd=None, capture_output=False):
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_utf8_env(),
    )

def _runner_script_args(version_label: str, options: RunOptions) -> list[str]:
    args = [
        str(Path(__file__).resolve().parent.parent / "run_marshal_tests.py"),
        "--current",
        "--version-label",
        version_label,
    ]
    if options.quick:
        args.append("--quick")
    if options.repeat_count is not None:
        args.extend(["--repeat", str(options.repeat_count)])
    if options.only_ids:
        args.extend(["--only", ",".join(sorted(options.only_ids))])
    if options.filter_text:
        args.extend(["--filter", options.filter_text])
    return args


def run_current_python(version_label="CURRENT", options: RunOptions | None = None):
    options = options or RunOptions()
    ensure_version_dirs()
    check_required_files()

    cases = filter_cases(collect_all_version_cases(), options)
    print("Running marshal tests with current Python")
    print(f"Version label: {version_label}")
    print(f"Python version: {platform.python_version()}")
    print(f"Total cases: {len(cases)}")
    print("-" * 80)

    if not cases:
        print("No cases matched filter.")
        return None, None

    results = []
    for case_group, test_id, name, value in cases:
        result = run_one_case(
            test_id,
            name,
            value,
            extra_fields={"version_label": version_label, "case_group": case_group},
            repeat_count=resolve_repeat_count(case_group, options),
        )
        results.append(result)
        print_case_result(result, show_group=True)

    csv_path, json_path = save_current_version_results(results, version_label)
    print("-" * 80)
    print("Current Python test finished.")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    print_result_summary(results, title="Summary (all groups)")
    return csv_path, json_path


def run_target_python(target_version, options: RunOptions | None = None):
    options = options or RunOptions()
    version_label = VERSION_TARGETS.get(target_version, f"PY-{target_version}")
    command = ["uv", "run", "--no-project", "--python", target_version, "python"]
    command_text = " ".join(command)
    run_time = datetime.now().isoformat(timespec="seconds")

    print(f"{version_label} | Python {target_version} | {command_text}")

    try:
        probe = _run_subprocess(
            command + ["--version"],
            cwd=BASE_DIR,
            capture_output=True,
        )
    except FileNotFoundError:
        probe = None

    if probe is None or probe.returncode != 0:
        msg = "command not found" if probe is None else (probe.stderr or probe.stdout).strip()
        print(f"  SKIPPED: {msg}")
        return _summary_row(version_label, target_version, command_text, run_time, "SKIPPED", msg)

    python_output = (probe.stdout or probe.stderr).strip()
    before = list_version_result_files()
    runner_args = _runner_script_args(version_label, options)

    print(f"  Running: {' '.join(command + runner_args)}")
    print("-" * 40)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    completed = _run_subprocess(
        command + runner_args,
        cwd=BASE_DIR,
        capture_output=False,
    )
    print("-" * 40)

    new_files = sorted(list_version_result_files() - before)
    if completed.returncode == 0:
        print("  DONE")
        for path in new_files:
            print(f"  Saved: {path}")
        return _summary_row(
            version_label,
            target_version,
            command_text,
            run_time,
            "DONE",
            "",
            python_output,
            completed.returncode,
            new_files,
        )

    print("  FAILED (exit %s)" % completed.returncode)
    return _summary_row(
        version_label,
        target_version,
        command_text,
        run_time,
        "FAILED",
        f"exit code {completed.returncode}",
        python_output,
        completed.returncode,
        new_files,
    )


def _summary_row(
    version_label,
    target_version,
    command_text,
    run_time,
    run_status,
    error_message,
    python_output="",
    return_code="",
    new_files=None,
):
    return {
        "version_label": version_label,
        "target_python_version": target_version,
        "command": command_text,
        "available": "YES" if run_status != "SKIPPED" else "NO",
        "actual_python_output": python_output,
        "run_status": run_status,
        "return_code": return_code,
        "result_files": "; ".join(str(p) for p in (new_files or [])),
        "error_message": error_message,
        "run_time": run_time,
    }


def run_selected_target_pythons(target_versions, options: RunOptions | None = None):
    options = options or RunOptions()
    ensure_version_dirs()
    check_required_files()

    print("Python version comparison runner")
    print(f"Result directory: {VERSION_RESULTS_DIR}")
    print(f"Targets: {', '.join(target_versions)}")
    print("-" * 80)

    rows = [run_target_python(v, options) for v in target_versions]
    for _ in target_versions:
        print("-" * 80)

    csv_path, json_path = save_summary(rows)
    print(f"Summary CSV: {csv_path}")
    print(f"Summary JSON: {json_path}")
    if options.compare_after:
        run_version_compare()
