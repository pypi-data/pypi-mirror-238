import json
import logging
import os
from decimal import Decimal
from functools import cached_property

import boto3
from botocore.exceptions import ClientError

from reach_commons.reach_aws.sqs.exceptions import (
    SQSClientPublishError,
    SQSClientTopicNotFound,
)

logger = logging.getLogger(__name__)

MESSAGE_ATTRIBUTES_TYPE = {
    str: "String",
    int: "Number",
    Decimal: "Number",
    float: "Number",
    bytes: "Binary",
    list: "String.Array",
    tuple: "String.Array",
}

FALLBACK_MESSAGE_ATTRIBUTES_TYPE = "String"


# noinspection PyMethodMayBeStatic
class BaseSQSClient:
    def __init__(
        self,
        topic_name=None,
        log_level="debug",
        region_name="us-east-1",
        profile_name=None,
    ):
        self.topic_name = topic_name
        self.log_level = log_level
        self.region_name = region_name
        self.profile_name = profile_name

    @property
    def log(self):
        return getattr(logger, self.log_level)

    @staticmethod
    def _prepare_message_attributes(attributes):
        message_attributes = {}
        for key, value in attributes.items():
            attr_type = MESSAGE_ATTRIBUTES_TYPE.get(
                type(value), FALLBACK_MESSAGE_ATTRIBUTES_TYPE
            )
            value_key = "BinaryValue" if attr_type == "Binary" else "StringValue"
            if attr_type in ("String.Array", "Number"):
                value = json.dumps(value)
            elif attr_type == "String":
                value = str(value)
            message_attributes[key] = {
                "DataType": attr_type,
                value_key: value,
            }
        return message_attributes

    def handle_exception(self, exc, message_data, message_attributes):
        error_msg = (
            "error_publishing_message, "
            "topic_name={}, "
            "message_data={!r}, "
            "message_attributes={!r}, "
            "error={!r}".format(self.topic_name, message_data, message_attributes, exc)
        )
        logger.error(error_msg)
        if exc.response["Error"]["Code"] == "NotFound":
            raise SQSClientTopicNotFound(error_msg)
        raise SQSClientPublishError(error_msg)


class SQSClient(BaseSQSClient):
    @cached_property
    def client(self):
        session = boto3.Session(
            region_name=self.region_name, profile_name=self.profile_name
        )
        return session.client("sqs")

    def publish(self, message_data, delay_seconds=1, message_attributes=None):
        if delay_seconds is None or delay_seconds < 1:
            logger.warning("Invalid delay_seconds value. It must be at least 1.")
            return False

        if delay_seconds > 43200:  # 12 hours in seconds
            logger.warning("Message delay exceeds 12 hours. Message not published.")
            return False
        message_attributes = message_attributes or {}
        message_attributes = self._prepare_message_attributes(message_attributes)

        logger.info(
            "topic_name={}, "
            "message_data={!r}, "
            "message_attributes={!r}".format(
                self.topic_name, message_data, message_attributes
            )
        )

        message = json.dumps(message_data)

        try:
            self.client.send_message(
                QueueUrl=self.topic_name,
                MessageBody=message,
                DelaySeconds=delay_seconds,
                MessageAttributes=message_attributes,
            )
        except ClientError as exc:
            self.handle_exception(exc, message_data, message_attributes)

        self.log(
            "published_message, "
            "topic_name={}, "
            "message={!r}, "
            "message_attributes={!r}".format(
                self.topic_name, message, message_attributes
            )
        )

        return True


class MessageFilter:
    """
    A utility class responsible for filtering SQS messages based on the service name.

    Methods:
        filter_messages(service_name: str, event: dict) -> list:
            Filters messages from the provided event based on the service name.
    """

    @staticmethod
    def filter_messages(event, service_name=None):
        """
        Filter messages from the provided event based on the given service name.

        If the service_name is None or matches the service specified in the message attributes,
        the message is included in the returned list.

        Args:
        - service_name (str): The name of the service to filter messages for.
                             If None, all messages are returned.
        - event (dict): The event data containing SQS records.

        Returns:
        - list: A list of messages filtered based on the service name.
        """
        logger.info(event)
        messages = []

        for record in event.get("Records", []):
            message_body = (
                record["body"]
                if isinstance(record["body"], dict)
                else json.loads(record["body"])
            )

            if (
                not service_name
                or service_name
                == record["messageAttributes"]["service_name"]["stringValue"]
            ):
                messages.append(message_body)

        return messages


class HubspotSQSMessage:
    """
    HubspotMessage is a utility class for sending messages related to Hubspot operations.

    Attributes:
        SERVICE_NAME (str): The default service name for Hubspot.
        TOPIC_NAME (str): The default topic name for the message queue.
        DEFAULT_LOG_LEVEL (str): The default log level for logging.
        DEFAULT_REGION (str): The default AWS region for the SQS client.
        DEFAULT_TOPIC_PREFIX (str): The default topic prefix, fetched from environment or set to "Staging".

    Example:
        hubspot_msg = HubspotMessage()
        hubspot_msg.send_business_message(business_id=10293)
    """

    SERVICE_NAME = "hubspot"
    TOPIC_NAME = "reach-data-bridge-messages-queue"
    DEFAULT_LOG_LEVEL = "info"
    DEFAULT_REGION = "us-east-1"
    DEFAULT_TOPIC_PREFIX = os.environ.get("ENV", "Staging")

    def __init__(
        self,
        log_level=DEFAULT_LOG_LEVEL,
        region_name=DEFAULT_REGION,
        topic_prefix=DEFAULT_TOPIC_PREFIX,
    ):
        self.log_level = log_level
        self.region_name = region_name
        self.topic_prefix = topic_prefix

    @property
    def client(self):
        return SQSClient(
            topic_name=f"{self.topic_prefix}-{self.TOPIC_NAME}",
            log_level=self.log_level,
            region_name=self.region_name,
        )

    def send_business_message(self, business_id, delay_seconds=1):
        return self.client.publish(
            message_data={
                "object_name": "business",
                "object_id": business_id,
                "delay_seconds": delay_seconds,
            },
            message_attributes={"service_name": self.SERVICE_NAME},
            delay_seconds=delay_seconds,
        )
