from src.helpers.assertions import Assert
from src.ui.components.web_element import Element
from src.ui.locator import Locators


class Paperless(Element):
    # Selectors
    _txt_label = ".go-paperless-label"
    _btn_get_started = "#start-paperless-button"
    _lnk_dismiss = "#dismiss-paperless-link"
    _lnk_settings = "#paperless-settings-link"

    # Locators
    txt_label = Locators.css(_txt_label)
    btn_get_started = Locators.css(_btn_get_started)
    lnk_dismiss = Locators.css(_lnk_dismiss)
    lnk_settings = Locators.css(_lnk_settings)

    def __init__(self, driver, locator, element=None):
        super().__init__(driver)
        self.locator = locator
        self.element = element

    @property
    def paperless(self):
        return self._element(locator=self.locator, element=self.element, timeout=self.timeout)

    # Getters
    def get_label(self):
        return self.get_child_element(child_locator=self.txt_label, base_element=self.paperless)

    # Actions
    def click_dismiss(self):
        self.get_child_element(child_locator=self.lnk_dismiss, base_element=self.paperless).click()

    def click_get_started(self):
        self.get_child_element(child_locator=self.btn_get_started, base_element=self.paperless).click()

    def click_settings(self):
        self.get_child_element(child_locator=self.lnk_settings, base_element=self.paperless).click()

    # Verifications
    def verify_label(self, expected_label):
        actual_header = self.get_label().text
        Assert.is_equal(actual_header, expected_label, "The label is not correct.")

    def verify_get_started_is_absent(self):
        self.is_element_absent(self.btn_get_started)
