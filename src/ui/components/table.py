from src.ui.components.web_element import Element
from src.ui.locator import Locators


class Table(Element):
    _row = "tr"
    _cell = "td"

    row = Locators.css(_row)
    cell = Locators.css(_cell)

    def __init__(self, driver, table_locator, element=None):
        super().__init__(driver)
        self.locator = table_locator
        self.element = element

    @property
    def table(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    def get_rows(self):
        return self.get_child_elements_list(child_locator=self.row, base_element=self.table)

    def extract_row_text(self, start_row_index=1):
        rows = self.get_rows()
        return [[row.text.strip()] for row in rows[start_row_index:]]

    def extract_cells_data(self, start_row_index=1):
        rows = self.get_rows()
        data = []

        for row in rows[start_row_index:]:
            columns = self.get_child_elements_list(child_locator=self.cell, base_element=row, show_info_logs=False)
            data.append([column.text.strip() for column in columns])
        return data
