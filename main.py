# Main entry point for the chatbot service — starts the chatbot orchestration.
from src.core.chat_service import ChatService


def main():
    # Start up the chatbot service and wire required components.
    # Initialize the chat service
    chat_service = ChatService()

    # Next: hook this into a server or CLI loop (not implemented yet)
    print("Chatbot Service initialized successfully!")
    print("The project structure is ready; implement the main loop next.")


if __name__ == "__main__":
    main()
