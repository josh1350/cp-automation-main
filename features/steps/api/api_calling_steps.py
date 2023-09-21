import json
import time

from behave import step, when

from src.api.headers import Headers
from src.helpers.behave_helper import BehaveHelper
from src.helpers.json_helper import JsonHelper
from src.helpers.logger import Log

log = Log()


@step("I have prepared request body as")
def given_i_prepare_request_body(context):
    text = BehaveHelper.format_context(context, context.text)
    context.request_body = text


@step("I have prepared request headers as")
def given_i_prepare_request_headers(context):
    text = BehaveHelper.format_context(context, context.text)
    header = Headers().get_json_format()
    header.update(json.loads(text))
    context.headers = header


@step("I have prepared request query string as")
def given_i_prepare_request_query(context):
    text = BehaveHelper.format_context(context, context.text)
    context.querystring = text


@when('I send "{http_method}" request to "{resource}" of "{site}"')
def when_i_send_to_resource(context, http_method, resource, site):
    resource = BehaveHelper.format_context(context, resource)
    if site.lower() == "okta":
        client = context.okta_client
        headers = Headers.get_okta_headers(context.okta_api_key)
        time.sleep(0.5)
    elif site.lower() == "cp_api":
        client = context.cp_api_client
        headers = Headers.get_auth_headers(context.cp_token)
    elif site.lower() == "fp":
        client = context.fp_api_client
        headers = Headers.get_auth_headers(context.cp_token)
    else:
        client = context.client
        headers = context.headers
    cookie = context.cookies
    response = None
    match http_method.lower():
        case "get":
            querystring = context.querystring.strip() if context.querystring is not None else None
            response = client.get_data(resource, querystring=querystring, headers=headers, cookies=cookie)
            context.querystring = None
        case "post":
            response = client.post_data(
                resource,
                data=context.request_body,
                headers=headers,
                cookies=cookie,
            )
        case "patch":
            response = client.patch_data(
                resource,
                data=context.request_body,
                headers=headers,
                cookies=cookie,
            )
        case "put":
            response = client.put_data(
                resource,
                data=context.request_body,
                headers=headers,
                cookies=cookie,
            )
        case "delete":
            response = client.delete_data(resource, headers=headers, cookies=cookie)
    context.response = response


@step('I save "{context_value}" from response by jpath "{jpath}"')
def when_i_save_value_from_response(context, context_value, jpath):
    value = JsonHelper.get_value(context.response.content, jpath)
    log.logger.info(f"Context: The '{context_value}' is saved as '{value}'")
    setattr(context, context_value, value)
