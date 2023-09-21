from behave import then

from src.ui.pages.dashboard.dashboard_page import DashboardPage


@then('Profile information contains "{info}"')
def verify_profile_information(context, info):
    DashboardPage(context).verify_prof_info(info)


@then("I should remain on the Dashboard")
def verify_dashboard_page(context):
    DashboardPage(context).verify_dashboard_is_present()
