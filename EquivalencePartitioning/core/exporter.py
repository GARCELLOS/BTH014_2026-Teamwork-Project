"""测试结果 CSV / JSON 导出。"""

import csv
import json
from datetime import datetime

from config import RESULTS_DIR, VERSION_RESULTS_DIR
from core.executor import _environment_fields

# CSV 不写每行重复的环境字段（完整信息在 JSON environment 中）
CSV_FIELDNAMES = [
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


def ensure_dirs():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_version_dirs():
    VERSION_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def get_environment(extra=None):
    environment = _environment_fields()
    if extra:
        environment.update(extra)
    return environment


def _rows_for_csv(results, fieldnames):
    return [
        {key: row.get(key, "") for key in fieldnames}
        for row in results
    ]


def save_results(results, result_prefix):
    ensure_dirs()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = RESULTS_DIR / f"{result_prefix}_results_{timestamp}.csv"
    json_path = RESULTS_DIR / f"{result_prefix}_results_{timestamp}.json"

    with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(_rows_for_csv(results, CSV_FIELDNAMES))

    output_data = {
        "environment": get_environment(),
        "results": results,
    }

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=2)

    print(f"CSV result saved to: {csv_path}")
    print(f"JSON result saved to: {json_path}")

    return csv_path, json_path


def version_text_for_filename(version_text):
    return version_text.replace(".", "_")


def save_current_version_results(results, version_label):
    ensure_version_dirs()

    import platform

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_version = platform.python_version()
    version_part = version_text_for_filename(current_version)

    csv_path = (
        VERSION_RESULTS_DIR
        / f"marshal_python_{version_part}_{version_label}_{timestamp}.csv"
    )
    json_path = (
        VERSION_RESULTS_DIR
        / f"marshal_python_{version_part}_{version_label}_{timestamp}.json"
    )

    with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=VERSION_CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(_rows_for_csv(results, VERSION_CSV_FIELDNAMES))

    output_data = {
        "environment": get_environment({"version_label": version_label}),
        "results": results,
    }

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=2)

    return csv_path, json_path


def list_version_result_files():
    ensure_version_dirs()

    csv_files = set(VERSION_RESULTS_DIR.glob("marshal_python_*.csv"))
    json_files = set(VERSION_RESULTS_DIR.glob("marshal_python_*.json"))

    return csv_files | json_files


def save_summary(summary_rows):
    ensure_version_dirs()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = VERSION_RESULTS_DIR / f"python_version_summary_{timestamp}.csv"
    json_path = VERSION_RESULTS_DIR / f"python_version_summary_{timestamp}.json"

    with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerows(summary_rows)

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(summary_rows, json_file, ensure_ascii=False, indent=2)

    return csv_path, json_path
