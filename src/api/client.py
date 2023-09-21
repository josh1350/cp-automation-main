import json
from typing import Any

import requests

from src.helpers.logger import Log

log = Log().logger


class ClientApi:
    """
    class that represents Client api methods
    """

    response = requests.models.Response

    def __init__(self, url: str):
        self._url = url

    # TODO: make from post and patch one common method
    def post_data(self, resource="", data: Any = None, headers: dict = None, **kwargs) -> response:
        """
        Make POST request to post data.

        :param resource: resource url
        :param data: payload
        :param headers: headers

        :return: response

        :Example:

        The following example will show how to make POST request.

        .. code-block:: python

            from http import HTTPStatus
            from api.base_api import ClientApi

            base = ClientApi('POST_URL')

            headers = {"Authorization": token}

            response = base.post_data(data=payload, headers=headers)
            assert response.status_code = HTTPStatus.OK
        """
        log.info(f"API: Making POST request to '{self._url}{resource}'")
        return requests.post(f"{self._url}{resource}", data=data, headers=headers, **kwargs)

    def patch_data(self, resource="", data: Any = None, headers: dict = None, **kwargs) -> response:
        """
        Make PATCH request to update data.

        :param resource: resource url
        :param data: payload
        :param headers: headers
        :return: response

        :Example:

        The following example will show how to make PATCH request.

        .. code-block:: python

            from http import HTTPStatus
            from api.base_api import ClientApi

            base = ClientApi('PATCH_URL')

            headers = {"Authorization": token}

            response = base.patch_data(data=payload, headers=headers)
            assert response.status_code = HTTPStatus.OK
        """
        log.info(f"API: Making PATCH request to '{self._url}{resource}'")
        return requests.patch(f"{self._url}{resource}", data=data, headers=headers, **kwargs)

    def put_data(self, resource="", data: Any = None, headers: dict = None, **kwargs) -> response:
        """
        Make PUT request to update data.

        :param resource: resource url
        :param data: payload
        :param headers: headers
        :return: response

        :Example:

        The following example will show how to make PUT request.

        .. code-block:: python

            from http import HTTPStatus
            from api.base_api import ClientApi

            base = ClientApi('PUT_URL')

            headers = {"Authorization": token}

            response = base.put_data(data=payload, headers=headers)
            assert response.status_code = HTTPStatus.OK
        """
        log.info(f"API: Making PUT request to '{self._url}{resource}'")
        return requests.put(f"{self._url}{resource}", data=data, headers=headers, **kwargs)

    def get_data(self, resource="", headers: dict = None, querystring: dict = None, **kwargs) -> response:
        """
        get data by endpoints with data

        :method: type of method
        :headers: headers
        :querystring: params for query string
        :kwargs: kwargs (data, json, params, ...)
        :return: response

        :Example:

        The following example will show how use that method

        .. code-block:: python

            from api.base_api import ClientApi

            class User(ClientApi):

                def get_user_data(self, method, headers: dict = None,
                    querystring: dict = None, **kwargs) -> ClientApi.response:

                    log.info("Customer: Get response")

                    return self.get_data(method, headers, querystring,
                     **kwargs)
        """
        log.info(f"API: Getting response from '{self._url}{resource}'")
        return requests.get(f"{self._url}{resource}", headers=headers, params=querystring, **kwargs)

    def delete_data(self, resource="", headers: dict = None, **kwargs) -> response:
        """
        Send DELETE request to delete some data

        :param resource: resource url
        :param headers: headers
        :kwargs: kwargs (data, json, params, ...)
        :return: response

        :Example:

        The following example will show how use that method

        .. code-block:: python

            from api.base_api import ClientApi

            def some_test():
                test_id = 123
                url = Property.LOCATION_URL.format(test_id)
                test = ClientApi(url)
                test.delete_data()

        """
        log.info(f"API: Making DELETE request to '{self._url}{resource}'")
        return requests.delete(f"{self._url}{resource}", headers=headers, **kwargs)

    @staticmethod
    def get_response_content(response_obj: response) -> Any:
        """
        Get response content

        :param response_obj: response object
        :return: dict (response content)

        :Example:

        The following example will show how get response content
        in dict type

        .. code-block:: python

                response = test.get_response_content(headers=headers,
                 querystring=querystring)

                print(response)
                >> {
                        "Logs": [
                            {content}
                        ],
                        "page": 1
                    }
        """
        log.info("Converting data response to dict")
        return json.loads(response_obj.content)


class AuthApi(ClientApi):
    def __init__(self, url):
        super().__init__(url)
