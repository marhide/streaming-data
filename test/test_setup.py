from src.setup import set_env_vars, set_secret_env_vars, create_secrets_tfvars_file
from os import getenv, path
from src.main import deactivate

import pytest

set_env_vars()
set_secret_env_vars('test', 'test_queue_name')
running_locally = getenv("GITHUB_ACTIONS") == None

#test set_env_vars

def test_set_env_vars_creates_correct_enivronmental_response_format():
    expected_response_format = 'json'
    test_response_format = getenv('response_format')
    assert test_response_format == expected_response_format

def test_set_env_vars_sets_correct_message_id():
    expected = 'guardian_content'
    test = getenv('message_id')
    assert test == expected

def test_set_env_vars_creates_correct_enivronmental_default_url():
    expected_default_url = 'https://content.guardianapis.com/search?'
    test_default_url = getenv('default_url')
    assert test_default_url == expected_default_url

def test_set_env_vars_sets_correct_default_search_term():
    expected_default_search_term = 'machine learning'
    test_default_search_term = getenv('default_search_term')
    assert expected_default_search_term == test_default_search_term

def test_set_env_vars_sets_correct_default_from_date():
    expected = '1900-01-01'
    test_default_from_date = getenv('default_from_date')
    assert test_default_from_date == expected

#test set_secret_env_vars

def test_set_secret_env_vars_creates_correct_enivronmental_api_key():
    expected_api_key = 'test'
    test_api_key = getenv('api_key')
    assert test_api_key == expected_api_key

def test_secret_set_env_vars_creates_correct_env_q_name():
    expected_queue_name = 'test_queue_name.fifo'
    test_queue_name = getenv('queue_name')
    assert test_queue_name == expected_queue_name

#test create_secret_tfvars_file

def test_create_tfvars_file_creates_a_file():
    create_secrets_tfvars_file()
    assert path.exists('./terraform/secrets.auto.tfvars')
    deactivate()

def test_create_tfvars_file_has_correct_conent():
    set_env_vars()
    set_secret_env_vars('test_999', 'test_queue_name_999')
    create_secrets_tfvars_file()
    with open('./terraform/secrets.auto.tfvars', 'r', encoding='utf-8') as test_file_content:
        assert test_file_content.read() == 'queue_name = "test_queue_name_999.fifo"'
        deactivate()
    

