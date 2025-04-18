from os import environ
import requests
import json


def create_request(search_term=None, from_date=None):

    url = environ['default_url']
    url += 'q=' + search_term.replace(' ', '%20') if search_term else ''
    url += '&from-date=' + from_date if from_date else ''

    request = (
        url,
        {
            'api-key': environ['api_key'],
            'format': environ['response_format']
        }
    )

    return request


def get_results(request):

    response = requests.get(*request)
    content = json.loads(response.text)
    results = content['response']['results']
    formatted_results = [format_result(result) for result in results]

    return formatted_results


def format_result(result):

    formatted_result = {
    'webPublicationDate': result['webPublicationDate'],
    'webTitle': result['webTitle'],
    'webUrl': result['webUrl']
    }

    return formatted_result


def sort_message_content(results, sort_by='webPublicationDate'):

    sorted_results = sorted(results, key=lambda result: result[sort_by], reverse=True)
    message_body = sorted_results[:10]

    return message_body


def get_message(search_term=None, from_date=None):

    request = create_request(search_term, from_date)
    results = get_results(request)
    formatted_results = map(format_result, results)

    message_body = sort_message_content(formatted_results)
    message = str({request[0]: message_body})

    return message