@e2e @settings
Feature: Settings

  Background:
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$test_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I save "user_email" from response by jpath "[0].profile.email"
    When I save "user_mobile_phone" from response by jpath "[0].profile.mobilePhone"
    When I save "user_last_password_chage" from response by jpath "[0].passwordChanged"
    When I send "GET" request to "client/{$user_guid}" of "cp_api"
    When I save "rep_code" from response by jpath "repCode"
    When I send "GET" request to "{$rep_code}" of "fp"
    When I save "corporate_name" from response by jpath "corporateAffiliateName"
    Given "random_number" is a random number length of 10
    Given "new_email" is a new email based on "{$user_email}"


  @negative @email @password @phone
  @allure.link.TMS_CP-355:CP-355
  @allure.issue.BUG_CP-351:CP-351
  Scenario: Settings page - Verify User Details
    Given I format date "{$user_last_password_chage}" and save it as "last_password_chage"
    When I login as a user named "Tester"
    When I open "Settings" page
    Then The details of the "email" on the Settings page is "Notifications from the {$corporate_name} client portal will be sent to this email address."
    Then The details of the "phone" on the Settings page is "Notifications from the {$corporate_name} client portal will be sent to this phone number."
    Then The details of the "password" on the Settings page is "Last updated on {$last_password_chage}"


  @negative @email
  @allure.link.TMS_CP-356:CP-356
  @allure.issue.BUG_CP-335:CP-335
  Scenario: Settings page - Update Email Address with not valid input data
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Email on the Settings page
    Then The email field in the Update Email modal on the Settings page is "{$user_email}"
    Then The password field in the Update Email modal on the Settings page is " "
    When I save the Email updates on the Settings page
    Then The "Please enter an updated email address." error message is displayed for "email" in Update Email on the Settings page
    Then The "Please enter password." error message is displayed for "password" in Update Email on the Settings page
    When I enter "{$test_password}" into the "password" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "Please enter an updated email address." error message is displayed for "email" in Update Email on the Settings page
    When I enter "behave$example.com" into the "email" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "Enter a valid email address." error message is displayed for "email" in Update Email on the Settings page
    When I enter "behave@example.c" into the "email" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "Enter a valid email address." error message is displayed for "email" in Update Email on the Settings page
    When I cleanup "email" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "Email address required." error message is displayed for "email" in Update Email on the Settings page
    When I enter "{$new_email}" into the "email" in Update Email on the Settings page
    When I enter "{$random_number}" into the "password" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "Incorrect password entered. 2 attempts remaining" error message is displayed for "password" in Update Email on the Settings page
    When I enter "behave$example.com" into the "email" in Update Email on the Settings page
    When I save the Email updates on the Settings page


  @negative @email
  @allure.link.TMS_CP-357:CP-357
  @allure.issue.BUG_CP-335:CP-335
  Scenario: Settings page - Cancel Email Updating and Verify Fields Reset
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Email on the Settings page
    When I enter "{$test_password}" into the "password" in Update Email on the Settings page
    When I enter "{$new_email}" into the "email" in Update Email on the Settings page
    When I cancel the Email updates on the Settings page
    When I open the Update Email on the Settings page
    Then The email field in the Update Email modal on the Settings page is "{$user_email}"
    Then The password field in the Update Email modal on the Settings page is " "


  @positive @email
  @allure.link.TMS_CP-358:CP-358
  @allure.issue.BUG_CP-354:CP-354
  Scenario: Settings page - Successful Email Updating and Verification
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Email on the Settings page
    When I enter "{$test_password}" into the "password" in Update Email on the Settings page
    When I enter "{$new_email}" into the "email" in Update Email on the Settings page
    When I save the Email updates on the Settings page
    Then The "title" of success updates for the "Email" on the Settings page is "Email Address Updated"
    Then The "content" of success updates for the "Email" on the Settings page is "Your email address has been updated for your {$corporate_name} client portal. To update the email address on your financial accounts, contact your financial professional."
    When I close success message on the "Email" updates on the Settings page
    Then The "{$new_email}" is in the Email description on the Settings page
    When I open the Update Email on the Settings page
    Then The email field in the Update Email modal on the Settings page is "{$new_email}"
    Then The password field in the Update Email modal on the Settings page is " "


  @positive @password
  @allure.link.TMS_CP-394:CP-394
  Scenario: Settings page - Cancel Password Updating and Verify Fields Reset
    Given "${password_to_input}" is a random secret length of "12"
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Password on the Settings page
    When I enter "${password_to_input}" into the "current" password in Update Password on the Settings page
    When I enter "${password_to_input}" into the "new" password in Update Password on the Settings page
    When I enter "${password_to_input}" into the "confirm" password in Update Password on the Settings page
    When I "show" the "current" password field in the Update Password modal on the Settings page
    When I "show" the "new" password field in the Update Password modal on the Settings page
    When I cancel the Password updates on the Settings page
    When I open the Update Password on the Settings page
    Then The "current" password field in the Update Password modal on the Settings page has text " "
    Then The "new" password field in the Update Password modal on the Settings page has text " "
    Then The "confirm" password field in the Update Password modal on the Settings page has text " "
    Then The "current" password field in the Update Password modal on the Settings page has "hide" status
    Then The "new" password field in the Update Password modal on the Settings page has "hide" status
    Then The "confirm" password field in the Update Password modal on the Settings page has "hide" status


  @positive @password
  @allure.link.TMS_CP-395:CP-395
  Scenario: Settings page - Show and hide password in Password Updating
    Given "password_to_input" is a random secret length of "12"
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Password on the Settings page
    Then The "current" password field in the Update Password modal on the Settings page has text " "
    Then The "new" password field in the Update Password modal on the Settings page has text " "
    Then The "confirm" password field in the Update Password modal on the Settings page has text " "
    When I enter "{$password_to_input}" into the "current" password in Update Password on the Settings page
    When I enter "{$password_to_input}" into the "new" password in Update Password on the Settings page
    When I enter "{$password_to_input}" into the "confirm" password in Update Password on the Settings page
    When I "show" the "current" password field in the Update Password modal on the Settings page
    Then The "current" password field in the Update Password modal on the Settings page has "show" status
    Then The "new" password field in the Update Password modal on the Settings page has "hide" status
    Then The "confirm" password field in the Update Password modal on the Settings page has "hide" status
    When I "show" the "new" password field in the Update Password modal on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has "show" status
    Then The "confirm" password field in the Update Password modal on the Settings page has "show" status
    When I "hide" the "new" password field in the Update Password modal on the Settings page
    Then The "current" password field in the Update Password modal on the Settings page has "show" status
    Then The "new" password field in the Update Password modal on the Settings page has "hide" status
    Then The "confirm" password field in the Update Password modal on the Settings page has "hide" status


  @positive @password
  @allure.link.TMS_CP-396:CP-396
  Scenario: Settings page - New password criteria for Password Updating
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Password on the Settings page
    Then The new password criteria is "absent" the Update Password modal on the Settings page

    When I enter "Ab1!" into the "new" password in Update Password on the Settings page
    Then The new password criteria is "present" the Update Password modal on the Settings page
    Then The new password criteria contains "Upper and lower case letters, A number, A special character (e.g. !@#$), No spaces" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "At least 8 characters" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "passw0r!" into the "new" password in Update Password on the Settings page
    Then The new password criteria contains "At least 8 characters, A number, A special character (e.g. !@#$), No spaces" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "Upper and lower case letters" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "passwOr!" into the "new" password in Update Password on the Settings page
    Then The new password criteria contains "At least 8 characters, Upper and lower case letters, A special character (e.g. !@#$), No spaces" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "A number" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "passwOr1" into the "new" password in Update Password on the Settings page
    Then The new password criteria contains "At least 8 characters, Upper and lower case letters, A number, No spaces" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "A special character (e.g. !@#$)" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "My new passw0r!" into the "new" password in Update Password on the Settings page
    Then The new password criteria contains "At least 8 characters, Upper and lower case letters, A number, A special character (e.g. !@#$)" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "No spaces" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "pass" into the "new" password in Update Password on the Settings page
    Then The new password criteria contains "No spaces" as "valid" in the Update Password modal on the Settings page
    Then The new password criteria contains "At least 8 characters, Upper and lower case letters, A number, A special character (e.g. !@#$)" as "invalid" in the Update Password modal on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error

    When I enter "{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "pass" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "new" password field in the Update Password modal on the Settings page has error
    Then The "confirm" password field in the Update Password modal on the Settings page has error
    Then The "confirm" password field in the Update Password modal on the Settings page has "Invalid password" error message

    When I enter "{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "default" password field in the Update Password modal on the Settings page has "Your password cannot be any of your last 4 passwords." error message


  @positive @password
  @allure.link.TMS_CP-397:CP-397
  Scenario: Settings page - Successful Password Updating and Verification

    Given "first_password_prefix" is a random secret length of "4"
    Given "second_password_prefix" is a random secret length of "4"
    Given "third_password_prefix" is a random secret length of "4"
    Given "fourth_password_prefix" is a random secret length of "4"
    When I login as a user named "Tester"
    When I open "Settings" page
    When I open the Update Password on the Settings page

    When I enter "{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$first_password_prefix}{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$first_password_prefix}{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "title" of success updates for the "password" on the Settings page is "Information"
    Then The "content" of success updates for the "password" on the Settings page is "Your password has been updated."
    When I close success message on the "password" updates on the Settings page
    When I log out of the account
    When I enter username: "{$test_username}" and password: "{$test_password}"
    And I click on the Sign In
    Then I should see an error message: "We do not recognize your username and/or password. Please try again."
    And I should remain on the login page
    When I enter username: "{$test_username}" and password: "{$first_password_prefix}{$test_password}"
    And I click on the Sign In
    When I open "Settings" page

    When I open the Update Password on the Settings page
    When I enter "{$first_password_prefix}{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$second_password_prefix}{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$second_password_prefix}{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    When I close success message on the "password" updates on the Settings page

    When I open the Update Password on the Settings page
    When I enter "{$second_password_prefix}{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$third_password_prefix}{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$third_password_prefix}{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    When I close success message on the "password" updates on the Settings page

    When I open the Update Password on the Settings page
    When I enter "{$second_password_prefix}{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$fourth_password_prefix}{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$fourth_password_prefix}{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "current" password field in the Update Password modal on the Settings page has "Incorrect password entered." error message

    When I enter "{$third_password_prefix}{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "default" password field in the Update Password modal on the Settings page has "Your password cannot be any of your last 4 passwords." error message

    When I enter "{$fourth_password_prefix}{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$fourth_password_prefix}{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    When I close success message on the "password" updates on the Settings page

    When I open the Update Password on the Settings page
    When I enter "{$fourth_password_prefix}{$test_password}" into the "current" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "new" password in Update Password on the Settings page
    When I enter "{$test_password}" into the "confirm" password in Update Password on the Settings page
    When I save the Password updates on the Settings page
    Then The "title" of success updates for the "password" on the Settings page is "Information"
    Then The "content" of success updates for the "password" on the Settings page is "Your password has been updated."
    When I close success message on the "password" updates on the Settings page

    When I have prepared request query string as
    """
    search=profile.login eq "{$test_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_last_password_chage" from response by jpath "[0].passwordChanged"
    Given I format date "{$user_last_password_chage}" and save it as "last_password_chage"
    Then The details of the "password" on the Settings page is "Last updated on {$last_password_chage}"


  @positive @password @cleanup
  @allure.link.TMS_CP-399:CP-399
  Scenario: Settings page - Password cleanup
    When I have prepared request query string as
    """
    search=profile.login eq "{$test_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_id" from response by jpath "[0].id"
    When I have prepared request body as
    """
    {
      "credentials": {
        "password" : { "value": "{$test_password}" }
      }
    }
    """
    When I send "PUT" request to "api/v1/users/{$user_id}" of "okta"