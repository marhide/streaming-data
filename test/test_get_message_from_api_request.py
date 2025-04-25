import pytest

from src.get_message_from_api_request import (
    format_result,
    get_results,
    create_request,
    sort_message_content,
)
from src.setup import set_env_vars, set_secret_env_vars



# test create_request
set_env_vars()
set_secret_env_vars("test", "test_queue_name")


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
    expected = "https://content.guardianapis.com/search?"
    assert request[0] == expected


def test_create_request_has_correct_query_url_when_given_search_term():
    search_term = "machine learning"
    request = create_request(search_term)
    expected = "https://content.guardianapis.com/search?q=machine%20learning"
    assert request[0] == expected


def test_create_request_has_correct_query_url_when_given_only_from_date():
    from_date = "2023-01-01"
    request = create_request(from_date=from_date)
    expected = "https://content.guardianapis.com/search?&from-date=2023-01-01"
    assert request[0] == expected


def test_create_request_has_correct_query_url_when_given_search_term_and_from_date():
    search_term = "machine learning"
    from_date = "2023-01-01"
    request = create_request(search_term, from_date)
    expected = "https://content.guardianapis.com/search?q=machine%20learning&from-date=2023-01-01"
    assert request[0] == expected


# test get_results

test_req = create_request()


def test_get_results_returns_a_list_when_given_correct_input():
    result = get_results(test_req)
    assert isinstance(result, list)


def test_get_results_returns_list_of_only_dicts_when_given_correct_input():
    result = get_results(test_req)
    for item in result:
        assert isinstance(item, dict)


def test_get_results_raises_an_error_when_given_bad_request():
    set_secret_env_vars("bad_test_api_key", "test_queue_name")
    test_bad_request = create_request()
    set_secret_env_vars("test", "test_queue_name")
    with pytest.raises(Exception) as e_info:
        get_results(test_bad_request)


# test format_result


def test_format_result_returns_dict_when_given_correct_input():
    test_input = {
        "webPublicationDate": "test_webPublicationDate",
        "webTitle": "test_webTitle",
        "webUrl": "test_webUrl",
    }

    results = format_result(test_input)
    assert isinstance(results, dict)


def test_format_result_returns_dict_with_three_kvs_when_given_correct_input():
    test_input = {
        "webPublicationDate": "test_webPublicationDate",
        "webTitle": "test_webTitle",
        "webUrl": "test_webUrl",
    }

    results = format_result(test_input)
    assert len(results) == 3


# test sort_message_content


def sort_message_content_returns_list_when_given_a_correct_list_of_dicts():
    test_input = [{"k": "v"}]
    result = sort_message_content(test_input, "k")

    assert isinstance(result, list)


def sort_message_return_list_with_10_items_when_given_list_with_more_than_10_items():
    test_list = [{"k": i} for i in range(1, 100)]
    result = sort_message_content(test_list)

    assert len(result) == 10


def sort_message_content_returns_list_in_correct_order():
    test_list = [{"k": "bbb"}, {"k": "aaa"}, {"k": "ccc"}]
    expected_list = [{"k": "ccc"}, {"k": "bbb"}, {"k": "aaa"}]

    result = sort_message_content(test_list)
    assert result == expected_list
