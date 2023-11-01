from __future__ import annotations
import json
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.constants import *  # noqa: E402
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402


logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)


class OurObject:

    def __init__(self, **kwargs):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME, object={'kwargs': kwargs})
        self.kwargs = kwargs
        logger.end(INIT_METHOD_NAME, object={'kwargs': kwargs})

    def get(self, attr_name: str):
        arguments = getattr(self, 'kwargs', None)
        value = arguments.get(attr_name, None)
        return value

    def get_all_arguments(self):
        return getattr(self, 'kwargs', None)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def from_json(self, json_string: str) -> OurObject:
        self.__dict__ = json.loads(json_string)
        return self

    def __eq__(self, other) -> bool:
        if not isinstance(other, OurObject):
            return False
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    # TODO Shall we call it get_http_headers()? create_http_headers()?
    def make_header(self, jwt_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
        }
        return headers
