import sys
from typing import ClassVar
# NOTE: requires TWO separate imports in order to work the way I want:
from loguru import logger
from loguru._logger import Logger


class LoggingUtility():
    """
    from logging_utility import LoggingUtility as LU
    LU.info('some message')
    """
    __logger: ClassVar[Logger] = logger


    @classmethod
    def start_logging(cls, filename: str = 'log.txt') -> None:
        """
        Start logging using Loguru to the specified file.
        :rtype: object
        """
        log_format: str = '{time} - {name} - {level} - {function} - {message}'
        cls.__logger.remove()
        cls.__logger.add(filename, format = log_format, rotation = '10 MB',
                         retention = '5 days')
        # Add a handler that logs only DEBUG messages to stdout
        cls.__logger.add(sys.stdout, level = "DEBUG",
                         filter = lambda record: record["level"].name == "DEBUG")


    @classmethod
    def log_info_and_debug(cls, msg: str) -> None:
        cls.__logger.info(msg)
        cls.__logger.debug(msg)


    @classmethod
    def debug(cls, msg: str) -> None:
        cls.__logger.debug(msg)


    @classmethod
    def info(cls, msg: str) -> None:
        cls.__logger.info(msg)


    @classmethod
    def warning(cls, msg: str) -> None:
        cls.__logger.warning(msg)


    @classmethod
    def success(cls, msg: str) -> None:
        cls.__logger.success(msg)


    @classmethod
    def critical(cls, msg: str) -> None:
        cls.__logger.critical(msg)
