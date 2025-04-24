from src.utils import validate_date
import pytest


# test validate_date


def test_validate_date_raises_error_if_given_incorrect_date():
    bad_test_date = "not a date"
    with pytest.raises(Exception):
        validate_date(bad_test_date)


def test_validate_date_does_not_raise_error_if_given_correct_date():
    test_date = "1999-01-01"
    try:
        validate_date(test_date)
    except Exception as e:
        assert False, f"raised an exception {e}"


def test_validate_date_raises_error_if_given_incorrect_date_in_correct_format():
    suspicious_date = "2024-04-31"
    with pytest.raises(Exception):
        validate_date(suspicious_date)


def test_validates_date_doesnt_raise_error_if_given_empty_string():
    empty_input = ""
    try:
        validate_date(empty_input)
    except Exception as e:
        assert False, f"raised an exception {e}"
