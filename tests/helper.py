# pylint: disable=W1514

"""Helper module."""

import json
import os

from tests.mock_repository import get_mock_repository

TEST_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_ROOT_DIR, "data")
TEST_QUIZ_DATA_DIR = os.path.join(TEST_DATA_DIR, "quiz")


def get_entity(data_file, model):
    """Construct an object given json data file and a model.
    :param data_file: json datas file
    :param model: given model i.e. NewQuiz, Quiz etc.
    :return: constructed entity"""

    file_path = os.path.join(TEST_QUIZ_DATA_DIR, data_file)
    with open(file_path, "r") as file_handle:
        json_data = json.load(file_handle)
        entity = model(**json_data)
        return entity


def get_quiz_json_data(quiz_id: int):
    """Loads json data for a quiz given quiz id.
    :param quiz_id: quiz id to load
    :return: json object representing quiz object"""

    default_id = 5
    quiz_data = get_mock_repository().quiz.get(quiz_id)
    if quiz_data is None:
        quiz_data = get_mock_repository().quiz.get(default_id)

    kwargs = {"use_db_field": False}
    result = json.loads(quiz_data.to_json(**kwargs))
    return result
