from os import getenv

import boto3

try:
    from src.get_message_from_api_request import get_message
    from src.user_input import input_search_term, input_from_date
    from src.setup import SetupEnv
except ImportError:
    from get_message_from_api_request import get_message
    from user_input import input_search_term, input_from_date
    from setup import SetupEnv


def get_queue(queue_name):
    '''Gets an SQS queue of a specified name from AWS.'''

    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    return queue


def send_message_to_queue(queue, message_body):
    '''Sends a message to an SQS queue and returns the response from that action.'''

    group_id = getenv("message_id")

    response = queue.send_message(
        MessageBody=message_body,
        MessageAttributes={},
        MessageGroupId=group_id,
    )

    return response


def run_app(api_key=None, queue_name=None, search_term=None, from_date=None, sort_by=None, sort_order=None):
    '''Runs the whole application'''

    with SetupEnv(api_key=api_key, queue_name=queue_name):
        try:
            search_term = input_search_term(search_term)
            from_date = input_from_date(from_date)

            message = get_message(search_term=search_term, from_date=from_date, sort_by=sort_by, sort_order=sort_order)

            queue_name = getenv("queue_name")

            print(f'api key: {api_key}\nqueue_name: {queue_name}\nsearch_term: {search_term}\nfrom_date: {from_date}\nsort_by: {sort_by}\nsort_order: {sort_order}')

            queue = get_queue(queue_name)

            response = send_message_to_queue(queue, message)
            return response

        except:
            raise Exception("Something has gone wrong.")


if __name__ == "__main__":
    api_key = getenv('GUARDIAN_API_KEY')
    queue_name = getenv('SQS_QUEUE_NAME')
    responose = run_app(api_key, queue_name)