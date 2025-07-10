# gemini_handler.py
import google.generativeai as genai
import logging
from config import load_api_key

# --- Configuration ---
try:
    # Load the API key using the centralized function
    API_KEY = load_api_key()
    genai.configure(api_key=API_KEY)
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
except ValueError as e:
    # This will catch the error if the API key is not found
    logging.error(e)
    # We will handle the user-facing error in the Streamlit app
    API_KEY = None

# --- Model Initialization ---
def get_gemini_model():
    """
    Initializes and returns the Gemini Pro model instance.
    Handles potential errors during model initialization.

    Returns:
        GenerativeModel instance or None if initialization fails.
    """
    if not API_KEY:
        return None
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        logging.error(f"Failed to initialize Gemini model: {e}")
        return None

# --- Main Generation Function ---
def generate_recipe(prompt, conversation_history=None):
    """
    Generates content using the Gemini model with conversation history.

    Args:
        prompt (str): The user prompt to send to the model.
        conversation_history (list, optional): A list of past interactions. Defaults to None.

    Returns:
        tuple: A tuple containing the generated text (str) and the updated
               conversation history (list). Returns (None, history) on failure.
    """
    model = get_gemini_model()
    if not model:
        error_message = "Gemini API is not configured. Please check your API key."
        logging.error(error_message)
        # Return the error message to be displayed to the user
        return error_message, conversation_history or []

    # Initialize chat if history is not provided
    chat = model.start_chat(history=conversation_history or [])

    try:
        logging.info("Sending prompt to Gemini API...")
        response = chat.send_message(prompt, stream=False) # Use stream=False for a complete response
        generated_text = response.text
        logging.info("Successfully received response from Gemini API.")
        return generated_text, chat.history
    except Exception as e:
        logging.error(f"An error occurred while communicating with the Gemini API: {e}")
        error_message = f"Sorry, I couldn't generate a recipe right now. Error: {e}"
        # Return the error and the history up to the point of failure
        return error_message, chat.history

if __name__ == '__main__':
    # For testing the Gemini handler directly
    print("--- Testing Gemini Handler ---")
    if not API_KEY:
        print("Cannot run test: Gemini API key is not configured.")
    else:
        from prompts import get_recipe_prompt
        test_ingredients = ["lamb", "tomatoes", "onions", "garlic"]
        test_prompt = get_recipe_prompt(test_ingredients, "Halal", "Pakistani", "Medium")
        
        print("\n--- Sending Test Prompt ---")
        recipe, history = generate_recipe(test_prompt)
        
        if recipe and "Sorry" not in recipe:
            print("\n--- Generated Recipe ---")
            print(recipe)
            print("\n--- Conversation History ---")
            print(history)
        else:
            print("\n--- Test Failed ---")
            print(recipe)
