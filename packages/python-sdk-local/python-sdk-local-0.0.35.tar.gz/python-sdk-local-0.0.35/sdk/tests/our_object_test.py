import sys
import os
from dotenv import load_dotenv

sys.path.append(os.getcwd())
from python_sdk_local.sdk.src import our_object  # noqa: E402
from python_sdk_local.sdk.src.constants import *  # noqa: E402
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_TEST)


def test_our_object():
    TEST_OUR_OBJECT_FUNCTION_NAME = "test_our_object"
    logger.start(TEST_OUR_OBJECT_FUNCTION_NAME)

    our_object_1 = our_object.OurObject(a=1, b="Our Object Test")
    our_object_2 = our_object.OurObject(a=1, b="Our Object Test")
    our_object_3 = our_object.OurObject(a="Object3", b=3)

    # Test == and != operators
    assert our_object_1 == our_object_2
    assert our_object_1 != our_object_3

    # Test get() method
    a1 = our_object_1.get('a')
    a2 = our_object_2.get('a')
    a3 = our_object_3.get('a')
    b1 = our_object_1.get('b')
    b2 = our_object_2.get('b')
    b3 = our_object_3.get('b')

    assert a1 == a2 == 1
    assert a3 == "Object3"
    assert b1 == b2 == "Our Object Test"
    assert b3 == 3

    # Test get_all_arguments() method
    assert our_object_1.get_all_arguments() == {'a': 1, 'b': 'Our Object Test'}
    assert our_object_2.get_all_arguments() == {'a': 1, 'b': 'Our Object Test'}
    assert our_object_3.get_all_arguments() == {'a': 'Object3', 'b': 3}

    # Test to_json() and from_json() methods
    our_object_1_json = our_object_1.to_json()
    our_object_2_json = our_object_2.to_json()
    our_object_3_json = our_object_3.to_json()
    assert our_object_1_json == '{"kwargs": {"a": 1, "b": "Our Object Test"}}'
    assert our_object_2_json == '{"kwargs": {"a": 1, "b": "Our Object Test"}}'
    assert our_object_3_json == '{"kwargs": {"a": "Object3", "b": 3}}'

    our_object4 = our_object.OurObject()
    our_object5 = our_object.OurObject()
    our_object6 = our_object.OurObject()
    assert our_object4.from_json(our_object_1_json) == our_object_1
    assert our_object5.from_json(our_object_2_json) == our_object_2
    assert our_object6.from_json(our_object_3_json) == our_object_3

    # Test make_header
    header = our_object_1.make_header(logger.userContext.get_user_JWT())
    assert 'Authorization' in header

    logger.end(TEST_OUR_OBJECT_FUNCTION_NAME)
