# noqa: FNE001
from src.helpers.assertions import Assert
from src.helpers.logger import Log
from src.ui.components.dashboard.guided_tour_component import GuidedTour
from src.ui.components.dashboard.paperless_component import Paperless
from src.ui.components.table import Table
from src.ui.locator import Locators
from src.ui.pages.portal_page import PortalPage

log = Log().logger


class DashboardPage(PortalPage):
    # Selectors
    _profile_title = "//p[contains(@class, 'profile-title')]"
    _shepherd = "//div[@class='shepherd-content']/parent::div[not(@hidden)]"
    _investments_heading = "#investments-heading"
    _paperless_block = "#paperless-block"
    _profile_block = "#profile-block"
    _applications_block = "#applications-block"
    _dashboard_block = "#dashboard"
    _documents_table = "#documents-table"

    # Locators
    tour_popup = Locators.xpath(_shepherd)
    txt_profile_title = Locators.xpath(_profile_title)
    investments_heading = Locators.css(_investments_heading)
    block_paperless = Locators.css(_paperless_block)
    block_profile = Locators.css(_profile_block)
    block_applications = Locators.css(_applications_block)
    block_dashboard = Locators.css(_applications_block)
    tbl_documents = Locators.css(_documents_table)

    def __init__(self, context):
        self.endpoint = "clientportal/"
        super().__init__(context, self.endpoint)

    # Methods
    def verify_prof_info(self, expected_info):
        info = self.web_element.get_visible_element(self.txt_profile_title).text
        Assert.is_equal(expected_info, info, f"{expected_info} is not present on the page")

    def get_guided_tour(self):
        # TODO: Test should passed without scrolling
        self.web_element.execute_script("window.scrollBy(0,1)")
        guided_tour = GuidedTour(self.context.driver, self.tour_popup)
        return guided_tour

    def get_paperless_block(self):
        paperless = Paperless(self.context.driver, self.block_paperless)
        return paperless

    def get_documents_table(self):
        documents_table = Table(self.context.driver, self.tbl_documents)
        return documents_table

    def get_documents_rows(self):
        return self.get_documents_table().get_rows()

    def verify_dashboard_is_present(self):
        self.web_element.is_element_present(self.block_dashboard)
        active_tab_name = self.nav_bar.get_active_tab()
        Assert.is_equal(
            active_tab_name,
            "Dashboard",
            f"You are not on the Dashboard Page. {self.get_page_url()} is opened",
        )

    def verify_guided_tour_is_hidden(self):
        self.web_element.wait_elements_invisibility(self.tour_popup)

    def wait_guided_tour_is_hidden(self):
        self.web_element.wait_element_is_invisible(self.tour_popup)

    def is_paperless_block_absent(self) -> bool:  # noqa: FNE001
        is_absent = self.web_element.is_element_absent(self.block_paperless, delay=5)
        return is_absent

    def verify_guided_tour_is_absent(self):
        is_absent = self.web_element.is_element_absent(self.tour_popup, delay=10)
        Assert.is_true(is_absent, "Guided Tour is present, should be absent.")

    def verify_element_is_in_tour(self, element_locator):
        guided_element_class = "shepherd-enabled shepherd-target"
        element_class = self.web_element.get_visible_element(element_locator).get_attribute("class")
        Assert.contains(guided_element_class, element_class, "Expected element is not highlighted by the Guided Tour")
