from configparser import ConfigParser
from pathlib import Path
from os import environ


def create_secret_config():

    secret_config_path = Path('secret_config.ini')
    
    if not secret_config_path.exists():
        new_api_key = input('No Guardian API key found!\nPlase enter your Guardian API key:')

        with open('secret_config.ini', 'w', encoding='utf-8') as file:
            file.write('[secrets]\nguardian_api_key = '+ new_api_key)


def init_env_vars():

    config_files_to_read = [
        'config.ini', 
        'secret_config.ini'
        ]

    config = ConfigParser()
    config.read(config_files_to_read)

    environ['api_key'] = config['secrets']['guardian_api_key']
    environ['response_format'] = config['config']['response_format']
    environ['deafault_url'] = config['config']['deafault_url']
    environ['queue_name'] = config['config']['queue_name']

def create_request(search_term=None, date_from=None):

    query = ''

    if search_term:
        search_term = 'q=' + search_term.replace(' ', '%20')
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


def format_result(result):
    
    formatted_result = {
    'webPublicationDate': result['webPublicationDate'],
    'webTitle': result['webTitle'],
    'webUrl': result['webUrl']
    }

    return formatted_result