from configparser import ConfigParser
from pathlib import Path
from os import environ

def init_env_vars():

    config_files_to_read = [
        'config.ini', 
        'secret_config.ini'
        ]

    config = ConfigParser()
    config.read(config_files_to_read)

    environ['api_key'] = config['secrets']['guardian_api_key']
    environ['response_format'] = config['headers']['response_format']
    environ['deafault_url'] = config['url']['deafault_url']

def create_secrets_config():
    secrets_config_path = Path('secret_config.ini')
    
    if not secrets_config_path.exists():
        new_api_key = input('No Guardian API key found!\nPlase enter your Guardian API key:')

        with open('secret_config.ini', 'w', encoding='utf-8') as file:
            file.write('[secrets]\nguardian_api_key = '+ new_api_key)