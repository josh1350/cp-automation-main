from src.ui.components.settings.update_email_modal import UpdateEmailModal
from src.ui.components.settings.update_password_modal import UpdatePasswordModal
from src.ui.components.settings.update_success_modal import UpdateSuccessModal
from src.ui.locator import Locators
from src.ui.pages.portal_page import PortalPage


class SettingsPage(PortalPage):
    # Selectors
    _lnk_update_email = "//a[contains(@data-bs-target, '#updateEmailModal')]"
    _lnk_update_phone = "//a[contains(@data-bs-target, '#phoneNumber')]"
    _lnk_update_password = "//a[contains(@data-bs-target, '#password')]"
    _lnk_paperless = "//h3[text()='Paperless Setting']/following-sibling::a"
    _lnk_guided_tour = "//a[contains(@onclick, 'guidedTourKeyName')]"
    _lbl_email = "#profileEmail"
    _lbl_mobile = "#formatted-phone-number"
    _lbl_email_detail = ".settings__section:nth-child(1) .text-detail"
    _lbl_phone_detail = ".settings__section:nth-child(2) .text-detail"
    _lbl_password_detail = ".settings__section:nth-child(3) .text-detail"

    _modal_email = "#updateEmailModal .modal-content"
    _modal_password = "#password .modal-content"
    _success_email_modal = "#settingsChangeSuccessModal"
    _success_phone_modal = "#phoneChangeSuccessModal"
    _success_password_modal = "#passwordChangeSuccessModal"

    # Locators
    lnk_update_email = Locators.xpath(_lnk_update_email)
    lnk_update_phone = Locators.xpath(_lnk_update_phone)
    lnk_update_password = Locators.xpath(_lnk_update_password)
    lnk_paperless = Locators.xpath(_lnk_paperless)
    lnk_guided_tour = Locators.xpath(_lnk_guided_tour)

    lbl_email = Locators.css(_lbl_email)
    lbl_mobile = Locators.css(_lbl_mobile)

    lbl_email_detail = Locators.css(_lbl_email_detail)
    lbl_phone_detail = Locators.css(_lbl_phone_detail)
    lbl_password_detail = Locators.css(_lbl_password_detail)

    modal_email = Locators.css(_modal_email)
    modal_password = Locators.css(_modal_password)
    success_email_modal = Locators.css(_success_email_modal)
    success_phone_modal = Locators.css(_success_phone_modal)
    success_password_modal = Locators.css(_success_password_modal)

    def __init__(self, context):
        self.endpoint = "clientportal/settings"
        super().__init__(context, self.endpoint)

    # Getters
    def update_email_modal(self):
        return UpdateEmailModal(self.context.driver, self.modal_email)

    def update_password_modal(self):
        return UpdatePasswordModal(self.context.driver, self.modal_password)

    def get_success_email_update_modal(self):
        return UpdateSuccessModal(self.context.driver, self.success_email_modal)

    def get_success_phone_update_modal(self):
        return UpdateSuccessModal(self.context.driver, self.success_phone_modal)

    def get_success_password_update_modal(self):
        return UpdateSuccessModal(self.context.driver, self.success_password_modal)

    def get_email_from_details(self):
        return self.web_element.get_visible_element(self.lbl_email).text.strip()

    def get_mobile_from_details(self):
        return self.web_element.get_visible_element(self.lbl_mobile).text.strip()

    def get_email_details(self):
        return self.web_element.get_visible_element(self.lbl_email_detail).text.strip()

    def get_phone_details(self):
        return self.web_element.get_visible_element(self.lbl_phone_detail).text.strip()

    def get_password_details(self):
        return self.web_element.get_visible_element(self.lbl_password_detail).text.strip()

    # Methods
    def start_guided_tour(self):
        self.web_element.get_visible_element(self.lnk_guided_tour).click()
        self.web_element.wait_element_is_invisible(self.lnk_guided_tour)

    def open_update_email(self):
        self.web_element.click_element(self.lnk_update_email)

    def open_update_password(self):
        self.web_element.click_element(self.lnk_update_password)
