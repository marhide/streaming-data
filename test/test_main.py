import os
from unittest import mock

import boto3
from moto import mock_aws

from src.main import get_queue, send_message_to_queue, input_search_term, input_from_date
from src.setup import set_env_vars, set_secret_env_vars


set_env_vars()
set_secret_env_vars("test", "test_queue_name")

# this fixes the tests breaking in github actions as it needs the region to be specified whilst running on there
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@mock_aws
def test_get_queue_returns_queue_object():
    test_queue_name = "mock_queue"
    mock_sqs = boto3.resource("sqs")
    mock_sqs.create_queue(QueueName=test_queue_name)
    test_queue = get_queue(test_queue_name)

    assert (
        test_queue.url == "https://sqs.eu-west-2.amazonaws.com/123456789012/mock_queue"
    )

@mock_aws
def test_send_message_to_queue_returns_status_code_200_when_given_a_queue_obj_and_correct_message():
    test_queue_name = "mock_queue.fifo"
    mock_sqs = boto3.resource("sqs")
    mock_sqs.create_queue(
        QueueName=test_queue_name,
        Attributes={"FifoQueue": "True", "ContentBasedDeduplication": "True"},
    )
    test_queue = get_queue(test_queue_name)
    test_message = str({"header": "body"})

    response = send_message_to_queue(test_queue, str(test_message))
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


class TestInputSearchTerm():
    @mock.patch('src.main.input', create=True)
    def test_input_search_term_returns_correct_search_term_that_is_input(self, mocked_input):
        mocked_input.side_effect = ['test search']
        result = input_search_term()
        assert result == 'test search'

    @mock.patch('src.main.input', create=True)
    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['test search with space at the end ']
        result = input_search_term()
        assert result == 'test search with space at the end'

    @mock.patch('src.main.input', create=True)
    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_search_term()
        assert result == 'machine learning'


class TestInputFromDate():
    @mock.patch('src.main.input', create=True)
    def test_input_from_date_returns_correct_date_when_input_correct_date(self, mocked_input):
        mocked_input.side_effect = ['2000-01-01']
        result = input_from_date()
        assert result == '2000-01-01'

    @mock.patch('src.main.input', create=True)
    def test_input_from_date_returns_none_when_given_empty_str(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_from_date()
        assert result is None

    @mock.patch('src.main.input', create=True)
    def test_input_from_date_returns_correct_date_when_given_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date', '1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'

    @mock.patch('src.main.input', create=True)
    def test_input_from_date_returns_correct_date_when_given_many_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date' for _ in range(99)] + ['1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'