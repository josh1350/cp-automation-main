from behave import when

from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.ui.pages.admin.admin_home_page import AdminHomePage
from src.ui.pages.admin.maintenance_config_page import AdminMaintenancePage


@when("I log out of the admin account")
def log_out_admin_account(context):
    AdminHomePage(context).nav_bar.get_logout_lnk().click()


@when("I view site from admin panel")
def view_site_admin_account(context):
    AdminHomePage(context).nav_bar.get_view_site_lnk().click()


@when("I open Maintenance configs from admin home page")
def change_maintenance_confid(context):
    AdminHomePage(context).click_change_maintenance_confid()


@when('I add Maintenance config with "{title}" as a title and "{message}" as a message')
def add_maintenance_confid(context, title, message):
    if AdminMaintenancePage(context).verify_add_maintenance_visibility():
        AdminMaintenancePage(context).click_add_maintenance_confid()
    else:
        AdminMaintenancePage(context).open_first_maintenance_confid()
    AdminMaintenancePage(context).add_title(BehaveHelper.format_context(context, title))
    AdminMaintenancePage(context).add_message(BehaveHelper.format_context(context, message))


@when("I click Maintenance on")
def maintenance_on(context):
    AdminMaintenancePage(context).click_maintenance_on()


@when("I delete all Maintenance configs")
def delete_maintenance(context):
    AdminMaintenancePage(context).delete_all_configs()


@when('I "{action}" Maintenance config')
def save_maintenance_config(context, action):
    maintenance_page = AdminMaintenancePage(context)
    match action.lower():
        case "save":
            maintenance_page.save()
        case "save and add another":
            maintenance_page.save_and_add()
        case "save and continue editing":
            maintenance_page.save_and_continue()
        case _:
            raise AutomationException(f"The are no such button as {action}.")
