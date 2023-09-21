from src.ui.locator import Locators
from src.ui.pages.admin.admin_page import AdminPage


class AdminHomePage(AdminPage):
    # Selectors
    _lnk_maintenance_config = ".model-maintenanceconfig > th > a"
    _lnk_add_maintenance_config = ".model-maintenanceconfig  .addlink"
    _lnk_change_maintenance_config = ".model-maintenanceconfig  .changelink"

    # Locators
    lnk_maintenance_config = Locators.css(_lnk_maintenance_config)
    lnk_add_maintenance_config = Locators.css(_lnk_add_maintenance_config)
    lnk_change_maintenance_config = Locators.css(_lnk_change_maintenance_config)

    def __init__(self, context):
        self.endpoint = "admin/"
        super().__init__(context, self.endpoint)

    # Methods
    def click_add_maintenance_confid(self):
        self.web_element.get_visible_element(self.lnk_add_maintenance_config).click()

    def click_change_maintenance_confid(self):
        self.web_element.get_visible_element(self.lnk_change_maintenance_config).click()
