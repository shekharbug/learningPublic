#!/usr/bin/env python3
#####################################################################
# filename  : ag_ai_01.py
# Author    : Shekhar
# Created   : 17-Mar-2026
# Version   : 1.0
# Description: 
# Reference Link: 
# History   : 
#####################################################################
from dotenv import load_dotenv
import os
import os
from google import genai
from google.genai import types

load_dotenv()

# 1. SETUP: Initialize the Gemini Client
# Replace 'YOUR_API_KEY' with your actual key or set it as an environment variable
GEMINI_API_KEY = os.getenv('MY_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

# 2. DEFINE THE TOOL: A real Python function the AI can use
# The "Docstring" (the text in triple quotes) is CRITICAL.
# Gemini reads this to understand WHAT the function does and WHEN to use it.
def get_current_weather(location: str):
    """
    Fetches the current weather for a specific city.
    Args:
        location: The name of the city (e.g., 'London', 'New York').
    """
    # In a real app, you would call a Weather API here.
    # For this example, we use mock data.
    weather_database = {
        "London": "15°C and Cloudy",
        "New York": "22°C and Sunny",
        "Tokyo": "18°C and Rainy"
    }
    return weather_database.get(location, "Weather data not available for this city.")

# 3. CONFIGURE THE AGENT: Tell Gemini which tools it has
# We use 'gemini-2.0-flash' because it is extremely fast and handles tools well.
tools_list = [get_current_weather]

# 4. START THE CONVERSATION
# We use a chat session so the agent remembers the context.
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        tools=tools_list,
        system_instruction="You are a helpful weather assistant. Use the tools provided to give accurate data."
    )
)

def run_agent():
    user_input = "What is the weather like in London?"
    print(f"User: {user_input}")

    # The magic happens here: Gemini will see 'London', realize it has a
    # 'get_current_weather' tool, and call it automatically.
    response = chat.send_message(user_input)

    print(f"Agent: {response.text}")

if __name__ == "__main__":
    run_agent()