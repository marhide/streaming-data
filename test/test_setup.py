import os

import pytest

from src.setup import set_env_vars, set_secret_env_vars, create_secrets_tfvars_file, SetupEnv


@pytest.fixture(scope='class', autouse=False)
def run_set_env_vars():
    set_env_vars()


@pytest.fixture(scope='class', autouse=False)
def run_set_secret_env_vars():
    set_secret_env_vars("test", "test_queue_name")


class TestSetEnvVars():
    def test_set_env_vars_creates_correct_enivronmental_response_format(self, run_set_env_vars):
        expected_response_format = "json"
        test_response_format = os.getenv("response_format")
        assert test_response_format == expected_response_format

    def test_set_env_vars_sets_correct_message_id(slef, run_set_env_vars):
        expected = "guardian_content"
        test = os.getenv("message_id")
        assert test == expected

    def test_set_env_vars_creates_correct_enivronmental_default_url(self, run_set_env_vars):
        expected_default_url = "https://content.guardianapis.com/search?"
        test_default_url = os.getenv("default_url")
        assert test_default_url == expected_default_url

    def test_set_env_vars_sets_correct_default_search_term(self, run_set_env_vars):
        expected_default_search_term = "machine learning"
        test_default_search_term = os.getenv("default_search_term")
        assert expected_default_search_term == test_default_search_term

    def test_set_env_vars_sets_correct_default_from_date(self, run_set_env_vars):
        expected = "1900-01-01"
        test_default_from_date = os.getenv("default_from_date")
        assert test_default_from_date == expected


class TestSetSecretEnvVars():

    def test_set_secret_env_vars_creates_correct_enivronmental_api_key(self, run_set_secret_env_vars):
        expected_api_key = "test"
        test_api_key = os.getenv("api_key")
        assert test_api_key == expected_api_key


    def test_secret_set_env_vars_creates_correct_env_q_name(self, run_set_secret_env_vars):
        expected_queue_name = "test_queue_name.fifo"
        test_queue_name = os.getenv("queue_name")
        assert test_queue_name == expected_queue_name


class TestCreateSecretTfvarsFile:

    def test_create_tfvars_file_creates_a_file(self):
        create_secrets_tfvars_file()
        assert os.path.exists("./terraform/secrets.auto.tfvars")

        os.remove('./terraform/secrets.auto.tfvars')

    def test_create_tfvars_file_has_correct_conent(self, run_set_secret_env_vars):
        create_secrets_tfvars_file()
        with open(
            "./terraform/secrets.auto.tfvars", "r", encoding="utf-8"
        ) as test_file_content:
            assert test_file_content.read() == 'queue_name = "test_queue_name.fifo"'

        os.remove('./terraform/secrets.auto.tfvars')


class TestSetupEnv:

    def test_setupenv_sets_correct_api_key_when_input_as_arg(self):
        test_api_key = 'test'
        test_queue_name = 'test_queue_name'
        with SetupEnv(api_key=test_api_key, queue_name=test_queue_name):
            assert os.getenv('api_key') == 'test'

    def test_setupenv_sets_correct_queue_name_when_input_as_arg(self):
        test_api_key = 'test'
        test_queue_name = 'test_queue_name'
        with SetupEnv(api_key=test_api_key, queue_name=test_queue_name):
            assert os.getenv('queue_name') == 'test_queue_name.fifo'