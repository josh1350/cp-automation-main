@api @invite_api
Feature: Invite API

  Background:
    Given "first_name" is a random string length of "10"
    Given "last_name" is a random string length of "10"
    Given "business_name" is a random string length of "10"
    Given "mobile_phone" is a random phone number
    Given I save "behave.{$first_name}@avantax.com" as a "email"
    Given "guid" is a random number length of 10
    Given "new_guid" is a random number length of 10
    Given "new_mobile_phone" is a random phone number
    Given I save "behave.{$first_name}_new@avantax.com" as a "new_email"
    Given I save "23746" as a "rep_code"
    When I have prepared request headers as
    """
    {
        "username": "{$cp_api_username}",
        "password": "{$cp_api_password}"
    }
    """


  @positive
  @allure.link.TMS_CP-261:CP-261
  Scenario: Send Invite to the person
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "201"
    Then The response JSON is equivalent to
    """
    {
        "code": 201,
        "message": "User has been created"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_id" from response by jpath "[0].id"
    Then The response JSON is equivalent to, ignoring "created, lastUpdated"
    """
    [
        {
            "id": "{$user_id}",
            "status": "STAGED",
            "activated": null,
            "statusChanged": null,
            "lastLogin": null,
            "passwordChanged": null,
            "type": {
                "id": "otyoc51jg6J8baSlL1d6"
            },
            "profile": {
                "firstName": "{$first_name}",
                "lastName": "{$last_name}",
                "mobilePhone": "{$mobile_phone}",
                "isNonPerson": false,
                "secondEmail": null,
                "guid": "{$guid}",
                "login": "{$email}",
                "email": "{$email}"
            },
            "credentials": {
                "provider": {
                    "type": "OKTA",
                    "name": "OKTA"
                }
            },
            "_links": {
                "self": {
                    "href": "https://avantax.oktapreview.com/api/v1/users/{$user_id}"
                }
            }
        }
    ]
    """
    When I send "POST" request to "api/v1/users/{$user_id}/lifecycle/deactivate" of "okta"
    When I send "DELETE" request to "api/v1/users/{$user_id}" of "okta"

  @positive
  @allure.link.TMS_CP-262:CP-262
  @allure.issue.BUG_CP-214:CP-214
  Scenario: Send Invite to the non person
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
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "BusinessName": "{$business_name}",
        "isNonPerson": "true"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "201"
    Then The response JSON is equivalent to
    """
    {
        "code": 201,
        "message": "User has been created"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_id" from response by jpath "[0].id"
    When I send "POST" request to "api/v1/users/{$user_id}/lifecycle/deactivate" of "okta"
    When I send "DELETE" request to "api/v1/users/{$user_id}" of "okta"

  @positive
  @allure.link.TMS_CP-263:CP-263
  Scenario: Verify that invited user cannot be created again
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "201"
    Then The response JSON is equivalent to
    """
    {
        "code": 201,
        "message": "User has been created"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_id" from response by jpath "[0].id"
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "Invite with _GUID `{$guid}` already exists"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email sw "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON by jpath "[].profile" is equivalent to
    """
    [
     {
       "firstName": "{$first_name}",
       "lastName": "{$last_name}",
       "mobilePhone": "{$mobile_phone}",
       "isNonPerson": false,
       "secondEmail": null,
       "guid": "{$guid}",
       "login": "{$email}",
       "email": "{$email}"
     }
    ]
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$new_guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message":  "Okta user with email address `{$email}` already exists"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email sw "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON by jpath "[].profile" is equivalent to
    """
    [
     {
       "firstName": "{$first_name}",
       "lastName": "{$last_name}",
       "mobilePhone": "{$mobile_phone}",
       "isNonPerson": false,
       "secondEmail": null,
       "guid": "{$guid}",
       "login": "{$email}",
       "email": "{$email}"
     }
    ]
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$new_guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$new_email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message":  "Okta user with phone number `{$mobile_phone}` already exists"
    }
    """
    When I have prepared request query string as
    """
    search=profile.mobilePhone sw "{$mobile_phone}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON by jpath "[].profile" is equivalent to
    """
    [
     {
       "firstName": "{$first_name}",
       "lastName": "{$last_name}",
       "mobilePhone": "{$mobile_phone}",
       "isNonPerson": false,
       "secondEmail": null,
       "guid": "{$guid}",
       "login": "{$email}",
       "email": "{$email}"
     }
    ]
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}{$new_guid}",
        "PhoneNumber": "{$new_mobile_phone}",
        "Email": "{$new_email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "201"
    Then The response JSON is equivalent to
    """
    {
        "code": 201,
        "message": "User has been created"
    }
    """
    When I have prepared request query string as
    """
    search=profile.firstName sw "{$first_name}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON by jpath "[].profile" is equivalent to
    """
    [
     {
       "firstName": "{$first_name}",
       "lastName": "{$last_name}",
       "mobilePhone": "{$mobile_phone}",
       "isNonPerson": false,
       "secondEmail": null,
       "guid": "{$guid}",
       "login": "{$email}",
       "email": "{$email}"
     },
     {
       "firstName": "{$first_name}",
       "lastName": "{$last_name}",
       "mobilePhone": "{$new_mobile_phone}",
       "isNonPerson": false,
       "secondEmail": null,
       "guid": "{$guid}{$new_guid}",
       "login": "{$new_email}",
       "email": "{$new_email}"
     }
    ]
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$new_email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "new_user_id" from response by jpath "[0].id"
    When I send "POST" request to "api/v1/users/{$user_id}/lifecycle/deactivate" of "okta"
    When I send "POST" request to "api/v1/users/{$new_user_id}/lifecycle/deactivate" of "okta"
    When I send "DELETE" request to "api/v1/users/{$user_id}" of "okta"
    When I send "DELETE" request to "api/v1/users/{$new_user_id}" of "okta"

  @negative
  @allure.link.TMS_CP-264:CP-264
  Scenario: Send Invite without required fields for isNonPerson=false
    When I have prepared request body as
    """
    {
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"_GUID\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"PhoneNumber\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"Email\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.mobilePhone eq "{$mobile_phone}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"RepCode\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`FirstName` and `LastName` are required if `isNonPerson` is `false`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`FirstName` and `LastName` are required if `isNonPerson` is `false`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`FirstName` and `LastName` are required if `isNonPerson` is `false`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`FirstName` and `LastName` are required if `isNonPerson` is `false`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"isNonPerson\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {}
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"_GUID\": [\"This field is required.\"], \"PhoneNumber\": [\"This field is required.\"], \"Email\": [\"This field is required.\"], \"RepCode\": [\"This field is required.\"], \"isNonPerson\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request body as
    """
    {
        "_GUID": null,
        "PhoneNumber": null,
        "Email": null,
        "RepCode": null,
        "FirstName": null,
        "LastName": null,
        "isNonPerson": null
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"_GUID\": [\"This field may not be null.\"], \"PhoneNumber\": [\"This field may not be null.\"], \"Email\": [\"This field may not be null.\"], \"RepCode\": [\"This field may not be null.\"], \"isNonPerson\": [\"This field may not be null.\"], \"FirstName\": [\"This field may not be null.\"], \"LastName\": [\"This field may not be null.\"]}"
    }
    """

  @negative
  @allure.link.TMS_CP-265:CP-265
  Scenario: Send Invite without required fields for isNonPerson=true
    When I have prepared request body as
    """
    {
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "isNonPerson": "true"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"_GUID\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "true"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`BusinessName` is required if `isNonPerson` is `true`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "BusinessName": null,
        "isNonPerson": "true"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"BusinessName\": [\"This field may not be null.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "BusinessName": "",
        "isNonPerson": "true"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"non_field_errors\": [\"`BusinessName` is required if `isNonPerson` is `true`\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq "{$email}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    When I have prepared request body as
    """
    {
        "BusinessName": "{$business_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"_GUID\": [\"This field is required.\"], \"PhoneNumber\": [\"This field is required.\"], \"Email\": [\"This field is required.\"], \"RepCode\": [\"This field is required.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.businessName eq "{$business_name}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """

  @negative
    @allure.link.TMS_CP-266:CP-266
  Scenario Outline: Send Invite with blank required field
    When I have prepared request body as
    """
    {
        "_GUID": <guid>,
        "PhoneNumber": <phone_number>,
        "Email": <email>,
        "RepCode": <rep_code>,
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"<error_field>\": [\"This field may not be blank.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=<query_to_search>
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    Examples:
      | guid    | email      | phone_number      | rep_code      | error_field | query_to_search             |
      | ""      | "{$email}" | "{$mobile_phone}" | "{$rep_code}" | _GUID       | profile.email eq "{$email}" |
      | "$guid" | ""         | "{$mobile_phone}" | "{$rep_code}" | Email       | profile.guid eq "{$guid}"   |
      | "$guid" | "{$email}" | ""                | "{$rep_code}" | PhoneNumber | profile.guid eq "{$guid}"   |
      | "$guid" | "{$email}" | "{$mobile_phone}" | ""            | RepCode     | profile.guid eq "{$guid}"   |

  @negative
    @allure.link.TMS_CP-267:CP-267
  Scenario Outline: Send Invite with invalid email
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": "{$mobile_phone}",
        "Email": <email>,
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"Email\": [\"Enter a valid email address.\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.email eq <email>
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    Examples:
      | email                    |
      | "behaveexample.com"      |
      | "behave@"                |
      | "behave$example.com"     |
      | "behave@example$com"     |
      | "behave@example@com"     |
      | "behave@example.com."    |
      | "behave@example..com"    |
      | "behave@example com"     |
      | "behave use@example.com" |
      | "behave@example.c"       |

  @negative
    @allure.link.TMS_CP-268:CP-268
  Scenario Outline: Send Invite with invalid mobile
    When I have prepared request body as
    """
    {
        "_GUID": "{$guid}",
        "PhoneNumber": <mobile>,
        "Email": "{$email}",
        "RepCode": "{$rep_code}",
        "FirstName": "{$first_name}",
        "LastName": "{$last_name}",
        "isNonPerson": "false"
    }
    """
    When I send "POST" request to "api/invite" of "cp"
    Then The status code is "400"
    Then The response JSON is equivalent to
    """
    {
        "code": 400,
        "message": "{\"PhoneNumber\": [\"`PhoneNumber` should be 10 digits string\"]}"
    }
    """
    When I have prepared request query string as
    """
    search=profile.mobilePhone eq <mobile>
    """
    When I send "GET" request to "api/v1/users" of "okta"
    Then The response JSON is equivalent to
    """
    []
    """
    Examples:
      | mobile             |
      | "123"              |
      | "1234567890123456" |
      | "+1(555)1234567"   |
      | "+19295821397"     |
      | "555-123-4567"     |
      | "123456789J"       |
      | "929 582 1397"     |
      | "929.5821397"      |
      | "929.5821397"      |