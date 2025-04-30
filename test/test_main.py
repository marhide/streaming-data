import os
from unittest import mock

import pytest
import boto3
import moto

from src.main import get_queue, send_message_to_queue, input_search_term, input_from_date, run_app
from fixtures import mock_sqs, run_set_env_vars, run_set_secret_env_vars, test_api_key, test_queue_name, test_queue_url

# this fixes the tests breaking in github actions as it needs the region to be specified whilst running on there
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

# test_api_key = 'test'
# test_queue_name = 'test_queue_name'
# test_queue_url = f'https://sqs.eu-west-2.amazonaws.com/123456789012/{test_queue_name}.fifo'


@pytest.mark.usefixtures('mock_sqs')
class TestGetQueue:
    def test_get_queue_returns_queue_object(self):
        test_queue = get_queue(test_queue_name+'.fifo')
        assert test_queue.url == test_queue_url


@pytest.mark.usefixtures('mock_sqs')
@pytest.mark.usefixtures('run_set_env_vars')
class TestSendMessageToQueue:
    def test_send_message_to_queue_returns_status_code_200_when_given_a_queue_obj_and_correct_message(self):
        test_queue = get_queue(test_queue_name+'.fifo')
        test_message = str({"header": "body"})

        response = send_message_to_queue(test_queue, test_message)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def test_send_message_to_queue_sends_the_correct_message_to_the_queue(self, mock_sqs):
        test_queue = get_queue(test_queue_name+'.fifo')
        test_message = str({"test_header": "test_body"})

        send_message_to_queue(test_queue, test_message)
        recieved_message = mock_sqs.receive_message(QueueUrl=test_queue_url)
        assert recieved_message['Messages'][0]['Body'] == test_message


@mock.patch('src.main.input', create=True)
class TestInputSearchTerm:
    def test_input_search_term_returns_correct_search_term_that_is_input(self, mocked_input):
        mocked_input.side_effect = ['test search']
        result = input_search_term()
        assert result == 'test search'

    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['test search with space at the end ']
        result = input_search_term()
        assert result == 'test search with space at the end'

    @pytest.mark.usefixtures('run_set_env_vars')
    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_search_term()
        assert result == 'machine learning'


@mock.patch('src.main.input', create=True)
class TestInputFromDate:
    def test_input_from_date_returns_correct_date_when_input_correct_date(self, mocked_input):
        mocked_input.side_effect = ['2000-01-01']
        result = input_from_date()
        assert result == '2000-01-01'

    def test_input_from_date_returns_none_when_given_empty_str(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_from_date()
        assert result is None

    def test_input_from_date_returns_correct_date_when_given_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date', '1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'

    def test_input_from_date_returns_correct_date_when_given_many_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date' for _ in range(9)] + ['1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'


@mock.patch('builtins.input', create=True)
@pytest.mark.usefixtures('mock_sqs')
class TestRunApp:
    def test_run_app_returns_status_code_200_when_given_correct_args_and_test_inputs(self, mocked_input):
        mocked_input.side_effect = ['test search', '2000-01-01',]
        response = run_app(api_key=test_api_key, queue_name=test_queue_name)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def test_run_app_returns_status_code_200_when_given_no_args_and_corrrect_inputs(self, mocked_input):
        mocked_input.side_effect = [test_api_key, test_queue_name, 'test search', '2000-01-01']
        response = run_app()
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200