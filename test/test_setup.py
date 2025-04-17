from src.setup import init_env_vars
from os import getenv

import pytest

init_env_vars()
running_locally = getenv("GITHUB_ACTIONS") == None

#test init_env_vars

def test_init_env_vars_creates_correct_enivronmental_deafault_url():
    expected_default_url = 'https://content.guardianapis.com/search?'
    test_default_url = getenv('deafault_url')
    assert test_default_url == expected_default_url

def test_init_env_vars_creates_correct_enivronmental_response_format():
    expected_response_format = 'json'
    test_response_format = getenv('response_format')
    assert test_response_format == expected_response_format

@pytest.mark.skipif(running_locally, reason='test only checks for mock api key in github actions')
def test_init_env_vars_creates_correct_enivronmental_api_key():
    expected_api_key = 'test_api_key'
    test_api_key = getenv('api_key')
    assert test_api_key == expected_api_key