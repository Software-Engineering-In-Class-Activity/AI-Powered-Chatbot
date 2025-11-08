# Message: represents a single chat message with sender, text, and timestamp.
from datetime import datetime
from typing import Optional


class Message:
    # sender_type: 'user' or 'bot'; text: the message body; timestamp defaults to now.

    def __init__(self, sender_type: str, text: str, 
                 timestamp: Optional[datetime] = None):
        # Create a Message; if timestamp omitted, use the current time.
        self.sender_type: str = sender_type
        self.text: str = text
        self.timestamp: datetime = timestamp if timestamp is not None else datetime.now()
