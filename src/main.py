from os import environ
from src.utils import init_env_vars, create_secret_config, format_result
import requests
from pprint import pprint
import json

def create_request(search_term=None, date_from=None):

    query = ''

    if search_term:
        search_term = '?q=' + search_term.replace(' ', '%20')
        query += search_term

    if date_from:
        date_from = '&from-date=' + date_from
        query += date_from

    url = environ['deafault_url'] + query

    request = (
        url,
        {
            'api-key': environ['api_key'],
            'format': environ['response_format']
        }
    )

    return request

def get_status_code(request=None):

    if request == None:
        request = create_request()

    response = requests.get(*request)
    status_code = response.status_code
    return status_code

def get_content(request):
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

    status_code = get_status_code(request)
    content = get_content(request)

    print(f'status code: {status_code}')

    print(f'conent: {content}')