"""marshal.dumps 执行与重复运行稳定性判定。"""

import hashlib
import marshal
import platform
from datetime import datetime

from config import DEFAULT_REPEAT_COUNT


def calc_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def short_repr(value, max_length=300):
    try:
        text = repr(value)
    except RecursionError:
        return f"<repr failed: RecursionError; type={type(value).__name__}>"
    except Exception as exc:
        return (
            f"<repr failed: {type(exc).__name__}; "
            f"type={type(value).__name__}>"
        )

    if len(text) > max_length:
        return text[:max_length] + "...<truncated>"
    return text


def _environment_fields():
    return {
        "os_name": platform.system(),
        "python_version": platform.python_version(),
        "marshal_version": marshal.version,
        "machine": platform.machine(),
        "platform": platform.platform(),
        "run_time": datetime.now().isoformat(timespec="seconds"),
    }


def _single_attempt(value):
    try:
        byte_stream = marshal.dumps(value)
        return {
            "status": "SUCCESS",
            "sha256": calc_sha256(byte_stream),
            "size": len(byte_stream),
            "exception_type": "",
            "exception_message": "",
        }
    except Exception as exc:
        return {
            "status": "EXCEPTION",
            "sha256": "",
            "size": "",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }


def judge_final_result(attempts, successes=None, failures=None):
    if successes is None:
        successes = [a for a in attempts if a["status"] == "SUCCESS"]
    if failures is None:
        failures = [a for a in attempts if a["status"] == "EXCEPTION"]

    if len(successes) == len(attempts):
        hashes = {a["sha256"] for a in successes}
        return "STABLE_SUCCESS" if len(hashes) == 1 else "UNSTABLE_HASH"

    if len(failures) == len(attempts):
        exc_types = {a["exception_type"] for a in failures}
        return (
            "STABLE_EXCEPTION" if len(exc_types) == 1
            else "UNSTABLE_EXCEPTION"
        )

    return "UNSTABLE_MIXED"


def _status_from_final_result(final_result):
    if final_result == "STABLE_SUCCESS":
        return "SUCCESS"
    if final_result == "STABLE_EXCEPTION":
        return "EXCEPTION"
    return "UNSTABLE"


def run_one_case(test_id, name, value, extra_fields=None, repeat_count=None):
    repeat_count = (
        repeat_count if repeat_count is not None
        else DEFAULT_REPEAT_COUNT
    )
    if repeat_count < 1:
        raise ValueError(f"repeat_count must be >= 1, got {repeat_count}")

    attempts = [_single_attempt(value) for _ in range(repeat_count)]
    successes = [a for a in attempts if a["status"] == "SUCCESS"]
    failures = [a for a in attempts if a["status"] == "EXCEPTION"]
    final_result = judge_final_result(attempts, successes, failures)
    status = _status_from_final_result(final_result)

    result = {
        "os_name": platform.system(),
        "test_id": test_id,
        "test_name": name,
        "input_repr": short_repr(value),
        "status": status,
        "sha256": "",
        "size": "",
        "exception_type": "",
        "exception_message": "",
        "repeat_count": repeat_count,
        "final_result": final_result,
        "success_runs": len(successes),
        "exception_runs": len(failures),
        "unique_sha256_count": len(
            {a["sha256"] for a in attempts if a["sha256"]}
        ),
    }

    if extra_fields:
        result = {**extra_fields, **result}

    if final_result == "STABLE_SUCCESS":
        sample = attempts[0]
        result["sha256"] = sample["sha256"]
        result["size"] = sample["size"]
    elif final_result == "STABLE_EXCEPTION":
        sample = attempts[0]
        result["exception_type"] = sample["exception_type"]
        result["exception_message"] = sample["exception_message"]
    elif successes:
        sample = successes[0]
        result["sha256"] = sample["sha256"]
        result["size"] = sample["size"]
        result["exception_type"] = (
            failures[0]["exception_type"] if failures else ""
        )
        result["exception_message"] = (
            failures[0]["exception_message"] if failures else ""
        )
    elif failures:
        sample = failures[0]
        result["exception_type"] = sample["exception_type"]
        result["exception_message"] = sample["exception_message"]

    return result
