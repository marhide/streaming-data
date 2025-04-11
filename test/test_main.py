from src.main import get_status_code
from src.init_env import init_environment

init_environment()

def test_get_response_code_returns_int():
    response = get_status_code()
    assert isinstance(response, int)

def test_get_response_code_returns_200():
    excepted = 200
    response = get_status_code()
    assert response == excepted