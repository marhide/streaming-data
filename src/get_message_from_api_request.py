from os import environ
import requests
import json


def create_request(search_term=None, date_from=None):

    query = ''

    if search_term:
        search_term = 'q=' + search_term.replace(' ', '%20')
        query += search_term

    if date_from:
        date_from = '&from-date=' + date_from
        query += date_from

    url = environ['deafault_url'] + query

    request = (
        url,
        {
            'api-key': environ['api_key'],
            'format': environ['response_format']
        }
    )

    return request


def format_result(result):

    formatted_result = {
    'webPublicationDate': result['webPublicationDate'],
    'webTitle': result['webTitle'],
    'webUrl': result['webUrl']
    }

    return formatted_result


def get_results(request):

    response = requests.get(*request)
    content = json.loads(response.text)

    results = content['response']['results']
    formatted_results = [format_result(result) for result in results]

    return formatted_results


def sort_message_content(results):

    sorted_results = sorted(results, key=lambda result: result['webPublicationDate'], reverse=True)
    message_body = sorted_results[:10]

    return message_body


def get_message(search_term=None, date_from=None):

    request = create_request(search_term, date_from)
    results = get_results(request)
    formatted_results = map(format_result, results)

    message_body = sort_message_content(formatted_results)
    message = str({request[0]: message_body})

    return message