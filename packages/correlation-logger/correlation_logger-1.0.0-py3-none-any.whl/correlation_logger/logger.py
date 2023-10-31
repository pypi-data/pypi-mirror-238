"""
This module contains class to create a Logger
"""
import logging
import sys
from enum import Flag, auto

from src.correlation_logger.cloudwatch_handler import CloudWatchHandler


class LogSink(Flag):
    """Define the output of the log"""
    CONSOLE = auto()
    CLOUDWATCH = auto()


class Logger:
    """This class is used to create a logger"""

    def __init__(self,
                 name: str,
                 log_sink: LogSink = LogSink.CONSOLE,
                 log_level: int = logging.ERROR,
                 cloudwatch_handler: CloudWatchHandler = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-4s %(name)s : %(message)-2s"
        )

        if log_sink in LogSink.CONSOLE:
            # create console handler with a higher log level
            ch = logging.StreamHandler(stream=sys.stdout)
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        if log_sink in LogSink.CLOUDWATCH:
            # cloudwatch handler is required if log is sent to cloudwatch
            assert cloudwatch_handler is not None
            fh = cloudwatch_handler
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @property
    def name(self):
        """Get current log name"""
        return self.logger.name

    @name.setter
    def name(self, value: str):
        """Set current log name"""
        self.logger.name = value

    def debug(self, msg: str, correlation_id: str):
        """Write log in DEBUG level"""
        self.logger.debug(" # ".join((correlation_id, msg)))

    def info(self, msg: str, correlation_id: str):
        """Write log in INFO level"""
        self.logger.info(" # ".join((correlation_id, msg)))

    def warning(self, msg: str, correlation_id: str):
        """Write log in WARNING level"""
        self.logger.warning(" # ".join((correlation_id, msg)))

    def error(self, msg: str, correlation_id: str):
        """Write log in ERROR level"""
        self.logger.error(" # ".join((correlation_id, msg)))

    def critical(self, msg: str, correlation_id: str):
        """Write log in CRITICAL level"""
        self.logger.critical(" # ".join((correlation_id, msg)))
