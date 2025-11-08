# User: simple model for storing basic user information.
from typing import Optional


class User:
    # user_id: unique id; name and email are optional metadata fields.

    def __init__(self, user_id: str, name: str = "", email: str = ""):
        # Store basic user info used across the chatbot.
        self.user_id: str = user_id
        self.name: str = name
        self.email: str = email
