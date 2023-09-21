@e2e @guided_tour
Feature: Guided Tour

  Background:
    Given I am on the login page
    And I enter "Sharon" credentials
    And I click on the Sign In

  @positive
  @allure.link.TMS_CP-107:CP-107
  Scenario: Navigating forward through the Guided Tour
    Then The guided tour overlay is "displayed"
    And The guided tour header is "Welcome! We are glad you're here."
    And The guided tour content is "Take a guided tour to get familiar with your portal."
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Investments balance"
    And The guided tour content is "View the balance for your investment accounts. You can learn more about your accounts by going to the accounts tab."
    And The Guided Tour highlighted "Investments" element
    Then I verify Paperless block on the Guided Tour after click on "Next" button
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Contact information"
    And The guided tour content is "Have questions? We are happy to help. You can find your Financial Professional’s information here."
    And The Guided Tour highlighted "Profile" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Applications"
    And The guided tour content is "Directly access your other financial applications."
    And The Guided Tour highlighted "Applications" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Account information"
    And The guided tour content is "View your asset allocation and account balances."
    And The Guided Tour highlighted "Accounts" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Your Documents"
    And The guided tour content is "View and download your account statements, reports, and other documents."
    And The Guided Tour highlighted "Documents" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Settings"
    And The guided tour content is "Manage your portal profile."
    And The Guided Tour highlighted "Settings" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour overlay is "hidden"

  @positive
  @allure.link.TMS_CP-108:CP-108
  Scenario: Navigating backward through the Guided Tour
    Then The guided tour overlay is "displayed"
    When I go to the end of the Guided Tour
    Then The guided tour header is "Settings"
    And The guided tour content is "Manage your portal profile."
    And The Guided Tour highlighted "Settings" element
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Your Documents"
    And The guided tour content is "View and download your account statements, reports, and other documents."
    And The Guided Tour highlighted "Documents" element
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Account information"
    And The guided tour content is "View your asset allocation and account balances."
    And The Guided Tour highlighted "Accounts" element
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Applications"
    And The guided tour content is "Directly access your other financial applications."
    And The Guided Tour highlighted "Applications" element
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Contact information"
    And The guided tour content is "Have questions? We are happy to help. You can find your Financial Professional’s information here."
    And The Guided Tour highlighted "Profile" element
    Then I verify Paperless block on the Guided Tour after click on "Back" button
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Investments balance"
    And The guided tour content is "View the balance for your investment accounts. You can learn more about your accounts by going to the accounts tab."
    And The Guided Tour highlighted "Investments" element
    When I click on the "Back" button on the Guided Tour
    Then The guided tour header is "Welcome! We are glad you're here."
    And The guided tour content is "Take a guided tour to get familiar with your portal."
    Then The back button is hidden on the Guided Tour

  @positive
  @allure.link.TMS_CP-109:CP-109
  Scenario: Skipping the Guided Tour
    Then The guided tour overlay is "displayed"
    When I click on the "Next" button on the Guided Tour
    And I click on the "Skip" button on the Guided Tour
    Then The guided tour overlay is "hidden"
    And I should remain on the Dashboard

  @positive
  @allure.link.TMS_CP-110:CP-110
  Scenario: Revisiting the Guided Tour
    Then The guided tour overlay is "displayed"
    When I go to the end of the Guided Tour
    And I click on the "Next" button on the Guided Tour
    And I log out of the account
    When I enter "Sharon" credentials
    And I click on the Sign In
    Then The guided tour overlay is "absent"

  @positive
  @allure.link.TMS_CP-111:CP-111
  Scenario: Start Guided Tour from the Settings page
    Then The guided tour overlay is "displayed"
    When I click on the "Skip" button on the Guided Tour
    And I open "Settings" page
    And I start the Guided Tour from the Settings page
    Then I should remain on the Dashboard
    And The guided tour header is "Welcome! We are glad you're here."
    And The guided tour content is "Take a guided tour to get familiar with your portal."
    When I go to the end of the Guided Tour
    And I click on the "Next" button on the Guided Tour
    Then The guided tour overlay is "hidden"

  @positive @adaptive
  @allure.link.TMS_CP-113:CP-113 @allure.issue.BUG_CP-272:CP-272
  Scenario: Navigating forward through the Guided Tour with small window resolution
    When I set the browser window size to 393x851
    Then The guided tour overlay is "displayed"
    And The guided tour header is "Welcome! We are glad you're here."
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Investments balance"
    And The Guided Tour highlighted "Investments" element
    Then I verify Paperless block on the Guided Tour after click on "Next" button
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Contact information"
    And The Guided Tour highlighted "Profile" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Applications"
    And The Guided Tour highlighted "Applications" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Account information"
    And The Guided Tour highlighted "Accounts" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Your Documents"
    And The Guided Tour highlighted "Documents" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour header is "Settings"
    And The Guided Tour highlighted "Settings" element
    When I click on the "Next" button on the Guided Tour
    Then The guided tour overlay is "hidden"
