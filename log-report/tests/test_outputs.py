"""Verifier for the dynamo/log-report task.

Each test below maps 1:1 to a numbered success criterion in instruction.md.

The expected values are the ground truth for the access.log that ships in
environment/, so passing requires actually parsing the log - merely creating
/app/report.json is not sufficient.
"""

import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")

EXPECTED_KEYS = {"total_requests", "unique_ips", "top_path"}
EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _load_report():
    """Parse /app/report.json and return the decoded object.

    Decoded as utf-8-sig so that a leading byte-order mark - which some editors
    and Windows-authored tooling prepend - does not fail an otherwise correct
    report. Plain utf-8 would leave the BOM in place and json.load would raise.
    """
    with REPORT_PATH.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def _is_int(value):
    """True for real integers; bool is a subclass of int and is not accepted."""
    return isinstance(value, int) and not isinstance(value, bool)


def test_report_is_a_valid_json_object():
    """Criterion 1: /app/report.json exists and parses as a single JSON object."""
    assert REPORT_PATH.exists(), "/app/report.json was not created"
    report = _load_report()
    assert isinstance(report, dict), (
        f"expected a JSON object at the top level, got {type(report).__name__}"
    )


def test_report_has_exactly_the_required_keys():
    """Criterion 2: the object has exactly total_requests, unique_ips and top_path."""
    report = _load_report()
    assert set(report) == EXPECTED_KEYS, (
        f"expected exactly {sorted(EXPECTED_KEYS)}, got {sorted(report)}"
    )


def test_total_requests_counts_every_request():
    """Criterion 3: total_requests is an integer equal to the non-empty line count."""
    value = _load_report()["total_requests"]
    assert _is_int(value), f"total_requests must be an integer, got {type(value).__name__}"
    assert value == EXPECTED_TOTAL_REQUESTS, (
        f"expected total_requests == {EXPECTED_TOTAL_REQUESTS}, got {value}"
    )


def test_unique_ips_counts_distinct_clients():
    """Criterion 4: unique_ips is an integer equal to the distinct client IP count."""
    value = _load_report()["unique_ips"]
    assert _is_int(value), f"unique_ips must be an integer, got {type(value).__name__}"
    assert value == EXPECTED_UNIQUE_IPS, (
        f"expected unique_ips == {EXPECTED_UNIQUE_IPS}, got {value}"
    )


def test_top_path_is_the_most_requested_path():
    """Criterion 5: top_path is a string equal to the most frequently requested path."""
    value = _load_report()["top_path"]
    assert isinstance(value, str), f"top_path must be a string, got {type(value).__name__}"
    assert value == EXPECTED_TOP_PATH, (
        f"expected top_path == {EXPECTED_TOP_PATH!r}, got {value!r}"
    )
