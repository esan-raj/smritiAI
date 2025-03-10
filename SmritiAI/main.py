from modules.transcriber import transcriber_app
from modules.gemini_chatbot import chatbot_app
from modules.todo import todo_app
from modules.langflow_chatbot import chatbot_app_langflow
import streamlit as st

st.title("🚀 Testing Features")

test_mode = st.selectbox("Select Feature to Test", ["Transcriber", "Chatbot","Langflow Chatbot", "To-Do List"])

if test_mode == "Transcriber":
    transcriber_app()
elif test_mode == "Chatbot":
    chatbot_app()
elif test_mode == "Langflow Chatbot":
    chatbot_app_langflow()
elif test_mode == "To-Do List":
    todo_app()
