from src.ui.components.table import Table
from src.ui.locator import Locators


class TableGrid(Table):
    _row = ".table-grid__content--row"
    _year_row = ".table-grid__content--year"
    _cell = "div.w-full"
    _content = ".table-grid__content--block"

    row = Locators.css(_row)
    year_row = Locators.css(_year_row)
    cell = Locators.css(_cell)
    content = Locators.css(_content)

    def __init__(self, driver, table_locator, element=None):
        super().__init__(driver, table_locator, element)

    def get_year_blocks(self):
        return self.get_child_elements_list(child_locator=self.content, base_element=self.table)

    def extract_cells_data(self, start_row_index=0):
        year_content = self.get_year_blocks()
        data = {}

        for content in year_content:
            year = self.get_child_element(child_locator=self.year_row, base_element=content).text.strip()
            rows = self.get_child_elements_list(child_locator=self.row, base_element=content)
            for row in rows[start_row_index:]:
                columns = self.get_child_elements_list(child_locator=self.cell, base_element=row, show_info_logs=False)
                row_data = [column.text.strip() for column in columns]

                if year not in data:
                    data[year] = []

                data[year].append(row_data)

        return data
