from src.main import get_status_code

def test_get_response_code_returns_int():
    response = get_status_code()
    assert isinstance(response, int)

def test_get_response_code_returns_200():
    response = get_status_code()
    assert response == 200