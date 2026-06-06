"""跨 Python 版本结果对比（pivot 表）。"""

import csv
from collections import defaultdict
from datetime import datetime

from config import VERSION_RESULTS_DIR


def _pick_latest_csv_per_label(csv_files):
    """每个 version_label 只保留最新一份 marshal_python_*.csv。"""
    by_label = {}
    for path in csv_files:
        try:
            with path.open(encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                row = next(reader, None)
                if not row:
                    continue
                label = row.get("version_label", "")
        except OSError:
            continue

        if not label:
            parts = path.stem.split("_")
            for part in reversed(parts):
                if part.startswith("PY-"):
                    label = part
                    break
            else:
                label = path.stem

        prev = by_label.get(label)
        if prev is None or path.stat().st_mtime > prev.stat().st_mtime:
            by_label[label] = path

    return by_label


def load_version_rows(csv_path):
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_pivot_rows(version_to_rows):
    """version_to_rows: {PY-01: [rows...], ...}"""
    pivot = defaultdict(dict)

    for label, rows in version_to_rows.items():
        for row in rows:
            group = row.get("case_group", "")
            test_id = row.get("test_id", "")
            key = (group, test_id)
            pivot[key]["case_group"] = group
            pivot[key]["test_id"] = test_id
            pivot[key]["test_name"] = row.get("test_name", "")
            pivot[key][f"{label}_status"] = row.get("status", "")
            pivot[key][f"{label}_final"] = row.get("final_result", "")
            pivot[key][f"{label}_sha256"] = row.get("sha256", "")

    return sorted(
        pivot.values(),
        key=lambda r: (r.get("case_group", ""), r.get("test_id", "")),
    )


def cross_version_hash_consistent(pivot_row, labels):
    hashes = [
        pivot_row.get(f"{label}_sha256", "")
        for label in labels
        if pivot_row.get(f"{label}_sha256")
    ]
    if len(hashes) < 2:
        return "N/A"
    return "YES" if len(set(hashes)) == 1 else "NO"


def run_version_compare(output_dir=None):
    output_dir = output_dir or VERSION_RESULTS_DIR
    csv_files = list(output_dir.glob("marshal_python_*.csv"))
    if not csv_files:
        print("未找到版本对比 CSV（results/python_versions/marshal_python_*.csv）")
        return None

    latest = _pick_latest_csv_per_label(csv_files)
    if not latest:
        print("无法从结果文件中解析 version_label")
        return None

    labels = sorted(latest.keys())
    version_to_rows = {
        label: load_version_rows(path) for label, path in latest.items()
    }

    pivot_rows = build_pivot_rows(version_to_rows)
    for row in pivot_rows:
        row["hash_consistent_across_versions"] = (
            cross_version_hash_consistent(row, labels)
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"cross_version_pivot_{timestamp}.csv"

    fieldnames = [
        "case_group", "test_id", "test_name",
        "hash_consistent_across_versions",
    ]
    for label in labels:
        fieldnames.extend([
            f"{label}_status", f"{label}_final", f"{label}_sha256",
        ])

    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(pivot_rows)

    consistent = sum(
        1 for r in pivot_rows
        if r["hash_consistent_across_versions"] == "YES"
    )
    differing = sum(
        1 for r in pivot_rows
        if r["hash_consistent_across_versions"] == "NO"
    )

    print("-" * 80)
    print("Cross-version pivot")
    print(f"  Versions used: {', '.join(labels)}")
    print(f"  Test cases:    {len(pivot_rows)}")
    print(f"  Same sha256:   {consistent}")
    print(f"  Different:     {differing}")
    print(f"  Saved:         {out_path}")

    return out_path
