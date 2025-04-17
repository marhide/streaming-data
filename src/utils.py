from configparser import ConfigParser
from pathlib import Path
from os import environ, getenv


def create_secret_config():

    secret_config_path = Path('secret_config.ini')
    
    if not secret_config_path.exists():
        new_api_key = input('No Guardian API key found!\nPlase enter your Guardian API key:')
        content = '[secrets]\nguardian_api_key = '+ new_api_key

        with open('secret_config.ini', 'w', encoding='utf-8') as file:
            file.write(content)


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
    environ['queue_name'] = config['secrets']['queue_name']
    environ['message_id'] = config['config']['message_id']


def create_secrets_tfvars_file():
    filepath = './terraform/secrets.auto.tfvars'
    content = 'queue_name = "' + getenv('queue_name') + '"'

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)