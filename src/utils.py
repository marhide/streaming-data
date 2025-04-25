import datetime

def validate_date(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
