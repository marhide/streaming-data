from os import getenv, environ
from pathlib import Path
from configparser import ConfigParser


def create_secret_config(api_key=None, queue_name=None):

    secret_config_path = Path('secret_config.ini')
    
    if not secret_config_path.exists():

        if api_key is None:
            api_key = input('Enter your Guardian API key:')

        if queue_name is None:
            queue_name = input('Choose a name for the SQS queue:')

        content = '[secrets]\nguardian_api_key = ' + api_key + '\nqueue_name = ' + queue_name

        with open('secret_config.ini', 'w', encoding='utf-8') as file:
            file.write(content)


def set_env_vars():

    config_files_to_read = [
        'config.ini', 
        'secret_config.ini'
        ]

    config = ConfigParser()
    config.read(config_files_to_read)

    environ['response_format'] = config['config']['response_format']
    environ['message_id'] = config['config']['message_id']
    environ['default_url'] = config['config']['default_url']
    environ['default_search_term'] = config['config']['default_search_term']
    environ['default_from_date'] = config['config']['default_from_date']

    #secret
    environ['api_key'] = config['secrets']['guardian_api_key']
    environ['queue_name'] = config['secrets']['queue_name'] + '.fifo'


def create_secrets_tfvars_file():
    filepath = './terraform/secrets.auto.tfvars'
    content = 'queue_name = "' + getenv('queue_name') + '"'

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def setup_env(api_key=None, queue_name=None):
    create_secret_config(api_key, queue_name)
    set_env_vars()
    create_secrets_tfvars_file()


if __name__ == '__main__':
    setup_env()