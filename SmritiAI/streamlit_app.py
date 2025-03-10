import streamlit as st
from modules.transcriber import transcriber_app
from modules.gemini_chatbot import chatbot_app
from modules.todo import todo_app

# Set up Streamlit page
st.set_page_config(page_title="SmiritiAI|Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 SmiritiAI | Dashboard")
app_mode = st.sidebar.radio("Select an Option:", ["🏠 Home", "🎙️ Transcriber", "🤖 Chatbot", "📝 To-Do List"])

# Navigation logic
if app_mode == "🏠 Home":
    st.title("Welcome to the SmiritiAI Dashboard! 🚀")
    st.write("Choose an option from the sidebar to get started.")

elif app_mode == "🎙️ Transcriber":
    transcriber_app()

elif app_mode == "🤖 Chatbot":
    chatbot_app()

elif app_mode == "📝 To-Do List":
    todo_app()
