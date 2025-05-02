import sys

from loguru import logger


class LoggingUtility():
    # from logging_utility import LoggingUtility
    @staticmethod
    def start_logging() -> logger:
        """

        :rtype: object
        """
        log_format: str = '{time} - {name} - {level} - {function} - {message}'
        logger.remove()
        logger.add('formatted_log.txt', format = log_format, rotation = '10 MB',
                   retention = '5 days')
        # Add a handler that logs only DEBUG messages to stdout
        logger.add(sys.stdout, level = "DEBUG",
                   filter = lambda record: record["level"].name == "DEBUG")
        return logger


    @staticmethod
    def log_info_and_debug(msg: str) -> None:
        logger.info(msg)
        logger.debug(msg)
