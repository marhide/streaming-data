from src.main import get_status_code, create_request
from src.init_env import init_environment

init_environment()

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
    expected = 'https://content.guardianapis.com/search'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_search_term():
    search_term = 'machine learning'
    request = create_request(search_term)
    expected = 'https://content.guardianapis.com/search?q=machine%20learning'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_only_date_from():
    date_from = '2023-01-01'
    request = create_request(date_from=date_from)
    expected = 'https://content.guardianapis.com/search&from-date=2023-01-01'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_search_term_and_date_from():
    search_term = 'machine learning'
    date_from = '2023-01-01'
    request = create_request(search_term, date_from)
    expected = 'https://content.guardianapis.com/search?q=machine%20learning&from-date=2023-01-01'
    assert request[0] == expected

#test get_response_code

def test_get_status_code_returns_int():
    status_code = get_status_code()
    assert isinstance(status_code, int)

def test_get_status_code_returns_200():
    excepted = 200
    status_code = get_status_code()
    assert status_code == excepted

def test_get_status_code_returns_200_when_given_query():
    search_term = 'machine learning'
    date_from = '2023-01-01'
    request = create_request(search_term, date_from)
    status_code = get_status_code(request)
    assert status_code == 200