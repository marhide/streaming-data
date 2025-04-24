from src.main import get_queue, send_message_to_queue
from src.setup import set_env_vars, set_secret_env_vars
from moto import mock_aws

import boto3
import os

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
