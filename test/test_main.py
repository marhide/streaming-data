import os
from unittest import mock

import pytest

from src.main import get_queue, send_message_to_queue, run_app
from fixtures import mock_sqs, run_set_env_vars, run_set_secret_env_vars, test_api_key, test_queue_name, test_queue_url

# this fixes the tests breaking in github actions as it needs the region to be specified whilst running on there
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.mark.usefixtures('mock_sqs')
class TestGetQueue:
    def test_get_queue_returns_queue_object_wth_correct_url(self):
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

    def test_run_app_returns_status_code_200_when_passed_all_correct_args(self, _):
        response = run_app(api_key=test_api_key, queue_name=test_queue_name, search_term='test search', from_date='1999-09-09', sort_by='date', sort_order='asc')
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200