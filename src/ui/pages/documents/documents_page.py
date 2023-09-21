from src.helpers.logger import Log
from src.ui.components.documens.mailing_tab_component import MailingsTab
from src.ui.components.documens.report_tab_component import ReportsTab
from src.ui.components.documens.statement_tab_component import StatementsTab
from src.ui.components.documens.taxes_tab_component import TaxesTab
from src.ui.locator import Locators
from src.ui.pages.portal_page import PortalPage

log = Log().logger


class DocumentsPage(PortalPage):
    # Selectors
    _statements_tab = "#home-tab"
    _reports_tab = "#profile-tab"
    _mailings_tab = "#mailing-tab"
    _taxes_tab = "#taxes-tab"
    _statements_tab_content = "#statements-tab-pane"
    _reports_tab_content = "#report-tab-pane"
    _mailings_tab_content = "#mailings-tab-pane"
    _taxes_tab_content = "#taxes-tab-pane"

    # Locators
    statements_tab = Locators.css(_statements_tab)
    reports_tab = Locators.css(_reports_tab)
    mailings_tab = Locators.css(_mailings_tab)
    taxes_tab = Locators.css(_taxes_tab)
    statements_tab_content = Locators.css(_statements_tab_content)
    reports_tab_content = Locators.css(_reports_tab_content)
    mailings_tab_content = Locators.css(_mailings_tab_content)
    taxes_tab_content = Locators.css(_taxes_tab_content)

    def __init__(self, context):
        self.endpoint = "clientportal/documents/"
        super().__init__(context, self.endpoint)

    # Getters
    def get_statements_tab(self):
        return StatementsTab(self.context.driver, self.statements_tab_content)

    def get_reports_tab(self):
        return ReportsTab(self.context.driver, self.reports_tab_content)

    def get_mailings_tab(self):
        return MailingsTab(self.context.driver, self.mailings_tab_content)

    def get_taxes_tab(self):
        return TaxesTab(self.context.driver, self.taxes_tab_content)

    # Methods
    def open_statements_tab(self):
        self.web_element.get_visible_element(self.statements_tab).click()

    def open_reports_tab(self):
        self.web_element.get_visible_element(self.reports_tab).click()

    def open_mailings_tab(self):
        self.web_element.get_visible_element(self.mailings_tab).click()

    def open_taxes_tab(self):
        self.web_element.get_visible_element(self.taxes_tab).click()
