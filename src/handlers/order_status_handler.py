"""
OrderStatusHandler - Handles order status inquiries using Ozwell AI.
"""

import os
import requests
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from src.models.context import Context
from src.models.response import Response

# Load environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class OrderStatusHandler:
    """
    Handles user questions about their order status.
    This class checks a local order database, and when needed,
    uses Ozwell AI to generate a natural and friendly response.
    """

    # A small built-in database to simulate stored orders.
    # In a real system, this would come from an actual backend or database.
    ORDERS_DB = {
        "ORD-12345": {
            "order_id": "ORD-12345",
            "customer_name": "Ayush",
            "status": "Shipped",
            "items": ["Wireless Mouse", "USB-C Cable"],
            "total": "$45.99",
            "order_date": "November 8, 2025",
            "estimated_delivery": "November 15, 2025",
            "tracking_number": "1Z999AA10123456784",
            "carrier": "UPS"
        },
        "ORD-67890": {
            "order_id": "ORD-67890",
            "customer_name": "Drashti",
            "status": "Processing",
            "items": ["Laptop Stand", "Keyboard", "Monitor"],
            "total": "$329.99",
            "order_date": "November 12, 2025",
            "estimated_delivery": "November 18, 2025",
            "tracking_number": None,
            "carrier": None
        },
        "ORD-11111": {
            "order_id": "ORD-11111",
            "customer_name": "Dishank",
            "status": "Delivered",
            "items": ["Phone Case", "Screen Protector"],
            "total": "$24.99",
            "order_date": "November 1, 2025",
            "estimated_delivery": "November 5, 2025",
            "delivery_date": "November 4, 2025",
            "tracking_number": "1Z999AA10987654321",
            "carrier": "UPS"
        },
        "ORD-22222": {
            "order_id": "ORD-22222",
            "customer_name": " Anayat ",
            "status": "Cancelled",
            "items": ["Headphones"],
            "total": "$89.99",
            "order_date": "November 10, 2025",
            "cancellation_date": "November 11, 2025",
            "cancellation_reason": "Customer request",
            "refund_status": "Processed"
        },
        "ORD-33333": {
            "order_id": "ORD-33333",
            "customer_name": "Dr.V",
            "status": "Out for Delivery",
            "items": ["Gaming Mouse", "Mouse Pad"],
            "total": "$79.99",
            "order_date": "November 9, 2025",
            "estimated_delivery": "November 13, 2025 (Today!)",
            "tracking_number": "1Z999AA10555555555",
            "carrier": "UPS"
        }
    }

    def __init__(self):
        """
        Load the API key and prepare the handler.
        The API key is required to communicate with Ozwell AI.
        """
        self.api_key = os.getenv('OZWELL_API_KEY')
        if not self.api_key:
            raise ValueError("OZWELL_API_KEY is missing from environment variables.")
        self.ozwell_url = "https://ai.bluehive.com/api/v1/completion"

    def _extract_order_id(self, query: str) -> Optional[str]:
        """
        Try to find an order ID in the user's message.
        We simply search for a known order ID pattern inside the text.
        """
        query_upper = query.upper()
        for order_id in self.ORDERS_DB:
            if order_id in query_upper:
                return order_id
        return None

    def _get_order_info(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Look up an order in the local database.
        Returns the order info if found, otherwise None.
        """
        return self.ORDERS_DB.get(order_id)

    def handle(self, query: str) -> Response:
        """
        Process a user request about the status of an order.

        Steps:
        1. Try to find the order ID in the query.
        2. Retrieve the order information if it exists.
        3. Use Ozwell AI to generate a friendly explanation of the order status.
        4. Provide suggestions and links for follow-up actions.
        """
        try:
            # Identify which order the user is asking about.
            order_id = self._extract_order_id(query)

            if not order_id:
                # User didn't provide a recognizable order ID.
                return Response(
                    text=(
                        "I couldn't find an order number in your message. "
                        "Please include the order ID in the format ORD-XXXXX so I can check the status for you."
                    ),
                    suggestions=[
                        "Check order ORD-12345",
                        "What is the status of ORD-67890?",
                        "Track my order ORD-11111"
                    ]
                )

            # Retrieve details for the identified order.
            order_info = self._get_order_info(order_id)

            if not order_info:
                # The order ID was found in text but not in our database.
                return Response(
                    text=(
                        f"I couldn't locate order {order_id} in our records. "
                        "Please verify the number and try again. "
                        "If the issue continues, our support team can assist you."
                    ),
                    links=["https://techshop.com/contact"],
                    suggestions=[
                        "Try a different order number",
                        "Contact customer support"
                    ]
                )

            # Build a system message to guide the AI.
            system_message = (
                "You are a customer service assistant for TechShop Inc. "
                "Use the order information provided to give a clear and friendly update. "
                "Keep the explanation helpful and concise. "
                "If the order has shipped, include tracking details. "
                "If it was delivered, acknowledge it. "
                "If it is still processing or was cancelled, explain it politely."
            )

            # Convert order info into a readable context for the AI.
            order_context = (
                f"Order Information:\n"
                f"- Order ID: {order_info['order_id']}\n"
                f"- Status: {order_info['status']}\n"
                f"- Items: {', '.join(order_info['items'])}\n"
                f"- Total: {order_info['total']}\n"
                f"- Order Date: {order_info['order_date']}\n"
            )

            if order_info.get('estimated_delivery'):
                order_context += f"- Estimated Delivery: {order_info['estimated_delivery']}\n"

            if order_info.get('delivery_date'):
                order_context += f"- Delivered On: {order_info['delivery_date']}\n"

            if order_info.get('tracking_number'):
                order_context += f"- Tracking Number: {order_info['tracking_number']}\n"
                order_context += f"- Carrier: {order_info['carrier']}\n"

            if order_info.get('cancellation_reason'):
                order_context += f"- Cancellation Reason: {order_info['cancellation_reason']}\n"
                order_context += f"- Refund Status: {order_info['refund_status']}\n"

            # Build the request for Ozwell AI.
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": f"User asked: {query}\n\n{order_context}\n\nGive a friendly explanation about this order.",
                "systemMessage": system_message,
                "temperature": 0.7,
                "maxTokens": 250
            }

            # Call the AI service.
            ai_response = requests.post(self.ozwell_url, headers=headers, json=payload)

            if ai_response.ok:
                # Try to extract the AI-written message.
                try:
                    answer = ai_response.json()["choices"][0]["message"]["content"]
                except Exception:
                    # If AI response format is unexpected, fall back.
                    answer = f"Order {order_id} is currently listed as {order_info['status']}."
                    if order_info.get('tracking_number'):
                        answer += f" Tracking number: {order_info['tracking_number']}."
            else:
                # If AI call fails, provide a simple fallback.
                answer = f"Order {order_id} is currently listed as {order_info['status']}."
                if order_info.get('tracking_number'):
                    answer += f" Tracking number: {order_info['tracking_number']}."

            # Prepare suggestions based on what is relevant for this order.
            suggestions = []
            if order_info.get('tracking_number'):
                suggestions.append(f"Track package {order_info['tracking_number']}")
            suggestions.extend([
                "Check another order",
                "Contact customer support"
            ])

            # Add helpful links.
            links = []
            if order_info.get('tracking_number'):
                links.append(f"https://www.ups.com/track?tracknum={order_info['tracking_number']}")
            links.append("https://techshop.com/orders")

            return Response(
                text=answer,
                links=links,
                suggestions=suggestions[:3]
            )

        except Exception as e:
            # Catch unexpected errors and respond in a friendly manner.
            return Response(
                text=(
                    "Something went wrong while trying to check your order. "
                    f"Here are the details: {str(e)}"
                ),
                suggestions=["Try again", "Contact support"]
            )
