import sys
import os
from datetime import time, datetime, timedelta, date
import re
from dotenv import load_dotenv
sys.path.append(os.getcwd())
from .constants import *  # noqa: E402¸
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)
loggers = {}


def timedelta_to_time_format(timedelta: timedelta) -> str:
    """
    Convert a timedelta to a time format in HH:MM:SS.

    Parameters:
        timedelta (datetime.timedelta): The timedelta to be converted.

    Returns:
        str: A string in HH:MM:SS format representing the time duration.

    Example:
        Usage of timedelta_to_time_format:

        >>> from datetime import timedelta
        >>> duration = timedelta(hours=2, minutes=30, seconds=45)
        >>> formatted_time = timedelta_to_time_format(duration)
        >>> print(formatted_time)
        '02:30:45'
    """
    TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "timedelta_to_time_format"
    logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)

    # Calculate the total seconds and convert to HH:MM:SS format
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    logger.end(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME,
               object={'formatted_time': formatted_time})
    return formatted_time


def is_valid_time_range(time_range: tuple) -> bool:
    """
    Validate that the time range is in the format 'HH:MM:SS'.
    """
    IS_VALID_TIME_RANGE_METHOD_NAME = "is_valid_time_range"
    logger.start(IS_VALID_TIME_RANGE_METHOD_NAME,
                 object={"time_range": time_range})
    if len(time_range) != 2:
        logger.end(IS_VALID_TIME_RANGE_METHOD_NAME, object={
                   "is_valid_time_range_result": False, "reason": "len(time_range) != 2"})
        return False

    for time_obj in time_range:
        if not isinstance(time_obj, time):
            logger.end(IS_VALID_TIME_RANGE_METHOD_NAME, object={
                "is_valid_time_range_result": False, "reason": "time_range contains non-time objects"})
            return False
    logger.end(IS_VALID_TIME_RANGE_METHOD_NAME, object={
               "is_valid_time_range_result": True})
    return True


def is_valid_date_range(date_range: tuple) -> bool:
    """
    Validate that the date range is in the format 'YYYY-MM-DD'.
    """
    IS_VALID_DATE_RANGE_METHOD_NAME = "is_valid_date_range"
    logger.start(IS_VALID_DATE_RANGE_METHOD_NAME,
                 object={"date_range": date_range})
    if len(date_range) != 2:
        logger.end(IS_VALID_DATE_RANGE_METHOD_NAME, object={
                   "is_valid_date_range_result": False, "reason": "len(date_range) != 2"})
        return False

    for date_obj in date_range:
        if not isinstance(date_obj, date):
            logger.end(IS_VALID_DATE_RANGE_METHOD_NAME, object={
                "is_valid_date_range_result": False, "reason": "date_range contains non-date objects"})
            return False
    logger.end(IS_VALID_DATE_RANGE_METHOD_NAME, object={
               "is_valid_date_range_result": True})
    return True


def is_valid_datetime_range(datetime_range: tuple) -> bool:
    """
    Validate that the datetime range is in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    IS_VALID_DATETIME_RANGE_METHOD_NAME = "is_valid_datetime_range"
    logger.start(IS_VALID_DATETIME_RANGE_METHOD_NAME,
                 object={"datetime_range": datetime_range})
    if len(datetime_range) != 2:
        logger.end(IS_VALID_DATETIME_RANGE_METHOD_NAME, object={
                   "is_valid_datetime_range_result": False, "reason": "len(datetime_range) != 2"})
        return False

    for datetime_obj in datetime_range:
        if not isinstance(datetime_obj, datetime):
            logger.end(IS_VALID_DATETIME_RANGE_METHOD_NAME, object={
                "is_valid_datetime_range_result": False, "reason": "datetime_range contains non-datetime objects"})
            return False
    logger.end(IS_VALID_DATETIME_RANGE_METHOD_NAME, object={
               "is_valid_datetime_range_result": True})
    return True


def is_list_of_dicts(obj):
    """
    Check if an object is a list of dictionaries.

    Parameters:
        obj (object): The object to be checked.

    Returns:
        bool: True if the object is a list of dictionaries, False otherwise.

    Example:
        Usage of is_list_of_dicts:

        >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> result = is_list_of_dicts(data)
        >>> print(result)
        True

        >>> data = [1, 2, 3]
        >>> result = is_list_of_dicts(data)
        >>> print(result)
        False
    """
    IS_LIST_OF_DICTS_FUNCTION_NAME = "is_list_of_dicts"
    logger.start(IS_LIST_OF_DICTS_FUNCTION_NAME, object={"obj": obj})
    try:
        if not isinstance(obj, list):
            is_list_of_dicts_result = False
            logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={
                       "is_list_of_dicts_result": is_list_of_dicts_result})
            return is_list_of_dicts_result
        for item in obj:
            if not isinstance(item, dict):
                is_list_of_dicts_result = False
                logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={
                           "is_list_of_dicts_result": is_list_of_dicts_result})
                return is_list_of_dicts_result
        is_list_of_dicts_result = True
        logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={
                   "is_list_of_dicts_result": is_list_of_dicts_result})
        return is_list_of_dicts_result
    except Exception as e:
        logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, exception=e)
        raise e


def is_time_in_time_range(check_time: time, time_range: tuple) -> bool:
    """
    Check if the given time is within the specified time range.

    Parameters:
        check_time (str): The time to check in 'HH:MM:SS' format.
        time_range (tuple): A tuple containing start and end times in 'HH:MM:SS' format.

    Returns:
        bool: True if the check_time is within the time range, False otherwise.
    """
    if not is_valid_time_range(time_range) or not isinstance(check_time, time):
        return False
    
    start_time, end_time = time_range
    return start_time <= check_time <= end_time


def is_date_in_date_range(check_date: date, date_range: tuple) -> bool:
    """
    Check if the given date is within the specified date range.

    Parameters:
        check_date (str): The date to check in 'YYYY-MM-DD' format.
        date_range (tuple): A tuple containing start and end dates in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the check_date is within the date range, False otherwise.
    """
    if not is_valid_date_range(date_range) or not isinstance(check_date, date):
        return False

    start_date, end_date = date_range
    return start_date <= check_date <= end_date


def is_datetime_in_datetime_range(check_datetime: datetime, datetime_range: tuple) -> bool:
    """
    Check if the given datetime is within the specified datetime range.

    Parameters:
        check_datetime (str): The datetime to check in 'YYYY-MM-DD HH:MM:SS' format.
        datetime_range (tuple): A tuple containing start and end datetimes in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        bool: True if the check_datetime is within the datetime range, False otherwise.
    """

    if not is_valid_datetime_range(datetime_range) or not isinstance(check_datetime, datetime):
        return False

    start_datetime, end_datetime = datetime_range
    return start_datetime <= check_datetime <= end_datetime


class MiniLogger:

    @staticmethod
    def info(message: str, object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        PRINT_LOG_METHOD_NAME = "print_log"
        logger.start(PRINT_LOG_METHOD_NAME, object={
                     "message": message, "object": object})
        if object is None:
            print(f"{datetime.datetime.now()} - {message}")
        else:
            print(f"{datetime.datetime.now()} - {message} - {object}")
        logger.end(PRINT_LOG_METHOD_NAME)

    @staticmethod
    def error(message: str, object: dict = None):
        """
        Print a log error message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        PRINT_LOG_ERROR_METHOD_NAME = "print_log_error"
        logger.start(PRINT_LOG_ERROR_METHOD_NAME, object={
                     "message": message, "object": object})
        if object is None:
            print(f"{datetime.datetime.now()} - ERROR - {message}",
                  file=sys.stderr)
        else:
            print(
                f"{datetime.datetime.now()} - ERROR - {message} - {object}", file=sys.stderr)
        logger.end(PRINT_LOG_ERROR_METHOD_NAME)
