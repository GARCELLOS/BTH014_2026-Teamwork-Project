"""测试结果 CSV / JSON 导出。"""

import csv
import json
import platform
from datetime import datetime

from config import RESULTS_DIR, VERSION_RESULTS_DIR
from core.executor import _environment_fields

CSV_FIELDNAMES = [
    "os_name",
    "test_id",
    "test_name",
    "input_repr",
    "status",
    "sha256",
    "size",
    "exception_type",
    "exception_message",
    "repeat_count",
    "final_result",
    "success_runs",
    "exception_runs",
    "unique_sha256_count",
]

VERSION_CSV_FIELDNAMES = ["version_label", "case_group", *CSV_FIELDNAMES]

SUMMARY_FIELDNAMES = [
    "version_label",
    "target_python_version",
    "command",
    "available",
    "actual_python_output",
    "run_status",
    "return_code",
    "result_files",
    "error_message",
    "run_time",
]


def _rows_for_csv(results, fieldnames):
    return [{key: row.get(key, "") for key in fieldnames} for row in results]


def _write_results(
    results, output_dir, csv_name, json_name, fieldnames, env_extra=None
):
    """Common write logic for both single-group and version-mode results."""
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / csv_name
    json_path = output_dir / json_name

    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_rows_for_csv(results, fieldnames))

    env = _environment_fields()
    if env_extra:
        env.update(env_extra)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"environment": env, "results": results},
            f, ensure_ascii=False, indent=2,
        )

    return csv_path, json_path


def ensure_version_dirs():
    VERSION_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def save_results(results, result_prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path, json_path = _write_results(
        results,
        RESULTS_DIR,
        f"{result_prefix}_results_{timestamp}.csv",
        f"{result_prefix}_results_{timestamp}.json",
        CSV_FIELDNAMES,
    )
    print(f"CSV result saved to: {csv_path}")
    print(f"JSON result saved to: {json_path}")
    return csv_path, json_path


def save_current_version_results(results, version_label):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_part = platform.python_version().replace(".", "_")
    csv_path, json_path = _write_results(
        results,
        VERSION_RESULTS_DIR,
        f"marshal_python_{version_part}_{version_label}_{timestamp}.csv",
        f"marshal_python_{version_part}_{version_label}_{timestamp}.json",
        VERSION_CSV_FIELDNAMES,
        {"version_label": version_label},
    )
    return csv_path, json_path


def list_version_result_files():
    ensure_version_dirs()
    return set(VERSION_RESULTS_DIR.glob("marshal_python_*.csv")) | set(
        VERSION_RESULTS_DIR.glob("marshal_python_*.json")
    )


def save_summary(summary_rows):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path, json_path = _write_results(
        summary_rows,
        VERSION_RESULTS_DIR,
        f"python_version_summary_{timestamp}.csv",
        f"python_version_summary_{timestamp}.json",
        SUMMARY_FIELDNAMES,
    )
    return csv_path, json_path
