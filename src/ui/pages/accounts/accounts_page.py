from src.helpers.logger import Log
from src.ui.components.accounts.transactions_tab import TransactionsTab
from src.ui.locator import Locators
from src.ui.pages.portal_page import PortalPage

log = Log().logger


class AccountsPage(PortalPage):
    # Selectors
    _transactions_tab = "#transactions-tab"
    _summary_tab = "#summary-tab"
    _allocation_tab = "#allocation-tab"
    _holdings_tab = "#holdings-tab"
    _transactions_content = "#transactions"
    _account_list = ".accounts-list-container"
    _accounts_subtext = ".account-subtext"

    # Locators
    summary_tab = Locators.css(_summary_tab)
    allocation_tab = Locators.css(_allocation_tab)
    holdings_tab = Locators.css(_holdings_tab)
    transactions_tab = Locators.css(_transactions_tab)
    transactions_content = Locators.css(_transactions_content)
    account_list = Locators.css(_account_list)
    accounts_subtext = Locators.css(_accounts_subtext)

    def __init__(self, context):
        self.endpoint = "clientportal/accounts/"
        super().__init__(context, self.endpoint)

    # Methods
    def get_transactions_tab(self):
        return TransactionsTab(self.context.driver, self.transactions_content)

    def open_summary_tab(self):
        self.web_element.get_visible_element(self.summary_tab).click()

    def open_allocation_tab(self):
        self.web_element.get_visible_element(self.allocation_tab).click()

    def open_holdings_tab(self):
        self.web_element.get_visible_element(self.holdings_tab).click()

    def open_transactions_tab(self):
        self.web_element.get_visible_element(self.transactions_tab).click()

    def open_account(self, text):
        account_list = self.web_element.get_visible_element(self.account_list)
        accounts = self.web_element.get_child_elements_list(
            base_element=account_list, child_locator=self.accounts_subtext
        )
        for account in accounts:
            if account.text == text:
                account.click()
                break
