from behave import then, when

from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.models.accounts.transactions_model import TransactionsModel
from src.ui.pages.accounts.accounts_page import AccountsPage


@when('I open "{tab}" tab on Accounts page')
def open_accounts_tab(context, tab):
    tab_to_open = tab.lower()
    if tab_to_open == "summary":
        AccountsPage(context).open_summary_tab()
    if tab_to_open == "allocation":
        AccountsPage(context).open_allocation_tab()
    if tab_to_open == "holdings":
        AccountsPage(context).open_holdings_tab()
    if tab_to_open == "transactions":
        AccountsPage(context).open_transactions_tab()


@when('I select "{account_name}" account')
def select_account_name(context, account_name):
    AccountsPage(context).open_account(BehaveHelper.format_context(context, account_name))


@when("I extract transactions data from table")
def extract_table_data(context):
    while AccountsPage(context).get_transactions_tab().is_expand_exist():
        AccountsPage(context).get_transactions_tab().expand_data()
    row_data = AccountsPage(context).get_transactions_tab().get_rows_data()
    data = []
    for row in row_data:
        if len(row) == 6:
            data.append(TransactionsModel(*row))
        else:
            raise AutomationException("The Transaction column from table has wrong count")
    context.transaction_rows = data


@when('I filter transactions by date using "{value}"')
def filter_table_data(context, value):
    if value.lower() == "all":
        filter_value = "transaction-filter-date-all"
    elif value.lower() == "30 days":
        filter_value = "transaction-filter-date-30-days"
    elif value.lower() == "90 days":
        filter_value = "transaction-filter-date-90-days"
    elif value.lower() == "year to date":
        filter_value = "transaction-filter-date-year-to-date"
    elif value.lower() == "previous year":
        filter_value = "transaction-filter-date-previous-year"
    else:
        raise AutomationException(f"The are no such option as {value}")
    AccountsPage(context).get_transactions_tab().select_date_filter(filter_value)


@then("The transactions type filter contains unique events from table")
def verify_unique_types_in_transaction_filter(context):
    unique_values = list(set([row.event for row in context.transaction_rows]))
    filter_values = AccountsPage(context).get_transactions_tab().get_existing_type_filter_options()
    for value in unique_values:
        Assert.contains(value, filter_values)


@then("No transactions are present in the table")
def verify_no_transactions(context):
    is_no_transactions = AccountsPage(context).get_transactions_tab().is_no_transactions_exist()
    Assert.is_true(is_no_transactions)


@then("All transactions type filter options can filter data table correctly")
def verify_transaction_type_filtered_correctly(context):
    filter_values = AccountsPage(context).get_transactions_tab().get_existing_type_filter_options().split("\n")
    for value in filter_values[1:]:
        AccountsPage(context).get_transactions_tab().select_type_filter(value)
        extract_table_data(context)
        unique_value = list(set([row.event for row in context.transaction_rows]))
        Assert.is_equal(unique_value, [value])


@then('The transactions type filter contains "{value}"')
def verify_transaction_type_filter(context, value):
    filter_values = AccountsPage(context).get_transactions_tab().get_existing_type_filter_options().split("\n")
    Assert.is_equal(filter_values, [value])
