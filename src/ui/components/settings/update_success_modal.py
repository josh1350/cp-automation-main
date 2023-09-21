from src.helpers.logger import Log
from src.ui.components.settings.modal_window import ModalWindow
from src.ui.locator import Locators

log = Log().logger


class UpdateSuccessModal(ModalWindow):
    _btn_close = ".btn-close"

    btn_close = Locators.css(_btn_close)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver, locator, element)

    def close(self):
        close_element = self.get_child_element(self.btn_close, base_element=self.get_header())
        self.click_element(element=close_element)
        close_locator = Locators.css(f"{self.locator.value} {self._btn_close}")
        self.wait_element_is_invisible(close_locator)
        if self.is_element_clickable(close_locator):
            log.info("Browser: Retrying close modal")
            self.close()
