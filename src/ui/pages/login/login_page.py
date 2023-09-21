# noqa: FNE001
from src.helpers.assertions import Assert
from src.ui.locator import Locators
from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    # Selectors
    _email_field = "//input[@name='username']"
    _password_field = "//input[@name='password']"
    _btn_login = "//input[@id='okta-signin-submit']"
    _txt_input_error = "//p[contains(@class, 'input-error')]"
    _txt_user_error = "//p[contains(@class, 'custom-error-label')]"

    # Locators
    txt_email = Locators.xpath(_email_field)
    txt_password = Locators.xpath(_password_field)
    txt_input_error = Locators.xpath(_txt_input_error)
    txt_user_error = Locators.xpath(_txt_user_error)
    btn_login = Locators.xpath(_btn_login)

    # Methods
    def __init__(self, context, endpoint=None):
        self.endpoint = "accounts/login" if endpoint is None else endpoint
        super().__init__(context, self.endpoint)

    def enter_credentials(self, email, password):
        self.web_element.clear_textbox_with_keyboard(self.txt_email)
        self.web_element.input_to_element(self.txt_email, input_text=email)
        self.web_element.clear_textbox_with_keyboard(self.txt_password)
        self.web_element.input_to_element(self.txt_password, input_text=password)

    def click_signin(self):
        self.web_element.get_visible_element(self.btn_login).click()
        self.web_element.wait_element_is_invisible(self.btn_login)

    def verify_redirection_from_login(self):
        url = self.get_page_url()
        Assert.not_contains(self.endpoint, url, "Login page is still opened")

    def verify_login_is_opened(self):
        url = self.get_page_url()
        Assert.contains(self.endpoint, url, "Login page is not opened")

    def verify_user_name_error_absent(self):
        is_error_absent = self.web_element.is_element_absent(self.txt_user_error)
        Assert.is_true(is_error_absent, "Wrong username")

    def verify_user_name_message(self, message):
        error = self.web_element.get_visible_element(self.txt_user_error).text
        Assert.is_equal(error, message)

    def verify_credentials_error_absent(self):
        is_error_absent = self.web_element.is_element_absent(self.txt_input_error)
        Assert.is_true(is_error_absent, "Wrong credentials")
