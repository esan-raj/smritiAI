import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDGJl3XfCzixZzJAWsBx_Zv-V_gfhdUHvA")

# Chatbot function
def chatbot_app():
    st.title("💬 Gemini AI Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.markdown(message)

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", user_input))

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        response = genai.GenerativeModel("gemini-1.5-pro").generate_content(user_input).text

        # Append AI response to chat history
        st.session_state.chat_history.append(("🤖 Bot", response))

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)
