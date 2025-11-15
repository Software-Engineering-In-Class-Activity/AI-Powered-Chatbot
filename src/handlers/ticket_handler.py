"""
TicketHandler - Handles support ticket creation.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict
from src.models.context import Context
from src.models.response import Response


class TicketHandler:
    """
    Handles requests for creating support tickets.
    Tickets are stored in a local JSON file to simulate
    how a real support system might keep records.
    """

    def __init__(self):
        """
        Prepare the storage file for support tickets.
        Makes sure the data directory exists and that
        the JSON file is created if this is the first ticket.
        """
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self.tickets_file = os.path.join(self.data_dir, 'tickets.json')

        # Make sure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # If no ticket file exists yet, create an empty one
        if not os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'w') as f:
                json.dump([], f, indent=2)

    def _generate_ticket_id(self) -> str:
        """
        Create a unique ticket ID.
        ID format grows based on how many tickets exist.
        Example: TKT-00001, TKT-00002, etc.
        """
        try:
            with open(self.tickets_file, 'r') as f:
                tickets = json.load(f)
                next_id = len(tickets) + 1
        except Exception:
            # If something goes wrong reading the file, fall back to ID 1
            next_id = 1

        return f"TKT-{next_id:05d}"

    def _save_ticket(self, ticket: Dict[str, Any]) -> bool:
        """
        Save the new ticket into the JSON storage file.
        Returns True if saving was successful.
        """
        try:
            # Load existing tickets
            with open(self.tickets_file, 'r') as f:
                tickets = json.load(f)

            # Add the new ticket to the list
            tickets.append(ticket)

            # Save updated list
            with open(self.tickets_file, 'w') as f:
                json.dump(tickets, f, indent=2)

            return True

        except Exception as e:
            # For debugging purposes; real systems wouldn't print raw errors
            print(f"Error saving ticket: {str(e)}")
            return False

    def handle(
        self,
        subject: str,
        description: str,
        customer_name: str = "Ayush Dhoundiyal",
        customer_email: str = "ayush@techcareassistant.com"
    ) -> Response:
        """
        Create a support ticket using the subject and description provided.
        Automatically fills in metadata such as timestamp and status.
        """

        try:
            # Generate a new ticket ID
            ticket_id = self._generate_ticket_id()

            # Build the ticket record
            ticket = {
                "ticket_id": ticket_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "subject": subject,
                "description": description,
                "status": "Open",
                "priority": "Medium",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Attempt to save the ticket
            if self._save_ticket(ticket):
                message = (
                    f"Thank you, {customer_name}. Your support ticket has been created.\n\n"
                    f"Ticket Details:\n"
                    f"- Ticket ID: {ticket_id}\n"
                    f"- Subject: {subject}\n"
                    f"- Status: Open\n"
                    f"- Created: {ticket['created_at']}\n\n"
                    f"Our support team will review your request and respond within 24 hours "
                    f"at {customer_email}.\n\n"
                    f"If you need to follow up, please reference ticket ID {ticket_id}."
                )

                return Response(
                    text=message,
                    links=[
                        "https://TechCareassistantbo.com/support",
                        "https:/TechCareassistantbo.com/contact"
                    ],
                    suggestions=[
                        "Check ticket status",
                        "Create another ticket",
                        "Contact support"
                    ]
                )

            # If saving failed, treat as an error
            else:
                raise Exception("The ticket could not be saved.")

        except Exception as e:
            error_message = (
                "We were unable to create your support ticket due to an unexpected error. "
                f"Details: {str(e)}\n\n"
                "Please try again, or contact our support team directly if the problem continues."
            )

            return Response(
                text=error_message,
                links=["https://TechCareassistantbot.com/contact"],
                suggestions=["Try again", "Contact support"]
            )