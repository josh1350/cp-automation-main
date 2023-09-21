from src.ui.components.web_element import Element
from src.ui.locator import Locators


class AdminNavBar(Element):
    # Selectors
    _btn_logout = "#logout-form"
    _btn_view_site = "#user-tools a"

    # Locators
    btn_logout = Locators.css(_btn_logout)
    btn_view_site = Locators.css(_btn_view_site)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def nav_bar(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    def get_logout_lnk(self):
        return self.get_child_element(child_locator=self.btn_logout, base_element=self.nav_bar)

    def get_view_site_lnk(self):
        return self.get_child_element(child_locator=self.btn_view_site, base_element=self.nav_bar)
