from datetime import date
from os import getenv


def input_search_term(search_term=None):
    '''Asks the user to input a search term and returns it. Returns the deafault search term from the config file if the user enters an empty string.'''

    if search_term is None:
        search_term = input("Enter search term: ").strip()

    if isinstance(search_term, str):
        if search_term == "":
            search_term = getenv("default_search_term")
        return search_term.strip()
    else:
        raise TypeError


def validate_date(date_text):
    '''Takes a date in the form of a string and checks if it is in YYYY-MM-DD format (ISO 8601), raising an error if it is not.'''

    try:
        date.fromisoformat(date_text)
        return date_text
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD.")


def input_from_date(from_date=None):
    '''Asks the user to input a date and only returns it is it is in the correct format.'''

    if from_date is None:
        counter = 0
        while True:
            counter += 1
            from_date = input("Enter from date in format YYYY-MM-DD: ").strip()
            if from_date == "":
                return None
            try:
                validate_date(from_date)
                return from_date
            except:
                print("Incorrect date format.")
                if counter >= 3:
                    print("Hint: leave blank for no from date limit in search results.")
    else:
        return validate_date(from_date)