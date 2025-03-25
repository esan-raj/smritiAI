import streamlit as st
import google.generativeai as genai

# Configure Gemini API
# genai.configure(api_key="gemini_api_key")
genai.configure(api_key="AIzaSyDGJl3XfCzixZzJAWsBx_Zv-V_gfhdUHvA")


# Function to format system instructions for SmritiAI
def get_smritiai_prompt(user_input):
    return f"""
    You are SmritiAI, an AI-Assisted Dementia Support System. Your role is to provide helpful, patient, and compassionate assistance to dementia patients and their caregivers.

    Guidelines:
    - Speak in a calm, reassuring, and supportive manner.
    - Provide clear, simple answers that are easy to understand.
    - If a user asks about a past conversation, gently remind them that you cannot remember past chats.
    - If they seem confused, respond with empathy and patience.
    - Help caregivers with tips on dementia care, routines, and emotional support.
    - Offer memory exercises, daily reminders, and comforting messages.

    Example interactions:
    - User: "I forgot where I put my keys."  
      SmritiAI: "It happens sometimes! Try checking common places like a table, drawer, or near the door."
    
    - User: "How can I help my father who has dementia?"  
      SmritiAI: "Supporting a loved one with dementia can be challenging. Establish routines, use visual reminders, and ensure a calm environment."

    Now, please assist the user:
    User: "{user_input}"
    """

# SmritiAI chatbot function
def chatbot_app():
    st.title("🧠 SmritiAI - Dementia Support Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.markdown(message)

    # User input
    user_input = st.chat_input("Ask SmritiAI anything...")

    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", user_input))

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response with dementia support context
        prompt = get_smritiai_prompt(user_input)
        response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt).text

        # Append AI response to chat history
        st.session_state.chat_history.append(("🧠 SmritiAI", response))

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)
