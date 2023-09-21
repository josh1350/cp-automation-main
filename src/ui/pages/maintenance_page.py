from src.ui.locator import Locators
from src.ui.pages.base_page import BasePage


class MaintenancePage(BasePage):
    # Selectors
    _lbl_title = "#maintenance-title"
    _lbl_message = "#maintenance-message"

    # Locators
    lbl_title = Locators.css(_lbl_title)
    lbl_message = Locators.css(_lbl_message)

    # Methods
    def __init__(self, context):
        self.endpoint = "maintenance/"
        super().__init__(context, self.endpoint)

    def get_title(self):
        return self.web_element.get_visible_element(self.lbl_title)

    def get_message(self):
        return self.web_element.get_visible_element(self.lbl_message)
