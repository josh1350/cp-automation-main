import json
import os
from datetime import datetime

import requests

from src.api.headers import Headers
from src.helpers.exceptions.tms_exception import TmsException
from src.helpers.logger import Log

log = Log().logger


class TricentisJira:
    def __init__(self, project_key, api_key):
        self.project_key = project_key
        self.api_key = api_key
        self.base_url = "https://api.ttm4j.tricentis.com"
        self.tms_url = f"{self.base_url}/v1/projects/{self.project_key}/"
        self.run_time = datetime.now().strftime("%m.%d.%y_%H:%M")
        self.cycle_name = f"Auto_run_{self.run_time}"
        self.headers = Headers.get_auth_headers(self.api_key)

    def send_test_result(self, test_result):
        url = f"{self.tms_url}test-runs"

        payload = {
            "cycleName": self.cycle_name,
            "includeAttachments": True,
            "testRuns": [test_result],
        }
        response = requests.post(url, json=payload, headers=self.headers)
        log.info(f"TTM4J API: Response is {response.text}")
        if response.status_code == 201:
            log.info("TTM4J API: Test results sent to TTM4J successfully!")
        else:
            log.error(
                f"TTM4J API:Failed to send test results of {test_result['testCaseKey']} to TTM4J. "
                f"Status code: {response.status_code}"
            )
            raise TmsException(f"Status code: {response.status_code}")
        return response

    def define_cycle(self, tags):
        tags_str = str(tags)
        if "api" in tags_str:
            self.cycle_name = f"API_{self.run_time}"
        elif "e2e" in tags_str:
            self.cycle_name = f"E2E_{self.run_time}"
        else:
            self.cycle_name = f"Auto_{self.run_time}"

    def send_file(self, filepath, run_id):
        mime_type = "image/png" if filepath.endswith("png") else "text/plain"
        response = self.__post_attachment(filepath, run_id, mime_type)
        response = self.__put_attachment(response, filepath, mime_type)

        log.info(f"TTM4J API: Response is {response.text}")
        if response.status_code == 200:
            log.info("TTM4J API: Attachment added to the test result in TTM4J successfully!")
        else:
            log.error(
                f"TTM4J API: Failed to add attachment to the test result in TTM4J. "
                f"Status code: {response.status_code}"
            )

            raise TmsException(f"Status code: {response.status_code}")

    def __post_attachment(self, filepath, run_id, mime_type):
        url = f"{self.tms_url}test-runs/{run_id}/attachments"
        file_size = os.path.getsize(filepath)
        data = {"fileName": filepath, "mimeType": mime_type, "size": file_size}
        response = requests.post(url, headers=self.headers, json=data)
        return response

    def __put_attachment(self, response, filepath, mime_type):
        upload_url = json.loads(response.text)["uploadUrl"]
        finish_url = json.loads(response.text)["finishUrl"]

        attachment_file = open(filepath, "rb")
        data = attachment_file.read()
        headers = Headers.get_custom_format(mime_type)
        requests.put(upload_url, data=data, headers=headers)
        response = requests.put(f"{self.base_url}/{finish_url}", headers=self.headers)
        return response
