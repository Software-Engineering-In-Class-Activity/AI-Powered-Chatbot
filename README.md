
Overview

This project is a command-line chatbot that helps customers with everyday support needs.
It is designed to be easy to use, easy to test, and easy to extend.
All responses are generated using Python logic and Ozwell AI where needed.

The chatbot supports six main functions:
	1.	Answering frequently asked questions
	2.	Checking the status of a customer’s order
	3.	Resetting a password
	4.	Creating a support ticket
	5.	Escalating to a human support agent
	6.	Collecting customer feedback


How to Run the Project

Install required packages
pip install -r requirements.txt

Start the chatbot
python main.py
You will see a menu where you can choose any of the available services.

Features

1. FAQ

The chatbot can answer basic questions about operating hours, shipping, returns, payments, contact details, and other common topics.

2. Order Status

You can check the status of an order by giving an order ID like ORD-12345.
The bot uses a small sample database of five orders.
It tells you whether your order is shipped, delivered, processing, cancelled, or out for delivery.

3. Password Reset

The bot can reset the password for one user (Ayush Dhoundiyal).
It checks if the password is strong and saves the new password securely using hashing.

4. Support Ticket Creation

You can submit a support ticket with a subject and description.
The bot stores each ticket in a JSON file and gives you a ticket ID like TKT-00001.

5. Escalation to Human Agent

If a customer needs real human support, they can provide their name, phone number, and reason.
The bot validates the phone number and creates an escalation request in a JSON file.

6. Feedback Collection

Customers can share a rating (1–5) and optional comments.
The bot saves the feedback and gives a simple confirmation.

 Configuration

Create a file named .env inside the src/ folder:
OZWELL_API_KEY=your-api-key-here
This allows the chatbot to use the Ozwell AI API for question answering.

Sample Order IDs

You can test the Order Status feature using these IDs:
	•	ORD-12345
	•	ORD-67890
	•	ORD-11111
	•	ORD-22222
	•	ORD-33333

Purpose of This Project

This project was created to demonstrate:
	•	how to build a modular chatbot using Python,
	•	how to structure a software engineering project cleanly,
	•	how to use basic NLP routing and handler patterns,
	•	and how to store data simply using JSON files.

It is fully functional and ready for further expansion (such as web UI, database, or multi-user support).
=======
# TechCare-Assistant-Chatbot
>>>>>>> 31bdad966100dbf13102d47c29b889354e87bddb
