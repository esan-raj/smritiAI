import base64
import streamlit as st
import datetime
import re
from modules.reminder_manager import add_reminder

# Initialize session state for to-do list
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

def parse_relative_time(time_str):
    """
    Parses relative time expressions like 'in 2 hours' and returns an absolute datetime.
    """
    match = re.match(r"in (\d+) (minute|minutes|hour|hours|day|days)", time_str, re.IGNORECASE)
    if match:
        amount, unit = match.groups()
        amount = int(amount)

        now = datetime.datetime.now()
        if "minute" in unit:
            return now + datetime.timedelta(minutes=amount)
        elif "hour" in unit:
            return now + datetime.timedelta(hours=amount)
        elif "day" in unit:
            return now + datetime.timedelta(days=amount)
    return None  # If no match, return None

def add_task(task, due_date, due_time, phone_number):
    """
    Adds a task to the to-do list and schedules a reminder if time is provided.
    """
    if not phone_number:
        st.warning("⚠️ Phone number is required to set a reminder!")
        return
    
    full_due_time = None

    # Check if due_time is given as a relative time (e.g., "in 2 hours")
    if isinstance(due_time, str):
        full_due_time = parse_relative_time(due_time)
    elif due_date and due_time:
        full_due_time = datetime.datetime.combine(due_date, due_time)

    st.session_state.todo_list.append({
        "task": task,
        "due_date": due_date,
        "due_time": due_time,
        "phone_number": phone_number
    })

    if full_due_time:
        add_reminder(task, full_due_time, phone_number)
        st.success(f"✅ Reminder set for '{task}' at {full_due_time.strftime('%Y-%m-%d %H:%M:%S')}.")

def remove_task(index):
    """
    Removes a task from the to-do list.
    """
    if 0 <= index < len(st.session_state.todo_list):
        del st.session_state.todo_list[index]
        st.success("✅ Task removed successfully.")

def todo_app():
    """
    Streamlit To-Do List App with Dynamic Reminders.
    """
    logo_path = "D:\SmritiAI\SmritiAI\images\Smriti_ai_logo.jpg"

# Display logo in the sidebar
    def get_base64_encoded_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Convert image to base64
    logo_base64 = get_base64_encoded_image(logo_path)

    # Display the image in the sidebar (center-aligned)
    # st.sidebar.markdown(
    #     f"""
    #     <div style="display: flex; justify-content: center; align-items: center;">
    #         <img src="data:image/jpg;base64,{logo_base64}" width="150">
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.title("📝 Smart To-Do List with Reminders")

    task = st.text_input("Enter a task:")
    
    col1, col2 = st.columns(2)
    with col1:
        due_date = st.date_input("Select a due date:", value=None)
    with col2:
        due_time = st.text_input("Enter a due time (HH:MM AM/PM or 'in 2 hours'):", value="")

    phone_number = st.text_input("📱 Enter phone number (Required for reminders):", value="")

    if st.button("➕ Add Task"):
        if task:
            add_task(task, due_date, due_time, phone_number)
        else:
            st.warning("⚠️ Task cannot be empty!")

    st.subheader("📌 Your To-Do List")
    if st.session_state.todo_list:
        for idx, item in enumerate(st.session_state.todo_list):
            st.write(f"🔹 {item['task']} (Due: {item['due_date']} {item['due_time']})")
            if st.button(f"❌ Remove", key=f"remove_{idx}"):
                remove_task(idx)
    else:
        st.write("No tasks added yet.")

# Run the app

