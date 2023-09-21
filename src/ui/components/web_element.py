# flake8: noqa
from typing import List

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.helpers.logger import Log
from src.ui.locator import Locators

log = Log().logger


class Element:
    def __init__(self, driver):
        self.driver = driver
        self.locator_css = Locators.css
        self.locator_xpath = Locators.xpath
        self.locator_id = Locators.id_
        self.keys = Keys
        self.timeout = 10

    # Getters

    def _element(
        self,
        locator: Locators.Locator,
        element: WebElement,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> WebElement:
        """
        Get element object accepting either Web element or it's locator
        Is needed to use both possible options for other action methods

        :param locator: Locator to find element
        :param element: itself
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        if element:
            return element
        elif locator:
            return self.get_visible_element(locator, timeout=timeout, show_error_logs=show_error_logs)
        else:
            raise Exception("Unknown way to define an element")

    def get_visible_element(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> WebElement:
        """
        Find visible element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg=f"Browser: Finding  element (visible) with locator {locator}")
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(
                ec.visibility_of_element_located(locator=locator)
            )
            return element
        except TimeoutException:
            error = f"Cannot find visible element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def get_present_element(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> WebElement:
        """
        Find present element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg=f"Browser: Finding element (present) with locator {locator}")
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located(locator=locator))
            return element
        except TimeoutException:
            error = f"Cannot find present element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def get_clickable_element(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> WebElement:
        """
        Find clickable element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg=f"Browser: Finding element (present) with locator {locator}")
        try:
            element = WebDriverWait(self.driver, timeout=timeout).until(ec.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            error = f"Cannot find clickable element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def get_visible_elements_list(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> List[WebElement]:
        """
        Find multiple visible elements

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: List of web elements
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg=f"Browser: Finding multiple elements list (visible) with locator {locator}")
        try:
            elements_list = WebDriverWait(self.driver, timeout=timeout).until(
                ec.visibility_of_all_elements_located(locator=locator)
            )
            return elements_list
        except TimeoutException:
            error = f"Cannot find list of visible elements with locator {locator} within {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def get_present_elements_list(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ) -> List[WebElement]:
        """
        Find multiple present elements

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: List of web elements
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg=f"Browser: Finding multiple elements list (present) with locator {locator}")
        try:
            elements_list = WebDriverWait(self.driver, timeout=timeout).until(
                ec.presence_of_all_elements_located(locator=locator)
            )
            return elements_list
        except TimeoutException:
            error = f"Cannot find list of present elements with locator {locator} within {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def get_child_element(
        self,
        child_locator: Locators.Locator,
        base_element: WebElement = None,
        base_locator: Locators.Locator = None,
        timeout: float = None,
    ) -> WebElement:
        """
        Find child element

        :param child_locator: Locator of the child element
        :param base_element: Base element itself (if possible)
        :param base_locator: Locator to find base element
        :param timeout: Time limit to find base element
        :return: Child web element
        """
        if timeout is None:
            timeout = self.timeout

        log.info(f"Browser: Finding child element with it's locator {child_locator}")
        parent_el = self._element(locator=base_locator, element=base_element, timeout=timeout)
        try:
            child_el = WebDriverWait(parent_el, timeout).until(
                ec.presence_of_element_located((child_locator.by, child_locator.value))
            )
            return child_el
        except NoSuchElementException:
            error = f"Cannot find child element with locator {child_locator}"
            log.error(msg=error)
            raise AssertionError(error)

    def get_child_elements_list(
        self,
        child_locator: Locators.Locator,
        base_element: WebElement = None,
        base_locator: Locators.Locator = None,
        timeout: float = None,
        show_info_logs=True,
    ) -> List[WebElement]:
        """
        Find child element

        :param child_locator: Locator of the child elements
        :param base_element: Base element itself (if possible)
        :param base_locator: Locator to find base element
        :param timeout: Time limit to find base element
        :param show_info_logs: Display logs or not
        :return: List of child web elements
        """
        if timeout is None:
            timeout = self.timeout
        if show_info_logs:
            log.info(f"Browser: Finding multiple child elements list with locator {child_locator}")
        parent_el = self._element(locator=base_locator, element=base_element, timeout=timeout)
        try:
            child_elements = parent_el.find_elements(by=child_locator.by, value=child_locator.value)
            return child_elements
        except NoSuchElementException:
            error = f"Cannot find multiple child elements list with locator {child_locator}"
            log.error(msg=error)
            raise AssertionError(error)

    def is_element_displayed(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        timeout: float = None,
    ) -> bool:
        """
        Check that element is displayed (with is_displayed() element's method). \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find the element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        :return: Boolean value whether element is displayed
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg="Browser: Checking that element is displayed")
        try:
            is_displayed = self._element(
                locator=locator, element=element, timeout=timeout, show_error_logs=False
            ).is_displayed()
            return is_displayed
        except (TimeoutException, AssertionError):
            log.info(msg="Browser: Element is not found")
            return False

    def is_element_present(self, locator: Locators.Locator = None, timeout: float = None) -> bool:
        """
        Check that element is present in DOM (aka find element).

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :return: Boolean value whether element is present in DOM
        """
        if timeout is None:
            timeout = self.timeout

        log.info(f"Browser: Checking that element is present in DOM with locator {locator}")
        try:
            self.get_present_element(locator=locator, timeout=timeout, show_error_logs=False)
            log.info(msg="Browser: Element is found")
            return True
        except (TimeoutException, AssertionError):
            log.info(msg="Browser: Element is not found")
            return False

    def is_element_absent(self, locator: Locators.Locator = None, timeout: float = None, delay: float = None) -> bool:
        """
        Check that element is absent in DOM.

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :param delay: Time limit to wait element
        :return: Boolean value whether element is absent in DOM
        """
        if timeout is None:
            timeout = self.timeout

        log.info(f"Browser: Checking that element is absent in DOM with locator {locator}")
        if delay is not None:
            try:
                self.get_visible_element(locator=locator, timeout=delay, show_error_logs=False)
            except AssertionError:
                log.info(f"Element is absent after {delay} seconds")

        try:
            self.wait_elements_invisibility(locator=locator, timeout=timeout, show_error_logs=False)
            log.info(msg="Browser: Element is absent")
            return True
        except (TimeoutException, AssertionError):
            log.info(msg="Browser: Element is present")
            return False

    def is_element_clickable(self, locator: Locators.Locator = None, timeout: float = None, delay: float = None) -> bool:
        """
        Check that element is clickable.

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :param delay: Time limit to find element
        :return: Boolean value whether element is clickable
        """
        if delay is not None:
            try:
                self.get_visible_element(locator=locator, timeout=delay, show_error_logs=False)
            except AssertionError:
                log.info(f"Element is not present after {delay} seconds")

        log.info(f"Browser: Checking that element is clickable with locator {locator}")
        try:
            self.get_clickable_element(locator=locator, timeout=timeout, show_error_logs=False)
            log.info(msg="Browser: Element is clickable")
            return True
        except (TimeoutException, AssertionError):
            log.info(msg="Browser: Element is not clickable")
            return False

    # Setters

    def input_to_element(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        input_text="",
        timeout: float = None,
        log_input: bool = False,
    ):
        """
        Input some text to element. \n
        Accepts either element's locator or element itself

        :param locator: Locator to find the element
        :param element:  itself (if possible)
        :param input_text: Value to input to the element
        :param timeout: Time limit to find element
        :param log_input: Bool value whether to log input
        """
        if timeout is None:
            timeout = self.timeout

        el = self._element(locator=locator, element=element, timeout=timeout)
        if log_input:
            log.info(f"Browser: making input to element: '{input_text}'")
        else:
            log.info("Browser: making input to element: (hidden input)")
        el.send_keys(input_text)

    def select_in_dropdown(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        visible_text="",
        value="",
        index: int = None,
        timeout: float = None,
    ):  # noqa: CFQ002
        """
        Input some text to element. \n
        Accepts either element's locator or element itself

        :param locator: Locator to find the element
        :param element:  itself (if possible)
        :param visible_text: visible text in select element
        :param value: value in select element
        :param index: index in select element
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        dropdown_element = self._element(locator=locator, element=element, timeout=timeout)
        dropdown = Select(dropdown_element)
        if visible_text != "":
            dropdown.select_by_visible_text(visible_text)
            log.info(msg=f"Browser: Selected from dropdown by visible text - {visible_text}")

        elif value != "":
            dropdown.select_by_value(value)
            log.info(msg=f"Browser: Selected from dropdown by value - {value}")

        elif index:
            dropdown.select_by_index(index)
            log.info(msg=f"Browser: Selected from dropdown by index - {index}")
        else:
            log.error(msg="Browser: No option for select is specified")

    def accept_alert(self):
        """
        Accept alert notification.
        """
        log.info(msg="Browser: Accepting alert")
        self.driver.switch_to.alert.accept()

    def click_keyboard_button(self, keyboard_button: str):
        """
        Click button on keyboard.

        :param keyboard_button: Button to be clicked.
               Can also accept button from Keys package using self.keys.<button>
        """
        log.info(msg="Browser: Click Keyboard button")
        actions = ActionChains(self.driver)
        actions.send_keys(keyboard_button).perform()

    def clear_textbox(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        timeout: float = None,
    ):
        """
        Clear element's input value. \n
        Accepts either element's locator or element itself

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self._element(locator=locator, element=element, timeout=timeout)
        log.info(msg="Browser: Clearing element's input value")
        el.clear()

    def clear_textbox_with_keyboard(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        timeout: float = None,
    ):
        """
        Clear element's input value. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self._element(locator=locator, element=element, timeout=timeout)
        log.info(msg="Browser: Clearing element's input value with keyboard")
        self.input_to_element(element=el, input_text=f"{self.keys.CONTROL} + a")
        self.input_to_element(element=el, input_text=self.keys.DELETE)

    # Actions
    def execute_script(self, script: str, *args):
        """
        Execute script in browser

        :param script: Script to execute
        :param args: Additional args for execute_script
        """
        log.info(msg=f"Browser: Executing script: {script}")
        self.driver.execute_script(script, *args)

    def click_element(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        timeout: float = None,
    ):
        """
        Click an element. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find element
        :param element:  itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self._element(locator=locator, element=element, timeout=timeout)
        log.info(msg="Browser: Clicking element")
        el.click()

    def click_outside(self):
        """
        Clicking outside, in example, to close pop-ups
        """
        log.info(msg="Browser: Click outside")
        self.click_element(locator=self.locator_css("body"))

    def moveto_and_click_element(
        self,
        locator_to_move: Locators.Locator = None,
        element_to_move: WebElement = None,
        timeout_to_move: float = None,
        locator_to_click: Locators.Locator = None,
        element_to_click: WebElement = None,
        timeout_to_click: float = None,
    ):  # noqa: CFQ002
        """
        Move to an element and click another element. \n
        Accepts either elements' locators or elements themselves.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout_to_move: Time limit to find element, to which it is needed to move
        :param locator_to_click: Locator to find element, which is needed to be clicked
        :param element_to_click: Element itself (if possible), which is needed to be clicked
        :param timeout_to_click: Time limit to find element, which is needed to be clicked
        """
        element_to_move = self._element(locator=locator_to_move, element=element_to_move, timeout=timeout_to_move)
        element_to_click = self._element(locator=locator_to_click, element=element_to_click, timeout=timeout_to_click)
        log.info(msg="Browser: Move to element A (hover) and click element B")
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_move).click(element_to_click).perform()

    def moveto_element(
        self,
        locator_to_move: Locators.Locator = None,
        element_to_move: WebElement = None,
        timeout: float = None,
    ):
        """
        Move to an element. \n
        Accepts either element's locator or element itself.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout: Time limit to find element, to which it is needed to move
        """

        if timeout is None:
            timeout = self.timeout

        element_to_move = self._element(locator=locator_to_move, element=element_to_move, timeout=timeout)
        log.info(msg="Browser: Moving to element (hover)")
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_move).perform()

    def moveto_element_offset(
        self,
        locator_to_move: Locators.Locator = None,
        element_to_move: WebElement = None,
        timeout: float = None,
        x_offset: int = 0,
        y_offset: int = 0,
    ):
        """
        Move to an element with offset. \n
        Accepts either element's locator or element itself.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout: Time limit to find element, to which it is needed to move
        :param x_offset: x coordinate within the element (x=0, y=0 position of top left pixel)
        :param y_offset: y coordinate within the element
        """

        element_to_move = self._element(locator=locator_to_move, element=element_to_move, timeout=timeout)
        log.info(msg="Browser: Moving to element with offset (hover)")
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element_to_move, x_offset, y_offset).perform()

    def scroll_into_element_center(
        self,
        locator: Locators.Locator = None,
        element: WebElement = None,
        timeout: float = None,
    ):
        """
        Scroll into element's center.

        :param locator: Locator to find element
        :param element:  itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        element = self._element(locator=locator, element=element, timeout=timeout)
        script = "arguments[0].scrollIntoView({block: 'center'});"
        self.execute_script(script, element)
        log.info(msg="Browser: Scroll to element center")

    def wait_elements_invisibility(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ):
        """
        Wait till single element is invisible.

        :param locator: Locator to find element
        :param timeout: Timeout for element to be invisible
        :param show_error_logs: Boolean value whether to log error
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg="Browser: Wait till single element is invisible")
        try:
            WebDriverWait(self.driver, timeout=timeout).until(ec.invisibility_of_element_located(locator=locator))
        except TimeoutException:
            error = f"Element with locator {locator} is visible after {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
            raise AssertionError(error)

    def wait_element_is_invisible(
        self,
        locator: Locators.Locator,
        timeout: float = None,
        show_error_logs: bool = True,
    ):
        """
        Wait till single element is invisible without exeption.

        :param locator: Locator to find element
        :param timeout: Timeout for element to be invisible
        :param show_error_logs: Boolean value whether to log error
        """
        if timeout is None:
            timeout = self.timeout

        log.info(msg="Browser: Wait till single element is invisible")
        try:
            WebDriverWait(self.driver, timeout=timeout).until(ec.invisibility_of_element_located(locator=locator))
        except TimeoutException:
            error = f"Element with locator {locator} is visible after {timeout} seconds"
            if show_error_logs:
                log.error(msg=error)
