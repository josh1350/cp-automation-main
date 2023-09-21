from behave import then, when

from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.logger import Log
from src.ui.pages.dashboard.dashboard_page import DashboardPage

log = Log().logger


@when("I go to the end of the Guided Tour")
def go_to_end_of_guided_tour(context):
    while DashboardPage(context).get_guided_tour().is_skip_button_is_present():
        log.info(f"Header ---- {DashboardPage(context).get_guided_tour().get_header().text}")
        DashboardPage(context).get_guided_tour().go_to_next_step()


@when('I click on the "{button}" button on the Guided Tour')
def click_guided_tour_button(context, button):
    guided_tour = DashboardPage(context).get_guided_tour()
    match button.lower():
        case "next":
            guided_tour.go_to_next_step()
        case "skip":
            guided_tour.skip_tour()
        case "back":
            guided_tour.go_to_back_step()
        case _:
            raise AutomationException(f"The are no such options as {button}.")


@then('The guided tour overlay is "{condition}"')
def verify_guided_tour_condition(context, condition):
    match condition.lower():
        case "displayed":
            DashboardPage(context).get_guided_tour()
        case "hidden":
            DashboardPage(context).verify_guided_tour_is_hidden()
        case "absent":
            DashboardPage(context).verify_guided_tour_is_absent()
        case _:
            raise AutomationException(f"The are no such options as {condition}. Please use displayed, absent or hidden")


@then('The guided tour header is "{message}"')
def verify_guided_tour_header(context, message):
    DashboardPage(context).get_guided_tour().verify_header(message)


@then('The guided tour content is "{message}"')
def verify_guided_tour_content(context, message):
    DashboardPage(context).get_guided_tour().verify_content(message)


@then('The Guided Tour highlighted "{element}" element')
def verify_guided_tour_highlighted_element(context, element):
    dashboard_page = DashboardPage(context)
    match element.lower():
        case "investments":
            element_locator = dashboard_page.investments_heading
        case "paperless":
            element_locator = dashboard_page.block_paperless
        case "profile":
            element_locator = dashboard_page.block_profile
        case "applications":
            element_locator = dashboard_page.block_applications
        case "accounts":
            element_locator = dashboard_page.nav_bar.tab_accounts
        case "documents":
            element_locator = dashboard_page.nav_bar.tab_documents
        case "settings":
            element_locator = dashboard_page.nav_bar.tab_settings
        case _:
            raise AutomationException(f"The are no such options as {element}.")
    dashboard_page.verify_element_is_in_tour(element_locator)


@then('I verify Paperless block on the Guided Tour after click on "{button}" button')
def verify_guided_tour_paperless_block(context, button):
    if not DashboardPage(context).is_paperless_block_absent():
        click_guided_tour_button(context, button)
        header = "Paperless preferences"
        content = (
            "Update your paperless preferences to receive your brokerage account documents electronically. "
            "Simply click “Get Started” and make changes to your accounts."
        )
        verify_guided_tour_content(context, content)
        verify_guided_tour_header(context, header)
        verify_guided_tour_highlighted_element(context, "paperless")
    else:
        log.info("Paperless preferences block is hidden, no need verify the Guided Tour for it.")


@then("The back button is hidden on the Guided Tour")
def verify_guided_tour_back_button_hidden(context):
    DashboardPage(context).get_guided_tour().verify_back_button_is_hidden()
