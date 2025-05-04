from unittest import mock

import pytest

from src.user_input import input_search_term, validate_date, input_from_date
from fixtures import run_set_env_vars


@mock.patch('src.user_input.input', create=True)
class TestInputSearchTerm:
    def test_input_search_term_returns_correct_search_term_that_is_input(self, mocked_input):
        mocked_input.side_effect = ['test search']
        result = input_search_term()
        assert result == 'test search'

    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['test search with space at the end ']
        result = input_search_term()
        assert result == 'test search with space at the end'

    @pytest.mark.usefixtures('run_set_env_vars')
    def test_input_search_term_returns_correct_search_term_that_is_input_but_without_space_at_end(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_search_term()
        assert result == 'machine learning'

    def test_input_search_term_returns_correct_search_when_arg_is_input(self, _):
        result = input_search_term('new search term')
        assert result == 'new search term'

    def test_input_search_term_removes_trailing_space_from_input(self, mocked_input):
        mocked_input.side_effect = ['has a space     ']
        result = input_search_term()
        assert result == 'has a space'

    def test_input_search_term_removes_leading_space_from_input(self, mocked_input):
        mocked_input.side_effect = ['         has a space']
        result = input_search_term()
        assert result == 'has a space'

    def test_input_search_term_removes_leading_and_trailing_space_from_input(self, mocked_input):
        mocked_input.side_effect = ['         has a space           ']
        result = input_search_term()
        assert result == 'has a space'

    def test_input_search_term_removes_trailing_space_from_arg(self, _):
        result = input_search_term('has a space     ')
        assert result == 'has a space'

    def test_input_search_term_removes_leading_space_from_arg(self, _):
        result = input_search_term('         has a space')
        assert result == 'has a space'

    def test_input_search_term_removes_leading_and_trailing_space_from_arg(self, _):
        result = input_search_term('         has a space           ')
        assert result == 'has a space'

    def test_input_raises_type_error_when_passed_arg_of_wrong_type(self, _):
        with pytest.raises(TypeError):
            input_search_term(9999)


class TestValidateDate():
    def test_validate_date_raises_error_if_given_incorrect_date(self):
        bad_test_date = "not a date"
        with pytest.raises(ValueError):
            validate_date(bad_test_date)

    def test_validate_date_does_not_raise_error_if_given_correct_date(self):
        test_date = "1999-01-01"
        try:
            validate_date(test_date)
        except Exception as e:
            assert False, f"raised an exception {e}"

    def test_validate_date_raises_error_if_given_incorrect_date_in_correct_format(self):
        suspicious_date = "2024-04-31"
        with pytest.raises(ValueError):
            validate_date(suspicious_date)

    def test_validate_date_raises_type_error_if_given_incorrect_data_type(self):
        with pytest.raises(TypeError):
            validate_date(9999)


@mock.patch('src.user_input.input', create=True)
class TestInputFromDate:
    def test_input_from_date_returns_correct_date_when_input_correct_date(self, mocked_input):
        mocked_input.side_effect = ['2000-01-01']
        result = input_from_date()
        assert result == '2000-01-01'

    def test_input_from_date_returns_none_when_given_empty_str(self, mocked_input):
        mocked_input.side_effect = ['']
        result = input_from_date()
        assert result is None

    def test_input_from_date_returns_correct_date_when_given_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date', '1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'

    def test_input_from_date_returns_correct_date_when_given_many_incorrect_date_then_correct_date(self, mocked_input):
        mocked_input.side_effect = ['not a date' for _ in range(9)] + ['1999-01-01']
        result = input_from_date()
        assert result == '1999-01-01'

    def test_input_from_date_returns_correct_date_when_given_correct_date_as_arg(self, _):
        result = input_from_date('1991-06-06')
        assert result == '1991-06-06'

    def test_input_from_date_raises_value_error_when_given_date_in_wrong_format_as_arg(self, _):
        with pytest.raises(ValueError):
            input_from_date('9999-99-99')
        
    def test_input_from_date_raises_type_error_when_given_wrong_data_type_as_arg(self, _):
        with pytest.raises(TypeError):
            input_from_date(['a list'])