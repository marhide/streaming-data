import pytest
import moto
import boto3

from src.setup import set_env_vars, set_secret_env_vars, deactivate

test_api_key = "test"
test_queue_name = "test_queue_name"
test_queue_url = (
    f"https://sqs.eu-west-2.amazonaws.com/123456789012/{test_queue_name}.fifo"
)
test_sqs_attributes = {"FifoQueue": "True", "ContentBasedDeduplication": "True"}


@pytest.fixture(scope="function", autouse=False)
def mock_sqs():
    with moto.mock_aws():
        sqs = boto3.client("sqs")
        sqs.create_queue(
            QueueName=test_queue_name + ".fifo", Attributes=test_sqs_attributes
        )
        yield sqs
        sqs.delete_queue(QueueUrl=test_queue_url)


@pytest.fixture(scope="function", autouse=False)
def run_set_env_vars():
    deactivate()
    yield set_env_vars()
    deactivate()


@pytest.fixture(scope="function", autouse=False)
def run_set_secret_env_vars():
    deactivate()
    yield set_secret_env_vars(api_key=test_api_key, queue_name=test_queue_name)
    deactivate()


@pytest.fixture(scope="function", autouse=False)
def run_set_all_env_vars():
    deactivate()
    yield set_env_vars(), set_secret_env_vars(
        api_key=test_api_key, queue_name=test_queue_name
    )
    deactivate()
