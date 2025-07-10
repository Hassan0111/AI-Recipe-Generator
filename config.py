# config.py
import os
from dotenv import load_dotenv

def load_api_key():
    """
    Loads the Google Gemini API key from environment variables.

    Tries to load from a .env file for local development first,
    then falls back to checking system environment variables, which
    is suitable for deployment platforms like Streamlit Cloud.

    Returns:
        str: The Google Gemini API key.

    Raises:
        ValueError: If the API key is not found.
    """
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Get the API key from the environment variable
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "Google Gemini API key not found. "
            "Please set the GOOGLE_API_KEY environment variable in your .env file or system settings."
        )
    return api_key

if __name__ == '__main__':
    # For testing the configuration loader
    try:
        key = load_api_key()
        print("API Key loaded successfully.")
    except ValueError as e:
        print(e)
