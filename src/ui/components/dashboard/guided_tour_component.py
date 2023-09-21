# noqa: FNE001
from selenium.common import TimeoutException

from src.helpers.assertions import Assert
from src.ui.components.web_element import Element
from src.ui.locator import Locators


class GuidedTour(Element):
    # Selectors
    _txt_header = ".shepherd-title"
    _txt_content = ".shepherd-text"
    _btn_skip = ".skip-tour-button"
    _btn_back = ".back-tour-button"
    _btn_next = ".next-button"

    # Locators
    txt_header = Locators.css(_txt_header)
    txt_content = Locators.css(_txt_content)
    btn_next = Locators.css(_btn_next)
    btn_back = Locators.css(_btn_back)
    btn_skip = Locators.css(_btn_skip)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def guided_tour(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    # Getters
    def get_header(self):
        return self.get_child_element(child_locator=self.txt_header, base_element=self.guided_tour)

    def get_content(self):
        return self.get_child_element(child_locator=self.txt_content, base_element=self.guided_tour)

    # Actions
    def go_to_next_step(self):
        btn_next = self.get_child_element(child_locator=self.btn_next, base_element=self.guided_tour)
        self.click_element(element=btn_next)

    def go_to_back_step(self):
        self.get_child_element(child_locator=self.btn_back, base_element=self.guided_tour).click()

    def skip_tour(self):
        self.get_child_element(child_locator=self.btn_skip, base_element=self.guided_tour).click()

    def get_next_button_text(self):
        return self.get_child_element(child_locator=self.btn_next, base_element=self.guided_tour).text

    # Verifications
    def verify_header(self, expected_header):
        actual_header = self.get_header().text
        Assert.is_equal(actual_header, expected_header, "Header is not correct.")

    def verify_content(self, expected_content):
        actual_content = self.get_content().text
        Assert.is_equal(actual_content, expected_content, "Content is not correct.")

    def is_skip_button_is_present(self) -> bool:
        try:
            self.get_child_element(child_locator=self.btn_skip, base_element=self.guided_tour)
        except TimeoutException:
            return False
        return True

    def verify_back_button_is_hidden(self):
        self.wait_elements_invisibility(self.btn_back)
