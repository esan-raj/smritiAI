import base64
import streamlit as st
from datetime import datetime
from modules.transcriber import transcriber_app
from modules.langflow_chatbot import chatbot_app_langflow
from modules.todo import todo_app
from modules.reminder_manager import get_reminders, remove_reminder, add_reminder

# Set up the dashboard page
st.set_page_config(page_title="SmritiAI | Dashboard", layout="wide")
st.title("🧠 SmritiAI Dashboard")

# Sidebar for navigation
logo_path = "D:\SmritiAI\SmritiAI\images\Smriti_ai_logo.jpg"

# Display logo in the sidebar
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert image to base64
logo_base64 = get_base64_encoded_image(logo_path)

# Display the image in the sidebar (center-aligned)
st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/jpg;base64,{logo_base64}" width="150">
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.header("Navigation")
selected_feature = st.sidebar.selectbox("Choose a Feature", ["Dashboard", "Chatbot", "Transcriber", "To-Do List"])

# Store phone number in session
if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""

phone_number = st.sidebar.text_input("📱 Enter phone number for reminders:", value=st.session_state.phone_number)
if phone_number:
    st.session_state.phone_number = phone_number

# Dashboard - Display reminders
if selected_feature == "Dashboard":
    st.subheader("🔔 Set a New Reminder")
    reminder_message = st.text_input("✍️ Reminder Message:")
    reminder_date = st.date_input("📆 Select Date:")
    reminder_time = st.time_input("⏰ Select Time:")

    if st.button("✅ Set Reminder"):
        if reminder_message and phone_number:
            reminder_datetime = datetime.combine(reminder_date, reminder_time)
            formatted_time = reminder_datetime.strftime("%H:%M")
            add_reminder("User", reminder_message, formatted_time, st.session_state.phone_number)
            st.success(f"🔔 Reminder set: '{reminder_message}' at {reminder_datetime}")
            st.rerun()
        else:
            st.error("❌ Please enter a message and phone number!")

    # Display upcoming reminders
    st.subheader("📅 Upcoming Reminders")
    upcoming_reminders = get_reminders(phone_number) if phone_number else []
    if upcoming_reminders:
        for reminder in upcoming_reminders:
            reminder_id, user, message, reminder_time, phone = reminder
            with st.expander(f"🔔 {message} at {reminder_time}"):
                st.write(f"👤 **User:** {user}")
                st.write(f"📱 **Phone:** {phone}")
                if st.button(f"🗑️ Delete Reminder {reminder_id}", key=f"delete_{reminder_id}"):
                    remove_reminder(reminder_id)
                    st.success(f"✅ Reminder {reminder_id} deleted!")
                    st.rerun()
    else:
        st.write("✅ No upcoming reminders.")

# Feature selection
elif selected_feature == "Chatbot":
    chatbot_app_langflow()
elif selected_feature == "Transcriber":
    transcriber_app()
elif selected_feature == "To-Do List":
    todo_app()
