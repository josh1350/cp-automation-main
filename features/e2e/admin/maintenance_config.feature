@e2e @maintenance
Feature: Maintenance config
  Background:
    Given I login as a user named "admin"
    And "generated_value" is a random string length of "10"

  @positive
  @allure.link.TMS_CP-149:CP-149
  Scenario: Create Maintenance config and start it
    When I open Maintenance configs from admin home page
    And I delete all Maintenance configs
    And I add Maintenance config with "Maintenance #{$generated_value}" as a title and "Maintenance message to display #{$generated_value}" as a message
    And I click Maintenance on
    And I "Save" Maintenance config
    And I log out of the admin account
    And I am on the login page
    Then The Maintenance page is displayed
    And The Maintenance page contains "Maintenance #{$generated_value}" as a "title"
    And The Maintenance page contains "Maintenance message to display #{$generated_value}" as a "message"
    When I login as a user named "admin"
    And I open Maintenance configs from admin home page
    And I delete all Maintenance configs

  @positive
  @allure.link.TMS_CP-167:CP-167
  Scenario: Start Maintenance config and verify from admin page
    When I open Maintenance configs from admin home page
    And I delete all Maintenance configs
    And I add Maintenance config with "Maintenance #{$generated_value}" as a title and "Maintenance message to display #{$generated_value}" as a message
    And I click Maintenance on
    And I "Save" Maintenance config
    And I view site from admin panel
    Then The Maintenance page is displayed
    And The Maintenance page contains "Maintenance #{$generated_value}" as a "title"
    And The Maintenance page contains "Maintenance message to display #{$generated_value}" as a "message"
    When I login as a user named "admin"
    And I open Maintenance configs from admin home page
    And I delete all Maintenance configs

  @positive
  @allure.link.TMS_CP-150:CP-150
  Scenario: Create Maintenance config without starting
    When I open Maintenance configs from admin home page
    And I delete all Maintenance configs
    And I add Maintenance config with "Maintenance #{$generated_value}" as a title and "Maintenance message to display #{$generated_value}" as a message
    And I "Save" Maintenance config
    And I log out of the admin account
    And I am on the login page
    And I login as a user named "Tester"
    Then I should be logged in successfully
    When I log out of the account
    And I login as a user named "admin"
    And I open Maintenance configs from admin home page
    And I delete all Maintenance configs

  @positive
  @allure.link.TMS_CP-166:CP-166
  Scenario: Start Maintenance config and delete it without stopping
    When I open Maintenance configs from admin home page
    And I delete all Maintenance configs
    And I add Maintenance config with "Maintenance #{$generated_value}" as a title and "Maintenance message to display #{$generated_value}" as a message
    And I click Maintenance on
    And I "Save" Maintenance config
    And I delete all Maintenance configs
    And I log out of the admin account
    And I am on the login page
    And I login as a user named "Tester"
    Then I should be logged in successfully
