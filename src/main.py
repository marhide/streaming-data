from pprint import pprint
from os import getenv
from datetime import date
import json

import boto3

try:
    from src.get_message_from_api_request import get_message
    from src.setup import SetupEnv
except ImportError:
    from get_message_from_api_request import get_message
    from setup import SetupEnv


def input_search_term():
    search_term = input("enter search term: ").strip()

    if search_term == "":
        search_term = getenv("default_search_term")

    return search_term


def validate_date(date_text):
    try:
        date.fromisoformat(date_text)
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def input_from_date():
    counter = 0
    while True:
        counter += 1
        from_date = input("enter from date in format yyyy-mm-dd: ").strip()
        if from_date == "":
            return None
        try:
            validate_date(from_date)
            return from_date
        except:
            print("incorrect date format")
            if counter >= 3:
                print("hint: leave blank for no from date limit in search results")


def get_queue(name):

    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=name)

    return queue


def send_message_to_queue(queue, message_body, message_attributes={}):

    group_id = getenv("message_id")

    response = queue.send_message(
        MessageBody=message_body,
        MessageAttributes=message_attributes,
        MessageGroupId=group_id,
    )

    return response


def run_app(api_key=None, queue_name=None):
    with SetupEnv(api_key=api_key, queue_name=queue_name):
        try:
            search_term = input_search_term()
            from_date = input_from_date()
            message = get_message(search_term, from_date)

            queue_name = getenv("queue_name")
            queue = get_queue(queue_name)

            response = send_message_to_queue(queue, message)
            return response

        except:
            raise Exception("Something has gone wrong.")


if __name__ == "__main__":
    api_key = getenv('GUARDIAN_API_KEY')
    queue_name = getenv('SQS_QUEUE_NAME')
    responose = run_app(api_key, queue_name)