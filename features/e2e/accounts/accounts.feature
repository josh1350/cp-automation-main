@e2e @accounts
Feature: Accounts Tests
  Background:
    Given I save "Jason Tallant - Individual" as a "account_number"
    And I login as a user named "Tester"
    When I open "Accounts" page
    When I select "{$account_number}" account
    When I open "transactions" tab on Accounts page

  @positive
  @allure.link.TMS_CP-176:CP-176
  Scenario: Filter transactions by date and event type
    When I filter transactions by date using "all"
    When I extract transactions data from table
    Then The transactions type filter contains unique events from table
    When I filter transactions by date using "30 days"
    Then No transactions are present in the table
    When I filter transactions by date using "90 days"
    When I extract transactions data from table
    Then The transactions type filter contains unique events from table
    Then All transactions type filter options can filter data table correctly
    When I filter transactions by date using "year to date"
    When I extract transactions data from table
    Then The transactions type filter contains unique events from table
    When I filter transactions by date using "previous year"
    When I extract transactions data from table
    Then The transactions type filter contains unique events from table

  @positive
  @allure.link.TMS_CP-177:CP-177
  Scenario: The transactions type filter contains only All events in case transactions is not present
    When I filter transactions by date using "30 days"
    Then No transactions are present in the table
    Then The transactions type filter contains "All events"
