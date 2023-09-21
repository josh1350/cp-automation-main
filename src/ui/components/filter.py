from src.ui.components.web_element import Element
from src.ui.locator import Locators


class Filter(Element):
    _option = "option"

    opt = Locators.css(_option)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def filter(self):  # noqa: FNE002
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    # Getters
    def get_option_values(self):
        options = self.get_child_elements_list(child_locator=self.opt, base_element=self.filter)
        return [option.get_attribute("value").strip() for option in options]

    def get_option_texts(self):
        child_elements = self.get_child_elements_list(child_locator=self.opt, base_element=self.filter)
        return [element.text for element in child_elements]

    # Methods
    def select(self, value="", text=""):
        self.select_in_dropdown(element=self.filter, value=value, visible_text=text)
