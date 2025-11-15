"""
EscalationHandler - Handles escalation to a human agent.
"""

import json
import os
from datetime import datetime
from typing import Optional
from src.models.response import Response


class EscalationHandler:
    """
    Handles escalation requests to a human agent.
    Saves customer information and the reason for escalation.
    """

    def __init__(self):
        self.escalations_file = "data/escalations.json"
        self._ensure_data_file()

    def _ensure_data_file(self) -> None:
        """Ensure the escalation JSON file exists."""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.escalations_file):
            with open(self.escalations_file, 'w') as f:
                json.dump([], f)

    def _generate_escalation_id(self) -> str:
        """
        Generate a unique escalation ID.

        Returns:
            str: Escalation ID in the format ESC-XXXXX
        """
        try:
            with open(self.escalations_file, 'r') as f:
                escalations = json.load(f)
            next_id = len(escalations) + 1
            return f"ESC-{next_id:05d}"
        except Exception:
            return "ESC-00001"

    def _validate_phone_number(self, phone: str) -> bool:
        """
        Validate the phone number format.
        Allows digits, with optional separators.

        Returns:
            bool: True if valid
        """
        cleaned = (
            phone.replace("-", "")
                 .replace(" ", "")
                 .replace("(", "")
                 .replace(")", "")
                 .replace("+", "")
        )

        return cleaned.isdigit() and 10 <= len(cleaned) <= 15

    def _save_escalation(self, customer_name: str, phone: str, reason: str) -> str:
        """
        Save an escalation request in the JSON file.

        Returns:
            str: Generated escalation ID
        """
        escalation_id = self._generate_escalation_id()

        escalation = {
            "escalation_id": escalation_id,
            "customer_name": customer_name,
            "phone_number": phone,
            "reason": reason,
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open(self.escalations_file, 'r') as f:
                escalations = json.load(f)

            escalations.append(escalation)

            with open(self.escalations_file, 'w') as f:
                json.dump(escalations, f, indent=2)

            return escalation_id

        except Exception as e:
            raise Exception(f"Failed to save escalation: {str(e)}")

    def handle(self, customer_name: str, phone: str, reason: Optional[str] = None) -> Response:
        """
        Handle the escalation request and return a confirmation response.

        Returns:
            Response: A message confirming the escalation
        """

        if not self._validate_phone_number(phone):
            return Response(
                text=(
                    "The phone number you entered does not appear to be valid. "
                    "Please enter a number that contains 10 to 15 digits."
                )
            )

        if not reason:
            reason = "Customer requested support from a human agent"

        try:
            escalation_id = self._save_escalation(customer_name, phone, reason)

            message = (
                f"Your request has been submitted successfully.\n\n"
                f"Escalation ID: {escalation_id}\n"
                f"Name: {customer_name}\n"
                f"Phone Number: {phone}\n\n"
                f"A human agent will reach out to you soon using the provided contact details.\n"
                f"Thank you for your patience."
            )

            return Response(text=message)

        except Exception as e:
            return Response(
                text=f"We were unable to submit your request due to an error: {str(e)}"
            )
