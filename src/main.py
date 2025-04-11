from configparser import ConfigParser
import requests


config = ConfigParser()
config.read('secrets.ini')
guardian_api_key = config['secrets']['guardian_api_key']

url = 'https://content.guardianapis.com/search?api-key=' + guardian_api_key


print(guardian_api_key)


r = requests.get(url)
print(r)