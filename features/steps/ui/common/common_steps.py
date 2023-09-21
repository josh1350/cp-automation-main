from behave import then, when

from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.ui.pages.base_page import BasePage
from src.ui.pages.maintenance_page import MaintenancePage
from src.ui.pages.portal_page import PortalPage


@when("I log out of the account")
def log_out_of_account(context):
    PortalPage(context).nav_bar.get_logout_tab().click()


@when("I switch to the Client portal tab")
def switch_to_portal(context):
    context.browser.switch_to_tab(context.base_url)


@when('I open "{page}" page')
def open_page(context, page):
    page_to_open = page.lower()
    if page_to_open == "dashboard":
        PortalPage(context).nav_bar.get_dashboard_tab().click()
    if page_to_open == "accounts":
        PortalPage(context).nav_bar.get_accounts_tab().click()
    if page_to_open == "documents":
        PortalPage(context).nav_bar.get_documents_tab().click()
    if page_to_open == "settings":
        PortalPage(context).nav_bar.get_settings_tab().click()


@when("I set the browser window size to {width:d}x{height:d}")
def set_browser_window_size(context, width, height):
    context.driver.set_window_size(width, height)


@then('The current url contains "{part_url}"')
def current_url_contains(context, part_url):
    current_url = BasePage(context).get_page_url()
    Assert.contains(part_url.lower(), current_url.lower())


@then("The Maintenance page is displayed")
def maintenance_page_opened(context):
    MaintenancePage(context).open()
    MaintenancePage(context).get_title()
    current_url = BasePage(context).get_page_url()
    Assert.contains(
        MaintenancePage(context).endpoint, current_url, f"The Maintenance Page is not opened. You are on {current_url}"
    )


@then('The Maintenance page contains "{text}" as a "{element}"')
def verify_maintenance_page_elements(context, text, element):
    _text = BehaveHelper.format_context(context, text)
    match element.lower():
        case "title":
            actual_text = MaintenancePage(context).get_title().text.strip()
        case "message":
            actual_text = MaintenancePage(context).get_message().text.strip()
        case _:
            raise AutomationException(f"The are no such element as {element}.")
    Assert.is_equal(_text, actual_text, f"The Maintenance Page is not contains expected {element} with a {_text}.")
