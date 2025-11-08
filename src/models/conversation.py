# Conversation: model for chat conversations with id, status, and messages.
from typing import List
from src.models.message import Message


class Conversation:
    # Tracks conversation id, current status, and the messages exchanged.

    def __init__(self, conversation_id: str, status: str = "active"):
        # conversation_id: unique id; status: 'active' by default.
        self.conversation_id: str = conversation_id
        self.status: str = status
        self.messages: List[Message] = []

    def add_message(self, msg: Message) -> None:
        # Append a Message object to the conversation's message list.
        # TODO: validate message shape, handle duplicates/timestamps.
        pass
