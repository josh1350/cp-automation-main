from behave import given

from src.helpers.behave_helper import BehaveHelper
from src.helpers.date_helper import DateHelper
from src.helpers.logger import Log
from src.helpers.string_helper import StringHelper

log = Log()


@given('I save "{value}" as a "{key}"')
def when_i_save_value(context, value, key):
    text = BehaveHelper.format_context(context, value)
    setattr(context, key, text)


@given('"{key}" is a random string length of "{length}"')
def generate_random_string(context, key, length):
    random_string = StringHelper.generate_string(length)
    log.logger.info(f"Context: The string '{random_string}' is saved as '{key}'")
    setattr(context, key, random_string)


@given('"{key}" is a random secret length of "{length}"')
def generate_random_secret(context, key, length):
    random_password = StringHelper.generate_password(length)
    log.logger.info(f"Context: The password '{random_password}' is saved as '{key}'")
    setattr(context, key, random_password)


@given('"{key}" is a new email based on "{old_email}"')
def modify_email(context, key, old_email):
    old_email = BehaveHelper.format_context(context, old_email)
    email = StringHelper.modify_email(old_email)
    log.logger.info(f"Context: The email '{email}' is saved as '{key}'")
    setattr(context, key, email)


@given('"{key}" is a random phone number')
def generate_random_phone(context, key):
    phone_number = StringHelper.generate_us_phone_number()
    phone_number = phone_number.replace("+1", "")
    log.logger.info(f"Context: The phone number '{phone_number}' is saved as '{key}'")
    setattr(context, key, phone_number)


@given('"{key}" is a random number length of {length}')
def generate_random_number(context, key, length):
    random_number = StringHelper.generate_number(length)
    log.logger.info(f"Context: The number '{random_number}' is saved as '{key}'")
    setattr(context, key, random_number)


@given('I format date "{date}" and save it as "{key}"')
def format_date(context, date, key):
    date_to_format = BehaveHelper.format_context(context, date)
    formatted_date = DateHelper.convert_date(date_to_format)
    log.logger.info(f"Context: The number '{formatted_date}' is saved as '{key}'")
    setattr(context, key, formatted_date)
