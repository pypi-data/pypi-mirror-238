from abc import ABC, abstractmethod

from item_local.item import Item

from enum import Enum


class Importance(Enum):
    LOW = 10
    MEDIUM = 20
    HIGH = 30


class Message(Item, ABC):
    def __init__(self, body: str, importance: Importance, subject: str = None) -> None:
        # TODO We should add all fields from message schema in the database (i.e. message_id, scheduled_sent_timestamp, message_sent_status : MessageSentStatus  ...)
        self.body = body
        self.importance = importance
        self.subject = subject

    # TODO Create a new Class of Recipient
    @abstractmethod
    def send(self, recipients: list, cc: list = None, bcc: list = None) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def was_read(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    def get_importance(self) -> Importance:
        return self.importance

    @abstractmethod
    def _can_send(self) -> bool:
        """Implement this with API management https://github.com/circles-zone/api-management-local-python-package"""
        raise NotImplementedError("Implement this with API management https://github.com/circles-zone/api-management-local-python-package")

    @abstractmethod
    def _after_send_attempt(self) -> None:
        """Update the DB if sent successfully, or with the problem details"""
        raise NotImplementedError("Update the DB if sent successfully, or with the problem details")
