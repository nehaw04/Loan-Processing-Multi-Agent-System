# check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

try:
    # Set your API key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    print("--- Finding all available models for your API key... ---")
    
    # List all models
    for m in genai.list_models():
        # Check if the model supports the 'generateContent' method
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found usable model: {m.name}")

    print("\n--- Finished ---")
    print("\nACTION: Copy one of the 'usable model' names (e.g., 'models/gemini-pro')")
    print("and paste it into your main.py file on line 15.")

except KeyError:
    print("ERROR: Could not find 'GOOGLE_API_KEY' in your .env file.")
except Exception as e:
    print(f"An error occurred: {e}")