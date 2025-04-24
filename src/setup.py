from os import getenv, environ
import os
from configparser import ConfigParser


def set_env_vars():

    config = ConfigParser()
    config.read("config.ini")

    environ["response_format"] = config["config"]["response_format"]
    environ["message_id"] = config["config"]["message_id"]
    environ["default_url"] = config["config"]["default_url"]
    environ["default_search_term"] = config["config"]["default_search_term"]
    environ["default_from_date"] = config["config"]["default_from_date"]
    environ["default_sort_by"] = config["config"]["default_sort_by"]
    environ["default_sort_order"] = config["config"]["default_sort_order"]


def set_secret_env_vars(api_key=None, queue_name=None):

    if api_key is None:
        api_key = input("Enter your Guardian API key:")

    if queue_name is None:
        queue_name = input("Choose a name for the SQS queue:")

    environ["api_key"] = api_key
    environ["queue_name"] = queue_name + ".fifo"


def create_secrets_tfvars_file(queue_name=None):

    if queue_name is None:
        queue_name = getenv("queue_name")

    filepath = "./terraform/secrets.auto.tfvars"
    content = 'queue_name = "' + queue_name + '"'

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def deactivate():

    os.remove("./terraform/secrets.auto.tfvars")

    environ_list = [
        "api_key",
        "queue_name",
        "response_format",
        "message_id",
        "default_url",
        "default_search_term",
        "default_from_date",
        "default_sort_by",
        "default_sort_order",
    ]

    for item in environ_list:

        try:
            os.environ.pop(item)

        except:
            raise Exception(f"{item} has not been set as an environ")


class SetupEnv:
    def __init__(self, api_key, queue_name):
        self.api_key = api_key
        self.queue_name = queue_name

    def __enter__(self):
        set_env_vars()
        set_secret_env_vars(self.api_key, self.queue_name)
        create_secrets_tfvars_file()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        deactivate()
