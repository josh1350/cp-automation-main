from src.ui.components.common.admin_nav_bar_component import AdminNavBar
from src.ui.locator import Locators
from src.ui.pages.base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, context, endpoint=""):
        super().__init__(context, endpoint)
        self.nav_bar = AdminNavBar(context.driver, locator=Locators.css("#header"))
