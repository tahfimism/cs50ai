# First, make sure you have the library installed by running:
# pip install -q -U google-generativeai

import google.generativeai as genai
import os

# --- 1. SET UP YOUR API KEY ---
# Replace 'YOUR_API_KEY' with the key you copied from Google AI Studio.
# For security, you can also store this in an environment variable.
API_KEY = "AIzaSyC_E6c-4SXtjIuopjH3-hREbi6UVVFUAhw"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

# --- 2. INSTANTIATE THE MODEL ---
# 'gemini-1.5-flash' is a fast, efficient model for general tasks.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. GET INTERACTIVE USER INPUT AND GENERATE A RESPONSE ---
while True:
    try:
        # Prompt the user for their input
        user_prompt = input("Enter your prompt (or type 'exit' to quit): ")

        # Check if the user wants to exit the program
        if user_prompt.lower() == 'exit':
            print("Exiting program.")
            break

        # Send the user's prompt to the model and get a response
        print("Thinking...")
        response = model.generate_content(user_prompt)

        # Print the response text
        print("\n--- AI Response ---")
        print(response.text)
        print("-------------------\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Continue the loop even if there's an error on one turn
        continue
