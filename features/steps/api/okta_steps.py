import json
import secrets
import time

import requests
from behave import given, step

from src.api.headers import Headers
from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.exceptions.okta_exception import OktaException
from src.helpers.json_helper import JsonHelper
from src.helpers.logger import Log

log = Log()


@step('I wait that user with id "{user_id}" is created')
def when_i_save_value_from_response(context, user_id):
    user_id = BehaveHelper.format_context(context, user_id)
    client = context.okta_client
    headers = Headers.get_okta_headers(context.okta_api_key)
    retry_limit = 5
    is_created = False
    time.sleep(3)
    for attempt in range(1, retry_limit + 1):
        response = client.get_data(f"api/v1/users/{user_id}", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            if user_data["status"] == "ACTIVE":
                log.logger.info(f"User '{user_id}' created successfully!")
                is_created = True
                break
            else:
                log.logger.warning(f"User '{user_id}' is still being processed. Retrying in 5 seconds...")
        else:
            log.logger.warning(f"User '{user_id}' not found. Retrying in 5 seconds...")

        time.sleep(5)

    if not is_created:
        raise OktaException(f"User '{user_id}' was not found after {retry_limit} retries.")


@given('I login as "{user_type}" using API')
def when_i_login(context, user_type):
    match user_type.lower():
        case "tester":
            username = context.test_username
            password = context.test_password
        case "sharon":
            username = context.sharon_username
            password = context.sharon_password
        case "admin":
            username = context.admin_username
            password = context.admin_password
        case _:
            raise AutomationException(f"The are no such user type as {user_type}")
    body = {
        "password": f"{password}",
        "username": f"{username}",
        "options": {
            "warnBeforePasswordExpired": True,
            "multiOptionalFactorEnroll": False,
        },
    }

    response = context.client_auth.post_data("api/v1/authn", data=json.dumps(body), headers=context.headers)
    Assert.contains(
        "sessionToken",
        str(response.content),
        "Authentication failed, sessionToken is not provided",
    )
    token = JsonHelper.get_value(response.content, "sessionToken")
    setattr(context, "sessionToken", token)

    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    cookies = {"okta-oauth-state": f"{state}", "okta-oauth-nonce": f"{nonce}"}

    params = {
        "client_id": f"{context.client_id}",
        "response_type": "code",
        "redirect_uri": f"{context.okta_redirect_url}",
        "nonce": f"{nonce}",
        "scope": f"{context.okta_scope}",
        "sessionToken": f"{context.sessionToken}",
        "state": f"{state}",
    }
    log.logger.info(f"Params: {str(params)}")
    log.logger.info(f"Cookies: {str(cookies)}")
    response = context.client_auth.get_data(
        f"oauth2/{context.okta_authorization_id}/v1/authorize",
        querystring=params,
        cookies=cookies,
    )
    context.cookies = JsonHelper.convert_request_cookie_to_json(response.request.headers["Cookie"])
    log.logger.info(f"Results cookies: {str(context.cookies)}")
    if "messages" not in str(context.cookies):
        Assert.contains(
            "sessionid",
            str(context.cookies),
            "Login unsuccessfully, session id is not present",
        )
    Assert.not_contains(
        "login",
        context.client.get_data(cookies=context.cookies).url,
        "Login unsuccessfully, redirected to Login",
    )
    context.response = response


@given("I get API cp token")
def get_cp_api_token(context):
    headers = Headers.get_basic_auth_headers(context.access_client_id, context.access_client_secret)
    payload = {"grant_type": "client_credentials"}
    response = requests.post(context.token_url, headers=headers, data=payload)
    Assert.is_equal(response.status_code, 200, "Authorization is failed")

    access_token = JsonHelper.get_value(response.text, "access_token")
    context.cp_token = access_token
