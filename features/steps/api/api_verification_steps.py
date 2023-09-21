import json

from behave import then

from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.json_helper import JsonHelper
from src.helpers.logger import Log
from src.helpers.string_helper import StringHelper

log = Log().logger


@then('The status code is "{expected_code}"')
def then_status_code_is(context, expected_code):
    status = context.response.status_code
    try:
        Assert.is_equal(status, int(expected_code))
    except AssertionError as e:
        log.error(context.response.content)
        raise e


@then("The response JSON is equivalent to")
def then_response_json_equivalent(context):
    body = BehaveHelper.format_context(context, context.text)
    expected_body = json.loads(body)
    actual_body = json.loads(context.response.content)
    Assert.is_equal(JsonHelper.sort(actual_body), JsonHelper.sort(expected_body))


@then('The response JSON is equivalent to, ignoring "{key_name}"')
def then_response_json_equivalent_ignoring(context, key_name):
    body = BehaveHelper.format_context(context, context.text)
    expected_body = json.loads(body)
    actual_body = json.loads(context.response.content)
    for key in key_name.split(", "):
        JsonHelper.delete_key_from_json(actual_body, key)
    Assert.is_equal(JsonHelper.sort(actual_body), JsonHelper.sort(expected_body))


@then('The response JSON by jpath "{jpath}" is equivalent to')
def then_response_json_jpath_equivalent(context, jpath):
    body = BehaveHelper.format_context(context, context.text)
    body = StringHelper().normalize(body)
    actual_body = JsonHelper.get_value(context.response.content, jpath)
    expected_body = json.loads(body)
    Assert.is_equal(JsonHelper.sort(actual_body), JsonHelper.sort(expected_body))
