from os import getenv, environ
from configparser import ConfigParser


def set_env_vars():

    config = ConfigParser()
    config.read('config.ini')

    environ['response_format'] = config['config']['response_format']
    environ['message_id'] = config['config']['message_id']
    environ['default_url'] = config['config']['default_url']
    environ['default_search_term'] = config['config']['default_search_term']
    environ['default_from_date'] = config['config']['default_from_date']


def set_secret_env_vars(api_key=None, queue_name=None):

    if api_key is None:
        api_key = input('Enter your Guardian API key:')

    if queue_name is None:
        queue_name = input('Choose a name for the SQS queue:')

    environ['api_key'] = api_key
    environ['queue_name'] = queue_name + '.fifo'


# class FileWriter(object):
#     def __init__(self, file_name):
#         self.file_name = file_name

#     def __enter__(self):
#         self.file = open(self.file_name, "w")
#         return self.file

#     def __exit__(self, exception_type, exception_value, traceback):
#         self.file.close()


def create_secrets_tfvars_file():
    filepath = './terraform/secrets.auto.tfvars'
    content = 'queue_name = "' + getenv('queue_name') + '"'

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def setup_env(api_key=None, queue_name=None):
    set_env_vars()
    set_secret_env_vars(api_key, queue_name)
    create_secrets_tfvars_file()


if __name__ == '__main__':
    setup_env()