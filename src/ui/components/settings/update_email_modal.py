from src.ui.components.settings.modal_window import ModalWindow
from src.ui.locator import Locators


class UpdateEmailModal(ModalWindow):
    _modal_title = "#updateEmailModalLabel"
    _fld_password = "#current-password"
    _toggle_password = "#toggle-password"
    _fld_email_address = "#email-address"
    _lbl_password_error = "div:nth-child(1) > p"
    _lbl_email_error = "div:nth-child(2) > p"

    fld_password = Locators.css(_fld_password)
    fld_email_address = Locators.css(_fld_email_address)
    lbl_password_error = Locators.css(_lbl_password_error)
    lbl_email_error = Locators.css(_lbl_email_error)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver, locator, element)

    def get_fld_email(self):
        return self.get_child_element(self.fld_email_address, self.get_body())

    def get_fld_password(self):
        return self.get_child_element(self.fld_password, self.get_body())

    def get_error_password(self):
        return self.get_visible_element(self.lbl_password_error)

    def get_error_email(self):
        return self.get_visible_element(self.lbl_email_error)

    def input_email(self, email):
        self.cleanup_email()
        self.input_to_element(element=self.get_fld_email(), input_text=email)

    def cleanup_email(self):
        self.clear_textbox_with_keyboard(element=self.get_fld_email())

    def input_password(self, password):
        self.cleanup_password()
        self.input_to_element(element=self.get_fld_password(), input_text=password)

    def cleanup_password(self):
        self.clear_textbox_with_keyboard(element=self.get_fld_password())
