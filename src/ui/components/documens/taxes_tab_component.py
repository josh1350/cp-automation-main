from src.ui.components.documens.documents_tab_component import DocumentsTab
from src.ui.components.filter import Filter
from src.ui.locator import Locators


class TaxesTab(DocumentsTab):
    _date_filter = "#reports-date-filter"
    _name_filter = "#reports-type-filter"
    _account_filter = "#reports-accounts-filter"

    # Locators
    sel_date_filter = Locators.css(_date_filter)
    sel_type_filter = Locators.css(_name_filter)
    sel_account_filter = Locators.css(_account_filter)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver, locator, element)

    # Getters

    def get_date_filter(self):
        date_element = self.get_child_element(child_locator=self.sel_date_filter, base_element=self.content)
        return Filter(self.driver, element=date_element)

    def get_account_filter(self):
        account_element = self.get_child_element(child_locator=self.sel_account_filter, base_element=self.content)
        return Filter(self.driver, element=account_element)

    def get_type_filter(self):
        date_element = self.get_child_element(child_locator=self.sel_type_filter, base_element=self.content)
        return Filter(self.driver, element=date_element)
