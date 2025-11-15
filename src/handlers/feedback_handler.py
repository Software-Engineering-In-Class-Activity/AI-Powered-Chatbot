"""
FeedbackHandler - Handles user feedback.
"""

import json
import os
from datetime import datetime
from typing import Optional
from src.models.response import Response


class FeedbackHandler:
    """
    Handles feedback submitted by customers.
    Saves the feedback so it can be reviewed later.
    """

    def __init__(self):
        # Path to the file where all feedback entries will be stored.
        self.feedback_file = "data/feedback.json"
        self._ensure_data_file()

    def _ensure_data_file(self):
        """
        Make sure the feedback storage file exists.
        If this is the first time feedback is being saved, create the file
        with an empty list inside it.
        """
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)

    def _generate_feedback_id(self) -> str:
        """
        Create a simple unique ID for each feedback entry.
        The ID is based on how many feedback entries already exist.
        Example: FB-00001, FB-00002, etc.
        """
        try:
            with open(self.feedback_file, 'r') as f:
                feedbacks = json.load(f)
                next_id = len(feedbacks) + 1
                return f"FB-{next_id:05d}"
        except Exception:
            # If there's an issue reading the file, fall back to the first ID.
            return "FB-00001"

    def _save_feedback(self, customer_name: str, rating: int, comments: str) -> str:
        """
        Store a feedback entry in the feedback file.

        Returns the unique feedback ID so it can be shown to the user.
        """
        feedback_id = self._generate_feedback_id()

        feedback = {
            "feedback_id": feedback_id,
            "customer_name": customer_name,
            "rating": rating,
            "comments": comments,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open(self.feedback_file, 'r') as f:
                feedbacks = json.load(f)

            feedbacks.append(feedback)

            with open(self.feedback_file, 'w') as f:
                json.dump(feedbacks, f, indent=2)

            return feedback_id

        except Exception as e:
            raise Exception(f"Failed to save feedback: {str(e)}")

    def handle(self, customer_name: str, rating: Optional[int] = None, comments: Optional[str] = None) -> Response:
        """
        Process a feedback submission from a customer.

        Every feedback entry gets:
        - a rating (1–5)
        - comments (optional)
        - a generated feedback ID
        """

        # Validate rating input in a simple and clear way.
        if rating is not None and (rating < 1 or rating > 5):
            return Response(
                text="The rating should be a number between 1 and 5."
            )

        # If no rating is provided, we assume a neutral rating.
        if rating is None:
            rating = 3

        # If customer does not provide comments, we store a placeholder.
        if not comments:
            comments = "No comments provided."

        try:
            # Save the feedback details.
            feedback_id = self._save_feedback(customer_name, rating, comments)

            # Build the message returned to the user.
            message = (
                "Thank you for sharing your feedback.\n\n"
                f"Feedback ID: {feedback_id}\n"
                f"Name: {customer_name}\n"
                f"Rating: {rating} out of 5\n"
                f"Comments: {comments}\n\n"
                "We appreciate you taking the time to tell us about your experience."
            )

            return Response(text=message)

        except Exception as e:
            return Response(
                text=f"We were not able to submit your feedback due to an error: {str(e)}"
            )