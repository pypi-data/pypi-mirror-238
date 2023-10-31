"""
cloudwatch_handler.py - CloudWatch Logging Handler

This module provides a custom logging handler for sending
log events to AWS CloudWatch Logs.
The `CloudwatchHandler` class, which inherits from `logging.Handler`,
allows you to send log data to a
specified CloudWatch Logs group and stream.

"""
import logging
import time

import boto3
from botocore.config import Config as AWSConfig


# pylint: disable=[too-many-arguments]
class CloudWatchHandler(logging.Handler):
    """
    CloudWatch Log Handler for Python Logging

    The `CloudwatchHandler` class is a custom logging handler
     that extends `logging.Handler`.
     It is designed to send log messages
     to an AWS CloudWatch Logs group and stream.

    Attributes:
    - level: The logging level (e.g., logging.DEBUG, logging.INFO)
    for filtering log messages.
    - region_name: The AWS region where CloudWatch Logs is located.
    - aws_access_key_id: The AWS access key ID used for authentication.
    - aws_secret_access_key: The AWS secret access key used for authentication.
    - log_group_name: The name of the CloudWatch Logs group where log data will be sent.
    - log_stream_name: The name of the CloudWatch Logs stream within the group.

    Methods:
    - __init__(level, region_name, aws_access_key_id,
    aws_secret_access_key, log_group_name, log_stream_name):
    Initializes the CloudwatchHandler instance with the provided parameters.

    - emit(record):
    Sends log events to CloudWatch Logs.
    Converts log records to CloudWatch log events
    and submits them to the specified log group and stream.

    Usage:
    - Create an instance of this class and add it
    to your Python logging configuration
    to send log data to CloudWatch Logs.
    """

    def __init__(
            self,
            level,
            region_name,
            aws_access_key_id,
            aws_secret_access_key,
            log_group_name,
            log_stream_name,
    ):
        super().__init__(level)
        region = AWSConfig(region_name)
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.client = boto3.client(
            service_name="logs",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=region,
        )

    def emit(self, record):
        """
        Emit Log Record to CloudWatch Logs

        This method is called to send log events to AWS CloudWatch Logs.
         It converts log records to CloudWatch log events
         and submits them to the specified log group and stream.

        Parameters:
        - record: The log record to be emitted.

        Usage:
        - This method is automatically called
        by the logging framework when a log event is generated.

        Note:
        - The `record` parameter contains information
        about the log event, including log level, message, and timestamp.
        - Log events are formatted and sent
        to the specified CloudWatch Logs group and stream.
        """
        timestamp = round(time.time() * 1000)
        message = self.format(record)
        self.client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name,
            logEvents=[{"timestamp": timestamp, "message": message}],
        )
