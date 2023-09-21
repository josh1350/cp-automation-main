from src.helpers.logger import Log
from src.ui.locator import Locators
from src.ui.pages.base_page import BasePage

log = Log().logger


class DocumentsPreviewPage(BasePage):
    # Selectors
    _pdf_element = "#pdf-view"

    # Locators
    pdf_element = Locators.css(_pdf_element)

    def __init__(self, context):
        self.endpoint = "clientportal/document/?documentType="
        super().__init__(context, self.endpoint)

    # Getters
    def get_pdf_element(self):
        return self.web_element.get_visible_element(self.pdf_element)
