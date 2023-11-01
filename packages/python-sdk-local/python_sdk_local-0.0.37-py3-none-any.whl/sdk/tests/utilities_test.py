from datetime import time, datetime, timedelta, date
import sys
import os
from dotenv import load_dotenv
from python_sdk_local.sdk.src import utilities
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.constants import *  # noqa: E402
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_TEST)

TEST_TIME_DELTA = timedelta(seconds=25853)
TEST_TIME_FORMAT = "07:10:53"


def test_timedelta_to_time_format():
    TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "test_timedelta_to_time_format"
    logger.start(TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)

    time_format = utilities.timedelta_to_time_format(TEST_TIME_DELTA)
    assert time_format == TEST_TIME_FORMAT

    logger.end(TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)


def test_is_list_of_dicts():
    TEST_IS_LIST_OF_DICTS_METHOD_NAME = "test_is_list_of_dicts"
    logger.start(TEST_IS_LIST_OF_DICTS_METHOD_NAME)

    assert utilities.is_list_of_dicts([]) == True
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}]) == True
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, 3]) == False
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, 'c']) == False
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, {'c': 3}]) == True
    assert utilities.is_list_of_dicts(
        [{'a': 1}, {'b': 2}, {'c': {'d': 5}}, 4]) == False

    logger.end(TEST_IS_LIST_OF_DICTS_METHOD_NAME)


def test_is_valid_time_range():
    valid_time_range = (time(12, 34, 56), time(23, 45, 12))
    invalid_time_range = (time(12, 34, 56), time(
        11, 22).hour)  # Invalid format

    assert utilities.is_valid_time_range(valid_time_range) is True
    assert utilities.is_valid_time_range(invalid_time_range) is False


def test_is_valid_date_range():
    valid_date_range = (date(2023, 10, 26), date(2023, 10, 27))
    invalid_date_range = (date(2023, 10, 26), time(
        23, 45, 12))  # Invalid format
    check_date_inside = date(2023, 10, 27)
    check_date_outside = date(2023, 10, 25)

    assert utilities.is_valid_date_range(valid_date_range) is True
    assert utilities.is_valid_date_range(invalid_date_range) is False
    assert utilities.is_date_in_date_range(
        check_date_inside, valid_date_range) is True
    assert utilities.is_date_in_date_range(
        check_date_outside, valid_date_range) is False


def test_is_valid_datetime_range():
    valid_datetime_range = (
        datetime(2023, 10, 26, 12, 34, 56), datetime(2023, 10, 27, 23, 45, 12))
    invalid_datetime_range = (
        datetime(2023, 10, 26, 12, 34, 56), time(23, 45, 12))  # Invalid format
    check_datetime_inside = datetime(2023, 10, 27, 15, 0, 0)
    check_datetime_outside = datetime(2023, 10, 25, 5, 0, 0)

    assert utilities.is_valid_datetime_range(valid_datetime_range) is True
    assert utilities.is_valid_datetime_range(invalid_datetime_range) is False
    assert utilities.is_datetime_in_datetime_range(
        check_datetime_inside, valid_datetime_range) is True
    assert utilities.is_datetime_in_datetime_range(
        check_datetime_outside, valid_datetime_range) is False


def test_timedelta_to_time_format():
    duration = timedelta(hours=2, minutes=30, seconds=45)
    formatted_time = utilities.timedelta_to_time_format(duration)
    assert formatted_time == "02:30:45"


def test_is_time_in_time_range():
    valid_time_range = (time(12, 34, 56), time(23, 45, 12))
    invalid_time_range = (time(12, 34, 56), time(23, 45))  # Invalid format
    check_time_inside = time(15, 0, 0)
    check_time_outside = time(5, 0, 0)

    assert utilities.is_time_in_time_range(
        check_time_inside, valid_time_range) is True
    assert utilities.is_time_in_time_range(
        check_time_outside, valid_time_range) is False


def test_is_date_in_date_range():
    valid_date_range = [date(2023, 10, 26), date(2023, 10, 27)]
    invalid_date_range = [date(2023, 10, 26), time(
        23, 45, 12)]  # Invalid format
    check_date_inside = date(2023, 10, 27)
    check_date_outside = date(2023, 10, 25)

    assert utilities.is_date_in_date_range(
        check_date_inside, valid_date_range) is True
    assert utilities.is_date_in_date_range(
        check_date_outside, valid_date_range) is False
    assert utilities.is_date_in_date_range(
        check_date_inside, invalid_date_range) is False


def test_is_datetime_in_datetime_range():
    valid_datetime_range = [
        datetime(2023, 10, 26, 12, 34, 56), datetime(2023, 10, 27, 23, 45, 12)]
    invalid_datetime_range = [
        datetime(2023, 10, 26, 12, 34, 56), time(23, 45, 12)]  # Invalid format
    check_datetime_inside = datetime(2023, 10, 27, 15, 0, 0)
    check_datetime_outside = datetime(2023, 10, 25, 5, 0, 0)

    assert utilities.is_datetime_in_datetime_range(
        check_datetime_inside, valid_datetime_range) is True
    assert utilities.is_datetime_in_datetime_range(
        check_datetime_outside, valid_datetime_range) is False
    assert utilities.is_datetime_in_datetime_range(
        check_datetime_inside, invalid_datetime_range) is False


def test_minilogger_info():
    utilities.MiniLogger.info("test_minilogger_info")


def test_minilogger_error():
    utilities.MiniLogger.error("test_minilogger_error")
