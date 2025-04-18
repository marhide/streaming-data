from src.get_message_from_api_request import get_message, create_request
from src.setup import setup_env

import requests
from pprint import pprint
import boto3
from os import getenv
import os


def get_status_code(request=None):

    if request == None:
        request = create_request()

    response = requests.get(*request)
    status_code = response.status_code

    return status_code


def get_queue(name):

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)

    return queue


def send_message_to_queue(queue, message_body, message_attributes={}):

    group_id = getenv('message_id')

    response = queue.send_message(
        MessageBody=message_body, MessageAttributes=message_attributes, MessageGroupId=group_id
    )
    
    return response


def deactivate():

    # os.remove('secret_config.ini')
    os.remove('./terraform/secrets.auto.tfvars')

    environ_list = [
        'api_key',
        'queue_name',
        'response_format',
        'message_id',
        'default_url',
        'default_search_term',
        'default_from_date'
        ]

    for item in environ_list:

        try:
            os.environ.pop(item)

        except:
            raise Exception(f'{item} has not been set as an environ')


if __name__ == '__main__':

    try:
        setup_env()

        search_term = getenv('default_search_term')
        from_date = getenv('default_from_date')


        message = get_message(search_term, from_date)

        queue_name = getenv('queue_name')
        queue = get_queue(queue_name)

        response = send_message_to_queue(queue, message)
        pprint(response)

    except:
        raise Exception('Something has gone wrong.')
    
    finally:
        deactivate()