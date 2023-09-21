from src.helpers.logger import Log
from src.ui.locator import Locators
from src.ui.pages.admin.admin_page import AdminPage

log = Log().logger


class AdminMaintenancePage(AdminPage):
    # Selectors
    _btn_add_maintenance_config = "li .addlink"
    _chk_maintenance_on = "#id_maintenance_on"
    _fld_title = "#id_title"
    _fld_message = "#id_message"
    _lnk_config_title = ".field-title a"
    _btn_save = "//input[@name = '_save']"
    _btn_save_and_add = "//input[@name = '_addanother']"
    _btn_save_and_continue = "//input[@name = '_continue']"
    _sel_config_action = "//select[@name = 'action']"
    _btn_go = "//button[@name = 'index']"
    _btn_yes = "//input[@type= 'submit']"
    _chk_select_all_configs = "#action-toggle"

    # Locators
    btn_add_maintenance_config = Locators.css(_btn_add_maintenance_config)
    chk_maintenance_on = Locators.css(_chk_maintenance_on)
    fld_title = Locators.css(_fld_title)
    fld_message = Locators.css(_fld_message)
    lnk_config_title = Locators.css(_lnk_config_title)
    chk_select_all_configs = Locators.css(_chk_select_all_configs)
    sel_config_action = Locators.xpath(_sel_config_action)
    btn_save = Locators.xpath(_btn_save)
    btn_go = Locators.xpath(_btn_go)
    btn_yes = Locators.xpath(_btn_yes)
    btn_save_and_add = Locators.xpath(_btn_save_and_add)
    btn_save_and_continue = Locators.xpath(_btn_save_and_continue)

    def __init__(self, context):
        self.endpoint = "admin/"
        super().__init__(context, self.endpoint)

    # Getters
    def get_maintenances(self):
        return self.web_element.get_visible_elements_list(self.lnk_config_title)

    # Methods
    def click_add_maintenance_confid(self):
        self.web_element.get_visible_element(self.btn_add_maintenance_config).click()

    def open_first_maintenance_confid(self):
        maintenance_list = self.get_maintenances()
        maintenance_list[0].click()

    def verify_add_maintenance_visibility(self):
        return self.web_element.is_element_clickable(self.btn_add_maintenance_config)

    def click_maintenance_on(self):
        self.web_element.get_visible_element(self.chk_maintenance_on).click()

    def save(self):
        self.web_element.get_visible_element(self.btn_save).click()

    def save_and_add(self):
        self.web_element.get_visible_element(self.btn_save_and_add).click()

    def save_and_continue(self):
        self.web_element.get_visible_element(self.btn_save_and_continue).click()

    def add_title(self, title):
        self.web_element.clear_textbox(self.fld_title)
        self.web_element.input_to_element(self.fld_title, input_text=title, log_input=True)

    def add_message(self, message):
        self.web_element.clear_textbox(self.fld_message)
        self.web_element.input_to_element(self.fld_message, input_text=message, log_input=True)

    def delete_all_configs(self):
        if self.web_element.is_element_present(self.chk_select_all_configs, timeout=5):
            self.web_element.get_visible_element(self.chk_select_all_configs).click()
            self.web_element.select_in_dropdown(locator=self.sel_config_action, value="delete_selected")
            self.web_element.get_visible_element(self.btn_go).click()
            self.web_element.get_visible_element(self.btn_yes).click()
        else:
            log.info("There are no maintenance config")
