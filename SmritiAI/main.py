from modules.transcriber import transcriber_app
from modules.gemini_chatbot import chatbot_app
from modules.todo import todo_app
import streamlit as st

st.title("🚀 Testing Features")

test_mode = st.selectbox("Select Feature to Test", ["Transcriber", "Chatbot", "To-Do List"])

if test_mode == "Transcriber":
    transcriber_app()
elif test_mode == "Chatbot":
    chatbot_app()
elif test_mode == "To-Do List":
    todo_app()
