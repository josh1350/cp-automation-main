@e2e @e2e_login
Feature: Login Authorization
  Background:
    Given I am on the login page

  @positive
  @allure.link.TMS_CP-32:CP-32
  @allure.issue.BUG_CP-33:CP-33
   Scenario: Successful login with valid credentials
      When I enter "Tester" credentials
      And I click on the Sign In
      Then I should be logged in successfully
      Then Profile information contains "Brian Stephens"
      And I should be logged in successfully

  @negative
  @allure.link.TMS_CP-34:CP-34
    Scenario Outline: Invalid login attempts with incorrect credentials
        When I enter username: "<username>" and password: "<password>"
        And I click on the Sign In
        Then I should see an error message: "We do not recognize your username and/or password. Please try again."
        And I should remain on the login page
        Examples:
            | username                | password        |
            | invalidEmail@email.net  | Avantax123!     |
            | StephensB@email.net     | invalidPassword |
            | invalidEmail@email.net  | invalidPassword |
            | invalidUser             | invalidPassword |
            | David99                 | invalidPassword |