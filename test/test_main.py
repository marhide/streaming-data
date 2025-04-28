import os
from unittest import mock
from pprint import pprint

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


class TestSendMessageToQueue():
    @mock_aws
    def test_send_message_to_queue_returns_status_code_200_when_given_a_queue_obj_and_correct_message(self):
        mock_sqs = boto3.resource("sqs")
        test_queue_name = "mock_queue.fifo"
        test_sqs_attributes = {"FifoQueue": "True", "ContentBasedDeduplication": "True"}
        mock_sqs.create_queue(
            QueueName=test_queue_name,
            Attributes=test_sqs_attributes,
        )
        test_queue = get_queue(test_queue_name)
        test_message = str({"header": "body"})

        response = send_message_to_queue(test_queue, test_message)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    @mock_aws
    def test_send_message_to_queue_sends_the_correct_message_to_the_queue(self):
        mock_sqs = boto3.resource("sqs")
        sqs_client = boto3.client("sqs")
        test_queue_name = "mock_queue.fifo"
        test_sqs_attributes = {"FifoQueue": "True", "ContentBasedDeduplication": "True"}
        mock_sqs.create_queue(
            QueueName=test_queue_name,
            Attributes=test_sqs_attributes,
        )
        test_queue = get_queue(test_queue_name)
        test_message = str({"test_header": "test_body"})

        send_message_to_queue(test_queue, test_message)
        recieved_message = sqs_client.receive_message(QueueUrl=test_queue_name)
        assert recieved_message['Messages'][0]['Body'] == test_message


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