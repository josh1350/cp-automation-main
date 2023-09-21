import os

from src.api.client import ClientApi
from src.api.tricentis import TricentisJira


class ContextHelper:
    @staticmethod
    def init_tricentis_config(context):
        project_key = os.getenv("JIRA_PROJECT_KEY")
        api_key = os.getenv("TTM4J_API_KEY")
        context.tricentis = TricentisJira(project_key, api_key)
        context.is_send_to_jira = os.getenv("SEND_TO_JIRA")
        context.test_results = []

    @staticmethod
    def init_user_credentials(context):
        context.test_username = os.getenv("TEST_USERNAME")
        context.test_password = os.getenv("TEST_PASSWORD")
        context.sharon_username = os.getenv("SHARON_USERNAME")
        context.sharon_password = os.getenv("SHARON_PASSWORD")
        context.admin_username = os.getenv("ADMIN_USERNAME")
        context.admin_password = os.getenv("ADMIN_PASSWORD")

    @staticmethod
    def init_ui_config(context):
        context.base_url = os.getenv("BASE_URL")
        context.browser_name = os.getenv("BROWSER")
        context.is_headless = os.getenv("HEADLESS")
        context.base_url = os.getenv("BASE_URL")
        context.is_maximize = os.getenv("MAXIMIZE")
        context.screen_width = os.getenv("SCREEN_WIDTH")
        context.screen_height = os.getenv("SCREEN_HEIGHT")

    @staticmethod
    def init_api_config(context):
        context.okta_url = os.getenv("BASE_OKTA_URL")
        context.cp_api_url = os.getenv("CP_API_URL")
        context.fp_api_url = os.getenv("FP_URL")
        context.client = ClientApi(context.base_url)
        context.client_id = os.getenv("CLIENT_ID")
        context.client_secret = os.getenv("CLIENT_SECRET")
        context.okta_client = ClientApi(context.okta_url)
        context.cp_api_client = ClientApi(context.cp_api_url)
        context.fp_api_client = ClientApi(context.fp_api_url)
        context.token_url = os.getenv("FP_TOKEN_URL")
        context.access_client_id = os.getenv("ACCESS_CLIENT_ID")
        context.access_client_secret = os.getenv("ACCESS_CLIENT_SECRET")
        context.okta_api_key = os.getenv("CP_API_SECRET")
        context.cp_api_username = os.getenv("API_AUTH_USERNAME")
        context.cp_api_password = os.getenv("API_AUTH_PASSWORD")
        context.okta_scope = os.getenv("SCOPES")
        base_url = os.getenv("BASE_URL")
        okta_redirect_url = os.getenv("REDIRECT_URI")
        context.okta_redirect_url = f"{base_url}{okta_redirect_url}"
        context.okta_authorization_id = os.getenv("AUTHORIZATION_ID")
