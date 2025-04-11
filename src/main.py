from configparser import ConfigParser
import requests

config = ConfigParser()
config.read('secrets.ini')
api_key = config['secrets']['guardian_api_key']

url = 'https://content.guardianapis.com/search'

_headers = {
    'api-key': api_key,
    'format': 'json'
}

r = requests.get(url, _headers)
print(r.status_code)