from src.init_env import init_environment
from os import environ

init_environment()

def test_init_environment_creates_correct_enivronmental_deafault_url():
    expected_default_url = 'https://content.guardianapis.com/search'
    test_default_url = environ['deafault_url']

    assert test_default_url == expected_default_url

def test_init_environment_creates_correct_enivronmental_response_format():
    expected_response_format = 'json'
    test_response_format = environ['response_format']

    assert test_response_format == expected_response_format

def test_init_environment_creates_correct_enivronmental_api_key():
    expected_api_key = 'test'
    test_api_key = environ['api_key']

    assert test_api_key == expected_api_key