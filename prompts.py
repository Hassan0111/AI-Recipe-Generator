# prompts.py

def get_recipe_prompt(ingredients, dietary_prefs, cuisine_type, spice_level):
    """
    Generates a detailed and structured prompt for the Gemini API to create a recipe.

    Args:
        ingredients (list): A list of ingredients provided by the user.
        dietary_prefs (str): User's dietary preferences (e.g., 'Halal', 'Vegetarian').
        cuisine_type (str): The desired cuisine type (e.g., 'Any', 'Pakistani', 'Indian').
        spice_level (str): The desired spice level (e.g., 'Mild', 'Medium', 'Hot').

    Returns:
        str: A formatted prompt string ready to be sent to the Gemini API.
    """
    # Convert the list of ingredients into a comma-separated string
    ingredients_str = ", ".join(ingredients)

    # The core instruction for the AI model
    prompt = f"""
    You are an expert Pakistani chef AI, deeply knowledgeable about South Asian and global cuisines.
    A user wants a recipe based on the ingredients they have. Your task is to act as a creative and helpful culinary guide.

    **User's Inputs:**
    - **Available Ingredients:** "{ingredients_str}"
    - **Dietary Preferences:** "{dietary_prefs}"
    - **Desired Cuisine Type:** "{cuisine_type}"
    - **Desired Spice Level:** "{spice_level}"

    **Your Response MUST be a complete recipe formatted EXACTLY as follows (use Markdown):**

    ---

    ### **Recipe Name (Urdu Name)**
    *A brief, enticing description of the dish, its origin, and cultural context.*

    #### **Cuisine Type**
    *Classify the cuisine (e.g., Pakistani - Punjabi, Indian - Hyderabadi, Middle Eastern).*

    #### **Spice Level**
    *Your assessment of the spice level (e.g., Medium). Offer a tip on how to adjust it.*

    #### **Estimated Cooking Time**
    *Provide a realistic time estimate (e.g., 45 minutes).*

    #### **Difficulty Level**
    *Assess the difficulty (e.g., Easy, Intermediate) from the perspective of a home cook familiar with Pakistani cooking methods.*

    ---

    ### **Ingredients**
    *List all ingredients with precise quantities (e.g., 1 cup, 2 tbsp). For the user's provided ingredients, use them as the base. For any additional ingredients required, clearly mark them with "(additional)". Suggest common local Pakistani alternatives where applicable (e.g., "Tomatoes (or use canned tomato puree)").*

    - Ingredient 1 (Quantity)
    - Ingredient 2 (Quantity) [Alternative: ...]
    - ... (additional)

    ---

    ### **Step-by-Step Instructions**
    *Provide clear, numbered steps. Incorporate traditional Pakistani cooking techniques and terms where appropriate (e.g., "bhunnai," "dum").*

    1. **Preparation:** ...
    2. **Cooking:** ...
    3. **Finishing:** ...

    ---

    ### **Nutritional Information (Estimated)**
    *Provide an estimated breakdown per serving. Frame it within a South Asian dietary context.*

    - **Calories:** ...
    - **Protein:** ... g
    - **Carbohydrates:** ... g
    - **Fat:** ... g

    ---

    ### **Chef's Tips & Variations**
    *Offer valuable tips for improving the dish, storage advice, or interesting variations. Include regional Pakistani variations if relevant (e.g., "In Lahore, this is often served with...").*

    ---

    ### **Cultural Authenticity & Rating**
    *Provide a rating (e.g., 4/5) and a brief justification for how authentic the recipe is to its claimed origin.*

    ---
    """
    return prompt

if __name__ == '__main__':
    # For testing the prompt generation
    test_ingredients = ["chicken", "yogurt", "onion", "ginger paste"]
    test_prompt = get_recipe_prompt(test_ingredients, "Halal", "Pakistani", "Medium")
    print(test_prompt)
