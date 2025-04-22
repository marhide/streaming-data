from src.get_message_from_api_request import get_message
from src.setup import setup_env
from src.utils import validate_date

from pprint import pprint
import boto3
from os import getenv
import os


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


def input_search_terms():
    search_term = input('enter search term: ')
    from_date = input('enter from date in format yyyy-mm-dd: ')

    validate_date(from_date)

    if search_term == '':
        search_term = getenv('default_search_term')

    return {'search_term': search_term, 'from_date': from_date}


def deactivate():

    os.remove('./terraform/secrets.auto.tfvars')

    environ_list = [
        'api_key',
        'queue_name',
        'response_format',
        'message_id',
        'default_url',
        'default_search_term',
        'default_from_date',
        'default_sort_by',
        'default_sort_order'
        ]

    for item in environ_list:

        try:
            os.environ.pop(item)

        except:
            raise Exception(f'{item} has not been set as an environ')


if __name__ == '__main__':

    try:
        setup_env()

        message = get_message(**input_search_terms())

        queue_name = getenv('queue_name')
        queue = get_queue(queue_name)

        response = send_message_to_queue(queue, message)
        pprint(response)

    except:
        raise Exception('Something has gone wrong.')
    
    finally:
        deactivate()