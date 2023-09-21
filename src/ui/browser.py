from typing import Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.helpers.logger import BrowserLogger


class Browser:
    def __init__(self):
        self.driver = webdriver
        self.__browser = None

    @property
    def browser_logger(self):
        return BrowserLogger()

    def init_driver(
        self,
        browser_name: str,
        is_headless: bool = False,
        is_maximize: bool = True,
        screen_resolution: Tuple = (1920, 1080),
    ):
        """
        Common method for getting browser driver per it's name
        :param is_headless: Boolean value whether to run browser in headless mode
        :param is_maximize: Boolean value whether to run browser in maximize window size
        :param browser_name: Browser name in string format
        :param screen_resolution: Browser screen resolution
        :return: Browser driver instance (with resolution updated from BrowserSetup)
        """
        if browser_name.lower() == "chrome":
            driver = self.chrome(is_headless=is_headless, screen_resolution=screen_resolution)
        elif browser_name.lower() == "edge":
            driver = self.edge_chromium(is_headless=is_headless)
        else:
            raise Exception(f"Unsupported browser {browser_name}")
        if is_maximize:
            driver.maximize_window()
        else:
            driver.set_window_size(*screen_resolution)
        self.__browser = driver
        return driver

    def chrome(self, is_headless: bool = False, screen_resolution: Tuple = (1920, 1080)):
        """
        Google Chrome driver
        :param is_headless: Boolean value whether to run browser in headless mode
        :param screen_resolution: Browser screen resolution
        :return: Instance of Google Chrome driver
        """

        driver = self.driver
        service = Service()
        options = driver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless")
            options.add_argument(f"--window-size={screen_resolution[0]},{screen_resolution[1]}")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        chrome_driver = driver.Chrome(service=service, options=options)
        return chrome_driver

    def edge_chromium(self, is_headless: bool = False, screen_resolution: Tuple = (1920, 1080)):
        """
        Edge driver
        :param is_headless: Boolean value whether to run browser in headless mode
        :param screen_resolution: Browser screen resolution
        :return: Instance of Edge driver
        """

        driver = self.driver
        options = driver.EdgeOptions()
        if is_headless:
            options.add_argument("--headless")
            options.add_argument(f"--window-size={screen_resolution[0]},{screen_resolution[1]}")
        chromium_driver = driver.Edge(options=options)
        return chromium_driver

    def save_browser_console_log(self):
        browser_log = self.browser_logger.browser_logger

        logs = self.__browser.get_log("browser")
        for console_log in logs:
            browser_log.warning(f"Browser Log: {console_log['message']}")

    def switch_to_tab(self, part_url):
        handles = self.__browser.window_handles

        for handle in handles:  # noqa: VNE002
            self.__browser.switch_to.window(handle)
            if part_url in self.__browser.current_url:
                return self.__browser
