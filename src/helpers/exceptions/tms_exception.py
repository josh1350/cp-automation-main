from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.logger import Log

log = Log().logger


class TmsException(AutomationException):  # noqa: N818
    """
    Class of TmsException for Tms-related errors.
    """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        message = f"TmsException: {self.message}"
        log.error(message)
        return message
