#@api @login_api @skip
#Feature: Test Login API using Okta
#
#
#  @positive
#  @allure.link.TMS_CP-85:CP-85
#  Scenario: Successful API Login using Okta
#      Given I login as "Tester" using API
#      When I send "GET" request to "clientportal/accounts/" of "cp"
#      Then The status code is "200"
