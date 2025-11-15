"""
Main entry point for the chatbot service - Multi-Use Case Menu
"""

from src.handlers.faq_handler import FAQHandler
from src.handlers.order_status_handler import OrderStatusHandler
from src.handlers.password_reset_handler import PasswordResetHandler
from src.handlers.ticket_handler import TicketHandler
from src.handlers.escalation_handler import EscalationHandler
from src.handlers.feedback_handler import FeedbackHandler


def space():
    print()
    print()


def display_main_menu():
    """Display the main menu."""
    space()
    print("TechCare Assistant Chatbot")
    space()
    print("Please select a service:")
    print("1. Frequently Asked Questions")
    print("2. Check Your Order Status")
    print("3. Reset Your Password")
    print("4. Create a Support Ticket")
    print("5. Speak with an Agent")
    print("6. Share Your Feedback")
    print("7. Exit")
    space()


def run_faq_chatbot():
    """Run the FAQ chatbot."""
    space()
    print("FAQ Assistant")
    space()
    print("You may ask about topics such as operating hours, shipping, returns,")
    print("payment methods, contact information, warranty, and account management.")
    print("Type 'back' to return to the main menu or 'quit' to exit.")
    space()

    try:
        faq_handler = FAQHandler()

        while True:
            space()
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                return 'quit'

            if user_input.lower() == 'back':
                return 'back'

            if not user_input:
                print("Please enter a question.")
                continue

            response = faq_handler.handle(user_input)
            print()
            print("Assistant:", response.text)

            if response.links:
                print()
                print("Helpful Links:")
                for link in response.links:
                    print("-", link)

            if response.suggestions:
                print()
                print("You may also want to ask:")
                for suggestion in response.suggestions[:3]:
                    print("-", suggestion)

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def run_order_status_chatbot():
    """Run the order status chatbot."""
    space()
    print("Order Status Checker")
    space()
    print("You can check the status of sample test orders such as:")
    print("ORD-12345, ORD-67890, ORD-11111, ORD-22222, ORD-33333")
    print("Type 'back' to return to the menu or 'quit' to exit.")
    space()

    try:
        order_handler = OrderStatusHandler()

        while True:
            space()
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                return 'quit'

            if user_input.lower() == 'back':
                return 'back'

            if not user_input:
                print("Please enter your order ID or question.")
                continue

            response = order_handler.handle(user_input)
            print()
            print("Assistant:", response.text)

            if response.links:
                print()
                print("Helpful Links:")
                for link in response.links:
                    print("-", link)

            if response.suggestions:
                print()
                print("Additional suggestions:")
                for suggestion in response.suggestions[:3]:
                    print("-", suggestion)

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def run_password_reset():
    """Run the password reset flow."""
    space()
    print("Password Reset")
    space()

    try:
        reset_handler = PasswordResetHandler()
        response = reset_handler.handle()
        print(response.text)
        space()

        while True:
            space()
            new_password = input("Enter new password (or 'back' to return): ").strip()

            if new_password.lower() == 'back':
                return 'back'

            if new_password.lower() in ['quit', 'exit']:
                return 'quit'

            if not new_password:
                print("Password cannot be empty.")
                continue

            confirm = input("Confirm new password: ").strip()

            if confirm != new_password:
                print("Passwords do not match. Please try again.")
                continue

            print()
            print("Updating password...")
            reset_response = reset_handler.reset_password(new_password)
            print(reset_response.text)

            if reset_response.suggestions:
                print()
                print("Next steps:")
                for suggestion in reset_response.suggestions[:3]:
                    print("-", suggestion)

            if "successfully" in reset_response.text.lower():
                input("Press Enter to return to the main menu...")
                return 'back'

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def run_support_ticket():
    """Run support ticket creation."""
    space()
    print("Support Ticket Creation")
    space()
    print("Type 'back' to return or 'quit' to exit.")
    space()

    try:
        ticket_handler = TicketHandler()

        while True:
            space()
            subject = input("Enter ticket subject: ").strip()

            if subject.lower() in ['quit', 'exit']:
                return 'quit'

            if subject.lower() == 'back':
                return 'back'

            if not subject:
                print("Subject cannot be empty.")
                continue

            description = input("Enter detailed description: ").strip()

            if description.lower() == 'back':
                return 'back'

            if not description:
                print("Description cannot be empty.")
                continue

            print()
            print("Creating your ticket...")
            response = ticket_handler.handle(subject, description)
            print(response.text)

            if response.links:
                print()
                print("Helpful Links:")
                for link in response.links:
                    print("-", link)

            if response.suggestions:
                print()
                print("Next steps:")
                for suggestion in response.suggestions[:3]:
                    print("-", suggestion)

            again = input("Create another ticket? (yes/no): ").strip().lower()
            if again not in ['yes', 'y']:
                return 'back'

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def run_escalation():
    """Run escalation to a human agent."""
    space()
    print("Escalation to Human Agent")
    space()
    print("Type 'back' to return or 'quit' to exit.")
    space()

    try:
        escalation_handler = EscalationHandler()

        while True:
            space()
            name = input("Your Name: ").strip()

            if name.lower() == 'back':
                return 'back'

            if name.lower() in ['quit', 'exit']:
                return 'quit'

            if not name:
                print("Name cannot be empty.")
                continue

            phone = input("Your Phone Number: ").strip()

            if phone.lower() == 'back':
                return 'back'

            if phone.lower() in ['quit', 'exit']:
                return 'quit'

            if not phone:
                print("Phone number cannot be empty.")
                continue

            reason = input("Brief description (optional): ").strip()
            if reason.lower() == 'back':
                return 'back'

            response = escalation_handler.handle(name, phone, reason if reason else None)
            print(response.text)

            if "success" in response.text.lower():
                again = input("Submit another request? (yes/no): ").strip().lower()
                if again not in ['yes', 'y']:
                    return 'back'
            else:
                retry = input("Try again? (yes/no): ").strip().lower()
                if retry not in ['yes', 'y']:
                    return 'back'

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def run_feedback():
    """Run feedback collection."""
    space()
    print("Share Your Feedback")
    space()
    print("Type 'back' to return or 'quit' to exit.")
    space()

    try:
        feedback_handler = FeedbackHandler()

        while True:
            space()
            name = input("Your Name: ").strip()

            if name.lower() == 'back':
                return 'back'

            if name.lower() in ['quit', 'exit']:
                return 'quit'

            if not name:
                print("Name cannot be empty.")
                continue

            rating_input = input("Rate your experience (1-5): ").strip()

            if rating_input.lower() == 'back':
                return 'back'

            if rating_input.lower() in ['quit', 'exit']:
                return 'quit'

            try:
                rating = int(rating_input) if rating_input else 3
            except ValueError:
                print("Invalid rating. Enter a number between 1 and 5.")
                continue

            comments = input("Comments (optional): ").strip()

            if comments.lower() == 'back':
                return 'back'

            response = feedback_handler.handle(name, rating, comments if comments else None)
            print(response.text)

            if "success" in response.text.lower():
                again = input("Submit another feedback? (yes/no): ").strip().lower()
                if again not in ['yes', 'y']:
                    return 'back'
            else:
                retry = input("Try again? (yes/no): ").strip().lower()
                if retry not in ['yes', 'y']:
                    return 'back'

    except Exception as e:
        print("An error occurred:", str(e))
        return 'back'


def main():
    """Main function to run the chatbot service."""
    print("Welcome to the TechCare Assistant Chatbot .")

    try:
        while True:
            display_main_menu()
            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                if run_faq_chatbot() == 'quit':
                    break

            elif choice == '2':
                if run_order_status_chatbot() == 'quit':
                    break

            elif choice == '3':
                if run_password_reset() == 'quit':
                    break

            elif choice == '4':
                if run_support_ticket() == 'quit':
                    break

            elif choice == '5':
                if run_escalation() == 'quit':
                    break

            elif choice == '6':
                if run_feedback() == 'quit':
                    break

            elif choice == '7':
                print()
                print("Thank you for using the TechCare Assistant Chatbot. Hope you liked it!.")
                break

            else:
                print()
                print("Invalid Input. Please re-enter a number from 1 to 7.")

    except KeyboardInterrupt:
        print()
        print("Session ended.")
    except Exception as e:
        print()
        print("An error occurred:", str(e))
        print("Please ensure your environment variables are set correctly.")


if __name__ == "__main__":
    main()
