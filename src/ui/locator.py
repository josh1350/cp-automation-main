"""
Locator object module
"""
from collections import namedtuple

from selenium.webdriver.common.by import By


class Locators:
    """
    Class of Locator object builder
    """

    Locator = namedtuple("Locator", ["by", "value"])

    @staticmethod
    def css(value: str) -> Locator:
        """
        Building Locator object by css selector
        """
        return Locators.Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def xpath(value: str) -> Locator:
        """
        Building Locator object by xpath selector
        """
        return Locators.Locator(By.XPATH, value)

    @staticmethod
    def id_(value: str) -> Locator:
        """
        Building Locator object by ID
        """
        return Locators.Locator(By.ID, value)
