# app.py
import streamlit as st
from gemini_handler import generate_recipe, API_KEY
from prompts import get_recipe_prompt
from recipe_utils import is_valid_input, parse_ingredients_from_text

# --- Page Configuration ---
st.set_page_config(
    page_title="BANAO AI Recipe",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Management ---
# Initialize session state variables
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'generated_recipe' not in st.session_state:
    st.session_state.generated_recipe = ""
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# --- UI Components ---

# --- Sidebar ---
with st.sidebar:
    st.title("🍲 AI Recipe Suggester")
    st.markdown("""
    Welcome! I'm your AI Chef. Tell me what ingredients you have, and I'll suggest a delicious recipe for you, complete with Pakistani cultural context.
    """)

    st.header("1. Your Ingredients")
    # Common Pakistani ingredients for multiselect
    common_ingredients = [
        "Chicken", "Beef", "Mutton/Lamb", "Fish", "Lentils (Daal)", "Chickpeas (Chana)",
        "Potatoes", "Onions", "Tomatoes", "Garlic", "Ginger", "Yogurt", "Rice",
        "Flour (Atta)", "Ghee/Oil", "Green Chilies", "Coriander", "Mint", "Lemon"
    ]
    selected_ingredients = st.multiselect(
        "Select from common ingredients:",
        options=common_ingredients,
        default=[]
    )

    text_ingredients = st.text_area(
        "Or type your own (comma-separated):",
        placeholder="e.g., bell peppers, paneer, cream"
    )

    # Voice input placeholder
    st.info("🎤 Voice input coming soon!", icon="💡")

    st.header("2. Your Preferences")
    dietary_prefs = st.selectbox(
        "Dietary Preferences:",
        ["Any", "Halal", "Vegetarian", "Vegan"],
        index=0
    )
    cuisine_type = st.selectbox(
        "Cuisine Type:",
        ["Any", "Pakistani", "Indian", "Middle Eastern", "Fusion"],
        index=1
    )
    spice_level = st.select_slider(
        "Desired Spice Level:",
        options=["Mild", "Medium", "Hot", "Extra Hot"],
        value="Medium"
    )

    st.header("3. Generate!")
    # Generate button
    generate_button = st.button("✨ Generate Recipe", type="primary", use_container_width=True)
    
    # New recipe button
    if st.session_state.generated_recipe:
        if st.button("🔄 Start New Recipe", use_container_width=True):
            # Reset state for a new recipe
            st.session_state.conversation_history = []
            st.session_state.generated_recipe = ""
            st.session_state.is_loading = False
            st.rerun() # Rerun the script to clear the display

# --- Main Content Area ---
st.header("Your AI-Generated Recipe")

# Check for API Key availability at the start
if not API_KEY:
    st.error("FATAL: Google Gemini API key is not configured. Please set it up following the README instructions.")
    st.stop() # Stop the app if no API key is found

# --- Logic for Recipe Generation ---
if generate_button and not st.session_state.is_loading:
    # Combine ingredients from both inputs
    parsed_text_ingredients = parse_ingredients_from_text(text_ingredients)
    final_ingredients = list(set([i.lower() for i in selected_ingredients] + parsed_text_ingredients))

    # --- Input Validation ---
    if not is_valid_input(final_ingredients):
        st.warning("Please provide at least one valid ingredient.")
    else:
        with st.spinner("Your AI Chef is thinking... 👩‍🍳"):
            st.session_state.is_loading = True
            
            # Construct the prompt
            prompt = get_recipe_prompt(final_ingredients, dietary_prefs, cuisine_type, spice_level)
            
            # Call the Gemini API
            recipe, history = generate_recipe(prompt, st.session_state.conversation_history)
            
            # Update session state
            st.session_state.generated_recipe = recipe
            st.session_state.conversation_history = history
            st.session_state.is_loading = False
            st.rerun() # Rerun to display the new recipe

# --- Display Area ---
if st.session_state.is_loading:
    st.info("Generating your recipe, please wait...")
elif st.session_state.generated_recipe:
    # Display the generated recipe (it's already in Markdown)
    st.markdown(st.session_state.generated_recipe)
    
    # --- Follow-up Questions (Conversation) ---
    st.markdown("---")
    st.subheader("Have a follow-up question?")
    follow_up_prompt = st.text_input(
        "Ask something about this recipe (e.g., 'How can I make this gluten-free?')",
        key="follow_up"
    )
    if follow_up_prompt:
        with st.spinner("Thinking..."):
            # Call Gemini again with the history
            response, history = generate_recipe(follow_up_prompt, st.session_state.conversation_history)
            st.session_state.conversation_history = history
            # Append the follow-up Q&A to the display
            st.session_state.generated_recipe += f"\n\n---\n\n**Your Question:** {follow_up_prompt}\n\n**Chef's Answer:** {response}"
            st.rerun() # Rerun to show the new answer
else:
    st.info("Your recipe will appear here once you provide ingredients and click 'Generate'.")

