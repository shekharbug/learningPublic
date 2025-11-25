#!/usr/bin/env python3
#####################################################################
# filename  : ai_studio_code.py
# Author    : Shekhar
# Created   : 13-Oct-2025
# Version   : 1.0
# Description: learning google llm 
# Reference Link: https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-lite
# History   : 
#####################################################################

# prerequites
# pip install -U -q "google"
# pip install -U -q "google.genai"

import os
from google import genai
from google.genai.errors import APIError

def run_chat_session():
    """
    Initializes a Gemini chat session that remembers history 
    and runs a continuous conversation loop.
    """
    # 1. Initialization
    try:
        # Client automatically uses the GEMINI_API_KEY environment variable
        client = genai.Client()
        # Use a model that's good for multi-turn chat
        model_name = "gemini-2.5-flash"
        # model_name = "gemini-2.0-flash"
    except Exception as e:
        print("Error: Could not initialize the Gemini Client.")
        print(f"Details: {e}")
        print("Please ensure you have set the GEMINI_API_KEY environment variable.")
        return False

    # 2. Create the Chat Session
    # The 'chats.create' method automatically manages the history for you.
    try:
        chat = client.chats.create(model=model_name)
    except APIError as e:
        print(f"Error creating chat session with model '{model_name}'.")
        print(f"Details: {e}")
        return False

    print("🤖 Gemini Chat Session Initialized 🤖")
    print(f"Model: {model_name}")
    print("Start chatting! Type 'quit' or 'exit' to end the session.")
    print("-" * 30)
    
    # 3. Conversation Loop
    while True:
        try:
            # Get user input
            prompt = input("You: ")
            
            # Check for exit commands
            if prompt.lower() in ["quit", "exit"]:
                print("\n👋 Chat session ended. Goodbye!")
                break
                
            if not prompt.strip():
                continue

            # Send the message and receive the response
            # The 'send_message' method automatically includes the 
            # previous messages stored in the 'chat' object.
            response = chat.send_message(prompt)
            
            # Print the model's reply
            print(f"Gemini: {response.text}\n")
            print(f'#'*80)
            print(f'#'*80)

        except APIError as e:
            print(f"\n❌ An API error occurred: {e}. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Chat session ended by user (Ctrl+C). Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    run_chat_session()