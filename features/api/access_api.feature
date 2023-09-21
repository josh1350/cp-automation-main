@api @access_api
Feature: Access API
  Background:
    Given "firstName" is a random string length of "5"
    Given "guid" is a random number length of 5
    Given "lastName" is a random string length of "5"
    Given "email" is a random string length of "5"
    Given "login" is a random string length of "5"
    Given "password" is a random secret length of "12"
    Given "mobilePhone" is a random number length of 10
    Given I save "123432" as a "user_gui"
    Given "random_value" is a random string length of "5"
    When I have prepared request body as
    """
    {
      "profile": {
        "firstName": "{$firstName}",
        "guid": "{$guid}",
        "lastName": "{$lastName}",
        "email": "{$email}@avantax.com",
        "mobilePhone": "{$mobilePhone}",
        "login": "{$login}"
      },
      "credentials": {
        "password" : { "value": "{$password}" }
      }
    }
    """
    When I send "POST" request to "api/v1/users?activate=true" of "okta"
    When I save "user_id" from response by jpath "id"
    When I wait that user with id "{$user_id}" is created

  @positive
  @allure.link.TMS_CP-154:CP-154
  Scenario: Provide Access to new user via API
    When I have prepared request headers as
    """
    {
        "username": "{$cp_api_username}",
        "password": "{$cp_api_password}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$guid}",
        "ClientPortalAccess": "true"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "200"
    Then The response JSON is equivalent to
    """
    {
        "code": 200,
        "message": "Success"
    }
    """
    When I send "GET" request to "api/v1/users/{$user_id}/groups" of "okta"
    Then The response JSON by jpath "[].profile" is equivalent to
    """
    [
      {
        "name": "Everyone",
        "description": "All users in your organization"
      },
      {
        "name": "Client Portal Customers",
        "description": "Client Portal Customers"
       }
    ]
    """
    When I send "POST" request to "api/v1/users/{$user_id}/lifecycle/deactivate" of "okta"
    When I send "DELETE" request to "api/v1/users/{$user_id}" of "okta"

  @negative
  @allure.link.TMS_CP-155:CP-155
  Scenario: Call Access API with invalid body
    When I have prepared request headers as
    """
    {
        "username": "{$cp_api_username}",
        "password": "{$cp_api_password}"
    }
    """
    When I have prepared request body as
    """
    {
        "ClientPortalAccess": "false"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "422"
    Then The response JSON is equivalent to
    """
    {
        "code": 422,
        "message": "{\"GUID\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "422"
    Then The response JSON is equivalent to
    """
    {
        "code": 422,
        "message": "{\"ClientPortalAccess\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}",
        "ClientPortalAccess": "{$random_value}"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "422"
    Then The response JSON is equivalent to
    """
    {
        "code": 422,
        "message": "{\"ClientPortalAccess\": [\"`ClientPortalAccess` should be either `true` or `false` string\"]}"
    }
    """
    When I have prepared request body as
    """
    {}
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "422"
    Then The response JSON is equivalent to
    """
    {
        "code": 422,
        "message": "{\"GUID\": [\"This field is required.\"], \"ClientPortalAccess\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$random_value}",
        "ClientPortalAccess": "true"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "404"
    Then The response JSON is equivalent to
    """
    {
        "code": 404,
        "message": "No Account Found in Okta"
    }
    """

  @negative
  @allure.link.TMS_CP-156:CP-156
  Scenario: Access API required authorization headers
    When I have prepared request headers as
    """
    {
        "username": "{$cp_api_username}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}",
        "ClientPortalAccess": "false"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "401"
    Then The response JSON is equivalent to
    """
    {
        "code": 401,
        "message": "Both `Username` and `Password` headers are required."
    }
    """
    When I have prepared request headers as
    """
    {
        "password": "{$cp_api_password}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}",
        "ClientPortalAccess": "false"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "401"
    Then The response JSON is equivalent to
    """
    {
        "code": 401,
        "message": "Both `Username` and `Password` headers are required."
    }
    """
    When I have prepared request headers as
    """
    {
        "username": "{$random_value}",
        "password": "{$cp_api_password}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}",
        "ClientPortalAccess": "false"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "401"
    Then The response JSON is equivalent to
    """
    {
        "code": 401,
        "message": "Wrong username or password."
    }
    """
    When I have prepared request headers as
    """
    {
        "username": "{$cp_api_username}",
        "password": "{$random_value}"
    }
    """
    When I have prepared request body as
    """
    {
        "GUID": "{$user_gui}",
        "ClientPortalAccess": "false"
    }
    """
    When I send "POST" request to "api/client/details/access" of "cp"
    Then The status code is "401"
    Then The response JSON is equivalent to
    """
    {
        "code": 401,
        "message": "Wrong username or password."
    }
    """