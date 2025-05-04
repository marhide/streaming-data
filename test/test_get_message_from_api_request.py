import os

import pytest
from copy import deepcopy

from src.get_message_from_api_request import (
    create_request,
    format_result,
    get_results,
    match_sort_by,
    match_sort_order_to_bool,
    sort_message_content,
)

from src.setup import set_secret_env_vars
from fixtures import run_set_env_vars, run_set_secret_env_vars, run_set_all_env_vars


@pytest.mark.usefixtures("run_set_all_env_vars")
class TestCreateRequest:
    def test_create_request_returns_tuple(self):
        request = create_request()
        assert isinstance(request, tuple)

    def test_create_request_has_str_as_first_item(self):
        request = create_request()
        assert isinstance(request[0], str)

    def test_create_request_has_dict_as_second_item(self):
        request = create_request()
        assert isinstance(request[1], dict)

    def test_create_request_has_correct_query_url(self):
        request = create_request()
        expected = "https://content.guardianapis.com/search?"
        assert request[0] == expected

    def test_create_request_has_correct_query_url_when_given_search_term(self):
        search_term = "machine learning"
        request = create_request(search_term)
        expected = "https://content.guardianapis.com/search?q=machine%20learning"
        assert request[0] == expected

    def test_create_request_has_correct_query_url_when_given_only_from_date(self):
        from_date = "2023-01-01"
        request = create_request(from_date=from_date)
        expected = "https://content.guardianapis.com/search?&from-date=2023-01-01"
        assert request[0] == expected

    def test_create_request_has_correct_query_url_when_given_search_term_and_from_date(
        self,
    ):
        search_term = "machine learning"
        from_date = "2023-01-01"
        request = create_request(search_term, from_date)
        expected = "https://content.guardianapis.com/search?q=machine%20learning&from-date=2023-01-01"
        assert request[0] == expected


@pytest.mark.usefixtures("run_set_all_env_vars")
class TestGetResults:
    def test_get_results_returns_a_list_when_given_correct_input(self):
        test_req = create_request()
        result = get_results(test_req)
        assert isinstance(result, list)

    def test_get_results_returns_list_of_only_dicts_when_given_correct_input(self):
        test_req = create_request()
        result = get_results(test_req)
        for item in result:
            assert isinstance(item, dict)

    def test_get_results_raises_an_error_when_given_bad_request(self):
        set_secret_env_vars("bad_test_api_key", "test_queue_name")
        test_bad_request = create_request()
        with pytest.raises(Exception) as e_info:
            get_results(test_bad_request)


class TestFormatResults:
    def test_format_result_returns_dict_when_given_correct_input(self):
        test_input = {
            "webPublicationDate": "test_webPublicationDate",
            "webTitle": "test_webTitle",
            "webUrl": "test_webUrl",
        }

        results = format_result(test_input)
        assert isinstance(results, dict)

    def test_format_result_returns_dict_with_three_kvs_when_given_correct_input(self):
        test_input = {
            "webPublicationDate": "test_webPublicationDate",
            "webTitle": "test_webTitle",
            "webUrl": "test_webUrl",
        }

        results = format_result(test_input)
        assert len(results) == 3


@pytest.mark.usefixtures("run_set_env_vars")
class TestMatchSortBy:
    def test_match_sort_by_returns_default_sort_by_from_env_when_passed_nothing(self):
        expected = os.getenv("default_sort_by")
        result = match_sort_by()
        assert result == expected

    def test_match_sort_by_returns_webTitle_when_passed_valid_title(self):
        test_title_match_list = ["webTitle", "title", "article", "name"]
        result_title_match_list = map(match_sort_by, test_title_match_list)
        for item in result_title_match_list:
            assert item == "webTitle"

    def test_match_sort_by_returns_webPublicationDate_when_passed_valid_date_order_name(
        self,
    ):
        test_date_match_list = ["webPublicationDate", "publicationdate", "date"]
        result_date_match_list = map(match_sort_by, test_date_match_list)
        for item in result_date_match_list:
            assert item == "webPublicationDate"

    def test_match_sort_by_returns_weburl_when_passed_valid_url_order_name(self):
        test_url_match_list = ["webUrl", "url"]
        result_url_match_list = map(match_sort_by, test_url_match_list)
        for item in result_url_match_list:
            assert item == "webUrl"

    def test_match_sort_by_returns_default_sort_by_when_given_wrong_input(self):
        expected = os.getenv("default_sort_by")
        result = match_sort_by("wrong input 999")
        assert result == expected

    def test_match_sort_by_returns_correct_sort_by_when_given_input_with_wrong_case(
        self,
    ):
        test_title_match_list = ["webtiTle", "tiTLE", "Article", "nAmE"]
        result_title_match_list = map(match_sort_by, test_title_match_list)
        for item in result_title_match_list:
            assert item == "webTitle"

    def test_match_sort_by_raises_error_when_given_wrong_data_type(self):
        with pytest.raises(AttributeError):
            match_sort_by(9999)

    def test_match_sort_by_returns_webPublicationDate_if_given_no_input_and_default_sort_by_env_is_wrong(
        self,
    ):
        os.environ["default_sort_by"] = "wrong value for testing"
        assert os.getenv("default_sort_by") != "webPublicationDate"
        result = match_sort_by()
        assert result == "webPublicationDate"


class TestMatchSortOrderToBool:
    def test_match_sort_order_to_bool_returns_bool(self):
        result = match_sort_order_to_bool()
        assert isinstance(result, bool)

    def test_match_sort_order_to_bool_return_true_when_passed_desc(self):
        result = match_sort_order_to_bool("desc")
        assert result is True

    def test_match_sort_order_to_bool_return_false_when_passed_asc(self):
        result = match_sort_order_to_bool("asc")
        assert result is False

    def test_match_sort_order_to_bool_return_true_when_passed_desc_in_wrong_case(self):
        result = match_sort_order_to_bool("dEsc")
        assert result is True

    def test_match_sort_order_to_bool_return_false_when_passed_asc_in_wrong_case(self):
        result = match_sort_order_to_bool("aSc")
        assert result is False

    def test_match_sort_order_to_bool_returns_false_when_env_var_set_to_asc_and_passed_nothing(
        self,
    ):
        os.environ["default_sort_order"] = "asc"
        assert os.getenv("default_sort_order") == "asc"
        result = match_sort_order_to_bool()
        assert result is False

    def test_match_sort_order_to_bool_returns_true_when_env_var_set_to_desc_and_passed_nothing(
        self,
    ):
        os.environ["default_sort_order"] = "desc"
        assert os.getenv("default_sort_order") == "desc"
        result = match_sort_order_to_bool()
        assert result is True

    def test_match_sort_order_to_bool_returns_false_when_env_var_set_to_asc_and_passed_incorrect_data_type(
        self,
    ):
        os.environ["default_sort_order"] = "asc"
        assert os.getenv("default_sort_order") == "asc"
        result = match_sort_order_to_bool(999)
        assert result is False

    def test_match_sort_order_to_bool_returns_true_when_env_var_set_to_desc_and_passed_incorrect_data_type(
        self,
    ):
        os.environ["default_sort_order"] = "desc"
        assert os.getenv("default_sort_order") == "desc"
        result = match_sort_order_to_bool(999)
        assert result is True

    def test_match_sort_order_to_bool_returns_true_when_passed_nothing_and_env_var_set_to_neither_asc_or_desc(
        self,
    ):
        os.environ["default_sort_order"] = "something else"
        assert os.getenv("default_sort_order") == "something else"
        result = match_sort_order_to_bool()
        assert result is True

    def test_match_sort_order_to_bool_returns_true_when_passed_something_incorrect_and_env_var_set_to_neither_asc_or_desc(
        self,
    ):
        os.environ["default_sort_order"] = "something else"
        assert os.getenv("default_sort_order") == "something else"
        result = match_sort_order_to_bool("incorrect")
        assert result is True

    def test_match_sort_order_to_bool_returns_true_when_passed_nothing_and_env_var_set_to_desc_in_wrong_case(
        self,
    ):
        os.environ["default_sort_order"] = "deSC"
        assert os.getenv("default_sort_order") == "deSC"
        result = match_sort_order_to_bool()
        assert result is True

    def test_match_sort_order_to_bool_returns_false_when_passed_nothing_and_env_var_set_to_asc_in_wrong_case(
        self,
    ):
        os.environ["default_sort_order"] = "ASC"
        assert os.getenv("default_sort_order") == "ASC"
        result = match_sort_order_to_bool()
        assert result is False


test_result_list = [
    {
        "webPublicationDate": "2000-01-01",
        "webTitle": "title1",
        "webUrl": "https://www.theguardian.com/article1",
    },
    {
        "webPublicationDate": "2000-01-02",
        "webTitle": "title2",
        "webUrl": "https://www.theguardian.com/article2",
    },
    {
        "webPublicationDate": "2000-01-03",
        "webTitle": "title3",
        "webUrl": "https://www.theguardian.com/article3",
    },
    {
        "webPublicationDate": "2000-01-04",
        "webTitle": "title4",
        "webUrl": "https://www.theguardian.com/article4",
    },
    {
        "webPublicationDate": "2000-01-05",
        "webTitle": "title5",
        "webUrl": "https://www.theguardian.com/article5",
    },
]

test_unordered_result_list = [
    {
        "webPublicationDate": "2000-01-04",
        "webTitle": "title4",
        "webUrl": "https://www.theguardian.com/article4",
    },
    {
        "webPublicationDate": "2000-01-02",
        "webTitle": "title2",
        "webUrl": "https://www.theguardian.com/article2",
    },
    {
        "webPublicationDate": "2000-01-05",
        "webTitle": "title5",
        "webUrl": "https://www.theguardian.com/article5",
    },
    {
        "webPublicationDate": "2000-01-03",
        "webTitle": "title3",
        "webUrl": "https://www.theguardian.com/article3",
    },
    {
        "webPublicationDate": "2000-01-01",
        "webTitle": "title1",
        "webUrl": "https://www.theguardian.com/article1",
    },
]

test_result_title_list = [
    {"webPublicationDate": "", "webTitle": "title1", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title2", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title3", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title4", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title5", "webUrl": ""},
]

test_unordered_title_list = [
    {"webPublicationDate": "", "webTitle": "title2", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title5", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title3", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title4", "webUrl": ""},
    {"webPublicationDate": "", "webTitle": "title1", "webUrl": ""},
]


class TestSortMessageContent:
    def test_sort_message_content_returns_list_when_given_a_correct_list_of_correct_dicts(
        self,
    ):
        result = sort_message_content(test_result_list)
        assert isinstance(result, list)

    def test_sort_message_content_returns_list_in_descending_date_order_when_env_var_is_set_to_desc(
        self,
    ):
        os.environ["default_sort_order"] = "desc"
        assert os.getenv("default_sort_order") == "desc"
        expected_list = deepcopy(test_result_list)
        expected_list.reverse()
        result = sort_message_content(test_unordered_result_list)
        assert result == expected_list

    def test_sort_message_content_returns_list_in_asc_date_order_when_env_var_is_set_to_asc(
        self,
    ):
        os.environ["default_sort_order"] = "asc"
        assert os.getenv("default_sort_order") == "asc"
        result = sort_message_content(test_unordered_result_list)
        assert result == test_result_list

    def test_sort_message_content_returns_list_in_descending_order_when_passed_desc_as_sort_order_arg(
        self,
    ):
        expected_list = deepcopy(test_result_list)
        expected_list.reverse()
        result = sort_message_content(test_unordered_result_list, sort_order="desc")
        assert result == expected_list

    def test_sort_message_content_returns_list_in_ascending_order_when_passed_asc_as_sort_order_arg(
        self,
    ):
        result = sort_message_content(test_unordered_result_list, sort_order="asc")
        assert result == test_result_list

    def test_sort_message_conent_returns_list_in_descending_title_order_when_passed_title_as_sort_by_arg(
        self,
    ):
        os.environ["default_sort_order"] = "desc"
        assert os.getenv("default_sort_order") == "desc"
        test_title_match_list = [
            "webTitle",
            "title",
            "article",
            "name",
            "TITLE",
            "arTicle",
        ]
        expected_list = deepcopy(test_result_title_list)
        expected_list.reverse()
        for test_sort_by in test_title_match_list:
            result = sort_message_content(
                test_unordered_title_list, sort_by=test_sort_by
            )
            assert result == expected_list

    def test_sort_message_conent_returns_list_in_ascending_title_order_when_passed_title_as_sort_by_arg_and_asc_as_sort_order_arg(
        self,
    ):
        test_title_match_list = [
            "webTitle",
            "title",
            "article",
            "name",
            "TITLE",
            "arTicle",
        ]
        for test_sort_by in test_title_match_list:
            result = sort_message_content(
                test_unordered_title_list, sort_by=test_sort_by, sort_order="asc"
            )
            assert result == test_result_title_list
