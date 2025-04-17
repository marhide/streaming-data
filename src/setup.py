from os import getenv, environ
from pathlib import Path
from configparser import ConfigParser


def create_secret_config(api_key=None, queue_name=None):

    secret_config_path = Path('secret_config.ini')
    
    if not secret_config_path.exists():

        if api_key is None:
            api_key = input('No Guardian API key found!\nPlase enter your Guardian API key:')

        if queue_name is None:
            queue_name = input('What should the SQS queue be named?')

        content = '[secrets]\nguardian_api_key = ' + api_key + '\nqueue_name = ' + queue_name

        with open('secret_config.ini', 'w', encoding='utf-8') as file:
            print(content)
            file.write(content)


def init_env_vars():

    config_files_to_read = [
        'config.ini', 
        'secret_config.ini'
        ]

    config = ConfigParser()
    config.read(config_files_to_read)

    environ['response_format'] = config['config']['response_format']
    environ['deafault_url'] = config['config']['deafault_url']
    environ['message_id'] = config['config']['message_id']

    #secret
    environ['api_key'] = config['secrets']['guardian_api_key']
    environ['queue_name'] = config['secrets']['queue_name']


def create_secrets_tfvars_file():
    filepath = './terraform/secrets.auto.tfvars'
    content = 'queue_name = "' + getenv('queue_name') + '"'

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def setup_env(api_key=None, queue_name=None):
    create_secret_config(api_key, queue_name)
    init_env_vars()
    create_secrets_tfvars_file()


if __name__ == '__main__':
    setup_env('test_api_key', 'test_queue_name')