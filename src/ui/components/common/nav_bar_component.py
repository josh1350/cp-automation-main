from src.ui.components.web_element import Element
from src.ui.locator import Locators


class NavBar(Element):
    # Selectors
    _tab_accounts = "#accounts-tab-link"
    _tab_documents = "#documents-tab-link"
    _tab_settings = "#settings-tab-link"
    _tab_logout = "//a[text()='Log Out']"
    _tab_dashboard = "//a[contains(text(),'Dashboard')]"
    _active_nav = ".active_nav"

    # Locators
    tab_accounts = Locators.css(_tab_accounts)
    tab_documents = Locators.css(_tab_documents)
    tab_settings = Locators.css(_tab_settings)
    active_nav = Locators.css(_active_nav)
    tab_logout = Locators.xpath(_tab_logout)
    tab_dashboard = Locators.xpath(_tab_dashboard)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def nav_bar(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    def get_dashboard_tab(self):
        return self.get_child_element(child_locator=self.tab_dashboard, base_element=self.nav_bar)

    def get_accounts_tab(self):
        return self.get_child_element(child_locator=self.tab_accounts, base_element=self.nav_bar)

    def get_documents_tab(self):
        return self.get_child_element(child_locator=self.tab_documents, base_element=self.nav_bar)

    def get_settings_tab(self):
        return self.get_child_element(child_locator=self.tab_settings, base_element=self.nav_bar)

    def get_logout_tab(self):
        return self.get_child_element(child_locator=self.tab_logout, base_element=self.nav_bar)

    def get_active_tab(self):
        return self.get_child_element(child_locator=self.active_nav, base_element=self.nav_bar).text.strip()
