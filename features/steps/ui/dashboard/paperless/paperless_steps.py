from behave import then, when

from src.helpers.assertions import Assert
from src.helpers.exceptions.automation_exception import AutomationException
from src.ui.pages.dashboard.dashboard_page import DashboardPage


@when('I click on "{button}" in the Paperless block')
def click_paperless_button(context, button):
    paperless_block = DashboardPage(context).get_paperless_block()
    match button.lower():
        case "get started":
            paperless_block.click_get_started()
        case "dismiss":
            paperless_block.click_dismiss()
        case "settings":
            paperless_block.click_settings()
        case _:
            raise AutomationException(f"The are no such button as {button}.")


@then('Paperless block is "{condition}"')
def verify_dashboard_page(context, condition):
    match condition.lower():
        case "present":
            should_be_absent = False
        case "absent":
            should_be_absent = True
        case _:
            raise AutomationException(f"The are no such condition as {condition}.")
    actual_condition = DashboardPage(context).is_paperless_block_absent()
    Assert.is_equal(
        actual_condition,
        should_be_absent,
        f"Paperless block has wrong status. Expected to be absent is {should_be_absent}, "
        f"but actual absent is {actual_condition}",
    )


@then('Paperless block contains "{message}" message')
def verify_paperless_message(context, message):
    actual_message = DashboardPage(context).get_paperless_block().get_label().text.strip()
    Assert.is_equal(
        actual_message, message, f"Paperless block has wrong label. Expected: {message}, " f"but was: {actual_message}"
    )


@then("The Get Started button on Paperless block is absent")
def verify_get_started_button(context):
    DashboardPage(context).get_paperless_block().verify_get_started_is_absent()
