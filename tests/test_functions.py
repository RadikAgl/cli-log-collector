"""Юнит тесты"""

from utils import (
    get_handler,
    get_log_level,
    merge_logs_numbers_dicts,
    reformat_report_for_out,
    get_log_numbers_as_dict,
)


def test_get_handler():
    line = ["foo", "www", "123", "api/test"]
    assert get_handler(line) == "api/test"


def test_get_log_level():
    log_level = "INFO"
    line = ["foo", "www", log_level, "api/test"]
    assert get_log_level(line) == log_level


def test_merge_logs_numbers_dicts():
    test_list = [
        {
            "url1": {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4},
            "url2": {"DEBUG": 5, "INFO": 6, "WARNING": 7, "ERROR": 8, "CRITICAL": 9},
        },
        {
            "url2": {"DEBUG": 1, "INFO": 1, "WARNING": 1, "ERROR": 1, "CRITICAL": 1},
            "url1": {
                "DEBUG": 15,
                "INFO": 16,
                "WARNING": 17,
                "ERROR": 18,
                "CRITICAL": 19,
            },
        },
    ]

    res = {
        "url1": {"DEBUG": 15, "INFO": 17, "WARNING": 19, "ERROR": 21, "CRITICAL": 23},
        "url2": {"DEBUG": 6, "INFO": 7, "WARNING": 8, "ERROR": 9, "CRITICAL": 10},
    }
    test_res = merge_logs_numbers_dicts(test_list)
    assert test_res["url1"]["INFO"] == res["url1"]["INFO"]
    assert test_res["url2"]["INFO"] == res["url2"]["INFO"]


def test_reformat_report_for_out():
    test_dict = {
        "url1": {"DEBUG": 15, "INFO": 17, "WARNING": 19, "ERROR": 21, "CRITICAL": 23},
        "url2": {"DEBUG": 6, "INFO": 7, "WARNING": 8, "ERROR": 9, "CRITICAL": 10},
    }
    handler = "handler"

    res = reformat_report_for_out(test_dict, handler)

    assert res[0][0] == handler.upper()
    assert res[-1][1] == 21
    assert res[0][1] == "DEBUG"
    assert res[1][-1] == 95
    assert len(res) == 4


def test_get_log_numbers_as_dict():
    file_name = "tests/file_for_testing.log"
    with open(file_name, "r") as file:
        log_numbers = get_log_numbers_as_dict(file)
    assert "/admin/dashboard/" in log_numbers
    assert log_numbers["/admin/dashboard/"]["INFO"] == 6
