#!/usr/bin/env python3
import os
import sys
import json
import requests
from dotenv import load_dotenv
import readline  # For better command line input handling

# Load environment variables from .env file
load_dotenv()

# Get Claude API key from environment variables
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    print("Error: CLAUDE_API_KEY not found in environment variables.")
    sys.exit(1)

# Claude API endpoint
API_URL = "https://api.anthropic.com/v1/messages"

# Headers for API requests
headers = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

# Initialize conversation history
conversation_history = []

# System prompt for the agent
system_prompt = "You are Claude, an AI assistant created by Anthropic. You are helpful, harmless, and honest. You are assisting a user via a command-line interface. You specialize in cryptocurrency trading, blockchain technology, and financial analysis. You can help with analyzing market trends, explaining blockchain concepts, and providing insights on trading strategies. However, you cannot execute actual trades or access real-time market data unless explicitly provided by the user."


def send_message(user_message):
    """Send a message to Claude API and return the response"""
    global conversation_history

    # Prepare the messages array with conversation history
    messages = []
    for message in conversation_history:
        messages.append(message)

    # Add the new user message
    messages.append({"role": "user", "content": user_message})

    # Prepare the request payload
    payload = {
        "model": "claude-3-7-sonnet-20250219",
        "max_tokens": 4000,
        "system": system_prompt,  # System prompt as a separate parameter
        "messages": messages
    }

    try:
        # Send the request to Claude API
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response
        result = response.json()
        assistant_message = result["content"][0]["text"]

        # Update conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append(
            {"role": "assistant", "content": assistant_message})

        return assistant_message

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Claude API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return "Sorry, I encountered an error while processing your request."


def print_welcome():
    """Print welcome message and instructions"""
    print("\n" + "=" * 80)
    print("Welcome to the Claude AI Command Line Agent!")
    print("Type your messages and Claude will respond.")
    print("Special commands:")
    print("  /exit - Exit the program")
    print("  /clear - Clear the conversation history")
    print("  /help - Show this help message")
    print("=" * 80 + "\n")


def main():
    global conversation_history
    print_welcome()

    # Main interaction loop
    while True:
        try:
            # Get user input
            # Green color for user prompt
            user_input = input("\n\033[1;32mYou: \033[0m")

            # Check for special commands
            if user_input.lower() == "/exit":
                print("\nExiting Claude Agent. Goodbye!")
                break
            elif user_input.lower() == "/clear":
                conversation_history = []
                print("\nConversation history cleared.")
                continue
            elif user_input.lower() == "/help":
                print_welcome()
                continue

            # If empty input, prompt again
            if not user_input.strip():
                continue

            # Send message to Claude and get response
            # Blue color for Claude's responses
            print("\n\033[1;34mClaude: \033[0m", end="")
            response = send_message(user_input)

            # Print the response
            print(response)

        except KeyboardInterrupt:
            print("\n\nExiting Claude Agent. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()
