from src.ui.components.settings.modal_window import ModalWindow
from src.ui.locator import Locators


class UpdatePasswordModal(ModalWindow):
    _btn_save = "#submit-password-update"
    _btn_cancel = "#cancel-password-update"
    _fld_current_password = "#current-password-input"
    _fld_new_password = "#new-password-input"
    _fld_confirm_password = "#confirm-password-input"
    _lbl_password_error = "./parent::div/ul/li"
    _lbl_list_error = ".errorlist"
    _lbl_error = ".error"
    _lbl_password_criteria = ".password-criteria"
    _lbl_valid_password_criteria = ".valid-password-criteria"
    _lbl_invalid_password_criteria = ".invalid-password-criteria"
    _lbl_default_password_criteria = ".registration-text"
    _btn_toggle_password = "./parent::div/button[@id='toggle-password']"

    fld_current_password = Locators.css(_fld_current_password)
    fld_new_password = Locators.css(_fld_new_password)
    fld_confirm_password = Locators.css(_fld_confirm_password)
    lbl_password_error = Locators.xpath(_lbl_password_error)
    lbl_errors = Locators.css(_lbl_list_error)
    lbl_error = Locators.css(_lbl_error)
    lbl_password_criteria = Locators.css(_lbl_password_criteria)
    lbl_valid_password_criteria = Locators.css(_lbl_valid_password_criteria)
    lbl_invalid_password_criteria = Locators.css(_lbl_invalid_password_criteria)
    lbl_default_password_criteria = Locators.css(_lbl_default_password_criteria)
    btn_toggle_password = Locators.xpath(_btn_toggle_password)
    btn_save = Locators.css(_btn_save)
    btn_cancel = Locators.css(_btn_cancel)

    def __init__(self, driver, locator=None, element=None):
        super().__init__(driver, locator, element)

    def get_fld_current_password(self):
        return self.get_child_element(self.fld_current_password, self.get_body())

    def get_fld_new_password(self):
        return self.get_child_element(self.fld_new_password, self.get_body())

    def get_fld_confirm_password(self):
        return self.get_child_element(self.fld_confirm_password, self.get_body())

    def get_password_criteria(self):
        return self.get_visible_element(self.lbl_password_criteria)

    def get_field_toggle(self, field):
        return self.get_child_element(self.btn_toggle_password, base_element=field)

    def get_field_toggle_status(self, field):
        return self.get_field_toggle(field).text.strip()

    def get_valid_criteria_list(self):
        criteria_elements = self.get_child_elements_list(
            self.lbl_valid_password_criteria, base_element=self.get_password_criteria()
        )
        return [element.text.strip() for element in criteria_elements]

    def get_invalid_criteria_list(self):
        criteria_elements = self.get_child_elements_list(
            self.lbl_invalid_password_criteria, base_element=self.get_password_criteria()
        )
        return [element.text.strip() for element in criteria_elements]

    def get_default_criteria_list(self):
        criteria_elements = self.get_child_elements_list(
            self.lbl_invalid_password_criteria, base_element=self.get_password_criteria()
        )
        return [element.text.strip() for element in criteria_elements]

    def get_field_error_text(self, field):
        return self.get_child_element(self.lbl_password_error, base_element=field).text.strip()

    def wait_for_error(self):
        return self.get_visible_element(self.lbl_error)

    def get_error_list_text(self):
        return self.get_child_element(self.lbl_errors, base_element=self.modal).text.strip()

    def is_criteria_list_absent(self) -> bool:
        return self.is_element_absent(self.lbl_password_criteria, delay=1)

    def input_current_password(self, password):
        self.cleanup_current_password()
        self.input_to_element(element=self.get_fld_current_password(), input_text=password)

    def input_new_password(self, password):
        self.cleanup_new_password()
        self.input_to_element(element=self.get_fld_new_password(), input_text=password)

    def input_confirm_password(self, password):
        self.cleanup_confirm_password()
        self.input_to_element(element=self.get_fld_confirm_password(), input_text=password)

    def cleanup_current_password(self):
        self.clear_textbox_with_keyboard(element=self.get_fld_current_password())

    def cleanup_new_password(self):
        self.clear_textbox_with_keyboard(element=self.get_fld_new_password())

    def cleanup_confirm_password(self):
        self.clear_textbox_with_keyboard(element=self.get_fld_confirm_password())
