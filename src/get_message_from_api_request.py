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
    status_code = response.status_code

    if status_code == 200:
        content = json.loads(response.text)
        results = content['response']['results']

        return results
    
    else:
        raise Exception(f'Error: status code {status_code}')


def format_result(result):

    formatted_result = {
    'webPublicationDate': result['webPublicationDate'],
    'webTitle': result['webTitle'],
    'webUrl': result['webUrl']
    }

    return formatted_result


def sort_message_content(results, sort_by='webPublicationDate', sort_order='desc'):

    if sort_order == 'asc':
        sort_order = False
    
    if sort_order == 'desc':
        sort_order = True

    sorted_results = sorted(results, key=lambda result: result[sort_by], reverse=sort_order)
    message_body = sorted_results[:10]

    return message_body


def get_message(search_term=None, from_date=None):

    request = create_request(search_term, from_date)
    results = get_results(request)
    formatted_results = map(format_result, results)

    message_body = sort_message_content(formatted_results, sort_by='webPublicationDate', sort_order='desc')
    message = str({request[0]: message_body})

    return message