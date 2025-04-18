from src.setup import set_env_vars
from os import getenv

import pytest

set_env_vars()
running_locally = getenv("GITHUB_ACTIONS") == None

#test set_env_vars

def test_set_env_vars_creates_correct_enivronmental_default_url():
    expected_default_url = 'https://content.guardianapis.com/search?'
    test_default_url = getenv('default_url')
    assert test_default_url == expected_default_url

def test_set_env_vars_creates_correct_enivronmental_response_format():
    expected_response_format = 'json'
    test_response_format = getenv('response_format')
    assert test_response_format == expected_response_format

@pytest.mark.skipif(running_locally, reason='test only checks for mock api key in github actions')
def test_set_env_vars_creates_correct_enivronmental_api_key():
    expected_api_key = 'test'
    test_api_key = getenv('api_key')
    assert test_api_key == expected_api_key