import os
from configparser import ConfigParser


environ_list = [
    'api_key', 
    'queue_name',
    'response_format',
    'message_id',
    'default_url',
    'default_search_term',
    'default_from_date',
    'default_sort_by',
    'default_sort_order'
    ]


def set_env_vars():
    '''Reads values from the config file and sets them as environmental variables.'''
    config = ConfigParser()
    config.read("config.ini")

    for item in environ_list:
        if item in config['config']:
            os.environ[item] = config['config'][item]


def set_secret_env_vars(api_key=None, queue_name=None):
    '''Sets it's given arguments as environmental variables. Prompts the user to input them if not passed any.'''
    if api_key is None:
        api_key = input("enter your Guardian API key: ")

    if queue_name is None:
        queue_name = input("enter the SQS queue name: ")

    os.environ["api_key"] = api_key
    os.environ["queue_name"] = queue_name + ".fifo"


def create_secrets_tfvars_file(queue_name=None):
    '''Function used by the Makefile to create a .tfvars file containing the name of the SQS queue.'''
    if queue_name is None:
        queue_name = os.getenv("queue_name")

    filepath = "./terraform/secrets.auto.tfvars"
    content = 'queue_name = "' + queue_name + '"'

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def deactivate():
    '''Deletes the tfvars file if it exists and removes at environmental variables set by the running the application'''
    tfvars_secrets_path = "./terraform/secrets.auto.tfvars"

    if os.path.exists(tfvars_secrets_path):
        os.remove(tfvars_secrets_path)

    for item in environ_list:
        if item in os.environ:
            try:
                os.environ.pop(item)
            except:
                raise Exception(f"{item} has not been set as an os.environ")
            
    print('\ndeactivation successful')


class SetupEnv():
    def __init__(self, api_key, queue_name):
        self.api_key = api_key
        self.queue_name = queue_name

    def __enter__(self):
        set_env_vars()
        set_secret_env_vars(self.api_key, self.queue_name)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        deactivate()
