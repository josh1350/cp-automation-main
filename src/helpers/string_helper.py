import random
import re
import string

import phonenumbers
from number_parser import parser
from phonenumbers import PhoneNumberFormat


class StringHelper:
    @staticmethod
    def remove_special_characters(text):
        pattern = r"[^a-zA-Z0-9\s]"
        cleaned_text = re.sub(pattern, "", text)
        return cleaned_text

    @staticmethod
    def normalize(text):
        normalized_string = text.strip().replace("\r", "").replace("\n", "")
        return normalized_string

    @staticmethod
    def word_to_number(word, ordinal=True):
        try:
            if ordinal:
                number = parser.parse_ordinal(word)
            else:
                number = parser.parse_number(word)
            return number
        except ValueError:
            return None

    @staticmethod
    def generate_string(length):
        characters = string.ascii_letters
        random_string = "".join(random.choice(characters) for _ in range(int(length)))
        return random_string

    @staticmethod
    def generate_us_phone_number():
        country_code = "US"
        while True:
            area_code = random.randint(200, 999)
            exchange_code = random.randint(200, 999)
            subscriber_number = random.randint(1000, 9999)

            full_phone_number = f"{area_code}{exchange_code}{subscriber_number}"
            parsed_number = phonenumbers.parse(full_phone_number, country_code)
            if phonenumbers.is_valid_number(parsed_number):
                formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                return formatted_number

    @staticmethod
    def generate_number(length):
        first_digit = str(random.randint(1, 9))
        rest_of_digits = [str(random.randint(0, 9)) for _ in range(int(length) - 1)]
        random_number = first_digit + "".join(rest_of_digits)
        return random_number

    @staticmethod
    def modify_email(email):  # noqa: FNE008
        number = StringHelper.generate_number(3)
        parts = email.split("@")
        username, domain = parts
        match = re.search(r"\+(\d+)", username)
        if match:
            numeric_suffix = int(match.group(1))
            modified_username = username.replace(f"+{numeric_suffix}", f"+{number}")
        else:
            modified_username = f"{username}+{number}"
        modified_email = f"{modified_username}@{domain}"
        return modified_email

    @staticmethod
    def generate_password(length):
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        password_pattern = [
            random.choice(lowercase_letters),
            random.choice(uppercase_letters),
            random.choice(digits),
            random.choice("!@*"),
        ]
        remaining_length = int(length) - len(password_pattern)
        rest_of_password = "".join(
            random.choice(string.ascii_letters + string.digits + "!@*") for _ in range(remaining_length)
        )
        random_password = "".join(password_pattern) + rest_of_password
        return random_password
