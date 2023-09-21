import json
import os
import secrets

import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv

from src.api.client import AuthApi
from src.api.headers import Headers
from src.helpers.behave_helper import BehaveHelper
from src.helpers.context_helper import ContextHelper
from src.helpers.exceptions.tms_exception import TmsException
from src.helpers.logger import Log
from src.helpers.string_helper import StringHelper
from src.ui.browser import Browser
from src.ui.pages.base_page import BasePage

load_dotenv()
log = Log()


# Setup
def before_all(context):
    # Get Jira base variables
    ContextHelper.init_tricentis_config(context)

    # Get User variables
    ContextHelper.init_user_credentials(context)

    # Get UI base variables
    ContextHelper.init_ui_config(context)

    # Get API base variables
    ContextHelper.init_api_config(context)


def before_scenario(context, scenario):
    context.client_auth = AuthApi(context.okta_url)
    context.headers = Headers().get_json_format()
    context.cookies = context.querystring = context.request_body = None

    if "e2e" in scenario.effective_tags:
        is_headless = eval(context.is_headless) if context.is_headless is not None else False
        screen_resolution = define_screen_resolution(context)
        log.logger.info("Browser: ########## Start application ##########")
        context.browser = Browser()
        browser_driver = context.browser.init_driver(
            browser_name=context.browser_name,
            is_headless=is_headless,
            is_maximize=context.is_maximize,
            screen_resolution=screen_resolution,
        )
        context.driver = browser_driver
        BasePage(context).open()


def define_screen_resolution(context):
    if context.screen_width is None or context.screen_height is None:
        resolution = None
    else:
        resolution = (int(context.screen_width), int(context.screen_height))
    screen_resolution = None if eval(context.is_maximize) else resolution
    return screen_resolution


def before_step(context, step):  # noqa: U100
    log.logger.info(f"Behave: Executing step: {step.name}")


# Teardown
def after_scenario(context, scenario):
    jira_result = None
    try:
        context.tricentis.define_cycle(scenario.effective_tags)
        jira_result = send_test_result_to_jira(context, scenario)
    except TmsException as e:
        log.logger.error(str(e))
    finally:
        if "e2e" in scenario.effective_tags:
            log.logger.info("Browser: ########## Close application ##########")
            context.browser.save_browser_console_log()
            context.driver.quit()
            del context.driver
            if scenario.status == "failed":
                add_attachment_to_jira(context, jira_result, context.screen_path)
                context.screen_path = None

            if os.path.getsize(context.browser.browser_logger.file_path) > 0:
                add_attachment_to_jira(context, jira_result, context.browser.browser_logger.file_path)
            else:
                log.logger.info("Browser: The Browser console log is empty. Console is not sent to TTM4J")
            context.browser.browser_logger.refresh_logger()

        add_attachment_to_jira(context, jira_result, log.file_path)
        log.refresh_logger()


def after_step(context, step):
    if step.status.name != "passed":
        allure.attach.file(
            log.file_path,
            name="Test log",
            attachment_type=AttachmentType.TEXT,
        )
        if hasattr(context, "driver"):
            save_screenshot(context, step)
            context.browser.save_browser_console_log()
            allure.attach.file(
                context.browser.browser_logger.file_path,
                name="Browser console log",
                attachment_type=AttachmentType.TEXT,
            )


# Helper Methods
def save_screenshot(context, step):
    step_name = StringHelper.remove_special_characters(step.name).replace(" ", "_")
    filename = f"{step_name}_{secrets.token_urlsafe(5)}.png"
    context.screen_path = f"{context.config.outfiles[0]}\\{filename}"
    context.driver.save_screenshot(context.screen_path)
    allure.attach.file(
        context.screen_path,
        name=f"Failed Screenshot of {step.name}",
        attachment_type=AttachmentType.PNG,
    )


def send_test_result_to_jira(context, scenario):
    if context.is_send_to_jira is not None and eval(context.is_send_to_jira):
        status = "passed" if scenario.status == "passed" else "failed"
        test_case_key = BehaveHelper.get_tc_id(scenario.tags)
        if test_case_key is not None:
            name = scenario.name if "Outline" not in scenario.keyword else f"{scenario.name} - {context.active_outline}"
            result = {
                "testCaseKey": test_case_key,
                "name": name,
                "status": status,
                "duration": scenario.duration,
                "testType": "Automated",
            }
            response = context.tricentis.send_test_result(result)
            context.test_results.append(result)
            return response
        else:
            log.logger.warning("Tricentis: The are no Jira link in TC!")


def add_attachment_to_jira(context, response, filepath):
    if context.is_send_to_jira is not None and eval(context.is_send_to_jira):
        try:
            response_json = json.loads(response.text)[0]
            run_id = response_json["key"]
            context.tricentis.send_file(filepath, run_id)
        except TmsException as e:
            log.logger.error(str(e))
