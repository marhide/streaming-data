from src.utils import init_env_vars, create_secret_config, create_secrets_tfvars_file
from src.get_message_from_api_request import get_message, create_request

import requests
from pprint import pprint
import boto3
from os import getenv


def get_status_code(request=None):

    if request == None:
        request = create_request()

    response = requests.get(*request)
    status_code = response.status_code

    return status_code


def send_message_to_queue(queue, message_body, message_attributes=None):

    if not message_attributes:
        message_attributes = {}

    response = queue.send_message(
        MessageBody=message_body, MessageAttributes=message_attributes
    )
    
    return response


def get_queue(name):

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)

    return queue


if __name__ == '__main__':
    create_secret_config()
    init_env_vars()
    create_secrets_tfvars_file()

    search_term = 'machine learning'
    date_from = '2023-01-01'
    message_id = getenv('message_id')

    message = get_message(search_term, date_from)

    queue_name = getenv('queue_name')
    queue = get_queue(queue_name)

    response = send_message_to_queue(queue, message)
    pprint(response)