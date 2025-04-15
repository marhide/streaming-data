
from src.utils import init_env_vars, create_secret_config, format_result, create_request
import requests
from pprint import pprint
import json
import boto3


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


if __name__ == '__main__':
    create_secret_config()
    init_env_vars()

    search_term = 'machine learning'
    date_from = '2023-01-01'

    request = create_request(search_term, date_from)

    # status_code = get_status_code(request)
    results = get_results(request)

    # print(f'status code: {status_code}')
    # print(f'results: {results}')

    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

    queue.send_message(MessageBody='test_body')