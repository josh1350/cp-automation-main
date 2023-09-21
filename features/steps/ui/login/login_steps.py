from behave import given, then, when

from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.logger import Log
from src.ui.pages.dashboard.dashboard_page import DashboardPage
from src.ui.pages.login.admin_login_page import AdminLoginPage
from src.ui.pages.login.login_page import LoginPage

log = Log().logger


@given("I am on the admin login page")
def open_admin_login_page(context):
    AdminLoginPage(context).open()


@given("I am on the login page")
@when("I am on the login page")
def open_login_page(context):
    LoginPage(context).open()


@when('I enter username: "{username}" and password: "{password}"')
@given('I enter username: "{username}" and password: "{password}"')
def enter_user_name(context, username, password):
    """
    Enters the provided username and password.
    Don't use for valid login! It is for exceptions verifications
    For valid logining use - @when('I login as "{user_type}"')
       Args:
           context: The behave context object.
           username: The username to be entered.
           password: The password to be entered.
    """
    username_input = BehaveHelper().format_context(context, username)
    password_input = BehaveHelper().format_context(context, password)
    LoginPage(context).enter_credentials(username_input, password_input)


@when('I enter "{user_type}" credentials')
@given('I enter "{user_type}" credentials')
def enter_credentials(context, user_type):
    match user_type.lower():
        case "tester":
            LoginPage(context).enter_credentials(context.test_username, context.test_password)
        case "sharon":
            LoginPage(context).enter_credentials(context.sharon_username, context.sharon_password)
        case "admin":
            AdminLoginPage(context).enter_credentials(context.admin_username, context.admin_password)
        case _:
            raise AutomationException(f"The are no such user type as {user_type}")


@when("I click on the Sign In")
@given("I click on the Sign In")
def sign_in(context):
    LoginPage(context).click_signin()


@when('I login as a user named "{user}"')
@given('I login as a user named "{user}"')
def login_as(context, user):
    if user.lower() == "admin":
        open_admin_login_page(context)
    else:
        open_login_page(context)
    enter_credentials(context, user)
    sign_in(context)

    if user.lower() != "admin":
        try:
            DashboardPage(context).get_guided_tour().skip_tour()
        except AssertionError:
            log.info("The guided tour is not found on the page. It seems that it has already been skipped.")


@then("I should be logged in successfully")
def then_i_verify_is_logged_in(context):
    LoginPage(context).verify_credentials_error_absent()
    LoginPage(context).verify_user_name_error_absent()
    LoginPage(context).verify_redirection_from_login()


@then('I should see an error message: "{message}"')
def then_i_see_error_message(context, message):
    LoginPage(context).verify_user_name_message(message)


@then("I should remain on the login page")
def then_i_remain_on_login(context):
    LoginPage(context).verify_login_is_opened()
