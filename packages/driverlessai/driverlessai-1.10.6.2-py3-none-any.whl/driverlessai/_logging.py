import logging
import sys

logger = logging.getLogger("driverlessai")


class ConsoleLoggingHandler(logging.StreamHandler):
    def __init__(self) -> None:
        super().__init__(sys.stdout)
        self.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))


def configure_console_logger() -> None:
    for handler in logger.handlers:
        if isinstance(handler, ConsoleLoggingHandler):
            return  # we have already added the ConsoleLoggingHandler
    logger.addHandler(ConsoleLoggingHandler())
    logger.setLevel(logging.INFO)
