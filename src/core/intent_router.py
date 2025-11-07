# IntentRouter is used to register and lookup handlers for detected intents.
from typing import Dict, Callable, Optional


class IntentRouter:
    # Simple mapping of intent names to handler callables.

    def __init__(self):
        # Start with an empty registry; use register() to add handlers.
        self.registry: Dict[str, Callable] = {}

    def register(self, intent: str, handler: Callable) -> None:
        # Attach a handler callable to an intent string.
        # Left with: add validation / overwrite behavior as needed.
        pass

    def get(self, intent: str) -> Optional[Callable]:
        # Return the handler for the given intent, or None if not found.
        pass
