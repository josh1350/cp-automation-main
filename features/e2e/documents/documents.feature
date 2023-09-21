@e2e @documents
Feature: Documents

  @positive
  @allure.link.TMS_CP-141:CP-141
  Scenario: Downloading a Document from the Documents
    Given I login as a user named "sharon"
    When I open "Documents" page
    When I click on the "first" document with "HVA108158" account number on the "Documents" Page
    Then The document PDF preview is opened

  @positive
  @allure.link.TMS_CP-142:CP-142
  Scenario: Downloading a Document from the Dashboard
    Given I login as a user named "sharon"
    When I click on the "first" document with "HVA108158" account number on the "dashboard" Page
    Then The document PDF preview is opened

  @positive
  @allure.link.TMS_CP-315:CP-315
  Scenario: 'No documents' label verification
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$test_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"
    When I filter documents "documents" from API response by "date" "last 30 days" and save it as "documents_30_days"

    When I login as a user named "Tester"
    When I open "Documents" page
    When I open "Statements" tab on Documents Page
    When I filter "statements" by date using "last 30 days" on the Documents page
    Then The are no "documents_30_days" Documents on "Statements" tab

    When I open "Mailings" tab on Documents Page
    When I filter "Mailings" by date using "last 30 days" on the Documents page
    Then The are no "documents_30_days" Documents on "Mailings" tab

    When I open "Taxes" tab on Documents Page
    Then The are no "documents" Documents on "Taxes" tab

  @positive
  @allure.link.TMS_CP-316:CP-316
  Scenario: The documents filter combination
    Given I get API cp token
    Given I save "HVA108158" as a "first_document_account"
    Given I save "HVA125372" as a "second_document_account"
    Given I save "Monthly / Quarterly Statement" as a "statement_document_type"
    Given I save "Consolidated 1099 Tax Form" as a "taxes_document_type"
    Given I save "Email Address Update RAP" as a "mailing_document_type"
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I filter documents "documents" from API response by "date" "last 90 days" and save it as "documents_90_days"
    When I filter documents "documents_90_days" from API response by "type" "{$statement_document_type}" and save it as "documents_90_statement_type"
    When I filter documents "documents_90_statement_type" from API response by "accounts" "{$second_document_account}" and save it as "documents_90_statement_type_account"

    When I filter documents "documents" from API response by "accounts" "{$first_document_account}" and save it as "first_mailings_account"
    When I filter documents "documents" from API response by "accounts" "{$second_document_account}" and save it as "second_mailings_account"
    When I filter documents "documents" from API response by "type" "{$mailing_document_type}" and save it as "documents_mailings_type"
    When I filter documents "second_mailings_account" from API response by "type" "{$mailing_document_type}" and save it as "second_mailings_account_type"

    When I filter documents "documents" from API response by "type" "{$taxes_document_type}" and save it as "documents_taxes_type"
    When I filter documents "documents_taxes_type" from API response by "accounts" "{$first_document_account}" and save it as "documents_taxes_type_account"

    When I login as a user named "sharon"
    When I open "Documents" page

    When I open "Statements" tab on Documents Page
    When I filter "statements" by date using "last 90 days" on the Documents page
    When I filter "statements" by "type" "{$statement_document_type}" on the Documents page
    Then The documents "statements" table contains "documents_90_statement_type" items
    When I filter "statements" by "accounts" "{$second_document_account}" on the Documents page
    Then The documents "statements" table contains "documents_90_statement_type_account" items

    When I open "Mailings" tab on Documents Page
    When I filter "Mailings" by date using "all" on the Documents page
    When I filter "Mailings" by "type" "{$mailing_document_type}" on the Documents page
    Then The documents "Mailings" table contains "documents_mailings_type" items
    When I filter "Mailings" by "accounts" "{$second_document_account}" on the Documents page
    Then The documents "Mailings" table contains "second_mailings_account_type" items
    When I filter "Mailings" by "accounts" "{$first_document_account}" on the Documents page
    Then The documents "Mailings" table contains "first_mailings_account" items

    When I open "Taxes" tab on Documents Page
    When I filter "Taxes" by date using "all" on the Documents page
    When I filter "Taxes" by "type" "{$taxes_document_type}" on the Documents page
    Then The documents "Taxes" table contains "documents_taxes_type" items
    When I filter "Taxes" by "accounts" "{$first_document_account}" on the Documents page
    Then The documents "Taxes" table contains "documents_taxes_type_account" items

  @positive
  @allure.link.TMS_CP-317:CP-317
  Scenario: Document filters contains unique names from table
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I filter documents "documents" from API response by "date" "current year" and save it as "documents_current_year"

    When I login as a user named "sharon"
    When I open "Documents" page

    When I open "Statements" tab on Documents Page
    When I filter "statements" by date using "all" on the Documents page
    Then The documents "statements" table contains "documents" items
    Then The Documents "type" filter on "statements" contains unique names from table
    Then The Documents "accounts" filter on "statements" contains unique names from table

    When I open "Reports" tab on Documents Page
    When I filter "Reports" by date using "all" on the Documents page
    Then The documents "Reports" table contains "documents" items

    When I open "Mailings" tab on Documents Page
    When I filter "Mailings" by date using "all" on the Documents page
    Then The documents "Mailings" table contains "documents" items
    Then The Documents "type" filter on "Mailings" contains unique names from table
    Then The Documents "accounts" filter on "Mailings" contains unique names from table

    When I open "Taxes" tab on Documents Page
    When I filter "Taxes" by date using "all" on the Documents page
    Then The documents "Taxes" table contains "documents" items
    Then The Documents "tax year" filter on "Taxes" contains unique names from table
    Then The Documents "type" filter on "Taxes" contains unique names from table
    Then The Documents "accounts" filter on "Taxes" contains unique names from table

  @positive
    @allure.link.TMS_CP-318:CP-318
  Scenario Outline: Document filtering by accounts
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I login as a user named "sharon"
    When I open "Documents" page
    When I open "<tab>" tab on Documents Page
    When I filter "<tab>" by date using "all" on the Documents page
    Then The Documents "accounts" filter options on "<tab>" can filter "documents" correctly
    Examples:
      | tab        |
      | Statements |
      | Mailings   |
      | Taxes      |

  @positive
    @allure.link.TMS_CP-319:CP-319
  Scenario Outline: Document filtering by type
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I login as a user named "sharon"
    When I open "Documents" page
    When I open "<tab>" tab on Documents Page
    When I filter "<tab>" by date using "all" on the Documents page
    Then The Documents "type" filter options on "<tab>" can filter "documents" correctly
    Examples:
      | tab        |
      | Statements |
      | Mailings   |
      | Taxes      |

  @positive
  @allure.link.TMS_CP-320:CP-320
  Scenario: Document default filters
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I login as a user named "sharon"
    When I open "Documents" page

    When I filter documents "documents" from API response by "date" "last 90 days" and save it as "documents_90_days"
    When I filter documents "documents" from API response by "date" "current year" and save it as "documents_current_year"
    When I filter documents "documents" from API response by "date" "2022" and save it as "documents_2022_year"

    When I open "Statements" tab on Documents Page
    Then The documents "statements" table contains "documents_90_days" items
    When I open "Reports" tab on Documents Page
    Then The documents "Reports" table contains "documents_current_year" items
    When I open "Mailings" tab on Documents Page
    Then The documents "Mailings" table contains "documents_90_days" items
    When I open "Taxes" tab on Documents Page
    Then The documents "Taxes" table contains "documents_2022_year" items

  @positive
  @allure.link.TMS_CP-321:CP-321
  Scenario: Document filtering by date
    Given I get API cp token
    When I have prepared request query string as
    """
    search=profile.login eq "{$sharon_username}"
    """
    When I send "GET" request to "api/v1/users" of "okta"
    When I save "user_guid" from response by jpath "[0].profile.guid"
    When I send "Get" request to "client/{$user_guid}/documentsByDateRange?documentType=all" of "cp_API"
    When I save "documents" from response by jpath "documents"

    When I filter documents "documents" from API response by "date" "last 30 days" and save it as "documents_30_days"
    When I filter documents "documents" from API response by "date" "last 90 days" and save it as "documents_90_days"
    When I filter documents "documents" from API response by "date" "current year" and save it as "documents_current_year"
    When I filter documents "documents" from API response by "date" "last year" and save it as "documents_last_year"
    When I filter documents "documents" from API response by "date" "2021" and save it as "documents_2021_year"
    When I filter documents "documents" from API response by "date" "2022" and save it as "documents_2022_year"

    When I login as a user named "sharon"
    When I open "Documents" page

    When I open "Statements" tab on Documents Page
    When I filter "statements" by date using "last year" on the Documents page
    Then The documents "statements" table contains "documents_last_year" items
    When I filter "statements" by date using "current year" on the Documents page
    Then The documents "statements" table contains "documents_current_year" items
    When I filter "statements" by date using "last 30 days" on the Documents page
    Then The documents "statements" table contains "documents_30_days" items
    When I filter "statements" by date using "last 90 days" on the Documents page
    Then The documents "statements" table contains "documents_90_days" items

    When I open "Reports" tab on Documents Page
    When I filter "Reports" by date using "last year" on the Documents page
    Then The documents "Reports" table contains "documents_last_year" items
    When I filter "Reports" by date using "current year" on the Documents page
    Then The documents "Reports" table contains "documents_current_year" items

    When I open "Mailings" tab on Documents Page
    When I filter "Mailings" by date using "last year" on the Documents page
    Then The documents "Mailings" table contains "documents_last_year" items
    When I filter "Mailings" by date using "current year" on the Documents page
    Then The documents "Mailings" table contains "documents_current_year" items
    When I filter "Mailings" by date using "last 30 days" on the Documents page
    Then The documents "Mailings" table contains "documents_30_days" items
    When I filter "Mailings" by date using "last 90 days" on the Documents page
    Then The documents "Mailings" table contains "documents_90_days" items

    When I open "Taxes" tab on Documents Page
    When I filter "Taxes" by date using "all" on the Documents page
    Then The documents "Taxes" table contains "documents" items
    When I filter "Taxes" by date using "2021" on the Documents page
    Then The documents "Taxes" table contains "documents_2021_year" items
    When I filter "Taxes" by date using "2022" on the Documents page
    Then The documents "Taxes" table contains "documents_2022_year" items
