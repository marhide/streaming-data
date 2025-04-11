from os import environ
from src.init_env import init_environment
import requests

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
    return response.status_code


if __name__ == '__main__':
    init_environment()

    search_term = 'machine learning'
    date_from = '2023-01-01'

    request = create_request(search_term, date_from)

    status_code = get_status_code(request)

    print(f'status code: {status_code}')