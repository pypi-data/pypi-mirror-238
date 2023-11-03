import os
import sys
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.mini_logger import MiniLogger



def test_minilogger_info():
    MiniLogger.info("test_minilogger_info")


def test_minilogger_error():
    MiniLogger.error("test_minilogger_error")