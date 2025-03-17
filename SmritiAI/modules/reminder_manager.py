import sqlite3
import threading
import time
from datetime import datetime
from twilio.rest import Client

# 📌 Twilio API Credentials
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

# 📌 Database Setup
def initialize_db():
    """Creates the reminders table if it doesn't exist."""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            reminder_time TEXT,
            phone_number TEXT
        )
    """)
    conn.commit()
    conn.close()

initialize_db()  # Ensure DB is created when module loads

# 📌 Function to Add a Reminder
def add_reminder(user, message, time, phone_number):
    """Save a reminder in the database with time format validation."""
    try:
        scheduled_time = datetime.strptime(time, "%H:%M")  # Validate time format
    except ValueError:
        return "⚠️ Invalid time format! Use HH:MM (24-hour format)."

    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (user, message, reminder_time, phone_number) VALUES (?, ?, ?, ?)", 
                   (user, message, time, phone_number))
    conn.commit()
    conn.close()
    print("Reminder saved successfully")
    return f"✅ Reminder set for '{user}': '{message}' at {time}."

# 📌 Function to Fetch Upcoming Reminders
# 📌 Function to Fetch Upcoming Reminders
def get_reminders(phone_number):
    """Fetch all upcoming reminders for a user."""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, user, message, reminder_time, phone_number FROM reminders WHERE phone_number = ?", (phone_number,))
    
    reminders = cursor.fetchall()  # Fetch all reminders
    conn.close()
    
    # ✅ Ensure 5 values per reminder
    valid_reminders = [tuple(reminder) if len(reminder) == 5 else None for reminder in reminders]
    return [r for r in valid_reminders if r]  # Remove None values

# 📌 Function to Delete a Reminder
def remove_reminder(reminder_id):
    """Delete a reminder based on its ID."""
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    affected_rows = cursor.rowcount  # Check if the deletion was successful
    conn.commit()
    conn.close()
    
    if affected_rows > 0:
        return f"✅ Reminder ID {reminder_id} deleted successfully!"
    else:
        return f"⚠️ Reminder ID {reminder_id} not found!"

# 📌 Function to Send SMS via Twilio
def format_phone_number(phone_number):
    """Ensure phone number is in E.164 format with +91 country code."""
    phone_number = phone_number.strip().replace(" ", "")  # Remove spaces
    if not phone_number.startswith("+"):
        phone_number = "+91" + phone_number  # Add +91 if missing
        print(phone_number)
    return phone_number

def send_sms(phone_number, message):
    """Send an SMS reminder using Twilio Trial account."""
    try:
        formatted_number = format_phone_number(phone_number)  # Ensure correct format
        print("this is twilio number -------------------------------------------------")
        print(TWILIO_PHONE_NUMBER)
        print("This is formatted number -----------------------------------------------------")
        print(formatted_number)
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=f"🔔 Reminder: {message}",
            from_=TWILIO_PHONE_NUMBER,  # Must use Twilio trial number
            
            to=formatted_number  # Use formatted number
        )
        
        print(f"📩 SMS sent successfully to {formatted_number}: {message}")
        return sms.sid

    except Exception as e:
        print(f"❌ Twilio SMS Sending Failed: {e}")
        return None


# 📌 Function to Check and Send Reminders
def reminder_checker():
    """Continuously check for due reminders and notify users via SMS."""
    while True:
        conn = sqlite3.connect("reminders.db")
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%H:%M")
        cursor.execute("SELECT id, user, message, phone_number FROM reminders WHERE reminder_time = ?", (now,))
        due_reminders = cursor.fetchall()

        for reminder_id, user, message, phone_number in due_reminders:
            print(f"🔔 Sending reminder to {user}: {message}")
            send_sms(phone_number, message)  # Send SMS notification

            # Delete reminder after sending
            cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            conn.commit()
        
        conn.close()
        time.sleep(60)  # Check every minute

# 📌 Run Reminder Checker in Background
reminder_thread = threading.Thread(target=reminder_checker, daemon=True)
reminder_thread.start()
