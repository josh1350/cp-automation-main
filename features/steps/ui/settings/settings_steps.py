import time

from behave import then, when

from src.enums.toggle_status import ToggleStatus
from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.logger import Log
from src.helpers.string_helper import StringHelper
from src.ui.pages.settings.settings_page import SettingsPage

log = Log().logger


# Step Definitions for Guided Tour
@when("I start the Guided Tour from the Settings page")
def start_guided_tour_from_settings(context):
    SettingsPage(context).start_guided_tour()


# Step Definitions for Update Email
@when("I open the Update Email on the Settings page")
def open_update_email_on_settings(context):
    SettingsPage(context).open_update_email()


@then('The email field in the Update Email modal on the Settings page is "{email}"')
def verify_email_field_in_update_email_modal(context, email):
    expected_email = BehaveHelper().format_context(context, email)
    actual_email = SettingsPage(context).update_email_modal().get_fld_email().get_attribute("value")
    Assert.is_equal(actual_email, expected_email)


@when("I save the Email updates on the Settings page")
def save_email_updates_on_settings(context):
    SettingsPage(context).update_email_modal().save()


@then('The "{email}" is in the Email description on the Settings page')
def verify_email_description_on_settings(context, email):
    expected_email = BehaveHelper.format_context(context, email)
    actual_email = SettingsPage(context).get_email_from_details()
    Assert.is_equal(actual_email, expected_email)


@when('I enter "{value}" into the "{field_name}" in Update Email on the Settings page')
def enter_value_into_field_in_update_email_modal(context, value, field_name):
    """
    Args:
        context (Context): Behave context object.
        value (str): Value to enter.
        field_name (str): Field name ("email" or "password").
    """
    input_value = BehaveHelper.format_context(context, value)
    if field_name.lower() == "email":
        SettingsPage(context).update_email_modal().input_email(input_value)
    elif field_name.lower() == "password":
        SettingsPage(context).update_email_modal().input_password(input_value)
    else:
        raise AutomationException(f"There is no such field as {field_name} in the 'Update Email' modal")


@when('I cleanup "{field_name}" in Update Email on the Settings page')
def cleanup_field_in_update_email_modal(context, field_name):
    """
    Args:
        context (Context): Behave context object.
        field_name (str): Field name ("email" or "password").
    """
    if field_name.lower() == "email":
        SettingsPage(context).update_email_modal().cleanup_email()
    elif field_name.lower() == "password":
        SettingsPage(context).update_email_modal().cleanup_password()
    else:
        raise AutomationException("There is no such field in the 'Update Email' modal")


@then('The "{error_message}" error message is displayed for "{field_name}" in Update Email on the Settings page')
def verify_error_message_for_field_in_update_email_modal(context, error_message, field_name):
    """
    Args:
        context (Context): Behave context object.
        error_message (str): Expected error message.
        field_name (str): Field name ("email" or "password").
    """
    if field_name.lower() == "email":
        actual_error = StringHelper().normalize(SettingsPage(context).update_email_modal().get_error_email().text)
    elif field_name.lower() == "password":
        actual_error = StringHelper().normalize(SettingsPage(context).update_email_modal().get_error_password().text)
    else:
        raise AutomationException("There is no such field in the 'Update Email' modal")

    Assert.is_equal(actual_error, error_message)


@when("I cancel the Email updates on the Settings page")
def cancel_email_updates_on_settings(context):
    SettingsPage(context).update_email_modal().cancel()


# Step Definitions for Update Password
@when("I open the Update Password on the Settings page")
def open_update_password_modal(context):
    SettingsPage(context).open_update_password()


@then('The "{field_type}" password field in the Update Password modal on the Settings page has text "{value}"')
def verify_fields_in_update_password_modal(context, field_type, value):
    """
    Args:
        context (Context): Behave context object.
        field_type (str): Type of password field ("current", "new", "confirm").
        value (str): Expected value.
    """
    expected_value = BehaveHelper().format_context(context, value)
    field = UpdatePasswordStepHelper().get_update_password_field(context, field_type)
    actual_value = field.get_attribute("value")
    Assert.is_equal(actual_value, expected_value)


@when('I "{action}" the "{field_type}" password field in the Update Password modal on the Settings page')
def update_showing_password_on_password_modal(context, action, field_type):
    """
    Args:
        context (Context): Behave context object.
        action (str): Action to perform ("show" or "hide").
        field_type (str): Type of password field ("current", "new", "confirm").
    """
    field = UpdatePasswordStepHelper().get_update_password_field(context, field_type)
    field_status = SettingsPage(context).update_password_modal().get_field_toggle_status(field)
    if ToggleStatus(field_status) == ToggleStatus.from_string(action.lower()):
        SettingsPage(context).update_password_modal().get_field_toggle(field).click()
    else:
        log.info(f"Browser: The password field has already status of '{action}'")


@then('The new password criteria is "{state}" the Update Password modal on the Settings page')
def verify_new_password_criteria_modal(context, state):
    """
    Args:
        context (Context): Behave context object.
        state (str): Expected state ("absent" or "present").
    """
    actual_state = SettingsPage(context).update_password_modal().is_criteria_list_absent()
    if state.lower() == "absent":
        Assert.is_true(actual_state, "The password list criteria is absent, expected to be present")
    elif state.lower() == "present":
        Assert.is_false(actual_state, "The password list criteria is present, expected to be absent")
    else:
        raise AutomationException("The are no such state as {state} for criteria")


@then(
    'The new password criteria contains "{values}" as "{criteria_type}" '
    "in the Update Password modal on the Settings page"
)
def verify_new_password_criteria_list_modal(context, values, criteria_type):
    """
    Args:
        context (Context): Behave context object.
        values (str): Expected values separated by commas.
        criteria_type (str): Type of criteria ("invalid", "valid", or "default").
    """
    if criteria_type.lower() == "invalid":
        criteria_list = SettingsPage(context).update_password_modal().get_invalid_criteria_list()
    elif criteria_type.lower() == "valid":
        criteria_list = SettingsPage(context).update_password_modal().get_valid_criteria_list()
    elif criteria_type.lower() == "default":
        criteria_list = SettingsPage(context).update_password_modal().get_default_criteria_list()
    else:
        raise AutomationException("The are no such criteria type as {criteria_type}")
    value_list = [value.strip() for value in values.split(",")]
    Assert.is_equal(criteria_list, value_list, "The password list criteria has wrong State")


@then('The "{field_type}" password field in the Update Password modal on the Settings page has error')
def verify_error_in_update_password_modal(context, field_type):
    """
    Args:
        context (Context): Behave context object.
        field_type (str): Type of password field ("current", "new", "confirm").
    """
    SettingsPage(context).update_password_modal().wait_for_error()
    time.sleep(1)
    field = UpdatePasswordStepHelper().get_update_password_field(context, field_type)
    actual_value = field.get_attribute("class")
    Assert.contains("error", actual_value)


@then(
    'The "{field_type}" password field in the Update Password modal on the Settings page '
    'has "{error_text}" error message'
)
def verify_message_in_update_password_modal(context, field_type, error_text):
    """
    Args:
        context (Context): Behave context object.
        field_type (str): Type of password field ("current", "new", "confirm", "default").
        error_text (str): Expected error message.
    """
    if field_type != "default":
        field = UpdatePasswordStepHelper().get_update_password_field(context, field_type)
        actual_value = SettingsPage(context).update_password_modal().get_field_error_text(field)
    else:
        actual_value = SettingsPage(context).update_password_modal().get_error_list_text()
    Assert.is_equal(actual_value, error_text)


@then('The "{field_type}" password field in the Update Password modal on the Settings page has "{status}" status')
def verify_field_type_in_update_password_modal(context, field_type, status):
    """
    Args:
        context (Context): Behave context object.
        field_type (str): Type of password field ("current", "new", "confirm").
        status (str): Expected status ("show" or "hide").
    """
    status_mapping = {"show": "text", "hide": "password"}
    field = UpdatePasswordStepHelper().get_update_password_field(context, field_type)
    actual_value = field.get_attribute("type")
    Assert.is_equal(actual_value, status_mapping.get(status.lower(), None))


@when('I enter "{value}" into the "{field_type}" password in Update Password on the Settings page')
def enter_value_into_field_in_update_password_modal(context, value, field_type):
    """
    Args:
        context (Context): Behave context object.
        value (str): Value to enter.
        field_type (str): Type of password field ("current", "new", "confirm").
    """
    input_value = BehaveHelper.format_context(context, value)
    UpdatePasswordStepHelper().input_to_update_password_field(context, field_type, input_value)


@then('The password field in the Update Email modal on the Settings page is "{password}"')
def verify_password_field_in_update_email_modal(context, password):
    expected_password = BehaveHelper().format_context(context, password)
    actual_password = SettingsPage(context).update_email_modal().get_fld_password().get_attribute("value")
    Assert.is_equal(actual_password, expected_password)


@when("I save the Password updates on the Settings page")
def save_password_updates_on_settings(context):
    SettingsPage(context).update_password_modal().save()


@when("I cancel the Password updates on the Settings page")
def cancel_password_updates_on_settings(context):
    SettingsPage(context).update_password_modal().cancel()


# General
@when('I close success message on the "{update_type}" updates on the Settings page')
def skip_success_message_on_settings(context, update_type):
    """
    Args:
        context (Context): Behave context object.
        update_type (str): Type of update ("email", "phone", "password").
    """
    match update_type.lower():
        case "email":
            SettingsPage(context).get_success_email_update_modal().close()
        case "phone":
            SettingsPage(context).get_success_phone_update_modal().close()
        case "password":
            SettingsPage(context).get_success_password_update_modal().close()
        case _:
            raise AutomationException(f"The are no such type for updates as {update_type}.")
    time.sleep(2)


@then('The "{element}" of success updates for the "{update_type}" on the Settings page is "{value}"')
def verify_success_message_on_settings(context, element, update_type, value):
    """
    Args:
        context (Context): Behave context object.
        element (str): Element to verify ("title" or "content").
        update_type (str): Type of update ("email", "phone", "password").
        value (str): Expected value.
    """
    expected_value = BehaveHelper.format_context(context, value)
    match update_type.lower():
        case "email":
            modal = SettingsPage(context).get_success_email_update_modal()
        case "phone":
            modal = SettingsPage(context).get_success_phone_update_modal()
        case "password":
            modal = SettingsPage(context).get_success_password_update_modal()
        case _:
            raise AutomationException(f"The are no such type for updates as {update_type}.")
    if element.lower() == "title":
        text = modal.get_title().text
    elif element.lower() == "content":
        text = modal.get_body().text
    else:
        raise AutomationException(f"The are no such element for updates as {element}.")
    Assert.is_equal(StringHelper.normalize(text), expected_value)


@then('The details of the "{section_type}" on the Settings page is "{value}"')
def verify_details_on_settings(context, section_type, value):
    """
    Args:
        context (Context): Behave context object.
        section_type (str): Type of section ("email", "phone", "password").
        value (str): Expected value.
    """
    expected_value = BehaveHelper.format_context(context, value)
    match section_type.lower():
        case "email":
            details = SettingsPage(context).get_email_details()
        case "phone":
            details = SettingsPage(context).get_phone_details()
        case "password":
            details = SettingsPage(context).get_password_details()
        case _:
            raise AutomationException(f"The are no such section as {section_type}.")
    Assert.is_equal(details, expected_value)


# Helper classes
class UpdatePasswordStepHelper:
    @staticmethod
    def get_update_password_field(context, field_type):
        match field_type.lower():
            case "current":
                return SettingsPage(context).update_password_modal().get_fld_current_password()
            case "new":
                return SettingsPage(context).update_password_modal().get_fld_new_password()
            case "confirm":
                return SettingsPage(context).update_password_modal().get_fld_confirm_password()
            case _:
                raise AutomationException(f"There are no such field as {field_type}.")

    @staticmethod
    def input_to_update_password_field(context, field_type, input_value):
        match field_type.lower():
            case "current":
                return SettingsPage(context).update_password_modal().input_current_password(input_value)
            case "new":
                return SettingsPage(context).update_password_modal().input_new_password(input_value)
            case "confirm":
                return SettingsPage(context).update_password_modal().input_confirm_password(input_value)
            case _:
                raise AutomationException(f"There are no such field as {field_type}.")
