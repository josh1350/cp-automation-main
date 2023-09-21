# flake8: noqa
import re
from ast import literal_eval
from decimal import Decimal
from typing import Dict, List

from .logger import Log

log = Log().logger


class Assert:
    @staticmethod
    def __assert(condition: bool, info_msg: str, error_msg: str):
        """
        Common assertion method that accepts condition,
        configures logging and allure details, and performs assertion \n
        :param condition: Condition for which assertion is to be performed
        :param info_msg: Information level message (for logging and allure step definition)
        :param error_msg: Error level message (for logging)
        """
        log.info(f"Assertion: {info_msg}")
        if not condition:
            log.error(f"Assertion Error: {error_msg}")
        assert condition, error_msg

    @staticmethod
    def is_true(value, error_msg: str = None):
        """
        Assert value is True \n
        :param value: Value to be asserted as True
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=bool(value) is True,
            info_msg="Result should be True",
            error_msg="Result is not True" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_false(value, error_msg: str = None):
        """
        Assert value is False \n
        :param value: Value to be asserted as False
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=bool(value) is False,
            info_msg="Result should be False",
            error_msg="Result is not False" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_none(value, error_msg: str = None):
        """
        Assert value is None (null) \n
        :param value: Value to be checked
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=value is None,
            info_msg="Value is None (null)",
            error_msg="Value is not None (null)" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_equal(actual, expected_equal, error_msg: str = None):
        """
        Assert two values are equal \n
        :param actual: Actual result
        :param expected_equal: Expected result
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=actual == expected_equal,
            info_msg="Actual result is equal to expected result",
            error_msg=f"Actual result ({type(actual)}: {actual}) "
            f"is not equal to expected ({type(expected_equal)}: {expected_equal})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_not_equal(actual, expected_not_equal, error_msg: str = None):
        """
        Assert two values are not equal \n
        :param actual: Actual result
        :param expected_not_equal: Expected result
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=actual != expected_not_equal,
            info_msg="Actual result is not equal to expected result",
            error_msg=f"Actual result ({type(actual)}: {actual}) "
            f"is equal to expected ({type(expected_not_equal)}: {expected_not_equal})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_equal_as_number(actual, expected_equal, error_msg: str = None):
        """
        Assert two values are equal as numbers \n
        :param actual: Actual result
        :param expected_equal: Expected result
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        decimal_actual, decimal_expected_equal = Decimal(str(actual)), Decimal(str(expected_equal))
        Assert.__assert(
            condition=decimal_actual == decimal_expected_equal,
            info_msg=f"Actual result (as number) ({decimal_actual}) is equal "
            f"to expected result (as number) ({decimal_expected_equal})",
            error_msg=f"Actual result (as number) ({decimal_actual}) is not equal "
            f"to expected result (as number) ({decimal_expected_equal})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_greater(value, greater_than_value, error_msg: str = None):
        """
        Assert value is greater than another value \n
        :param value: Value to be checked
        :param greater_than_value: Checked value should be greater than this value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=value > greater_than_value,
            info_msg="Value is greater than another value",
            error_msg=f"Value ({value}) is not greater than another value ({greater_than_value})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_greater_or_equal(value, greater_equal_than_value, error_msg: str = None):
        """
        Assert value is greater or equal than another value \n
        :param value: Value to be checked
        :param greater_equal_than_value: Checked value should be greater or equal than this value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=value >= greater_equal_than_value,
            info_msg="Value is greater or equal than another value",
            error_msg=f"Value ({value}) is not greater or equal " f"than another value ({greater_equal_than_value})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_less(value, less_than_value, error_msg: str = None):
        """
        Assert value is less than another value \n
        :param value: Value to be checked
        :param less_than_value: Checked value should be less than this value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=value < less_than_value,
            info_msg="Value is less than another value",
            error_msg=f"Value ({value}) is not less than another value ({less_than_value})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_less_or_equal(value, less_equal_than_value, error_msg: str = None):
        """
        Assert value is less or equal than another value \n
        :param value: Value to be checked
        :param less_equal_than_value: Checked value should be less or equal than this value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=value <= less_equal_than_value,
            info_msg="Value is less or equal than another value",
            error_msg=f"Value ({value}) is not less or equal " f"than another value ({less_equal_than_value})"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def type_is(value, type_: type, error_msg: str = None):
        """
        Assert value type \n
        :param value: Value to be checked
        :param type_: Expected type of value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=type(value) == type_,
            info_msg=f"Value type is {type_}",
            error_msg=f"Value type ({value}, {type(value)}) is not {type_}" if error_msg is None else error_msg,
        )

    @staticmethod
    def type_is_not(value, type_not: type, error_msg: str = None):
        """
        Assert value type is not as predefined \n
        :param value: Value to be checked
        :param type_not: Expected type of value not to be equal
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=type(value) != type_not,
            info_msg=f"Value type is not {type_not}",
            error_msg=f"Value type ({value}, {type(value)}) is {type_not}" if error_msg is None else error_msg,
        )

    @staticmethod
    def contains(value, in_value, error_msg: str = None):
        """
        Assert value is in another value \n
        :param value: Value to be checked
        :param in_value: Another value which is expected to include checked value
        :param error_msg: Message in case of assertion error (if None, then predefined message is used)
        """
        Assert.__assert(
            condition=value in in_value,
            info_msg="Value is in another value",
            error_msg=f"Value ({value}) is not in {in_value}" if error_msg is None else error_msg,
        )

    @staticmethod
    def not_contains(value, not_in_value, error_msg: str = None):
        """
        Assert value is not in another value \n
        :param value: Value to be checked
        :param not_in_value: Another value which is expected not to include checked value
        :param error_msg: Message in case of assertion error (if None, then predefined message is used)
        """
        Assert.__assert(
            condition=value not in not_in_value,
            info_msg="Value is not in another value",
            error_msg=f"Value ({value}) is in {not_in_value}" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_dict_subset_of_another_dict(dict_value: Dict, in_dict_value: Dict, error_msg: str = None):
        """
        Assert all pairs of key and value of a dict are in another dict \n
        :param dict_value: Dictionary of which key and value pairs to be checked
        :param in_dict_value: Dictionary which is expected to include pairs of checked dictionary
        :param error_msg: Message in case of assertion error (if None, then predefined message is used)
        """
        """ In order to avoid unhashable type (list) error, it is needed to change lists to sets"""
        dict_value = literal_eval(str(dict_value).replace("[", "(").replace("]", ")"))
        in_dict_value = literal_eval(str(in_dict_value).replace("[", "(").replace("]", ")"))

        Assert.__assert(
            condition=set(dict_value.items()).issubset(in_dict_value.items()),
            info_msg="Each pair of key and value from the dict are in another dict",
            error_msg="Not each pair of key and value from the dict are in another dict"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_list_of_dicts_subset_of_another(
        dict_list_value: List[Dict],
        in_dict_list_value: List[Dict],
        error_msg: str = None,
    ):
        """
        Assert all pairs of key and value of a dict from the list
        are in another dict from another sorted list \n
        :param dict_list_value: List of dictionaries of which key and value pairs to be checked
        :param in_dict_list_value: List of dictionaries which are expected to include pairs of checked dictionary
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        """ In order to avoid unhashable type (list) error, it is needed to change lists to sets"""
        dict_list_value = literal_eval(str(dict_list_value).replace("[", "(").replace("]", ")"))
        in_dict_list_value = literal_eval(str(in_dict_list_value).replace("[", "(").replace("]", ")"))
        Assert.__assert(
            condition=all(
                set(dict_list_value[i].items()).issubset(in_dict_list_value[i].items())
                for i in range(0, len(dict_list_value))
            ),
            info_msg="Each pair of key and value from the dict from the list "
            "are in another dict from another sorted list",
            error_msg="Not each pair of key and value from the dict from the list "
            "are in another dict from another sorted list"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def is_list_subset_of_another(
        list_value: List,
        in_list_value: List,
        error_msg: str = None,
    ):
        """
        Assert one list is subset_of another list \n
        :param list_value: List of which key and value pairs to be checked
        :param in_list_value: List which are expected to include pairs of checked dictionary
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        """ In order to avoid unhashable type (list) error, it is needed to change lists to sets"""
        Assert.__assert(
            condition=set(list_value).issubset(in_list_value),
            info_msg="Each value from the list " "are in another sorted list",
            error_msg="Not each value from the list " "are in another sorted list" if error_msg is None else error_msg,
        )

    @staticmethod
    def all_elements_equal_to(values_list, value_equal_to, error_msg: str = None):
        """
        Assert all elements are equal to another value \n
        :param values_list: List of values to be checked
        :param value_equal_to: Value to which list elements should be equal
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=all(i == value_equal_to for i in values_list),
            info_msg=f"All elements in list are equal to {value_equal_to}",
            error_msg=f"Not all elements in the list are equal to {value_equal_to}" if error_msg is None else error_msg,
        )

    @staticmethod
    def all_elements_as_numbers_equal_to(values_list, value_equal_to, error_msg: str = None):
        """
        Assert all elements (as numbers) are equal to another value \n
        :param values_list: List of values to be checked
        :param value_equal_to: Value to which list elements should be equal
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        decimal_value_equal_to = Decimal(str(value_equal_to))
        Assert.__assert(
            condition=all(Decimal(str(element)) == decimal_value_equal_to for element in values_list),
            info_msg=f"All elements (as numbers) in list are equal to {decimal_value_equal_to}",
            error_msg=f"Not all elements (as numbers) in the list " f"are equal to {decimal_value_equal_to}"
            if error_msg is None
            else error_msg,
        )

    @staticmethod
    def all_elements_are_true(values_list, error_msg: str = None):
        """
        Assert all elements are True \n
        :param values_list: List of values to be checked
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=all(bool(i) is True for i in values_list),
            info_msg="All elements in the list are True",
            error_msg="Not all elements in the list are True" if error_msg is None else error_msg,
        )

    @staticmethod
    def all_elements_are_false(values_list, error_msg: str = None):
        """
        Assert all elements are False \n
        :param values_list: List of values to be checked
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=all(bool(i) is False for i in values_list),
            info_msg="All elements in the list are False",
            error_msg="Not all elements in the list are False" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_pattern_matched(value: str, pattern: str, error_msg: str = None):
        """
        Assert value matches pattern (regex) \n
        :param value: Value to be checked
        :param pattern: Pattern (regex) to be used for checking the value
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=bool(re.match(pattern=pattern, string=value)) is True,
            info_msg="Value matches pattern",
            error_msg="Value does not match the pattern" if error_msg is None else error_msg,
        )

    @staticmethod
    def is_not_pattern_matched(value: str, pattern: str, error_msg: str = None):
        """
        Assert value does not match pattern (regex) \n
        :param value: Value to be checked
        :param pattern: Pattern (regex) to be used for checking the value (not to match)
        :param error_msg: Message in case of assertion error (if None, than predefined message is used)
        """
        Assert.__assert(
            condition=bool(re.match(pattern=pattern, string=value)) is False,
            info_msg="Value does not match pattern",
            error_msg="Value matches the pattern" if error_msg is None else error_msg,
        )
