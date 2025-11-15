"""
FAQHandler - Handles frequently asked questions using Ozwell AI.
"""

import os
import requests
from typing import Any
from dotenv import load_dotenv
from src.models.context import Context
from src.models.response import Response

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class FAQHandler:
    """
    Handles frequently asked questions using a knowledge base
    and  we use the Ozwell AI service.
    """

    FAQ_KNOWLEDGE_BASE = """
    Company Name: TechCare Assistant Chatbot

    Operating Hours:
    - Monday to Friday: 9:00 AM to 6:00 PM EST
    - Saturday: 10:00 AM to 4:00 PM EST
    - Sunday: Closed

    Shipping Information:
    - Standard Shipping: 5 to 7 business days (free for orders over $50)
    - Express Shipping: 2 to 3 business days ($15)
    - Overnight Shipping: 1 business day ($30)

    Return Policy:
    - Returns accepted within 30 days of purchase
    - Items must be unused and in original packaging
    - Refund processed within 5 to 7 business days after receiving the return

    Payment Methods:
    - Visa, MasterCard, American Express
    - PayPal
    - Apple Pay
    - Google Pay

    Contact Information:
    - Email: support@TechCareassistantbot.com
    - Phone: 1-800-BOT
    - Live Chat: Available on our website during business hours

    Warranty Information:
    - All products include a 1-year manufacturer warranty
    - Extended warranty available for purchase
    - Warranty covers manufacturing defects only

    Account Management:
    - Create an account on our website
    - Track orders using your account dashboard
    - Save multiple shipping addresses
    - View order history
    """

    def __init__(self):
        """Initialize FAQ handler and load API key."""
        self.api_key = os.getenv('OZWELL_API_KEY')
        if not self.api_key:
            raise ValueError("OZWELL_API_KEY is missing in the environment variables.")
        self.ozwell_url = "https://ai.bluehive.com/api/v1/completion"

    def handle(self, question: str) -> Response:
        """
        Process an FAQ question using Ozwell AI.

        Args:
            question (str): The customer's question.

        Returns:
            Response: A structured response containing the answer,
                      helpful links, and suggested follow-up questions.
        """
        try:
            system_message = f"""
You are a customer service assistant for Chatbot Service.
Use the following knowledge base to answer the customer's question clearly and politely.

If the knowledge base does not contain the required information,
let the customer know that you do not have that specific detail,
and suggest reaching out to support for more help.

Knowledge Base:
{self.FAQ_KNOWLEDGE_BASE}
"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": question,
                "systemMessage": system_message,
                "temperature": 0.7,
                "maxTokens": 300
            }

            response = requests.post(self.ozwell_url, headers=headers, json=payload)

            if response.ok:
                try:
                    answer = response.json()["choices"][0]["message"]["content"]
                except Exception as parsing_error:
                    answer = (
                        "I received a response from the service, but I was unable to interpret it. "
                        f"Details: {str(parsing_error)}"
                    )
            else:
                answer = (
                    "I could not retrieve a response from the AI service at this time. "
                    f"The service returned status code {response.status_code}."
                )

            suggestions = [
                "What are your operating hours?",
                "What is your return policy?",
                "How can I contact support?"
            ]

            return Response(
                text=answer,
                links=["https://TechCareassistantbot.com/faq", "https://TechCareassistantbo.com/contact"],
                suggestions=suggestions
            )

        except Exception as e:
            error_message = (
                "I was unable to process your question due to an unexpected error. "
                f"Details: {str(e)}"
            )

            return Response(
                text=error_message,
                suggestions=[
                    "You may try asking another question.",
                    "You may also contact customer support directly for assistance."
                ]
            )
