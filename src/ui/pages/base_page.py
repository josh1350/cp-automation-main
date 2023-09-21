from dotenv import load_dotenv

from src.helpers.logger import Log
from src.ui.components.web_element import Element

log = Log().logger
load_dotenv()


class BasePage:
    def __init__(self, context, endpoint=""):
        self.context = context
        self.endpoint = endpoint
        self.baseUrl = context.base_url
        context.endpoint = self.endpoint

    @property
    def web_element(self):
        return Element(self.context.driver)

    def open(self):
        """
        Open the Page.

        :return: Page object
        """
        self.context.driver.get(self.baseUrl + self.endpoint)

    def get_page_url(self):
        """
        Page url.

        :return: Page url
        """
        return self.context.driver.current_url
