import base64


class Headers:
    @staticmethod
    def get_json_format():
        return {"Accept": "application/json", "Content-Type": "application/json"}

    @staticmethod
    def get_text_format():
        return {"Accept": "*/*", "Content-Type": "text/plain"}

    @staticmethod
    def get_custom_format(content_type):
        return {"Accept": "*/*", "Content-Type": content_type}

    @staticmethod
    def get_auth_headers(api_key):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        return headers

    @staticmethod
    def get_basic_auth_headers(client_id, client_secret):
        encode = f"{client_id}:{client_secret}".encode()
        decoded_key = base64.b64encode(encode).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {decoded_key}",
        }
        return headers

    @staticmethod
    def get_okta_headers(api_key):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"SSWS {api_key}",
        }
        return headers
