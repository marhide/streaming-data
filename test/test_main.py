from src.main import get_status_code, create_request
from src.setup import set_env_vars

set_env_vars()

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