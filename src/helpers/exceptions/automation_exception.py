from src.helpers.logger import Log

log = Log().logger


class AutomationException(Exception):  # noqa: N818
    """
    Custom exception class for automation-related errors.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        message = f"AutomationException: {self.message}"
        log.error(message)
        return message
