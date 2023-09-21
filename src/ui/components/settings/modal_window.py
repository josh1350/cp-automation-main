from src.ui.components.web_element import Element
from src.ui.locator import Locators


class ModalWindow(Element):
    _header = ".modal-header"
    _modal_title = ".modal-title"
    _body = ".modal-body"
    _footer = ".modal-footer"
    _btn_cancel = ".actionButton"
    _btn_save = "button.actionButton"

    header = Locators.css(_header)
    modal_title = Locators.css(_modal_title)
    body = Locators.css(_body)
    footer = Locators.css(_footer)
    btn_cancel = Locators.css(_btn_cancel)
    btn_save = Locators.css(_btn_save)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def modal(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    def get_footer(self):
        return self.get_child_element(self.footer, self.modal)

    def get_body(self):
        return self.get_child_element(self.body, self.modal)

    def get_header(self):
        return self.get_child_element(self.header, self.modal)

    def get_title(self):
        return self.get_child_element(self.modal_title, self.modal)

    def save(self):
        save = self.get_child_element(self.btn_save, base_element=self.get_footer())
        save.click()

    def cancel(self):
        cancel = self.get_child_element(self.btn_cancel, base_element=self.get_footer())
        cancel.click()
