import logging
import os
import shutil


class Log:
    """
    Logger class \n
    Usage: \n
    - info: Log().logger.info(msg)
    - error: Log().logger.error(msg)
    """

    def __init__(self):
        self._set_formatting()
        self._test_results_dir = ".results"
        self.log_file_path = os.path.join(self._test_results_dir, "run.log")
        self._check_results_dir()
        self.level = logging.INFO
        self.active_logger = self.logger

    @property
    def logger(self):
        logger = logging.getLogger("test_log")
        if not logger.hasHandlers():
            self._create_file_handler(logger)
            logger.setLevel(self.level)
        return logger

    @property
    def file_path(self):
        return self.log_file_path

    def refresh_logger(self):
        """
        This method removes the existing file handlers from the logger and creates a new file handler.
        The purpose is to keep the log file specific to a particular test, discarding any logs from previous tests.
        """
        self._remove_file_handlers(self.active_logger)
        self._create_file_handler(self.active_logger)

    def _create_file_handler(self, my_logger):
        log_handler = logging.FileHandler(filename=self.log_file_path, mode="w")
        log_formatter = logging.Formatter(self.format)
        log_handler.setFormatter(log_formatter)
        my_logger.addHandler(log_handler)

    @staticmethod
    def _remove_file_handlers(my_logger):
        for handler in my_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                my_logger.removeHandler(handler)

    def _check_results_dir(self):
        if os.path.isdir(self._test_results_dir) and os.environ.get("TEST_RESULTS_FOR_LOGGING") is None:
            shutil.rmtree(self._test_results_dir)

        if not os.path.isdir(self._test_results_dir):
            os.mkdir(self._test_results_dir)
            os.environ["TEST_RESULTS_FOR_LOGGING"] = "true"

    def _set_formatting(self):
        self.format = "[%(asctime)s] - [%(levelname)s] - %(message)s"


class BrowserLogger(Log):
    def __init__(self):
        super().__init__()
        self.log_file_path = os.path.join(self._test_results_dir, "browser_console.log")
        self.active_logger = self.browser_logger

    @property
    def browser_logger(self):
        logger = logging.getLogger("browser_log")
        if len(logger.handlers) == 0:
            self._create_file_handler(logger)
            logger.setLevel(self.level)
        return logger
