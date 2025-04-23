from os import getenv
import requests
import json


def create_request(search_term=None, from_date=None):

    url = getenv('default_url')
    url += 'q=' + search_term.replace(' ', '%20') if search_term else ''
    url += '&from-date=' + from_date if from_date else ''

    request = (
        url,
        {
            'api-key': getenv('api_key'),
            'format': getenv('response_format')
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


def sort_message_content(results, sort_by=None, sort_order=None):

    def match_sort_by(sort_by, fn_has_ran=False):
        match sort_by:
            case 'title':
                return 'webTitle'
            case 'article':
                return'webTitle'
            case _:
                sort_by = getenv('default_sort_by')
                return 'webPublicationDate' if fn_has_ran else match_sort_by(sort_by, fn_has_ran=True)
    
    sort_by = match_sort_by(sort_by)
        
    if sort_order not in ['asc', 'desc']:
        sort_order = getenv('default_sort_order')

    __reverse = sort_order != 'asc'

    sorted_results = sorted(results, key=lambda result: result[sort_by], reverse=__reverse)
    message_body = sorted_results[:10]

    return message_body


def get_message(search_term=None, from_date=None, sort_by=None, sort_order=None):

    request = create_request(search_term, from_date)
    results = get_results(request)
    formatted_results = map(format_result, results)

    message_body = sort_message_content(formatted_results, sort_by, sort_order)
    message = str({request[0]: message_body})

    return message