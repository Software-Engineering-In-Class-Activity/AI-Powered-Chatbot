# ServiceLayer: encapsulates business logic and external API access.
from typing import Dict, List, Any, Optional


class ServiceLayer:
    # Thin abstraction over knowledge base, order system, ticketing, and feedback.

    def __init__(self):
        # Initialize clients, caches, or credentials needed for service calls.
        pass

    def kb_search(self, query: str) -> List[Dict[str, Any]]:
        # Search a knowledge base and return matching entries for a query.
        # Returns a list of result dicts.
        pass

    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        # Look up the status of an order by its ID and return details if found.
        pass

    def create_ticket(self, user_id: str, issue: str) -> Dict[str, Any]:
        # Create a support ticket for the given user and issue description.
        pass

    def record_feedback(self, user_id: str, feedback: str, 
                       rating: Optional[int] = None) -> bool:
        # Save user feedback (and optional rating). Return True on success.
        pass
