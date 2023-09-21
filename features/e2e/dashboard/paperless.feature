@e2e @paperless
Feature: Paperless block


  @positive
  @allure.link.TMS_CP-135:CP-135
  Scenario: Paperless Settings are hidden when “Enrolled” is selected for documents of user
    Given I login as a user named "Tester"
    Then Paperless block is "absent"

  @positive
  @allure.link.TMS_CP-136:CP-136
  Scenario: Dismiss Paperless Settings
    Given I login as a user named "Sharon"
    Then Paperless block is "present"
    And Paperless block contains "Go paperless! Start receiving account documents electronically." message
    When I click on "Dismiss" in the Paperless block
    Then Paperless block is "absent"
    When I log out of the account
    When I login as a user named "Sharon"
    Then Paperless block is "present"

  @positive
  @allure.link.TMS_CP-137:CP-137
  Scenario: Go Paperless
    Given I login as a user named "Sharon"
    Then Paperless block is "present"
    When I click on "Get Started" in the Paperless block
    When I switch to the Client portal tab
    Then Paperless block is "present"
    And Paperless block contains "You can update your electronic delivery preferences at any time on the Settings page" message
    And The Get Started button on Paperless block is absent
    When I log out of the account
    When I enter "Sharon" credentials
    When I click on the Sign In
    Then Paperless block is "present"
    And Paperless block contains "Go paperless! Start receiving account documents electronically." message
    When I click on "Get Started" in the Paperless block
    When I switch to the Client portal tab
    Then The Get Started button on Paperless block is absent