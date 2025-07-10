# recipe_utils.py
import re

def is_valid_input(ingredients):
    """
    Validates the user's ingredient input.

    Args:
        ingredients (list): A list of ingredients.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not ingredients:
        return False
    # Check if ingredients contain only reasonable characters (letters, spaces, hyphens)
    for ingredient in ingredients:
        if not re.match(r"^[a-zA-Z\s-]+$", ingredient):
            return False
    return True

def parse_ingredients_from_text(text_input):
    """
    Parses a comma-separated string of ingredients into a clean list.

    Args:
        text_input (str): The raw text input from the user.

    Returns:
        list: A list of cleaned, stripped ingredient strings.
    """
    if not text_input:
        return []
    # Split by comma, strip whitespace from each item, and filter out empty strings
    ingredients = [item.strip().lower() for item in text_input.split(',') if item.strip()]
    return ingredients

# Example of a more complex utility if needed in the future
def format_recipe_for_display(recipe_text):
    """
    (Optional) Further processes the Markdown response from Gemini if needed.
    For now, we will directly use the Markdown, but this function is a placeholder
    for future enhancements like converting to HTML or another format.

    Args:
        recipe_text (str): The Markdown text of the recipe.

    Returns:
        str: The processed recipe text.
    """
    # For now, just return the text as is.
    # Future idea: replace ### with st.subheader, etc.
    return recipe_text

if __name__ == '__main__':
    # --- Test Cases ---
    print("--- Testing Input Validation ---")
    print(f"['chicken', 'rice']: {is_valid_input(['chicken', 'rice'])}")
    print(f"[]: {is_valid_input([])}")
    print(f"['chicken', 'rice123']: {is_valid_input(['chicken', 'rice123'])}") # Should be False
    print(f"['chicken-thighs']: {is_valid_input(['chicken-thighs'])}")

    print("\n--- Testing Ingredient Parsing ---")
    print(f"'chicken, rice, onion ': {parse_ingredients_from_text('chicken, rice, onion ')}")
    print(f"'  beef ,   potatoes, , carrots': {parse_ingredients_from_text('  beef ,   potatoes, , carrots')}")
    print(f"Empty string: {parse_ingredients_from_text('')}")
