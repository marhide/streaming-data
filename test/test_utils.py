from src.utils import init_env_vars, format_result, create_request
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
    expected_api_key = 'test'
    test_api_key = getenv('api_key')
    assert test_api_key == expected_api_key

#test format_result

def test_format_result_returns_dict_when_given_correct_input():
    test_input = {
    'webPublicationDate': 'test_webPublicationDate',
    'webTitle': 'test_webTitle',
    'webUrl': 'test_webUrl'
    }

    results = format_result(test_input)
    assert isinstance(results, dict)

def test_format_result_returns_dict_with_three_kvs_when_given_correct_input():
    test_input = {
    'webPublicationDate': 'test_webPublicationDate',
    'webTitle': 'test_webTitle',
    'webUrl': 'test_webUrl'
    }

    results = format_result(test_input)
    assert len(results) == 3

#test create_request

def test_create_request_returns_tuple():
    request = create_request()
    assert isinstance(request, tuple)

def test_create_request_has_str_as_first_item():
    request = create_request()
    assert isinstance(request[0], str)

def test_create_request_has_dict_as_second_item():
    request = create_request()
    assert isinstance(request[1], dict)

def test_create_request_has_correct_query_url():
    request = create_request()
    expected = 'https://content.guardianapis.com/search?'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_search_term():
    search_term = 'machine learning'
    request = create_request(search_term)
    expected = 'https://content.guardianapis.com/search?q=machine%20learning'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_only_date_from():
    date_from = '2023-01-01'
    request = create_request(date_from=date_from)
    expected = 'https://content.guardianapis.com/search?&from-date=2023-01-01'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_search_term_and_date_from():
    search_term = 'machine learning'
    date_from = '2023-01-01'
    request = create_request(search_term, date_from)
    expected = 'https://content.guardianapis.com/search?q=machine%20learning&from-date=2023-01-01'
    assert request[0] == expected