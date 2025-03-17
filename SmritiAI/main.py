from modules.transcriber import transcriber_app
from modules.gemini_chatbot import chatbot_app
from modules.todo import todo_app
from modules.langflow_chatbot import chatbot_app_langflow
from modules.reminder_manager import get_reminders, remove_reminder, add_reminder
import streamlit as st
from datetime import datetime, timedelta

st.title("🚀 Testing Features")

# 📌 Ask user to enter their phone number (store in session)
if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""

phone_number = st.text_input("📱 Enter your phone number for reminders:", value=st.session_state.phone_number)

# Save phone number in session when user enters it
if phone_number:
    st.session_state.phone_number = phone_number

# 📌 Display Upcoming Reminders
st.subheader("📅 Upcoming Reminders")
if phone_number:
    upcoming_reminders = get_reminders(phone_number)
else:
    upcoming_reminders = []  # Empty list if phone number is not provided

if upcoming_reminders:
    for reminder in upcoming_reminders:
        reminder_id, user, message, reminder_time, phone = reminder  # Extract ID
        with st.expander(f"🔔 {message} at {reminder_time}"):
            st.write(f"👤 **User:** {user}")
            st.write(f"📱 **Phone Number:** {phone}")

            # Confirmation checkbox before deleting
            confirm_delete = st.checkbox(f"✅ Confirm delete for {reminder_id}", key=f"confirm_{reminder_id}")

            # Delete button (enabled only if confirmed)
            if st.button(f"🗑️ Delete Reminder {reminder_id}", key=f"delete_{reminder_id}") and confirm_delete:
                remove_reminder(reminder_id)
                st.success(f"✅ Reminder ID {reminder_id} deleted!")
                st.rerun()  # Refresh UI after deletion
else:
    st.write("✅ No upcoming reminders.")

# 📌 New: Set Reminder from Dashboard
st.subheader("🔔 Set a New Reminder")
reminder_message = st.text_input("✍️ Reminder Message:")
reminder_date = st.date_input("📆 Select Date:")
reminder_time = st.time_input("⏰ Select Time:")

if st.button("✅ Set Reminder", key="dashboard_reminder"):
    if reminder_message and phone_number:
        reminder_datetime = datetime.combine(reminder_date, reminder_time)
        formatted_time = reminder_datetime.strftime("%H:%M")  # Convert datetime to HH:MM format
        add_reminder("User", reminder_message, formatted_time, st.session_state.phone_number)

        st.success(f"🔔 Reminder set: '{reminder_message}' at {reminder_datetime}")
        st.rerun()
    else:
        st.error("❌ Please enter a message and your phone number!")

# 📌 Feature Selection
test_mode = st.selectbox("Select Feature to Test", ["Transcriber", "Chatbot", "Langflow Chatbot", "To-Do List"])

if test_mode == "Transcriber":
    transcriber_app()
elif test_mode == "Chatbot":
    chatbot_app()
elif test_mode == "Langflow Chatbot":
    chatbot_app_langflow()
elif test_mode == "To-Do List":
    todo_app()
