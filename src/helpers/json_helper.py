import json

import jmespath


class JsonHelper:
    @staticmethod
    def delete_key_from_json(json_obj, key_to_remove):
        if isinstance(json_obj, list):
            for obj in json_obj:
                if isinstance(obj, dict):
                    obj.pop(key_to_remove, None)
        elif isinstance(json_obj, dict):
            json_obj.pop(key_to_remove, None)
        else:
            raise ValueError("Invalid input: Expected JSON string, list of objects, or an object")
        modified_json_data = json.dumps(json_obj)
        return modified_json_data

    @staticmethod
    def get_value(content, jpath):
        response_data = json.loads(content)
        value = jmespath.search(jpath, response_data)
        return value

    @staticmethod
    def sort(json_body):
        value = sorted(json_body, key=lambda x: json.dumps(x, sort_keys=True))
        return value

    @staticmethod
    def convert_request_cookie_to_json(cookie_string):
        # Split the cookie string into individual cookies
        cookies = cookie_string.split(";")

        # Create a dictionary to store the cookie key-value pairs
        cookie_dict = {}

        # Iterate through each cookie and extract the key-value pair
        for cookie in cookies:
            key, value = cookie.strip().split("=")
            # Check if the key already exists in the dictionary
            if key in cookie_dict:
                # If the key exists, convert the value to a list
                if isinstance(cookie_dict[key], list):
                    cookie_dict[key].append(value)
                else:
                    cookie_dict[key] = [cookie_dict[key], value]
            else:
                # If the key does not exist, add the key-value pair to the dictionary
                cookie_dict[key] = value

        # Convert the cookie dictionary to JSON
        cookie_json = json.dumps(cookie_dict)

        return json.loads(cookie_json)
