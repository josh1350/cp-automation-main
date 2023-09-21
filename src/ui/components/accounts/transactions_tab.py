from src.ui.components.filter import Filter
from src.ui.components.table import Table
from src.ui.components.web_element import Element
from src.ui.locator import Locators


class TransactionsTab(Element):
    # Selectors
    _date_filter = "#date-filter"
    _type_filter = "#type-filter"
    _transactions_expand = "#transactions-expand"
    _no_transactions = ".no-transactions-block"
    _table = "//div[@class='transaction-data-wrapper']//table"

    # Locators
    sel_date_filter = Locators.css(_date_filter)
    sel_type_filter = Locators.css(_type_filter)
    btn_transactions_expand = Locators.css(_transactions_expand)
    lbl_no_transactions = Locators.css(_no_transactions)
    table = Locators.xpath(_table)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver)
        self.content = self._element(locator=locator, element=element, timeout=self.timeout)

    def select_date_filter(self, value):
        date_element = self.get_child_element(child_locator=self.sel_date_filter, base_element=self.content)
        date_filter = Filter(self.driver, element=date_element)
        date_filter.select(value=value)

    def select_type_filter(self, value):
        type_element = self.get_child_element(child_locator=self.sel_type_filter, base_element=self.content)
        type_filter = Filter(self.driver, element=type_element)
        type_filter.select(value=value)

    def get_existing_type_filter_options(self):
        return self.get_visible_element(self.sel_type_filter).text.strip()

    def get_rows_data(self):
        return Table(self.driver, self.table).extract_cells_data()

    def is_expand_exist(self) -> bool:
        return self.is_element_present(self.btn_transactions_expand)

    def is_no_transactions_exist(self) -> bool:
        return self.is_element_present(self.lbl_no_transactions)

    def expand_data(self):
        self.get_visible_element(self.btn_transactions_expand).click()
