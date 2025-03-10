import streamlit as st
import requests

# Langflow API settings
LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "9b4d72d9-6c80-4e27-962b-3120a9c0069e"  # Replace with your actual Flow ID from Langflow

# SmritiAI Chatbot function
def chatbot_app_langflow():
    st.title("🧠 SmritiAI - Dementia Support Chatbot (Langflow)")

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

        # Send request to Langflow
        response = send_to_langflow(user_input)

        # Append AI response to chat history
        st.session_state.chat_history.append(("🧠 SmritiAI", response))

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)

# Function to send user input to Langflow and get response
def send_to_langflow(user_input):
    payload = {"input": user_input}
    try:
        response = requests.post(f"{LANGFLOW_API_URL}/{FLOW_ID}", json=payload)
        if response.status_code == 200:
            data = response.json()
            # Extracting correct response from Langflow API JSON structure
            outputs = data.get("outputs", [])
            if outputs and isinstance(outputs, list):
                first_output = outputs[0].get("outputs", [])
                if first_output and isinstance(first_output, list):
                    return first_output[0]["outputs"]["message"]["message"]
            return "⚠️ No response from SmritiAI."
        else:
            return f"⚠️ Error {response.status_code}: Unable to connect to Langflow API."
    except requests.exceptions.RequestException:
        return "⚠️ Error: Langflow API is not running."

