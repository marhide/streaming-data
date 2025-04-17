from src.utils import init_env_vars, create_secret_config, format_result, create_request, create_message
import requests
from pprint import pprint
import json
import boto3
from os import getenv


def get_status_code(request=None):

    if request == None:
        request = create_request()

    response = requests.get(*request)
    status_code = response.status_code
    return status_code


def get_results(request):
    response = requests.get(*request)
    content = json.loads(response.text)

    results = content['response']['results']
    formatted_results = [format_result(result) for result in results]

    return formatted_results


def send_message(queue, message_body, message_attributes=None):

    if not message_attributes:
        message_attributes = {}

    response = queue.send_message(
        MessageBody=message_body, MessageAttributes=message_attributes
    )
    pprint(response)


def get_queue(name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)
    return queue


if __name__ == '__main__':
    create_secret_config()
    init_env_vars()

    search_term = 'machine learning'
    date_from = '2023-01-01'

    request = create_request(search_term, date_from)
    results = get_results(request)
    message = create_message(request, results)

    queue_name = getenv('queue_name')
    new_queue = get_queue(queue_name)

    send_message(new_queue, message)