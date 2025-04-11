from os import environ
from src.init_env import init_environment
import requests

def get_request():
    request = (
        environ['deafault_url'], 
        {
            'api-key': environ['api_key'],
            'format': environ['response_format']
        }
    )
    return request


def get_status_code():
    request = get_request()
    response = requests.get(*request)
    return response.status_code


if __name__ == '__main__':
    init_environment()
    print(f'status code: {get_status_code()}')