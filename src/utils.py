from configparser import ConfigParser
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