from src.ui.pages.login.login_page import LoginPage


class AdminLoginPage(LoginPage):
    def __init__(self, context):
        self.endpoint = "admin/login"
        super().__init__(context, self.endpoint)
