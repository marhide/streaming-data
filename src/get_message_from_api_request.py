import requests
import json
from os import getenv


def create_request(search_term=None, from_date=None):
    '''Creates and returns a request for the API using in the correct format using the URL, search term and from date.'''

    url = getenv("default_url")
    url += "q=" + search_term.replace(" ", "%20") if search_term else ""
    url += "&from-date=" + from_date if from_date else ""

    api_key = getenv("api_key")
    response_format = getenv('response_format')

    request = (url, {"api-key": api_key, "format": response_format})

    return request


def get_results(request):
    '''Sends a request to the API reuturns a list of all articles the API returned.'''

    response = requests.get(*request)
    status_code = response.status_code

    if status_code == 200:
        content = json.loads(response.text)
        results = content["response"]["results"]

        return results

    else:
        raise Exception(f"Error: status code {status_code}")


def format_result(result):
    'Formats an individual article result from the API into the format specified by the brief.'

    formatted_result = {
        "webPublicationDate": result["webPublicationDate"],
        "webTitle": result["webTitle"],
        "webUrl": result["webUrl"],
    }

    return formatted_result


def match_sort_by(sort_by=None, fn_has_ran=False):
    '''Takes an input string and matches it with a correct sort by type to return.'''

    correct_sort_by_list = ['webPublicationDate', 'webTitle', 'webUrl']

    if sort_by is not None:
        try:
            sort_by = sort_by.lower()
        except:
            raise AttributeError

    date_match_list = ['webpublicationdate', 'publicationdate', 'date']
    title_match_list = ['webtitle', 'title', 'article', 'name']
    url_match_list = ['weburl', 'url']

    if sort_by in date_match_list:
        sort_by = 'webPublicationDate'
    elif sort_by in title_match_list:
        sort_by = 'webTitle'
    elif sort_by in url_match_list:
        sort_by = 'webUrl'
    else:
        sort_by = getenv("default_sort_by")
    
    if fn_has_ran:
        if sort_by in correct_sort_by_list:
            return sort_by
        else:
            return 'webPublicationDate'
    
    return match_sort_by(sort_by, fn_has_ran=True) 


def match_sort_order_to_bool(sort_order=None):
    '''Matches a sort order type, eg. 'asc', to a boolean and returns the boolean value.'''


    correct_sort_orders = ["asc", "desc"]

    if isinstance(sort_order, str):
        sort_order = sort_order.lower()

    if sort_order not in correct_sort_orders:
        sort_order = getenv('default_sort_order')
        if isinstance(sort_order, str):
            sort_order = sort_order.lower()

    if sort_order in correct_sort_orders:
        reverse_order_bool = sort_order != 'asc'
    else:
        reverse_order_bool = True

    return reverse_order_bool


def sort_message_content(results, sort_by=None, sort_order=None):
    '''Sorts and returns a list of article data by a specified key and returns the first 10 results.'''

    sort_by = match_sort_by(sort_by)

    correct_sort_orders = ["asc", "desc"]

    if sort_order not in correct_sort_orders:
        sort_order = getenv("default_sort_order")

    reverse_order = match_sort_order_to_bool(sort_order)

    sorted_results = sorted(results, key=lambda result: result[sort_by], reverse=reverse_order)
    message_body = sorted_results[:10]

    return message_body


def get_message(search_term=None, from_date=None, sort_by=None, sort_order=None):
    '''Creates a search query for the API and sorts the response and returns it.'''

    request = create_request(search_term, from_date)
    results = get_results(request)
    formatted_results = map(format_result, results)

    message_body = sort_message_content(formatted_results, sort_by, sort_order)
    message = str({request[0]: message_body})

    return message
