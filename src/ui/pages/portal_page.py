from src.ui.components.common.nav_bar_component import NavBar
from src.ui.locator import Locators
from src.ui.pages.base_page import BasePage


class PortalPage(BasePage):
    def __init__(self, context, endpoint=""):
        super().__init__(context, endpoint)
        self.nav_bar = NavBar(context.driver, locator=Locators.xpath("//nav"))
