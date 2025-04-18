from src.get_message_from_api_request import format_result, create_request

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

def test_create_request_has_correct_query_url_when_given_only_from_date():
    from_date = '2023-01-01'
    request = create_request(from_date=from_date)
    expected = 'https://content.guardianapis.com/search?&from-date=2023-01-01'
    assert request[0] == expected

def test_create_request_has_correct_query_url_when_given_search_term_and_from_date():
    search_term = 'machine learning'
    from_date = '2023-01-01'
    request = create_request(search_term, from_date)
    expected = 'https://content.guardianapis.com/search?q=machine%20learning&from-date=2023-01-01'
    assert request[0] == expected