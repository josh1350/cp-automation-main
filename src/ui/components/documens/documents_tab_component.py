from src.ui.components.table_grid import TableGrid
from src.ui.components.web_element import Element
from src.ui.locator import Locators


class DocumentsTab(Element):
    # Selectors
    _table = ".table-grid__content"
    _no_documents = ".no-documents"

    # Locators
    tbl_grid = Locators.css(_table)
    lbl_no_documents = Locators.css(_no_documents)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def content(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    # Getters
    def get_table(self):
        table_element = self.get_child_element(child_locator=self.tbl_grid, base_element=self.content)
        return TableGrid(self.driver, element=table_element, table_locator=None)

    # Methods
    def is_no_documents_present(self) -> bool:
        return self.is_element_present(self.lbl_no_documents)
