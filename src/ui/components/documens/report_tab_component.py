from src.ui.components.documens.documents_tab_component import DocumentsTab
from src.ui.components.filter import Filter
from src.ui.locator import Locators


class ReportsTab(DocumentsTab):
    _date_filter = "#reports-date-filter"

    # Locators
    sel_date_filter = Locators.css(_date_filter)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver, locator, element)

    # Getters

    def get_date_filter(self):
        date_element = self.get_child_element(child_locator=self.sel_date_filter, base_element=self.content)
        return Filter(self.driver, element=date_element)
