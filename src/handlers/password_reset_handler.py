"""
PasswordResetHandler - Handles password reset requests.
"""

import os
import json
import hashlib
from typing import Dict, Optional
from src.models.context import Context
from src.models.response import Response


class PasswordResetHandler:
    """
    Manages password reset requests for a single configured user.
    This version simulates a real password reset system by storing
    hashed passwords in a local JSON file.
    """

    # The user this handler manages. In a real system,
    # this would come from a database or authentication service.
    USER_NAME = "Ayush Dhoundiyal"
    USER_ID = "ayush.dhoundiyal"

    def __init__(self):
        """
        Set up the handler by preparing the password file location.
        If the file does not already exist, we create it with a default password.
        """
        self.password_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'data',
            'passwords.json'
        )

        # Make sure the directory exists before writing to it
        os.makedirs(os.path.dirname(self.password_file), exist_ok=True)

        # Create the file if it does not already exist
        if not os.path.exists(self.password_file):
            self._initialize_password_file()

    def _initialize_password_file(self):
        """
        Create a new password file with a default password.
        This only runs when the file does not exist yet.
        """
        initial_data = {
            self.USER_ID: self._hash_password("TechShop2025!")
        }
        with open(self.password_file, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _hash_password(self, password: str) -> str:
        """
        Convert a plain password into a SHA-256 hash.
        Storing hashes instead of raw passwords is standard security practice.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_passwords(self) -> Dict[str, str]:
        """
        Load all stored password hashes from the file.

        If the file is missing or corrupted,
        it is recreated with a default entry.
        """
        try:
            with open(self.password_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Recreate the file if it is missing or unreadable
            self._initialize_password_file()
            return {self.USER_ID: self._hash_password("TechShop2025!")}

    def _save_passwords(self, passwords: Dict[str, str]) -> bool:
        """
        Save updated password hashes back to the file.
        Returns True if the save was successful.
        """
        try:
            with open(self.password_file, 'w') as f:
                json.dump(passwords, f, indent=2)
            return True
        except Exception:
            return False

    def _validate_password(self, password: str) -> tuple[bool, Optional[str]]:
        """
        Check whether a password meets the minimum security requirements.
        Returns (True, None) if valid, otherwise (False, error message).
        """
        if len(password) < 8:
            return False, "Your password must be at least 8 characters long."

        if not any(c.isupper() for c in password):
            return False, "Your password must include at least one uppercase letter."

        if not any(c.islower() for c in password):
            return False, "Your password must include at least one lowercase letter."

        if not any(c.isdigit() for c in password):
            return False, "Your password must include at least one number."

        return True, None

    def reset_password(self, new_password: str) -> Response:
        """
        Update the password for the configured user.
        Runs validation, saves the new password,
        and returns a human-readable result.
        """

        # First, check if the password meets requirements
        is_valid, error_message = self._validate_password(new_password)

        if not is_valid:
            return Response(
                text=f"Your password could not be updated. {error_message}",
                suggestions=[
                    "Try a stronger password.",
                    "Ensure it contains uppercase letters, lowercase letters, and numbers."
                ]
            )

        # Load the current password data
        passwords = self._load_passwords()

        # Replace the old password hash with the new one
        passwords[self.USER_ID] = self._hash_password(new_password)

        # Attempt to save the updated file
        if self._save_passwords(passwords):
            return Response(
                text=(
                    f"The password for {self.USER_NAME} has been updated successfully.\n\n"
                    "Your new password is now securely stored and ready to use."
                ),
                links=["https://techshop.com/login"],
                suggestions=[
                    "Try logging in with your new password.",
                    "Update your password manager.",
                    "Return to the main menu."
                ]
            )
        else:
            return Response(
                text=(
                    "We were unable to save your new password due to a system error. "
                    "Please try again or contact support if the issue continues."
                ),
                suggestions=["Try again", "Contact support"]
            )

    def handle(self) -> Response:
        """
        Provide an introduction message explaining whose password
        is being managed and the requirements for creating a new one.
        """
        return Response(
            text=(
                f"Password Reset for {self.USER_NAME}\n\n"
                f"User ID: {self.USER_ID}\n\n"
                "You will now be asked to create a new password.\n\n"
                "Password Requirements:\n"
                "- Minimum of 8 characters\n"
                "- At least one uppercase letter\n"
                "- At least one lowercase letter\n"
                "- At least one number"
            ),
            suggestions=[
                "Enter your new password when prompted.",
                "Return to the main menu."
            ]
        )