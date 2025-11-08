# Response: container for chatbot replies, links, and follow-up suggestions.
from typing import List, Optional


class Response:
    # text: reply body; links: optional related URLs; suggestions: follow-ups.

    def __init__(self, text: str = "", links: Optional[List[str]] = None, 
                 suggestions: Optional[List[str]] = None):
        # Initialize a Response with optional links and suggestions.
        self.text: str = text
        self.links: List[str] = links if links is not None else []
        self.suggestions: List[str] = suggestions if suggestions is not None else []
