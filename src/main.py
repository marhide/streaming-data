from configparser import ConfigParser
import requests

config_files_to_read = [
    'config.ini', 
    'secret_config.ini'
    ]

config = ConfigParser()
config.read(config_files_to_read)

api_key = config['secrets']['guardian_api_key']
response_format = config['headers']['format']
url = config['url']['deafault_url']

headers = {
    'api-key': api_key,
    'format': response_format
}

def get_status_code():
    response = requests.get(url, headers)
    return response.status_code